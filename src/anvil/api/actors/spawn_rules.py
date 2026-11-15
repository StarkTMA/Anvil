"""The behavior pack's `spawn_rules/<entity>.spawn_rules.json`: where and how an entity
spawns."""

from collections.abc import Sequence
from typing import Annotated, Any, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.filters import Filter
from anvil.lib.config import Pack
from anvil.lib.format_versions import SPAWN_RULES_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    Identifier,
    InRange,
    JsonComponent,
    JsonFile,
    JsonObject,
    JsonValue,
    JsonValueComponent,
    Merged,
    NonNegative,
    json_field,
)
from anvil.lib.jsonmodel.enums import Difficulty, Population
from anvil.lib.jsonmodel.types import MobEvent

__all__ = ["SpawnRule"]


# region Conditions


class _SpawnBiomeFilter(JsonValueComponent):
    """The biomes the entity spawns in.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/biome_filter)
    """

    identifier = "minecraft:biome_filter"

    filters: list[Filter] = json_field(default_factory=list)


class _SpawnBrightnessFilter(JsonComponent):
    """The light levels the entity spawns in.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/brightness_filter)
    """

    identifier = "minecraft:brightness_filter"

    min: Annotated[int, InRange(0, 15)] | None = None
    max: Annotated[int, InRange(0, 15)] | None = None
    adjust_for_weather: bool | None = None


class _SpawnDelayFilter(JsonComponent):
    """A delay before the entity spawns.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/delay_filter)
    """

    identifier = "minecraft:delay_filter"

    min: Annotated[int, NonNegative] | None = None
    max: Annotated[int, NonNegative] | None = None
    identifier_: str = json_field(key="identifier")
    spawn_chance: Annotated[int, InRange(0, 100)] | None = None


class _SpawnDensityLimit(JsonComponent):
    """How many of the entity may spawn around.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/density_limit)
    """

    identifier = "minecraft:density_limit"

    surface: Annotated[int, NonNegative] | None = None
    underground: Annotated[int, NonNegative] | None = None


class _SpawnDifficultyFilter(JsonComponent):
    """The difficulties the entity spawns on.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/difficulty_filter)
    """

    identifier = "minecraft:difficulty_filter"

    min: Difficulty | None = None
    max: Difficulty | None = None


class _SpawnDisallowInBubble(JsonComponent):
    """Keeps the entity from spawning in bubble columns.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/disallow_spawns_in_bubble)
    """

    identifier = "minecraft:disallow_spawns_in_bubble"


class _SpawnDistanceFilter(JsonComponent):
    """The distance from the nearest player the entity spawns at.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/distance_filter)
    """

    identifier = "minecraft:distance_filter"

    min: Annotated[float, NonNegative] | None = None
    max: Annotated[float, NonNegative] | None = None


class _SpawnHeightFilter(JsonComponent):
    """The heights the entity spawns at.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/height_filter)
    """

    identifier = "minecraft:height_filter"

    min: int | None = None
    max: int | None = None


class _Herd(JsonObject):
    """One herd size the entity spawns in."""

    min_size: Annotated[int, NonNegative] | None = None
    max_size: Annotated[int, NonNegative] | None = None
    event: str | None = None
    event_skip_count: Annotated[int, NonNegative] | None = None


class _SpawnHerd(JsonValueComponent):
    """The herds the entity spawns in.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/herd)
    """

    identifier = "minecraft:herd"

    herds: list[_Herd] = json_field(default_factory=list)


class _SpawnMobEventFilter(JsonComponent):
    """The mob event the entity spawns with.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/mob_event_filter)
    """

    identifier = "minecraft:mob_event_filter"

    event: MobEvent = json_field()


class _PermuteType(JsonObject):
    """One entity that may spawn in place of this one."""

    weight: Annotated[int, NonNegative] | None = None
    entity_type: str | None = None
    guaranteed_count: Annotated[int, NonNegative] | None = None


