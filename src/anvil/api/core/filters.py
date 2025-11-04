
from anvil.api.vanilla.biomes import MinecraftBiomeTags, MinecraftBiomeTypes
from anvil.lib.config import CONFIG
from anvil.lib.enums import (
    Difficulty,
    FilterEquipmentDomain,
    FilterOperation,
    FilterSubject,
    PlayerAbilities,
    Weather,
)
from anvil.lib.schemas import BiomeDescriptor, BlockDescriptor
from anvil.lib.types import Identifier


class Filter:
    # Basic configuration
    @staticmethod
    def _construct_filter(filter_name, subject, operator, domain, value):
        """Constructs a filter dictionary with the specified parameters.

        Parameters:
            filter_name (str): The name/test type of the filter
            subject (FilterSubject): The subject to test against
            operator (FilterOperation): The operation to perform
            domain (str|None): Optional domain for certain filter types
            value (any): The value to test against

        Returns:
            dict: A properly formatted filter dictionary
        """
        _filter = {"test": filter_name, "value": value}
        if subject != FilterSubject.Self:
            _filter["subject"] = subject
        if operator != FilterOperation.Equals:
            _filter["operator"] = operator
        if domain != None:
            _filter["domain"] = domain

        return _filter

    # Filter Groups
    @staticmethod
    def all_of(*filters: "Filter"):
        """Returns true when all of the filters evaluate to true.

        Parameters:
            *filters: Variable number of filter conditions

        Returns:
            dict: Filter group requiring all conditions to be true

        Example:
            Filter.all_of(
                Filter.is_family("monster"),
                Filter.is_difficulty(Difficulty.Hard)
            )

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filterlist
        """
        return {"all_of": [*filters]}

    @staticmethod
    def any_of(*filters: "Filter"):
        """Returns true when any of the filters evaluate to true.

        Parameters:
            *filters: Variable number of filter conditions

        Returns:
            dict: Filter group requiring at least one condition to be true

        Example:
            Filter.any_of(
                Filter.is_family("monster"),
                Filter.is_family("creature")
            )

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filterlist
        """
        return {"any_of": [*filters]}

    @staticmethod
    def none_of(*filters: "Filter"):
        """Returns true when none of the filters evaluate to true.

        Parameters:
            *filters: Variable number of filter conditions

        Returns:
            dict: Filter group requiring no conditions to be true

        Example:
            Filter.none_of(
                Filter.is_family("player"),
                Filter.has_tag("peaceful")
            )

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filterlist
        """
        return {"none_of": [*filters]}

    @classmethod
    def actor_health(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("actor_health", subject, operator, None, value)

    @classmethod
    def all_slots_empty(
        cls,
        value: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the designated equipment location for the subject entity is completely empty.

        Parameters:
            value (FilterEquipmentDomain, optional): The equipment location to test. Defaults to FilterEquipmentDomain.Any.
            subject (FilterSubject, optional): Subject to test the value against. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use in testing. Defaults to FilterOperation.Equals.
        """
        return cls._construct_filter("all_slots_empty", subject, operator, None, value)

    @classmethod
    def any_slot_empty(
        cls,
        value: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the designated equipment location for the subject entity has any empty slot.

        Parameters:
            value (FilterEquipmentDomain, optional): The equipment location to test. Defaults to FilterEquipmentDomain.Any.
            subject (FilterSubject, optional): Subject to test the value against. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use in testing. Defaults to FilterOperation.Equals.
        """
        return cls._construct_filter("all_slots_empty", subject, operator, None, value)

    @classmethod
    def bool_property(
        cls,
        value: bool,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "bool_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value
        )

    @classmethod
    def clock_time(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Compares the current time with a float value in the range (0.0, 1.0).

        Time values: 0.0=Noon, 0.25=Sunset, 0.5=Midnight, 0.75=Sunrise

        Parameters:
            value (float): Time value between 0.0 and 1.0
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing game time

        Example:
            Filter.clock_time(0.0)   # Test for noon
            Filter.clock_time(0.5)   # Test for midnight

        Note:
            Use hourly_clock_time for integer-based time (0-24000 range)

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/clock_time
        """
        return cls._construct_filter(
            "clock_time", subject, operator, None, max(0.0, min(1.0, value))
        )

    @classmethod
    def distance_to_nearest_player(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Compares the distance to the nearest Player with a float value.

        Parameters:
            value (float): The distance value to compare against (minimum 0.0)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing distance to nearest player

        Example:
            # Test if entity is within 10 blocks of nearest player
            Filter.distance_to_nearest_player(10.0, operator=FilterOperation.LessEqual)

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/distance_to_nearest_player
        """
        return cls._construct_filter(
            "distance_to_nearest_player", subject, operator, None, max(0, value)
        )

    @classmethod
    def enum_property(
        cls,
        value: str,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "enum_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value
        )

    @classmethod
    def float_property(
        cls,
        value: float,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "float_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value
        )

    @classmethod
    def has_ability(
        cls,
        value: PlayerAbilities,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity has the named ability.

        Parameters:
            value (str): The ability type to test. Valid values:
                - "flySpeed", "flying", "instabuild", "invulnerable",
                - "lightning", "mayfly", "mute", "noclip",
                - "verticalFlySpeed", "walkSpeed", "worldbuilder"
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing player ability

        Example:
            Filter.has_ability("instabuild")  # Test if player has creative mode
            Filter.has_ability("flying")      # Test if player can fly

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_ability
        """
        return cls._construct_filter("has_ability", subject, operator, None, value)

    @classmethod
    def has_biome_tag(
        cls,
        value: MinecraftBiomeTags,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Checks if the entity is in a biome with the specified tag."""
        return cls._construct_filter("has_biome_tag", subject, operator, None, value)

    @classmethod
    def has_component(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity contains the named component.

        Parameters:
            value (str): The component identifier to test for (e.g., "minecraft:health")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing for component presence

        Example:
            # Test if entity has health component
            Filter.has_component("minecraft:health")

            # Test if target has tameable component
            Filter.has_component("minecraft:tameable", subject=FilterSubject.Target)

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_component
        """
        return cls._construct_filter("has_component", subject, operator, None, value)

    @classmethod
    def has_container_open(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject Player entity has opened a container.

        Parameters:
            value (bool): Whether container is open
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing if player has container open

        Example:
            Filter.has_container_open(True)  # Test if player has container open

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_container_open
        """
        return cls._construct_filter(
            "has_container_open", subject, operator, None, value
        )

    @classmethod
    def has_damaged_equipment(
        cls,
        value: str,
        domain: FilterEquipmentDomain,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "has_damaged_equipment", subject, operator, domain, value
        )

    @classmethod
    def has_damage(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("has_damage", subject, operator, None, value)

    @classmethod
    def has_equipment(
        cls,
        value: int,
        domain: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("has_equipment", subject, operator, domain, value)

    @classmethod
    def has_equipment_tag(
        cls,
        value: str,
        domain: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("has_equipment", subject, operator, domain, value)

    @classmethod
    def has_mob_effect(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the Subject has the specified mob effect.

        Parameters:
            value (str): The mob effect identifier (e.g., "poison", "regeneration")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing mob effect presence

        Example:
            Filter.has_mob_effect("poison")       # Test if entity is poisoned
            Filter.has_mob_effect("regeneration") # Test if entity is regenerating

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_mob_effect
        """
        return cls._construct_filter("has_mob_effect", subject, operator, None, value)

    @classmethod
    def has_nametag(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject has been given a custom name.

        Parameters:
            value (bool): Whether entity has a nametag
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing nametag presence

        Example:
            Filter.has_nametag(True)  # Test if entity has been named

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_nametag
        """
        return cls._construct_filter("has_nametag", subject, operator, None, value)

    @classmethod
    def has_property(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "has_property", subject, operator, None, f"{CONFIG.NAMESPACE}:{value}"
        )

    @classmethod
    def has_ranged_weapon(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is holding a ranged weapon like a bow or crossbow.

        Parameters:
            value (bool): Whether entity has ranged weapon
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing ranged weapon possession

        Example:
            Filter.has_ranged_weapon(True)  # Test if entity has bow/crossbow

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_ranged_weapon
        """
        return cls._construct_filter(
            "has_ranged_weapon", subject, operator, None, value
        )

    @classmethod
    def has_silk_touch(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is holding an item with silk touch enchantment.

        Parameters:
            value (bool): Whether item has silk touch
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing silk touch presence

        Example:
            Filter.has_silk_touch(True)  # Test if held item has silk touch

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_silk_touch
        """
        return cls._construct_filter("has_silk_touch", subject, operator, None, value)

    @classmethod
    def has_tag(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("has_tag", subject, operator, None, value)

    @classmethod
    def has_target(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("has_target", subject, operator, None, value)

    @classmethod
    def has_trade_supply(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the target has any trade supply left.

        Parameters:
            value (bool): Whether entity has trade supply
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing trade supply availability

        Example:
            Filter.has_trade_supply(True)  # Test if villager has trades available

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/has_trade_supply
        """
        return cls._construct_filter("has_trade_supply", subject, operator, None, value)

    @classmethod
    def home_distance(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("home_distance", subject, operator, None, value)

    @classmethod
    def hourly_clock_time(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Compares the current 24 hour time with an int value in the range [0, 24000].

        This is an updated version of clock_time that uses integers based on in-game time.

        Parameters:
            value (int): Time value between 0 and 24000 (0=dawn, 6000=noon, 12000=sunset, 18000=midnight)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing game time in ticks

        Example:
            Filter.hourly_clock_time(6000)   # Test for noon
            Filter.hourly_clock_time(18000)  # Test for midnight

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/hourly_clock_time
        """
        return cls._construct_filter(
            "hourly_clock_time", subject, operator, None, max(0, min(24000, value))
        )

    @classmethod
    def inactivity_timer(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the specified duration in seconds of inactivity for despawning has been reached.

        Parameters:
            value (int): Inactivity duration in seconds
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing inactivity timer

        Example:
            Filter.inactivity_timer(300, operator=FilterOperation.GreaterEqual)  # 5+ minutes inactive

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/inactivity_timer
        """
        return cls._construct_filter(
            "inactivity_timer", subject, operator, None, max(0, value)
        )

    @classmethod
    def in_block(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is inside a specified Block type.

        Parameters:
            value (str): Block identifier (e.g., "minecraft:water", "minecraft:lava")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing if entity is inside block

        Example:
            Filter.in_block("minecraft:water")  # Test if entity is in water block
            Filter.in_block("minecraft:lava")   # Test if entity is in lava

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_block
        """
        return cls._construct_filter("in_block", subject, operator, None, value)

    @classmethod
    def in_caravan(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is in a caravan.

        Parameters:
            value (bool): Whether entity is in caravan
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing caravan membership

        Example:
            Filter.in_caravan(True)  # Test if llama is in caravan

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_caravan
        """
        return cls._construct_filter("in_caravan", subject, operator, None, value)

    @classmethod
    def in_clouds(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is in the clouds.

        Parameters:
            value (bool): Whether entity is in clouds
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing cloud height

        Example:
            Filter.in_clouds(True)  # Test if entity is at cloud level

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_clouds
        """
        return cls._construct_filter("in_clouds", subject, operator, None, value)

    @classmethod
    def in_contact_with_water(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity in contact with any water: water, rain, splash water bottle.

        Parameters:
            value (bool): Whether entity is in contact with water
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing water contact

        Example:
            Filter.in_contact_with_water(True)  # Test if entity touches any water source

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_contact_with_water
        """
        return cls._construct_filter(
            "in_contact_with_water", subject, operator, None, value
        )

    @classmethod
    def in_lava(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is in lava.

        Parameters:
            value (bool): Whether entity is in lava
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing lava immersion

        Example:
            Filter.in_lava(True)  # Test if entity is in lava

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_lava
        """
        return cls._construct_filter("in_lava", subject, operator, None, value)

    @classmethod
    def in_nether(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is in Nether dimension.

        Parameters:
            value (bool): Whether entity is in Nether
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing Nether dimension

        Example:
            Filter.in_nether(True)  # Test if entity is in Nether

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_nether
        """
        return cls._construct_filter("in_nether", subject, operator, None, value)

    @classmethod
    def in_overworld(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is in Overworld dimension.

        Parameters:
            value (bool): Whether entity is in Overworld
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing Overworld dimension

        Example:
            Filter.in_overworld(True)  # Test if entity is in Overworld

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_overworld
        """
        return cls._construct_filter("in_overworld", subject, operator, None, value)

    @classmethod
    def int_property(
        cls,
        value: int,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "int_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value
        )

    @classmethod
    def in_water(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("in_water", subject, operator, None, value)

    @classmethod
    def in_water_or_rain(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is in water or rain.

        Parameters:
            value (bool): Whether entity is in water or rain
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing water or rain exposure

        Example:
            Filter.in_water_or_rain(True)  # Test if entity is wet

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/in_water_or_rain
        """
        return cls._construct_filter("in_water_or_rain", subject, operator, None, value)

    @classmethod
    def is_altitude(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests the current altitude against a provided value.

        Parameters:
            value (int): Y-coordinate altitude to test
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing altitude/Y position

        Example:
            Filter.is_altitude(64, operator=FilterOperation.Greater)  # Above sea level

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_altitude
        """
        return cls._construct_filter("is_altitude", subject, operator, None, value)

    @classmethod
    def is_avoiding_mobs(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is fleeing from other mobs.

        Parameters:
            value (bool): Whether entity is avoiding mobs
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing avoidance behavior

        Example:
            Filter.is_avoiding_mobs(True)  # Test if entity is fleeing

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_avoiding_mobs
        """
        return cls._construct_filter("is_avoiding_mobs", subject, operator, None, value)

    @classmethod
    def is_baby(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is a baby.

        Parameters:
            value (bool): Whether entity is baby
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing baby state

        Example:
            Filter.is_baby(True)  # Test if entity is baby/child

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_baby
        """
        return cls._construct_filter("is_baby", subject, operator, None, value)

    @classmethod
    def is_biome(
        cls,
        value: MinecraftBiomeTypes | BiomeDescriptor,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "is_biome", subject, operator, None, value.identifier
        )

    @classmethod
    def is_block(
        cls,
        value: BlockDescriptor | Identifier,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the block has the given name.

        Parameters:
            value (BlockDescriptor | Identifier): Block descriptor or identifier to test
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing block type

        Example:
            Filter.is_block("minecraft:stone")  # Test if block is stone

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_block
        """
        from anvil.lib.schemas import MinecraftBlockDescriptor

        if not isinstance(value, (MinecraftBlockDescriptor, str)):
            raise TypeError(
                f"Expected MinecraftBlockDescriptor or Identifier, got {type(value).__name__}. Filter [is_block]"
            )

        return cls._construct_filter(
            "is_block",
            subject,
            operator,
            None,
            str(value),
        )

    @classmethod
    def is_bound_to_creaking_heart(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "is_bound_to_creaking_heart", subject, operator, None, value
        )

    @classmethod
    def is_brightness(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests the current brightness against a provided value in the range (0.0f, 1.0f).

        Parameters:
            value (float): Brightness value between 0.0 (darkest) and 1.0 (brightest)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing brightness level

        Example:
            Filter.is_brightness(0.5, operator=FilterOperation.Less)  # Test if dim

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_brightness
        """
        return cls._construct_filter(
            "is_brightness", subject, operator, None, max(0.0, min(1.0, value))
        )

    @classmethod
    def is_climbing(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is climbing.

        Parameters:
            value (bool): Whether entity is climbing
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing climbing state

        Example:
            Filter.is_climbing(True)  # Test if entity is on ladder/vines

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_climbing
        """
        return cls._construct_filter("is_climbing", subject, operator, None, value)

    @classmethod
    def is_color(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is the named color.

        Parameters:
            value (str): Color name (e.g., "red", "blue", "white", etc.)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing entity color

        Example:
            Filter.is_color("red")   # Test if sheep is red
            Filter.is_color("white") # Test if wolf is white

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_color
        """
        return cls._construct_filter("is_color", subject, operator, None, value)

    @classmethod
    def is_daytime(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_daytime", subject, operator, None, value)

    @classmethod
    def is_difficulty(
        cls,
        value: Difficulty,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter(
            "is_difficulty", subject, operator, None, str(value)
        )

    @classmethod
    def is_family(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is a member of the named family.

        Parameters:
            value (str): The family name to test for (e.g., "monster", "player", "mob")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing family membership

        Example:
            # Test if entity is a monster
            Filter.is_family("monster")

            # Test if target is not a player
            Filter.is_family("player", subject=FilterSubject.Target, operator=FilterOperation.Not)

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_family
        """
        return cls._construct_filter("is_family", subject, operator, None, value)

    @classmethod
    def is_game_rule(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether a named game rule is active.

        Parameters:
            value (str): Game rule name (e.g., "doMobSpawning", "keepInventory")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing game rule state

        Example:
            Filter.is_game_rule("doMobSpawning")  # Test if mob spawning enabled

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_game_rule
        """
        return cls._construct_filter("is_game_rule", subject, operator, None, value)

    @classmethod
    def is_humid(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the Subject is in an area with humidity.

        Parameters:
            value (bool): Whether area is humid
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing humidity level

        Example:
            Filter.is_humid(True)  # Test if in humid biome (jungle, swamp)

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_humid
        """
        return cls._construct_filter("is_humid", subject, operator, None, value)

    @classmethod
    def is_immobile(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is immobile.

        Parameters:
            value (bool): Whether entity is immobile
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing immobility state

        Example:
            Filter.is_immobile(True)  # Test if entity cannot move

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_immobile
        """
        return cls._construct_filter("is_immobile", subject, operator, None, value)

    @classmethod
    def is_in_village(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the Subject is inside the bounds of a village.

        Parameters:
            value (bool): Whether entity is in village
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing village bounds

        Example:
            Filter.is_in_village(True)  # Test if entity is within village

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_in_village
        """
        return cls._construct_filter("is_in_village", subject, operator, None, value)

    @classmethod
    def is_leashed(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is leashed.

        Parameters:
            value (bool): Whether entity is leashed
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing leash state

        Example:
            Filter.is_leashed(True)  # Test if mob is on leash

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_leashed
        """
        return cls._construct_filter("is_leashed", subject, operator, None, value)

    @classmethod
    def is_leashed_to(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity leashed to the calling entity.

        Parameters:
            value (bool): Whether subject is leashed to caller
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing leash connection

        Example:
            Filter.is_leashed_to(True, subject=FilterSubject.Target)  # Test if target is leashed to cls

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_leashed_to
        """
        return cls._construct_filter("is_leashed_to", subject, operator, None, value)

    @classmethod
    def is_mark_variant(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_mark_variant", subject, operator, None, value)

    @classmethod
    def is_missing_health(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is not at full health.

        Parameters:
            value (bool): Whether entity is missing health
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing damaged state

        Example:
            Filter.is_missing_health(True)  # Test if entity is damaged

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_missing_health
        """
        return cls._construct_filter(
            "is_missing_health", subject, operator, None, value
        )

    @classmethod
    def is_moving(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is moving.

        Parameters:
            value (bool): The movement state to test for
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing movement state

        Example:
            Filter.is_moving(True)  # Test if entity is moving

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_moving
        """
        return cls._construct_filter("is_moving", subject, operator, None, value)

    @classmethod
    def is_navigating(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is currently pathfinding.

        Parameters:
            value (bool): Whether entity is pathfinding
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing navigation state

        Example:
            Filter.is_navigating(True)  # Test if mob is pathfinding to destination

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_navigating
        """
        return cls._construct_filter("is_navigating", subject, operator, None, value)

    @classmethod
    def is_owner(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_owner", subject, operator, None, value)

    @classmethod
    def is_panicking(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_panicking", subject, operator, None, value)

    @classmethod
    def is_persistent(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject's persistence matches the bool value passed in.

        Parameters:
            value (bool): Persistence state to test
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing persistence

        Example:
            Filter.is_persistent(True)  # Test if entity won't despawn

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_persistent
        """
        return cls._construct_filter("is_persistent", subject, operator, None, value)

    @classmethod
    def is_raider(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_raider", subject, operator, None, value)

    @classmethod
    def is_riding(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_riding", subject, operator, None, value)

    @classmethod
    def is_riding_self(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is riding the calling entity.

        Parameters:
            value (bool): Whether subject is riding caller
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing rider relationship

        Example:
            Filter.is_riding_self(True, subject=FilterSubject.Target)  # Test if target is riding cls

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_riding_self
        """
        return cls._construct_filter("is_riding_self", subject, operator, None, value)

    @classmethod
    def is_sitting(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_sitting", subject, operator, None, value)

    @classmethod
    def is_skin_id(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_skin_id", subject, operator, None, value)

    @classmethod
    def is_sleeping(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the Subject is sleeping.

        Parameters:
            value (bool): Whether entity is sleeping
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing sleep state

        Example:
            Filter.is_sleeping(True)  # Test if villager is sleeping in bed

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_sleeping
        """
        return cls._construct_filter("is_sleeping", subject, operator, None, value)

    @classmethod
    def is_sneak_held(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity has the sneak input held.

        Parameters:
            value (bool): Whether sneak input is held
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing sneak input

        Example:
            Filter.is_sneak_held(True)  # Test if player is holding sneak button

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_sneak_held
        """
        return cls._construct_filter("is_sneak_held", subject, operator, None, value)

    @classmethod
    def is_sneaking(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject entity is sneaking.

        Parameters:
            value (bool): Whether entity is sneaking
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing sneak state

        Example:
            Filter.is_sneaking(True)  # Test if player is sneaking

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_sneaking
        """
        return cls._construct_filter("is_sneaking", subject, operator, None, value)

    @classmethod
    def is_snow_covered(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the Subject is in an area with snow cover.

        Parameters:
            value (bool): Whether area has snow cover
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing snow coverage

        Example:
            Filter.is_snow_covered(True)  # Test if in snowy biome

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_snow_covered
        """
        return cls._construct_filter("is_snow_covered", subject, operator, None, value)

    @classmethod
    def is_sprinting(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_sprinting", subject, operator, None, value)

    @classmethod
    def is_target(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_target", subject, operator, None, value)

    @classmethod
    def is_temperature_type(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests whether the current temperature is a given type.

        Parameters:
            value (str): Temperature type ("cold", "mild", "ocean", "warm")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing temperature category

        Example:
            Filter.is_temperature_type("cold")  # Test if in cold biome

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_temperature_type
        """
        return cls._construct_filter(
            "is_temperature_type", subject, operator, None, value
        )

    @classmethod
    def is_temperature_value(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests the current temperature against a provided value in the range (0.0, 1.0).

        Where 0.0 is the coldest temp and 1.0 is the hottest.

        Parameters:
            value (float): Temperature value between 0.0 (coldest) and 1.0 (hottest)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing temperature value

        Example:
            Filter.is_temperature_value(0.8, operator=FilterOperation.Greater)  # Test if very hot

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_temperature_value
        """
        return cls._construct_filter(
            "is_temperature_value", subject, operator, None, max(0.0, min(1.0, value))
        )

    @classmethod
    def is_underground(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is underground.

        Parameters:
            value (bool): Whether entity is underground
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing underground state

        Example:
            Filter.is_underground(True)  # Test if entity is below surface

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_underground
        """
        return cls._construct_filter("is_underground", subject, operator, None, value)

    @classmethod
    def is_underwater(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_underwater", subject, operator, None, value)

    @classmethod
    def is_variant(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_variant", subject, operator, None, value)

    @classmethod
    def is_vehicle_family(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity's vehicle is a member of the named family.

        Parameters:
            value (str): Vehicle family name to test
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing vehicle family

        Example:
            Filter.is_vehicle_family("boat")  # Test if riding boat

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_vehicle_family
        """
        return cls._construct_filter(
            "is_vehicle_family", subject, operator, None, value
        )

    @classmethod
    def is_visible(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("is_visible", subject, operator, None, value)

    @classmethod
    def is_waterlogged(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject block is submerged in water.

        Parameters:
            value (bool): Whether block is waterlogged
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing waterlogged state

        Example:
            Filter.is_waterlogged(True, subject=FilterSubject.Block)  # Test if block is waterlogged

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/is_waterlogged
        """
        return cls._construct_filter("is_waterlogged", subject, operator, None, value)

    @classmethod
    def light_level(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the mob is outside of the specified light level range (0, 16).

        Parameters:
            value (int): Light level value between 0 and 16
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing light level

        Example:
            Filter.light_level(7, operator=FilterOperation.Less)  # Test if dark enough for mob spawning

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/light_level
        """
        return cls._construct_filter(
            "light_level", subject, operator, None, max(0, min(16, value))
        )

    @classmethod
    def moon_intensity(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Compares the current moon intensity with a float value in the range (0.0, 1.0).

        Parameters:
            value (float): Moon intensity between 0.0 and 1.0
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing moon brightness

        Example:
            Filter.moon_intensity(1.0)  # Test for full moon

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/moon_intensity
        """
        return cls._construct_filter(
            "moon_intensity", subject, operator, None, max(0.0, min(1.0, value))
        )

    @classmethod
    def moon_phase(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Compares the current moon phase with an integer value in the range (0, 7).

        Parameters:
            value (int): Moon phase between 0 and 7 (0=full moon, 4=new moon)
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing moon phase

        Example:
            Filter.moon_phase(0)  # Test for full moon
            Filter.moon_phase(4)  # Test for new moon

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/moon_phase
        """
        return cls._construct_filter(
            "moon_phase", subject, operator, None, max(0, min(7, value))
        )

    @classmethod
    def on_fire(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is on fire.

        Parameters:
            value (bool): Whether entity is on fire
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing fire state

        Example:
            Filter.on_fire(True)  # Test if entity is burning

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/on_fire
        """
        return cls._construct_filter("on_fire", subject, operator, None, value)

    @classmethod
    def on_ground(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("on_ground", subject, operator, None, value)

    @classmethod
    def on_hot_block(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is on a hot block (like magma).

        Parameters:
            value (bool): Whether entity is on hot block
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing hot block contact

        Example:
            Filter.on_hot_block(True)  # Test if standing on magma block

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/on_hot_block
        """
        return cls._construct_filter("on_hot_block", subject, operator, None, value)

    @classmethod
    def on_ladder(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the subject entity is on a ladder.

        Parameters:
            value (bool): Whether entity is on ladder
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing ladder state

        Example:
            Filter.on_ladder(True)  # Test if entity is climbing ladder

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/on_ladder
        """
        return cls._construct_filter("on_ladder", subject, operator, None, value)

    @classmethod
    def owner_distance(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("owner_distance", subject, operator, None, value)

    @classmethod
    def random_chance(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("random_chance", subject, operator, None, value)

    @classmethod
    def rider_count(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("rider_count", subject, operator, None, value)

    @classmethod
    def surface_mob(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is a surface mob.

        Parameters:
            value (bool): Whether entity is surface mob
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing surface mob classification

        Example:
            Filter.surface_mob(True)  # Test if mob spawns on surface

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/surface_mob
        """
        return cls._construct_filter("surface_mob", subject, operator, None, value)

    @classmethod
    def taking_fire_damage(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests if the subject is taking fire damage.

        Parameters:
            value (bool): Whether entity is taking fire damage
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing fire damage

        Example:
            Filter.taking_fire_damage(True)  # Test if entity is burning and taking damage

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/taking_fire_damage
        """
        return cls._construct_filter(
            "taking_fire_damage", subject, operator, None, value
        )

    @classmethod
    def target_distance(
        cls,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("target_distance", subject, operator, None, value)

    @classmethod
    def trusts(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true if the subject is trusted by entity.

        Parameters:
            value (bool): Whether entity trusts subject
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing trust relationship

        Example:
            Filter.trusts(True, subject=FilterSubject.Player)  # Test if entity trusts player

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/trusts
        """
        return cls._construct_filter("trusts", subject, operator, None, value)

    @classmethod
    def was_last_hurt_by(
        cls,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return cls._construct_filter("was_last_hurt_by", subject, operator, None, value)

    @classmethod
    def weather(
        cls,
        value: Weather,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests the current weather in the dimension against a provided weather value.

        Parameters:
            value (str): Weather type ("clear", "rain", "thunder")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing weather conditions

        Example:
            Filter.weather("rain")     # Test if raining
            Filter.weather("thunder")  # Test if thunderstorm

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/weather
        """
        return cls._construct_filter("weather", subject, operator, None, value)

    @classmethod
    def weather_at_position(
        cls,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Tests the current weather, at the actor's position, against a provided weather value.

        Parameters:
            value (str): Weather type ("clear", "rain", "thunder")
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing local weather conditions

        Example:
            Filter.weather_at_position("rain")  # Test if raining at exact position

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/weather_at_position
        """
        return cls._construct_filter(
            "weather_at_position", subject, operator, None, value
        )

    @classmethod
    def y_rotation(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns the Y rotation of this entity.

        Parameters:
            value (float): Y rotation value in degrees
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Returns:
            dict: Filter testing Y rotation

        Example:
            Filter.y_rotation(0.0, operator=FilterOperation.Less)  # Test if facing north-ish

        Reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/filters/y_rotation
        """
        return cls._construct_filter("y_rotation", subject, operator, None, value)
