import os
from typing import Literal

from anvil.api.core.filters import Filter
from anvil.lib.config import CONFIG
from anvil.lib.enums import Difficulty, Population
from anvil.lib.schemas import (
    AddonObject,
    BlockDescriptor,
    JsonSchemes,
    MinecraftDescription,
)

__all__ = ["SpawnRule"]


class _SpawnRuleDescription(MinecraftDescription):
    def __init__(self, spawn_rule_obj, name: str, is_vanilla) -> None:
        """Initialize the spawn rule description.

        Parameters:
            spawn_rule_obj: Reference to the parent SpawnRule object.
            name (str): The entity identifier for this spawn rule.
            is_vanilla (bool): Whether this is a vanilla Minecraft entity.
        """
        super().__init__(name, is_vanilla)
        self._spawn_rule_obj: "SpawnRule" = spawn_rule_obj
        self._description["description"]["population_control"] = Population.Ambient

    def population_control(self, population: Population):
        """Assign the entity to a population pool for spawn limit management.

        Each population pool has its own spawn limits. Entities assigned to a pool
        will only spawn if that pool hasn't reached its spawn limit. The 'cat' pool
        functions differently than others - cat spawn rules are based on villages.

        Available pools:
        - **Animal**: Land animals (cows, pigs, sheep, etc.)
        - **UnderwaterAnimal**: Aquatic creatures (fish, dolphins, etc.)
        - **Monster**: Hostile mobs (zombies, skeletons, etc.)
        - **Ambient**: Ambient creatures (bats, etc.)

        Parameters:
            population (Population): The population pool to assign this entity to.

        Returns:
            SpawnRule: The parent spawn rule for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/cliententitydocumentation/datadrivenspawning?view=minecraft-bedrock-stable
        """
        self._description["description"]["population_control"] = population.value
        return self._spawn_rule_obj