class _SpawnPermuteType(JsonValueComponent):
    """The entities that may spawn in place of this one.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/permute_type)
    """

    identifier = "minecraft:permute_type"

    types: list[_PermuteType] = json_field(default_factory=list)


class _SpawnPlayerInVillageFilter(JsonComponent):
    """How close the player is to a village.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/player_in_village_filter)
    """

    identifier = "minecraft:player_in_village_filter"

    distance: Annotated[int, NonNegative] | None = None
    village_border_tolerance: Annotated[int, NonNegative] | None = None


class _SpawnAboveBlockFilter(JsonComponent):
    """The blocks the entity spawns above."""

    identifier = "minecraft:spawns_above_block_filter"

    blocks: list[Annotated[str | Block | BlockDescriptor, BlockId]] = json_field(
        default_factory=list
    )
    distance: Annotated[int, NonNegative] | None = None


class _SpawnLava(JsonComponent):
    """Lets the entity spawn in lava.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_lava)
    """

    identifier = "minecraft:spawns_lava"


class _SpawnOnBlockFilter(JsonValueComponent):
    """The blocks the entity spawns on.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_filter)
    """

    identifier = "minecraft:spawns_on_block_filter"

    blocks: list[Annotated[str | Block | BlockDescriptor, BlockId]] = json_field(
        default_factory=list
    )


class _SpawnOnBlockPreventedFilter(JsonValueComponent):
    """The blocks the entity never spawns on.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_prevented_filter)
    """

    identifier = "minecraft:spawns_on_block_prevented_filter"

    blocks: list[Annotated[str | Block | BlockDescriptor, BlockId]] = json_field(
        default_factory=list
    )


class _SpawnOnSurface(JsonComponent):
    """Lets the entity spawn on the surface.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_surface)
    """

    identifier = "minecraft:spawns_on_surface"


class _SpawnUnderground(JsonComponent):
    """Lets the entity spawn underground.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underground)
    """

    identifier = "minecraft:spawns_underground"


class _SpawnUnderwater(JsonComponent):
    """Lets the entity spawn underwater.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underwater)
    """

    identifier = "minecraft:spawns_underwater"


class _SpawnWeight(JsonComponent):
    """How often the condition is picked over the others.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/weight)
    """

    identifier = "minecraft:weight"

    default: Annotated[int, NonNegative] | None = None


class _SpawnWorldAgeFilter(JsonComponent):
    """The world age the entity starts spawning at.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/world_age_filter)
    """

    identifier = "minecraft:world_age_filter"

    min: Annotated[int, NonNegative] | None = None


class _SpawnEvent(JsonComponent):
    """The event run on the entity when it spawns.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawn_event)
    """

    identifier = "minecraft:spawn_event"

    event: str = json_field()


# endregion