class _SpawnRuleCondition:
    """Defines conditions that must be met for an entity to spawn.

    This class provides methods to set various spawn conditions including biome requirements,
    light levels, difficulty settings, spatial constraints, and behavioral modifiers.
    Multiple conditions can be combined to create precise spawn requirements.
    """

    def __init__(self):
        """Initialize an empty spawn condition set."""
        self._condition = {}

    def BiomeFilter(self, filter: Filter):
        """Specifies which biomes the entity can spawn in using biome tags.

        Biome tags include: animal, monster, desert, forest, jungle, ocean, nether,
        the_end, cold, warm, frozen, and many others. Each biome has multiple tags
        that can be used for filtering.

        Example biome tags:
        - monster: Most overworld biomes where hostile mobs spawn
        - animal: Biomes where passive animals spawn
        - nether: All nether dimension biomes
        - ocean: All ocean biomes

        Parameters:
            filter (Filter): Filter condition to test biome tags
                (e.g., Filter.has_biome_tag("monster")).

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/biome_filter?view=minecraft-bedrock-stable
        """
        if "minecraft:biome_filter" not in self._condition:
            self._condition.update({"minecraft:biome_filter": []})
        self._condition["minecraft:biome_filter"].append(filter)
        return self

    def BrightnessFilter(
        self,
        min_brightness: int = 0,
        max_brightness: int = 15,
        adjust_for_weather: bool = True,
    ):
        """Sets the light level range that allows the entity to spawn.

        Light levels range from 0 (complete darkness) to 15 (full sunlight).
        Most hostile mobs spawn in low light (0-7), while peaceful mobs typically
        require higher light levels.

        Parameters:
            min_brightness (int): Minimum light level for spawning (0-15). Defaults to 0.
            max_brightness (int): Maximum light level for spawning (0-15). Defaults to 15.
            adjust_for_weather (bool): Whether weather affects light level calculations
                (e.g., allows hostile mobs to spawn during day when it rains). Defaults to True.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/brightness_filter?view=minecraft-bedrock-stable
        """
        min_brightness = max(0, min_brightness)
        max_brightness = min(15, max_brightness)
        self._condition.update(
            {
                "minecraft:brightness_filter": {
                    "min": min_brightness,
                    "max": max_brightness,
                    "adjust_for_weather": adjust_for_weather,
                }
            }
        )
        return self

    def DelayFilter(
        self, minimum: int, maximum: int, identifier: str, spawn_chance: int
    ):
        """Sets specific time delays before entities will spawn.

        This creates a delay mechanism where the entity specified by identifier
        has a chance to spawn after a random delay period.

        Parameters:
            minimum (int): Minimum delay time before spawning can occur.
            maximum (int): Maximum delay time before spawning can occur.
            identifier (str): The entity identifier that will spawn after the delay.
            spawn_chance (int): Percentage chance (0-100) that the entity will spawn.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/delay_filter?view=minecraft-bedrock-stable
        """
        self._condition.update(
            {
                "minecraft:delay_filter": {
                    "min": minimum,
                    "max": maximum,
                    "identifier": identifier,
                    "spawn_chance": max(min(spawn_chance, 100), 0),
                }
            }
        )

        return self

    def DensityLimit(self, surface: int = -1, underground: int = -1):
        """Limits the number of this entity type that can spawn in a given area.

        This provides local density control separate from global population limits.
        Useful for preventing overcrowding of specific entity types in small areas.

        Parameters:
            surface (int): Maximum number of this entity type on the surface.
                Use -1 for unlimited. Defaults to -1.
            underground (int): Maximum number of this entity type underground.
                Use -1 for unlimited. Defaults to -1.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/density_limit?view=minecraft-bedrock-stable
        """
        density = {"minecraft:density_limit": {}}
        if surface != -1:
            density["minecraft:density_limit"]["surface"] = surface
        if underground != -1:
            density["minecraft:density_limit"]["underground"] = underground
        self._condition.update(density)
        return self

    def DistanceFilter(self, min: int, max: int):
        """Sets the distance range from players where entities can spawn.

        Entities will only spawn within this distance range from the nearest player.
        Typical values are 24-128 blocks for most mobs to prevent spawning too close
        or too far from players.

        Parameters:
            min (int): Minimum distance from a player for spawning (in blocks).
            max (int): Maximum distance from a player for spawning (in blocks).

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/distance_filter?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:distance_filter": {"min": min, "max": max}})
        return self

    def DifficultyFilter(
        self,
        min_difficulty: Difficulty = Difficulty.Easy,
        max_difficulty: Difficulty = Difficulty.Hard,
    ):
        """Restricts spawning to specific difficulty levels.

        Allows entities to spawn only within the specified difficulty range.
        Useful for making certain entities only appear on harder difficulties.

        Difficulty levels: Peaceful < Easy < Normal < Hard

        Parameters:
            min_difficulty (Difficulty): Minimum difficulty for spawning. Defaults to Easy.
            max_difficulty (Difficulty): Maximum difficulty for spawning. Defaults to Hard.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/difficulty_filter?view=minecraft-bedrock-stable
        """
        self._condition.update(
            {
                "minecraft:difficulty_filter": {
                    "min": min_difficulty,
                    "max": max_difficulty,
                }
            }
        )
        return self

    def EntityTypes(
        self,
        filters: Filter = None,
        max_dist: float = 16,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        """Defines entity targeting data for spawn-related behaviors.

        This encapsulates entity data used in certain spawn behaviors and components
        that need to reference or interact with other entities during spawning.

        Parameters:
            filters (Filter, optional): Conditions that make entities valid targets.
            max_dist (float): Maximum distance for entity interactions. Defaults to 16.
            must_see (bool): Whether line of sight is required. Defaults to False.
            must_see_forget_duration (float): Time to remember unseen targets (seconds). Defaults to 3.0.
            sprint_speed_multiplier (float): Sprint speed modifier. Defaults to 1.0.
            walk_speed_multiplier (float): Walk speed modifier. Defaults to 1.0.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/entity_types?view=minecraft-bedrock-stable
        """
        entity_types = {
            "max_dist": max_dist,
            "must_see": must_see,
            "must_see_forget_duration": must_see_forget_duration,
            "sprint_speed_multiplier": sprint_speed_multiplier,
            "walk_speed_multiplier": walk_speed_multiplier,
        }

        if filters is not None:
            entity_types["filters"] = filters

        self._condition.update({"minecraft:entity_types ": entity_types})
        return self

    def HeightFilter(self, min: int, max: int):
        """Restricts spawning to specific Y-coordinate ranges.

        Useful for creating entities that only spawn at certain heights,
        such as cave-dwelling mobs or high-altitude creatures.

        Parameters:
            min (int): Minimum Y-coordinate (height level) for spawning.
            max (int): Maximum Y-coordinate (height level) for spawning.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/height_filter?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:height_filter": {"min": min, "max": max}})
        return self

    def Herd(
        self,
        min_size: int = 1,
        max_size: int = 4,
        spawn_event: str = None,
        event_skip_count: int = 0,
    ):
        """Configures group spawning behavior for entities.

        When entities spawn, they will appear in groups (herds) of the specified size.
        Useful for animals that naturally appear in groups or for creating pack behaviors.

        Parameters:
            min_size (int): Minimum number of entities in a spawn group. Defaults to 1.
            max_size (int): Maximum number of entities in a spawn group. Defaults to 4.
            spawn_event (str, optional): Event to trigger on some spawned entities.
            event_skip_count (int): Number of entities spawned before triggering the event.
                Defaults to 0.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/herd?view=minecraft-bedrock-stable
        """
        if "minecraft:herd" not in self._condition:
            self._condition.update({"minecraft:herd": []})
        self_herd = {"min_size": min_size, "max_size": max_size}
        if spawn_event != None:
            self_herd.update(
                {"event": spawn_event, "event_skip_count": event_skip_count}
            )
        self._condition["minecraft:herd"].append(self_herd)
        return self

    def MobEventFilter(
        self,
        event: Literal[
            "minecraft:pillager_patrols_event",
            "minecraft:wandering_trader_event",
            "minecraft:ender_dragon_event",
        ],
    ):
        """Restricts spawning to specific mob events.

        Allows entities to spawn only during certain game events like pillager patrols,
        wandering trader visits, or ender dragon encounters.

        Parameters:
            event (Literal): The mob event that triggers spawning. Options:
                - "minecraft:pillager_patrols_event": Pillager patrol spawns
                - "minecraft:wandering_trader_event": Wandering trader spawns
                - "minecraft:ender_dragon_event": Ender dragon related spawns

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/mob_event_filter?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:mob_event_filter": {"event": event}})

        return self

    def PermuteType(self, entity_type: str, weight: int = 10, spawn_event: str = None):
        """Creates a chance for spawned entities to be replaced with a different type.

        Allows spawn variation where the original entity has a chance to spawn as
        a different entity type instead. Commonly used for zombie/zombie villager
        variations or baby/adult variants.

        Parameters:
            entity_type (str): The entity identifier to potentially spawn instead.
            weight (int): Relative weight for this permutation. Defaults to 10.
            spawn_event (str, optional): Event to trigger on the permuted entity.

        Returns:
            _SpawnRuleCondition: Self for method chaining.
        """
        if "minecraft:permute_type" not in self._condition:
            self._condition.update({"minecraft:permute_type": []})
        self_permute_type = {"entity_type": entity_type, "weight": weight}
        if spawn_event != None:
            self_permute_type.update({"entity_type": f"{entity_type}<{spawn_event}>"})
        self._condition["minecraft:permute_type"].append(self_permute_type)
        return self

    def PlayerInVillageFilter(self, distance: int, village_border_tolerance: int):
        """Filters spawning based on player proximity to villages.

        Controls whether entities can spawn based on how close players are to villages.
        Useful for village-related spawns or preventing certain spawns near villages.

        Parameters:
            distance (int): Required distance from village center.
            village_border_tolerance (int): Additional tolerance from village borders.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/player_in_village_filter?view=minecraft-bedrock-stable
        """
        self._condition.update(
            {
                "minecraft:player_in_village_filter": {
                    "distance": distance,
                    "village_border_tolerance": village_border_tolerance,
                }
            }
        )
        return self

    @property
    def SpawnInLava(self):
        """Allows the entity to spawn in lava blocks.

        Enables spawning in lava source blocks, typically used for nether creatures
        like striders or custom fire-resistant entities.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_lava?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:spawns_lava": {}})
        return self

    def SpawnsOnBlockFilter(self, blocks: tuple[BlockDescriptor]):
        """Restricts spawning to specific block types.

        Entity will only spawn on top of the specified blocks. Useful for creating
        specialized spawning requirements like mushroom island mobs or desert creatures.

        Parameters:
            blocks (tuple[BlockDescriptor]): Tuple of block types the entity can spawn on.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_filter?view=minecraft-bedrock-stable
        """
        if "minecraft:spawns_on_block_filter" not in self._condition:
            self._condition.update({"minecraft:spawns_on_block_filter": []})
        self._condition["minecraft:spawns_on_block_filter"] = [
            block.identifier for block in blocks
        ]
        return self

    def SpawnsOnBlockPreventedFilter(self, blocks: tuple[BlockDescriptor]):
        """Prevents spawning on specific block types.

        Entity will not spawn on the specified blocks, even if other conditions are met.
        Useful for preventing spawning on inappropriate surfaces.

        Parameters:
            blocks (tuple[BlockDescriptor]): Tuple of block types to prevent spawning on.

        Returns:
            _SpawnRuleCondition: Self for method chaining.
        """
        if "minecraft:spawns_on_block_prevented_filter" not in self._condition:
            self._condition.update({"minecraft:spawns_on_block_prevented_filter": []})
        self._condition["minecraft:spawns_on_block_prevented_filter"] = [
            block.identifier for block in blocks
        ]
        return self

    @property
    def SpawnOnSurface(self):
        """Allows the entity to spawn on the world surface.

        Enables spawning on the topmost solid blocks exposed to sky.
        Commonly used for overworld mobs and animals.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_surface?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:spawns_on_surface": {}})
        return self

    @property
    def SpawnUnderground(self):
        """Allows the entity to spawn in underground locations.

        Enables spawning in caves, tunnels, and other enclosed underground spaces.
        Typically used for cave-dwelling mobs and underground creatures.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underground?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:spawns_underground": {}})
        return self

    @property
    def SpawnUnderwater(self):
        """Allows the entity to spawn in water blocks.

        Enables spawning inside water source blocks or flowing water.
        Essential for aquatic creatures like fish, dolphins, and guardians.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underwater?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:spawns_underwater": {}})
        return self

    def Weight(self, weight: int = 0):
        """Sets spawn priority relative to other valid spawn conditions.

        Higher weight values make this spawn condition more likely to be chosen
        when multiple valid conditions exist. Weight acts as a probability multiplier
        in the spawn selection process.

        Parameters:
            weight (int): Spawn weight/priority value. Higher values = higher priority.
                Defaults to 0.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/weight?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:weight": {"default": weight}})
        return self

    def WorldAgeFilter(self, min: int):
        """Prevents spawning until the world reaches a minimum age.

        Useful for creating entities that only appear in established worlds
        or after certain progression milestones.

        Parameters:
            min (int): Minimum world age (in ticks) before spawning can occur.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/world_age_filter?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:world_age_filter": {"min": min}})

        return self

    @property
    def DisallowSpawnsInBubble(self):
        """Prevents the entity from spawning in water bubble columns.

        Blocks spawning in bubble columns created by magma blocks or soul sand underwater.
        Useful for aquatic entities that should avoid these special water areas.

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/disallow_spawns_in_bubble?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:disallow_spawns_in_bubble": {}})
        return self

    def SpawnEvent(self, event: str = "minecraft:entity_spawned"):
        """Specifies an event to trigger when the entity spawns.

        Allows custom initialization or setup when entities are spawned through spawn rules.
        Default behavior uses "minecraft:entity_spawned" event.

        Parameters:
            event (str): Event identifier to trigger on spawn.
                Defaults to "minecraft:entity_spawned".

        Returns:
            _SpawnRuleCondition: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawn_event?view=minecraft-bedrock-stable
        """
        self._condition.update({"minecraft:spawn_event": {"event": event}})
        return self

    def export(self):
        """Export the condition data for JSON serialization.

        Returns:
            dict: Condition data for spawn rules JSON.
        """
        return self._condition


class SpawnRule(AddonObject):
    _extension = ".spawn_rules.json"
    _path = os.path.join(CONFIG.BP_PATH, "spawn_rules")
    _object_type = "Spawn Rule"

    def __init__(self, identifier, is_vanilla):
        """Initialize a spawn rule for the specified entity.

        Parameters:
            identifier (str): Entity identifier (e.g., "mypack:custom_mob").
            is_vanilla (bool): Whether this is a vanilla Minecraft entity.
        """
        super().__init__(identifier, is_vanilla)
        self._description = _SpawnRuleDescription(
            self, self.identifier, self._is_vanilla
        )
        self._spawn_rule = JsonSchemes.spawn_rules()
        self._conditions: list[_SpawnRuleCondition] = []

    @property
    def description(self):
        """Access the spawn rule description for setting basic properties.

        Returns:
            _SpawnRuleDescription: Description interface for population control and metadata.
        """
        return self._description

    @property
    def add_condition(self):
        """Create and add a new spawn condition to this spawn rule.

        Each condition represents a different spawning scenario. Multiple conditions
        allow entities to spawn under various circumstances (e.g., surface vs underground).

        Returns:
            _SpawnRuleCondition: New condition interface for setting spawn requirements.
        """
        self._condition = _SpawnRuleCondition()
        self._conditions.append(self._condition)
        return self._condition

    def queue(self, directory: str = None):
        """Queue this spawn rule for generation in the behavior pack.

        Exports the description and all conditions to JSON format and adds the
        spawn rule file to the generation queue. Only queues if conditions exist.

        Parameters:
            directory (str, optional): Custom directory path. Uses default if None.

        Returns:
            SpawnRule: Self for method chaining, or None if no conditions exist.
        """
        if len(self._conditions) > 0:
            self._spawn_rule["minecraft:spawn_rules"].update(
                self._description._export()
            )
            self._spawn_rule["minecraft:spawn_rules"]["conditions"] = [
                condition.export() for condition in self._conditions
            ]
            self.content(self._spawn_rule)
            return super().queue(directory=directory)