class _SpawnRuleCondition(JsonValue):
    """A set of requirements the entity spawns under, written as one object of conditions.
    Each builder replaces the condition it sets, except `biome_filter`, `herd` and
    `permute_type`, which add to theirs."""

    conditions: Annotated[list[JsonComponent], Merged()] = json_field(
        default_factory=list
    )

    @classmethod
    def __schema_body__(cls, definitions: dict[str, Any]) -> dict[str, Any]:
        return {"type": "object", "additionalProperties": {"type": ["object", "array"]}}

    def _set(self, condition: JsonComponent) -> "_SpawnRuleCondition":
        self.conditions = [
            c for c in self.conditions if c.identifier != condition.identifier
        ] + [condition]
        return self

    def _get(self, cls: type[JsonComponent]) -> JsonComponent | None:
        return next((c for c in self.conditions if isinstance(c, cls)), None)

    def biome_filter(self, filter: Sequence[Filter]) -> "_SpawnRuleCondition":
        """Adds tests on the biome tags, which must all pass, such as
        `Filter.has_biome_tag("monster")`.

        Args:
            filter (Sequence[Filter]): The filters.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/biome_filter)
        """
        current = self._get(_SpawnBiomeFilter)
        filters = (current.filters if current else []) + list(filter)
        return self._set(_SpawnBiomeFilter(filters=filters))

    def brightness_filter(
        self,
        min_brightness: int = 0,
        max_brightness: int = 15,
        adjust_for_weather: bool = True,
    ) -> "_SpawnRuleCondition":
        """Sets the light levels the entity spawns in, from 0 (dark) to 15 (sunlight).

        Args:
            min_brightness (int, optional): The lowest light level. Defaults to 0.
            max_brightness (int, optional): The highest light level. Defaults to 15.
            adjust_for_weather (bool, optional): Lets the weather change the light level,
                so hostile mobs spawn by day in the rain. Defaults to True.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/brightness_filter)
        """
        return self._set(
            _SpawnBrightnessFilter(
                min=min_brightness,
                max=max_brightness,
                adjust_for_weather=adjust_for_weather,
            )
        )

    def delay_filter(
        self, minimum: int, maximum: int, identifier: str, spawn_chance: int
    ) -> "_SpawnRuleCondition":
        """Spawns an entity after a random delay.

        Args:
            minimum (int): The shortest delay.
            maximum (int): The longest delay.
            identifier (str): The entity that spawns after the delay.
            spawn_chance (int): The percent chance it spawns, 0 to 100.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/delay_filter)
        """
        return self._set(
            _SpawnDelayFilter(
                min=minimum,
                max=maximum,
                identifier_=identifier,
                spawn_chance=spawn_chance,
            )
        )

    def density_limit(
        self, surface: int | None = None, underground: int | None = None
    ) -> "_SpawnRuleCondition":
        """Limits how many of the entity may spawn around, apart from the population limit.

        Args:
            surface (int, optional): The most on the surface. Unlimited when unset.
            underground (int, optional): The most underground. Unlimited when unset.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/density_limit)
        """
        return self._set(_SpawnDensityLimit(surface=surface, underground=underground))

    def difficulty_filter(
        self,
        min_difficulty: Difficulty | None = None,
        max_difficulty: Difficulty | None = None,
    ) -> "_SpawnRuleCondition":
        """Sets the difficulties the entity spawns on.

        Args:
            min_difficulty (Difficulty, optional): The lowest difficulty.
            max_difficulty (Difficulty, optional): The highest difficulty.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/difficulty_filter)
        """
        return self._set(_SpawnDifficultyFilter(min=min_difficulty, max=max_difficulty))

    def disallow_spawns_in_bubble(self) -> "_SpawnRuleCondition":
        """Keeps the entity from spawning in bubble columns.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/disallow_spawns_in_bubble)
        """
        return self._set(_SpawnDisallowInBubble())

    def distance_filter(
        self, range: tuple[float, float] = (24, 128)
    ) -> "_SpawnRuleCondition":
        """Sets how far from the nearest player the entity spawns.

        Args:
            range (tuple[float, float], optional): The (min, max) distance in blocks.
                Defaults to (24, 128).

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/distance_filter)
        """
        return self._set(_SpawnDistanceFilter(min=range[0], max=range[1]))

    def height_filter(self, min: int, max: int) -> "_SpawnRuleCondition":
        """Sets the heights the entity spawns at.

        Args:
            min (int): The lowest Y.
            max (int): The highest Y.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/height_filter)
        """
        return self._set(_SpawnHeightFilter(min=min, max=max))

    def herd(
        self,
        min_size: int = 1,
        max_size: int = 4,
        spawn_event: str | None = None,
        event_skip_count: int = 0,
    ) -> "_SpawnRuleCondition":
        """Adds a herd size the entity spawns in.

        Args:
            min_size (int, optional): The smallest herd. Defaults to 1.
            max_size (int, optional): The largest herd. Defaults to 4.
            spawn_event (str, optional): An event run on some of the herd.
            event_skip_count (int, optional): How many spawn before the event runs.
                Defaults to 0, written only with an event.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/herd)
        """
        herd = _Herd(
            min_size=min_size,
            max_size=max_size,
            event=spawn_event,
            event_skip_count=None if spawn_event is None else event_skip_count,
        )
        current = self._get(_SpawnHerd)
        return self._set(_SpawnHerd(herds=(current.herds if current else []) + [herd]))

    def mob_event_filter(
        self,
        event: Literal[
            "minecraft:pillager_patrols_event",
            "minecraft:wandering_trader_event",
            "minecraft:ender_dragon_event",
        ],
    ) -> "_SpawnRuleCondition":
        """Spawns the entity only with a mob event.

        Args:
            event (str): `minecraft:pillager_patrols_event`,
                `minecraft:wandering_trader_event` or `minecraft:ender_dragon_event`.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/mob_event_filter)
        """
        return self._set(_SpawnMobEventFilter(event=event))

    def permute_type(
        self,
        entity_type: str | None,
        weight: int = 10,
        spawn_event: str | None = None,
        guaranteed_count: int | None = None,
    ) -> "_SpawnRuleCondition":
        """Adds an entity that may spawn in place of this one. The weights of all the
        permutations add up to 100.

        Args:
            entity_type (str | None): The entity spawned instead, or None for this entity.
            weight (int, optional): Its share out of 100. Defaults to 10.
            spawn_event (str, optional): An event run on the entity when it spawns.
            guaranteed_count (int, optional): How many spawn before the other permutations.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/permute_type)
        """
        if entity_type is not None and spawn_event is not None:
            entity_type = f"{entity_type}<{spawn_event}>"
        permutation = _PermuteType(
            weight=weight, entity_type=entity_type, guaranteed_count=guaranteed_count
        )
        current = self._get(_SpawnPermuteType)
        return self._set(
            _SpawnPermuteType(types=(current.types if current else []) + [permutation])
        )

    def player_in_village_filter(
        self, distance: int, village_border_tolerance: int
    ) -> "_SpawnRuleCondition":
        """Spawns the entity by how close the player is to a village.

        Args:
            distance (int): The distance from the village.
            village_border_tolerance (int): The tolerance past the village border.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/player_in_village_filter)
        """
        return self._set(
            _SpawnPlayerInVillageFilter(
                distance=distance, village_border_tolerance=village_border_tolerance
            )
        )

    def spawns_above_block_filter(
        self, blocks: Sequence[str | Block | BlockDescriptor], distance: int = 1
    ) -> "_SpawnRuleCondition":
        """Spawns the entity above some blocks.

        Args:
            blocks (Sequence[Block | BlockDescriptor | str]): The blocks.
            distance (int, optional): How far above the block. Defaults to 1.
        """
        return self._set(_SpawnAboveBlockFilter(blocks=list(blocks), distance=distance))

    def spawns_in_lava(self) -> "_SpawnRuleCondition":
        """Lets the entity spawn in lava.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_lava)
        """
        return self._set(_SpawnLava())

    def spawns_on_block_filter(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "_SpawnRuleCondition":
        """Spawns the entity only on some blocks.

        Args:
            blocks (Sequence[Block | BlockDescriptor | str]): The blocks.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_filter)
        """
        return self._set(_SpawnOnBlockFilter(blocks=list(blocks)))

    def spawns_on_block_prevented_filter(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "_SpawnRuleCondition":
        """Keeps the entity from spawning on some blocks.

        Args:
            blocks (Sequence[Block | BlockDescriptor | str]): The blocks.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_block_prevented_filter)
        """
        return self._set(_SpawnOnBlockPreventedFilter(blocks=list(blocks)))

    def spawns_on_surface(self) -> "_SpawnRuleCondition":
        """Lets the entity spawn on the surface.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_on_surface)
        """
        return self._set(_SpawnOnSurface())

    def spawns_underground(self) -> "_SpawnRuleCondition":
        """Lets the entity spawn underground, in caves.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underground)
        """
        return self._set(_SpawnUnderground())

    def spawns_underwater(self) -> "_SpawnRuleCondition":
        """Lets the entity spawn in water.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawns_underwater)
        """
        return self._set(_SpawnUnderwater())

    def weight(self, weight: int = 0) -> "_SpawnRuleCondition":
        """Sets how often this condition is picked over the others: higher spawns more.

        Args:
            weight (int, optional): The weight. Defaults to 0.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/weight)
        """
        return self._set(_SpawnWeight(default=weight))

    def world_age_filter(self, min: int) -> "_SpawnRuleCondition":
        """Waits until the world is old enough before the entity spawns.

        Args:
            min (int): The world age, in ticks.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/world_age_filter)
        """
        return self._set(_SpawnWorldAgeFilter(min=min))

    def spawn_event(
        self, event: str = "minecraft:entity_spawned"
    ) -> "_SpawnRuleCondition":
        """Sets the event run on the entity when it spawns.

        Args:
            event (str, optional): The event. Defaults to `minecraft:entity_spawned`.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/spawn_event)
        """
        return self._set(_SpawnEvent(event=event))


class _SpawnRuleDescription(JsonObject):
    """The `description` of a spawn rule, and its builders."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None
    population_control: Population = json_field(default=Population.Ambient)

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")

    def set_population_control(self, population: Population) -> "_SpawnRuleDescription":
        """Puts the entity in a population pool, whose spawn limit it counts toward:
        `Animal`, `WaterAnimal`, `Monster`, `Ambient`, `Cat` (spawned by villages) or
        `Pillager`. Defaults to `Ambient`.

        Args:
            population (Population): The pool.
        """
        self.population_control = population
        return self


class _SpawnRules(JsonObject):
    """The `minecraft:spawn_rules` body."""

    description: _SpawnRuleDescription = json_field(
        default_factory=_SpawnRuleDescription
    )
    conditions: list[_SpawnRuleCondition] = json_field(default_factory=list)


class _SpawnRulesFile(JsonObject):
    """The content of a spawn rules file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:spawn_rules",
    )

    format_version: str = json_field(default=SPAWN_RULES_VERSION, init=False)
    spawn_rules: _SpawnRules = json_field(
        default_factory=_SpawnRules, key="minecraft:spawn_rules"
    )


class SpawnRule(JsonFile[_SpawnRulesFile]):
    """An entity's spawn rules: its population pool and the conditions it spawns under.
    Written only when it has conditions.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/cliententitydocumentation/datadrivenspawning)
    """

    _extension = ".spawn_rules.json"
    _pack = Pack.BP
    _folder = "spawn_rules"
    _object_type = "Spawn Rule"

    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        """Creates the spawn rules of an entity.

        Args:
            identifier (str): The entity identifier, such as `mypack:custom_mob`.
            is_vanilla (bool, optional): If the entity is a vanilla one.
        """
        super().__init__(identifier, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _SpawnRuleDescription:
        """The description builders, such as `set_population_control`."""
        return self._document.spawn_rules.description

    @property
    def add_condition(self) -> _SpawnRuleCondition:
        """Adds a set of conditions the entity spawns under, and returns it. Each set is
        another way to spawn, such as on the surface or underground."""
        condition = _SpawnRuleCondition()
        self._document.spawn_rules.conditions.append(condition)
        return condition

    def queue(self, directory: str | None = None) -> "SpawnRule | None":
        """Queues the spawn rules for export, when they have conditions.

        Args:
            directory (str, optional): The folder inside `spawn_rules`.
        """
        if self._document.spawn_rules.conditions:
            return super().queue(directory=directory)
        return None
