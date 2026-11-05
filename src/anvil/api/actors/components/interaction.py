from typing import Annotated, Any, Literal

from anvil.api.actors.entity import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.components import EventTrigger
from anvil.api.core.filters import Filter
from anvil.api.items.items import Item
from anvil.api.vanilla.effects import MinecraftEffects
from anvil.api.world.loot_tables import LootTable
from anvil.api.world.trade_tables import TradeTable
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    AsObject,
    AtLeastOne,
    BlockId,
    Chance,
    EntityId,
    InRange,
    ItemId,
    ItemObject,
    JsonComponent,
    JsonObject,
    JsonValue,
    Keyed,
    MinMax,
    NonNegative,
    PropertyName,
    RangeMinMax,
    Trigger,
    Unique,
    Wrapped,
    json_field,
)
from anvil.lib.jsonmodel.enums import (
    ContainerType,
    Slots,
    Vibrations,
)
from anvil.lib.translator import AnvilTranslator

# region Parts: objects nested inside components


class EquippableSlot(JsonObject):
    """A slot of `minecraft:equippable` and the items it takes.

    Args:
        slot (int): The slot number.
        item (str | Item, optional): The item that can be equipped in this slot.
        accepted_items (list[str | Item], optional): The items that can go in this slot.
        interact_text (str, optional): Text shown on the interact button with touch controls. It is added to the language file.
        on_equip (EventTrigger | str, optional): Event to run when an item is equipped in this slot.
        on_unequip (EventTrigger | str, optional): Event to run when the item is removed from this slot.
    """

    slot: Annotated[int, NonNegative] = json_field()
    item: Annotated[str | Item, ItemId] | None = json_field(default=None)
    accepted_items: list[Annotated[str | Item, ItemId]] | None = json_field(
        default=None
    )
    interact_text: str | None = json_field(default=None)
    on_equip: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_unequip: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)

    def __post_init__(self) -> None:
        if self.interact_text is not None:
            self.interact_text = AnvilTranslator().localize(
                self.interact_text, prefix="action.interact"
            )


class FeedItem(JsonObject):
    """An item that raises the temper of an entity being tamed by riding.

    Args:
        item (str | Item): The item.
        temper_mod (int, optional): The temper the entity gains when fed this item. Game default 0.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    temper_mod: int | None = json_field(default=None)


class HealEffect(JsonObject):
    """An effect applied when an item heals the entity.

    Args:
        name (MinecraftEffects | str): The effect to apply.
        amplifier (int, optional): The amplifier of the effect. Game default 1.
        chance (float, optional): The chance that the effect is applied. Game default 1.
        duration (int | Literal["infinite"], optional): The duration of the effect in seconds. Game default 0.
    """

    name: MinecraftEffects | str = json_field()
    amplifier: int | None = json_field(default=None)
    chance: Annotated[float, Chance] | None = json_field(default=None)
    duration: int | Literal["infinite"] | None = json_field(default=None)


class HealItem(JsonObject):
    """An item that heals the entity.

    Args:
        item (str | Item): The item.
        heal_amount (int, optional): The health the entity gains when fed this item. Game default 1.
        result_item (str | Item, optional): The item the fed item becomes after a successful heal.
        effects (list[HealEffect], optional): Effects applied when this item heals the entity.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    heal_amount: int | None = json_field(default=None)
    result_item: Annotated[str | Item, ItemId] | None = json_field(default=None)
    effects: list[HealEffect] | None = json_field(default=None)


class NameAction(JsonObject):
    """A special name of `minecraft:nameable` and the event it runs.

    Args:
        name_filter (str | list[str]): The name, or names, that run the event.
        on_named (EventTrigger | str, optional): Event to run when the entity gets one of these names.
    """

    name_filter: str | list[str] = json_field()
    on_named: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)


class NPCOffsets(JsonObject):
    """Where an NPC is drawn in its dialogue portrait or skin picker.

    Args:
        translate (tuple[float, float, float]): The offset.
        scale (tuple[float, float, float]): The scale.
    """

    translate: tuple[float, float, float] = json_field()
    scale: tuple[float, float, float] = json_field()


class NPCData(JsonObject):
    """The skins and offsets of `minecraft:npc`.

    Args:
        skin_list (list[int]): The skin variants the NPC can use.
        portrait_offsets (NPCOffsets, optional): Where the NPC is drawn in its dialogue portrait.
        picker_offsets (NPCOffsets, optional): Where the NPC is drawn in the skin picker.
    """

    skin_list: list[Annotated[int, Wrapped("variant")]] = json_field()
    portrait_offsets: NPCOffsets | None = json_field(default=None)
    picker_offsets: NPCOffsets | None = json_field(default=None)


class SlotDropChance(JsonObject):
    """The chance to drop the item in an equipment slot.

    Args:
        slot (Slots): The equipment slot.
        drop_chance (float): The chance to drop the equipped item, from 0 to 1.
    """

    slot: Slots = json_field()
    drop_chance: Annotated[float, Chance] = json_field()


class TameItem(JsonObject):
    """A tame item that becomes another item after a successful tame.

    Args:
        item (str | Item): The tame item.
        result_item (str | Item): The item it becomes.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    result_item: Annotated[str | Item, ItemId] = json_field()


class AgeableFeedItem(JsonObject):
    """An item that ages a baby entity up when fed.

    Args:
        item (str | Item): The item.
        growth (float, optional): How much the entity ages when fed this item, from 0 to 1.
        result_item (str | Item, optional): The item the fed item becomes.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    growth: Annotated[float, Chance] | None = json_field(default=None)
    result_item: Annotated[str | Item, ItemId] | None = json_field(default=None)


class BreedItem(JsonObject):
    """An item that gets an entity into the love state, and the item it becomes.

    Args:
        item (str | Item): The item.
        result_item (str | Item, optional): The item the used item becomes.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    result_item: Annotated[str | Item, ItemId] | None = json_field(default=None)


class BreedPartner(JsonValue):
    """An entity `minecraft:breedable` can breed with. Written as `{mate_type: breed_event}`,
    with an empty object when it has no breed event.

    Args:
        mate_type (str | Entity): The entity this entity can mate with.
        breed_event (EventTrigger | str, optional): Event to run when this entity breeds.
    """

    mate_type: Annotated[str | Entity, EntityId] = json_field(exclude=True)
    breed_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )

    def __json__(self) -> Any:
        return JsonValue.__json__(self) or {}


class DenyParentsVariant(JsonObject):
    """How likely a baby of parents with the same variant takes a random variant instead.

    Args:
        chance (float): The chance of denying the parents' variant, from 0 to 1.
        min_variant (int): The inclusive minimum of the variant range.
        max_variant (int): The inclusive maximum of the variant range.
    """

    chance: Annotated[float, Chance] = json_field()
    min_variant: int = json_field()
    max_variant: int = json_field()


class EnvironmentRequirement(JsonObject):
    """Blocks that must be nearby for an entity to get into the love state.

    Args:
        block_types (list[str | Block | BlockDescriptor]): The blocks required nearby.
        count (int): How many of these blocks are required.
        radius (float): The search radius in blocks, from 0 to 16.
    """

    block_types: list[Annotated[str | Block | BlockDescriptor, BlockId]] = json_field()
    count: Annotated[int, NonNegative] = json_field()
    radius: Annotated[float, InRange(0, 16)] = json_field()


class GeneticVariant(JsonObject):
    """Allele values a gene is checked against, and the event run when they match.

    Each allele option is a number, or a `(min, max)` range.

    Args:
        birth_event (EventTrigger | str): Event to run when the mob is born with matching alleles.
        both_allele (int | tuple[float, float], optional): Matches when both the main and hidden allele match.
        either_allele (int | tuple[float, float], optional): Matches when the main or the hidden allele matches.
        hidden_allele (int | tuple[float, float], optional): Matches the hidden allele.
        main_allele (int | tuple[float, float], optional): Matches the main allele.
    """

    birth_event: Annotated[EventTrigger | str, Trigger] = json_field()
    both_allele: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
        default=None
    )
    either_allele: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
        default=None
    )
    hidden_allele: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
        default=None
    )
    main_allele: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
        default=None
    )

    def __validate__(self) -> None:
        if all(
            value is None
            for value in (
                self.both_allele,
                self.either_allele,
                self.hidden_allele,
                self.main_allele,
            )
        ):
            raise ValueError("GeneticVariant needs at least one allele option.")


class Gene(JsonObject):
    """A gene of `minecraft:genetics`.

    Args:
        name (str): The name of the gene.
        allele_range (int | tuple[float, float]): The allele values of this gene, a number or a `(min, max)` range.
        genetic_variants (list[GeneticVariant], optional): Allele combinations and the events they run. Add more with `add_genetic_variant`.
        mutation_rate (float, optional): Overrides the component's mutation rate for this gene, from 0 to 1. Game default -1 (not overridden).
        use_simplified_breeding (bool, optional): Babies inherit main alleles from the parents' main alleles and hidden alleles from the hidden ones.
    """

    name: str = json_field()
    allele_range: Annotated[int | tuple[int, int], RangeMinMax] = json_field()
    genetic_variants: list[GeneticVariant] = json_field(
        default_factory=list, omit_default=True
    )
    mutation_rate: Annotated[float, Chance] | None = json_field(default=None)
    use_simplified_breeding: bool | None = json_field(default=None)

    def add_genetic_variant(
        self,
        *,
        birth_event: EventTrigger | str,
        both_allele: int | tuple[float, float] | None = None,
        either_allele: int | tuple[float, float] | None = None,
        hidden_allele: int | tuple[float, float] | None = None,
        main_allele: int | tuple[float, float] | None = None,
    ) -> "Gene":
        """Adds a genetic variant. See `GeneticVariant` for the parameters."""
        self.genetic_variants.append(
            GeneticVariant(
                birth_event=birth_event,
                both_allele=both_allele,
                either_allele=either_allele,
                hidden_allele=hidden_allele,
                main_allele=main_allele,
            )
        )
        return self


class InteractParticle(JsonObject):
    """The particle effect at the start of an interaction.

    Args:
        particle_type (str): The particle to spawn.
        copper_event (Literal["none", "scrape", "wax_off", "wax_on"], optional): The copper event to play. Game default none.
        particle_offset_towards_interactor (bool, optional): The particle appears closer to the interacting entity. Game default false.
        particle_y_offset (float, optional): Offsets the particle in the y direction. Game default 0.
    """

    particle_type: str = json_field()
    copper_event: Literal["none", "scrape", "wax_off", "wax_on"] | None = json_field(
        default=None
    )
    particle_offset_towards_interactor: bool | None = json_field(default=None)
    particle_y_offset: float | None = json_field(default=None)


class InteractSpawnItems(JsonObject):
    """A loot table dropped on the ground after an interaction.

    Args:
        table (LootTable | str): The loot table, or its path relative to the behavior pack root.
        y_offset (float, optional): Offsets the spawn position in the y direction. Game default 1.
    """

    table: LootTable | str = json_field()
    y_offset: float | None = json_field(default=None)


class RepairEntityItem(JsonObject):
    """Repairs one of the entity's items on interaction.

    Args:
        slot (Slots | str): The slot holding the item to repair.
        amount (int, optional): Durability restored, more than 0. Game default 1.
    """

    slot: Slots | str = json_field()
    amount: Annotated[int, AtLeastOne] | None = json_field(default=None)


class Interaction(JsonObject):
    """An interaction of `minecraft:interact`.

    Args:
        add_items (LootTable | str, optional): Loot table with items added to the player's inventory.
        admire (bool, optional): The mob tries to admire the item. Needs `minecraft:admire_item` and its goal. Game default false.
        barter (bool, optional): The mob tries to barter for the item. Needs `minecraft:barter` and its goal. Game default false.
        cooldown (float, optional): Seconds before this entity can be interacted with again. Game default 0.
        cooldown_after_being_attacked (float, optional): Seconds before this entity can be interacted with after being attacked. Game default 0.
        drop_item_slot (Slots | str, optional): The slot whose item is dropped.
        drop_item_y_offset (float, optional): Offsets the dropped item in the y direction. Needs `drop_item_slot`. Game default 0.
        equip_item_slot (Slots | str, optional): The slot the item is equipped to.
        give_item (bool, optional): The mob replaces its main-hand item with the interacting item. Game default false.
        health_amount (int, optional): Health the entity gains, or loses when negative. Game default 0.
        hurt_item (int, optional): Damage the item takes. Game default 0.
        interact_text (str, optional): Text shown on the interact button with touch controls. It is added to the language file.
        on_interact (EventTrigger, optional): Event to run when the interaction happens.
        particle_on_start (InteractParticle, optional): Particle effect at the start of the interaction.
        play_sounds (list[str], optional): Sounds played when the interaction happens.
        repair_entity_item (RepairEntityItem, optional): Repairs one of the entity's items.
        spawn_entities (list[str | Entity], optional): Entities spawned by the interaction.
        spawn_items (LootTable | str | InteractSpawnItems, optional): Loot table with items dropped on the ground.
        swing (bool, optional): The player plays the swing animation. Game default true.
        take_item (bool, optional): The mob swaps its main-hand item into the player's empty selected slot. Game default false.
        transform_to_item (str, optional): The item the used item becomes, as `itemName:auxValue`.
        use_item (bool, optional): The interaction uses up the item. Game default false.
        vibration (Vibrations, optional): The vibration emitted. Game default entity_interact.
    """

    add_items: Annotated[LootTable | str, Wrapped("table")] | None = json_field(
        default=None
    )
    admire: bool | None = json_field(default=None)
    barter: bool | None = json_field(default=None)
    cooldown: Annotated[float, NonNegative] | None = json_field(default=None)
    cooldown_after_being_attacked: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    drop_item_slot: Slots | str | None = json_field(default=None)
    drop_item_y_offset: float | None = json_field(default=None)
    equip_item_slot: Slots | str | None = json_field(default=None)
    give_item: bool | None = json_field(default=None)
    health_amount: int | None = json_field(default=None)
    hurt_item: int | None = json_field(default=None)
    interact_text: str | None = json_field(default=None)
    on_interact: EventTrigger | None = json_field(default=None)
    particle_on_start: InteractParticle | None = json_field(default=None)
    play_sounds: list[str] | None = json_field(default=None)
    repair_entity_item: RepairEntityItem | None = json_field(default=None)
    spawn_entities: list[Annotated[str | Entity, EntityId]] | None = json_field(
        default=None
    )
    spawn_items: (
        Annotated[LootTable | str, Wrapped("table")] | InteractSpawnItems | None
    ) = json_field(default=None)
    swing: bool | None = json_field(default=None)
    take_item: bool | None = json_field(default=None)
    transform_to_item: str | None = json_field(default=None)
    use_item: bool | None = json_field(default=None)
    vibration: Vibrations | None = json_field(default=None)

    def __post_init__(self) -> None:
        if self.interact_text is not None:
            self.interact_text = AnvilTranslator().localize(
                self.interact_text, prefix="action.interact"
            )


class MutationFactor(JsonObject):
    """How likely babies are not to inherit one of their parents' variances, each from 0 to 1.

    Args:
        color (float, optional): Chance the baby gets a random color.
        extra_variant (float, optional): Chance of a mutation of the extra variant.
        variant (float, optional): Chance of a mutation of the variant.
    """

    color: Annotated[float, Chance] | None = json_field(default=None)
    extra_variant: Annotated[float, Chance] | None = json_field(default=None)
    variant: Annotated[float, Chance] | None = json_field(default=None)


class ShareableItem(JsonObject):
    """An item `minecraft:shareables` wants to share or pick up.

    Args:
        item (str | Item): The item, or an item tag.
        admire (bool, optional): The mob admires the item after picking it up. Game default false.
        barter (bool, optional): The mob barters for the item after picking it up. Game default false.
        consume_item (bool, optional): The mob consumes the item. Game default false.
        craft_into (str | Item, optional): The item the mob crafts with this item.
        max_amount (int, optional): Maximum number of this item the mob holds. Game default -1.
        pickup_limit (int, optional): Maximum number of this item picked up per goal tick. Game default -1.
        pickup_only (bool, optional): The mob only picks the item up and never drops it. Game default false.
        priority (int, optional): Item preference, 0 is the highest. Game default 0.
        stored_in_inventory (bool, optional): The mob puts the item in its inventory when it cannot equip it. Game default false.
        surplus_amount (int, optional): Number of this item considered extra, to share. Game default -1.
        want_amount (int, optional): Number of this item the mob wants. Game default -1.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    admire: bool | None = json_field(default=None)
    barter: bool | None = json_field(default=None)
    consume_item: bool | None = json_field(default=None)
    craft_into: Annotated[str | Item, ItemId] | None = json_field(default=None)
    max_amount: int | None = json_field(default=None)
    pickup_limit: int | None = json_field(default=None)
    pickup_only: bool | None = json_field(default=None)
    priority: int | None = json_field(default=None)
    stored_in_inventory: bool | None = json_field(default=None)
    surplus_amount: int | None = json_field(default=None)
    want_amount: int | None = json_field(default=None)


# endregion

# region Components


class EntityAdmireItem(JsonComponent):
    """Allows an entity to ignore attackable targets for a given duration.

    Args:
        cooldown_after_being_attacked (int, optional): Duration, in seconds, for which mob won't admire items if it was hurt. Game default 10.
        duration (int, optional): Duration, in seconds, that the mob admires an item. Game default 10.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_admire_item)
    """

    identifier = "minecraft:admire_item"

    cooldown_after_being_attacked: int | None = json_field(default=None)
    duration: int | None = json_field(default=None)


class EntityAgeable(JsonComponent):
    """Adds a timer for the entity to grow up. Feeding it `feed_items` speeds it up.

    Args:
        drop_items (list[str | Item], optional): Items dropped when the entity grows up.
        duration (float, optional): Seconds before the entity grows up; -1 stays a baby forever. Game default 1200.
        feed_items (list[str | Item | AgeableFeedItem], optional): Items that age the entity up when fed. Add more with `add_feed_item`.
        grow_up (EventTrigger | str, optional): Event to run when the entity grows up.
        interact_filters (Filter, optional): Conditions for the entity to be fed.
        pause_growth (EventTrigger | str, optional): Event to run when growth is paused by a `pause_growth_items` feed.
        pause_growth_items (list[str | Item], optional): Items that pause the growth of a baby.
        reset_growth (EventTrigger | str, optional): Event to run when growth is reset by a `reset_growth_items` feed.
        reset_growth_items (list[str | Item], optional): Items that reset the growth timer of a baby.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ageable)
    """

    identifier = "minecraft:ageable"

    drop_items: list[Annotated[str | Item, ItemId]] | None = json_field(default=None)
    duration: float | None = json_field(default=None)
    feed_items: list[Annotated[str | Item, ItemId] | AgeableFeedItem] = json_field(
        default_factory=list, omit_default=True
    )
    grow_up: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    interact_filters: Filter | None = json_field(default=None)
    pause_growth: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    pause_growth_items: list[Annotated[str | Item, ItemId]] | None = json_field(
        default=None
    )
    reset_growth: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    reset_growth_items: list[Annotated[str | Item, ItemId]] | None = json_field(
        default=None
    )

    def add_feed_item(
        self,
        *,
        item: str | Item,
        growth: float | None = None,
        result_item: str | Item | None = None,
    ) -> "EntityAgeable":
        """Adds an item that ages the entity up. Without options it is written as the item name.

        Args:
            item (str | Item): The item.
            growth (float, optional): How much the entity ages when fed this item, from 0 to 1.
            result_item (str | Item, optional): The item the fed item becomes.
        """
        if growth is None and result_item is None:
            self.feed_items.append(item)
        else:
            self.feed_items.append(
                AgeableFeedItem(item=item, growth=growth, result_item=result_item)
            )
        return self


class EntityArmorEquipmentSlotMapping(JsonComponent):
    """It defines to which armor slot an item equipped to 'minecraft:equippable''s second slot should be equipped to. It is automatically applied to all entities for worlds with a version greater than or equal to 1.21.10. It is strongly advised not to explicitly use this component, as no backwards compatibility for it will be provided.

    Args:
        armor_slot (Slots): The armor slot: `Slots.Chest` or `Slots.Body`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_armor_equipment_slot_mapping)
    """

    identifier = "minecraft:entity_armor_equipment_slot_mapping"

    armor_slot: Literal[Slots.Chest, Slots.Body] = json_field()


class EntityBarter(JsonComponent):
    """Enables the entity to drop an item as a barter exchange.

    Args:
        barter_table (LootTable | str): The loot table used to drop a random item, or its path.
        cooldown_after_being_attacked (int | tuple[float, float], optional): Seconds the mob won't barter after being hurt, or a `(min, max)` range. Game default 10.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_barter)
    """

    identifier = "minecraft:barter"

    barter_table: LootTable | str = json_field()
    cooldown_after_being_attacked: (
        Annotated[int | tuple[int, int], RangeMinMax] | None
    ) = json_field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.barter_table, LootTable):
            self.barter_table = self.barter_table.table_path


class EntityBreedable(JsonComponent):
    """Allows the entity to get into the love state used for breeding.

    Args:
        allow_sitting (bool, optional): The entity can breed while sitting. Game default false.
        blend_attributes (bool, optional): The parents' attributes are blended in the baby. Game default true.
        breed_cooldown (float, optional): Seconds before the entity can breed again. Game default 60.
        breed_items (list[str | Item | BreedItem], optional): Items that get the entity into the love state. Add more with `add_breed_item`.
        breeds_with (list[BreedPartner], optional): The entities this entity can breed with. Add more with `add_breeds_with`.
        causes_pregnancy (bool, optional): The entity becomes pregnant instead of spawning a baby. Game default false.
        combine_parent_colors (bool, optional): Without a color mutation, the baby's color blends the parents' colors. Game default false.
        deny_parents_variant (DenyParentsVariant, optional): How likely a baby of parents with the same variant takes another. Set it with `set_deny_parents_variant`.
        environment_requirements (list[EnvironmentRequirement], optional): Blocks required nearby to get into the love state. Add more with `add_environment_requirement`.
        extra_baby_chance (float, optional): Chance that up to 16 babies spawn, from 0 to 1. Game default 0.
        inherit_tamed (bool, optional): Babies are tamed if their parents are.
        love_filters (Filter, optional): Conditions for falling in love.
        mutation_factor (MutationFactor, optional): How likely babies are not to inherit their parents' variances. Set it with `set_mutation_factor`.
        require_full_health (bool, optional): The entity needs full health to breed. Game default false.
        require_tame (bool, optional): The entity needs to be tamed to breed. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breedable)
    """

    identifier = "minecraft:breedable"

    allow_sitting: bool | None = json_field(default=None)
    blend_attributes: bool | None = json_field(default=None)
    breed_cooldown: Annotated[float, NonNegative] | None = json_field(default=None)
    breed_items: list[Annotated[str | Item, ItemId] | BreedItem] = json_field(
        default_factory=list, omit_default=True
    )
    breeds_with: Annotated[list[BreedPartner], Keyed("mate_type")] = json_field(
        default_factory=list, omit_default=True
    )
    causes_pregnancy: bool | None = json_field(default=None)
    combine_parent_colors: bool | None = json_field(default=None)
    deny_parents_variant: DenyParentsVariant | None = json_field(default=None)
    environment_requirements: list[EnvironmentRequirement] = json_field(
        default_factory=list, omit_default=True
    )
    extra_baby_chance: Annotated[float, Chance] | None = json_field(default=None)
    inherit_tamed: bool | None = json_field(default=None)
    love_filters: Filter | None = json_field(default=None)
    mutation_factor: MutationFactor | None = json_field(default=None)
    require_full_health: bool | None = json_field(default=None)
    require_tame: bool | None = json_field(default=None)

    def add_breed_item(
        self,
        *,
        item: str | Item,
        result_item: str | Item | None = None,
    ) -> "EntityBreedable":
        """Adds an item that gets the entity into the love state.

        Args:
            item (str | Item): The item.
            result_item (str | Item, optional): The item the used item becomes.
        """
        if result_item is None:
            self.breed_items.append(item)
        else:
            self.breed_items.append(BreedItem(item=item, result_item=result_item))
        return self

    def add_breeds_with(
        self,
        *,
        mate_type: str | Entity,
        breed_event: EventTrigger | str | None = None,
    ) -> "EntityBreedable":
        """Adds an entity this entity can breed with. See `BreedPartner` for the parameters."""
        self.breeds_with.append(
            BreedPartner(mate_type=mate_type, breed_event=breed_event)
        )
        return self

    def add_environment_requirement(
        self,
        *,
        block_types: list[str | Block | BlockDescriptor],
        count: int,
        radius: float,
    ) -> "EntityBreedable":
        """Adds blocks required nearby. See `EnvironmentRequirement` for the parameters."""
        self.environment_requirements.append(
            EnvironmentRequirement(block_types=block_types, count=count, radius=radius)
        )
        return self

    def set_mutation_factor(
        self,
        *,
        color: float | None = None,
        extra_variant: float | None = None,
        variant: float | None = None,
    ) -> "EntityBreedable":
        """Sets how likely babies are not to inherit their parents' variances. See `MutationFactor` for the parameters."""
        self.mutation_factor = MutationFactor(
            color=color,
            extra_variant=extra_variant,
            variant=variant,
        )
        return self

    def set_deny_parents_variant(
        self,
        *,
        chance: float,
        min_variant: int,
        max_variant: int,
    ) -> "EntityBreedable":
        """Sets how likely a baby of parents with the same variant takes another. See `DenyParentsVariant` for the parameters."""
        self.deny_parents_variant = DenyParentsVariant(
            chance=chance,
            min_variant=min_variant,
            max_variant=max_variant,
        )
        return self


class EntityBribeable(JsonComponent):
    """Defines the way an entity can get into the 'bribed' state.

    Args:
        bribe_items (list[str | Item], optional): The items that can be used to bribe the entity. Add more with `add_bribe_items`.
        bribe_cooldown (float, optional): Time in seconds before the Entity can be bribed again. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_bribeable)
    """

    identifier = "minecraft:bribeable"

    bribe_items: list[Annotated[str | Item, ItemId]] = json_field(
        default_factory=list, omit_default=True
    )
    bribe_cooldown: Annotated[float, NonNegative] | None = json_field(default=None)

    def add_bribe_items(self, *items: str | Item) -> "EntityBribeable":
        """Adds items that bribe the entity."""
        self.bribe_items.extend(items)
        return self


class EntityDweller(JsonComponent):
    """Compels an entity to join and migrate between villages and other dwellings.

    Args:
        can_find_poi (bool, optional): Whether or not the entity can find and add POIs to the dwelling.
        can_migrate (bool, optional): Determines whether the entity can migrate between dwellings, or only have its initial dwelling.
        dweller_role (str, optional):
        dwelling_bounds_tolerance (float, optional): A padding distance for checking if the entity is within the dwelling.
        dwelling_role (str, optional): The role of which the entity plays in the dwelling. Current Roles: inhabitant, defender, hostile, passive.
        dwelling_type (str, optional): The type of dwelling the entity wishes to join. Current Types: village.
        first_founding_reward (int, optional): Determines how much reputation players are rewarded on first founding.
        preferred_profession (str, optional): Allows the user to define a starting profession for this particular Dweller, instead of letting them choose organically. (They still need to gain experience from trading before this takes effect.).
        update_interval_base (float, optional): How often the entity checks on their dwelling status in ticks. Positive values only.
        update_interval_variant (float, optional): The variant value in ticks that will be added to the update_interval_base.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dweller)
    """

    identifier = "minecraft:dweller"

    can_find_poi: bool | None = json_field(default=None)
    can_migrate: bool | None = json_field(default=None)
    dweller_role: str | None = json_field(default=None)
    dwelling_bounds_tolerance: float | None = json_field(default=None)
    dwelling_role: str | None = json_field(default=None)
    dwelling_type: str | None = json_field(default=None)
    first_founding_reward: int | None = json_field(default=None)
    preferred_profession: str | None = json_field(default=None)
    update_interval_base: float | None = json_field(default=None)
    update_interval_variant: float | None = json_field(default=None)


class EntityEconomyTradeTable(JsonComponent):
    """Defines this entity's ability to trade with players.

    Args:
        table (TradeTable | str): The trade table, or its path relative to the behavior pack root.
        convert_trades_economy (bool, optional): Converts legacy trade data into economy trade data. Game default false.
        cured_discount (tuple[int, int], optional): `(min, max)` cured villager discounts applied to prices. Game default (-25, -20).
        display_name (str, optional): Name shown while trading with this entity. It is added to the language file.
        hero_demand_discount (int, optional): Extra demand discount while the player has Hero of the Village. Game default -4.
        max_cured_discount (tuple[int, int], optional): `(min, max)` limits of the cured villager discounts. Game default (-25, -20).
        max_nearby_cured_discount (int, optional): Lowest nearby cured villager discount of the legacy pricing. Game default -200.
        nearby_cured_discount (int, optional): Nearby cured villager discount step of the legacy pricing. Game default -20.
        new_screen (bool, optional): Uses the newer trade screen. Game default false.
        persist_trades (bool, optional): Generated offers are saved with the entity. Game default false.
        show_trade_screen (bool, optional): Interacting opens the trade screen. Game default true.
        use_legacy_price_formula (bool, optional): Uses the legacy price calculation. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_economy_trade_table)
    """

    identifier = "minecraft:economy_trade_table"

    table: TradeTable | str = json_field()
    convert_trades_economy: bool | None = json_field(default=None)
    cured_discount: Annotated[tuple[int, int], MinMax] | None = json_field(default=None)
    display_name: str | None = json_field(default=None)
    hero_demand_discount: int | None = json_field(default=None)
    max_cured_discount: Annotated[tuple[int, int], MinMax] | None = json_field(
        default=None
    )
    max_nearby_cured_discount: int | None = json_field(default=None)
    nearby_cured_discount: int | None = json_field(default=None)
    new_screen: bool | None = json_field(default=None)
    persist_trades: bool | None = json_field(default=None)
    show_trade_screen: bool | None = json_field(default=None)
    use_legacy_price_formula: bool | None = json_field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.table, TradeTable):
            self.table = self.table.table_path
        if self.display_name is not None:
            self.display_name = AnvilTranslator().localize(
                self.display_name,
                prefix=f"tradetable.{CONFIG.NAMESPACE}.{CONFIG.PROJECT_NAME}",
                suffix="name",
            )


class EntityEquipItem(JsonComponent):
    """The entity puts on the desired equipment.

    Args:
        can_wear_armor (bool, optional): Whether the entity can pick up and wear armor from the ground. Game default false.
        excluded_items (list[str | Item], optional): Items the entity should not equip.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equip_item)
    """

    identifier = "minecraft:equip_item"

    can_wear_armor: bool | None = json_field(default=None)
    excluded_items: list[Annotated[str | Item, ItemId, ItemObject]] | None = json_field(
        default=None
    )


class EntityEquipment(JsonComponent):
    """Sets the equipment table to use for this entity.

    Args:
        table (LootTable | str, optional): The equipment table, or its path relative to the behavior pack's root.
        slot_drop_chance (list[SlotDropChance], optional): The chance to drop the item in each slot. Add more with `add_slot_drop_chance`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equipment)
    """

    identifier = "minecraft:equipment"

    table: LootTable | str | None = json_field(default=None)
    slot_drop_chance: list[SlotDropChance] = json_field(
        default_factory=list, omit_default=True
    )

    def __post_init__(self) -> None:
        if isinstance(self.table, LootTable):
            self.table = self.table.table_path

    def add_slot_drop_chance(
        self, *, slot: Slots, drop_chance: float
    ) -> "EntityEquipment":
        """Sets the chance to drop the item in a slot. See `SlotDropChance`."""
        self.slot_drop_chance.append(SlotDropChance(slot=slot, drop_chance=drop_chance))
        return self


class EntityEquippable(JsonComponent):
    """Defines an entity's behavior for having items equipped to it.

    Args:
        slots (list[EquippableSlot], optional): The slots and the items they take. Add more with `add_slot`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equippable)
    """

    identifier = "minecraft:equippable"

    slots: Annotated[list[EquippableSlot], Unique("slot")] = json_field(
        default_factory=list, omit_default=True
    )

    def add_slot(
        self,
        *,
        slot: int,
        item: str | Item | None = None,
        accepted_items: list[str | Item] | None = None,
        interact_text: str | None = None,
        on_equip: EventTrigger | str | None = None,
        on_unequip: EventTrigger | str | None = None,
    ) -> "EntityEquippable":
        """Adds a slot. See `EquippableSlot` for the parameters."""
        self.slots.append(
            EquippableSlot(
                slot=slot,
                item=item,
                accepted_items=accepted_items,
                interact_text=interact_text,
                on_equip=on_equip,
                on_unequip=on_unequip,
            )
        )
        return self


class EntityGenetics(JsonComponent):
    """Defines how a mob's genes and alleles pass to its offspring, and the events they run.

    Args:
        genes (list[Gene], optional): The genes of this entity. Add more with `add_gene`.
        mutation_rate (float, optional): Chance an allele is replaced with a random one at birth, from 0 to 1. Game default 0.03125.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_genetics)
    """

    identifier = "minecraft:genetics"

    genes: list[Gene] = json_field(default_factory=list, omit_default=True)
    mutation_rate: Annotated[float, Chance] | None = json_field(default=None)

    def add_gene(
        self,
        *,
        name: str,
        allele_range: int | tuple[float, float],
        genetic_variants: list[GeneticVariant] | None = None,
        mutation_rate: float | None = None,
        use_simplified_breeding: bool | None = None,
    ) -> "EntityGenetics":
        """Adds a gene. See `Gene` for the parameters; `Gene.add_genetic_variant` adds variants."""
        self.genes.append(
            Gene(
                name=name,
                allele_range=allele_range,
                genetic_variants=list(genetic_variants or []),
                mutation_rate=mutation_rate,
                use_simplified_breeding=use_simplified_breeding,
            )
        )
        return self


class EntityGiveable(JsonComponent):
    """Defines sets of items that can be used to trigger events when used on this entity. The item will also be taken and placed in the entity's inventory.

    Args:
        items (list[str | Item], optional): The items that can be given to the entity to place in their inventory. Add more with `add_items`.
        on_give (EventTrigger | str, optional): Event to fire when the correct item is given.
        cooldown (float, optional): An optional cool down in seconds to prevent spamming interactions. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_giveable)
    """

    identifier = "minecraft:giveable"

    items: list[Annotated[str | Item, ItemId]] = json_field(
        default_factory=list, omit_default=True
    )
    on_give: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    cooldown: Annotated[float, NonNegative] | None = json_field(default=None)

    def add_items(self, *items: str | Item) -> "EntityGiveable":
        """Adds items that can be given to the entity."""
        self.items.extend(items)
        return self


class EntityGrowsCrop(JsonComponent):
    """Could increase crop growth when entity walks over crop.

    Args:
        chance (float, optional): Value between 0-1. Chance of success per tick. Game default 0.
        charges (int, optional): Number of charges. Game default 10.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_grows_crop)
    """

    identifier = "minecraft:grows_crop"

    chance: Annotated[float, Chance] | None = json_field(default=None)
    charges: Annotated[int, NonNegative] | None = json_field(default=None)


class EntityHealable(JsonComponent):
    """Defines how the entity is healed by items.

    Args:
        items (list[HealItem], optional): The items that heal this entity. Add more with `add_item`.
        filters (Filter, optional): Conditions for using an item to heal the entity.
        force_use (bool, optional): Whether an item can be used at full health. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_healable)
    """

    identifier = "minecraft:healable"

    items: list[HealItem] = json_field(default_factory=list, omit_default=True)
    filters: Filter | None = json_field(default=None)
    force_use: bool | None = json_field(default=None)

    def add_item(
        self,
        *,
        item: str | Item,
        heal_amount: int | None = None,
        result_item: str | Item | None = None,
        effects: list[HealEffect] | None = None,
    ) -> "EntityHealable":
        """Adds an item that heals the entity. See `HealItem` for the parameters."""
        self.items.append(
            HealItem(
                item=item,
                heal_amount=heal_amount,
                result_item=result_item,
                effects=effects,
            )
        )
        return self


class EntityInteract(JsonComponent):
    """Defines interactions with this entity.

    Args:
        interactions (list[Interaction], optional): The interactions. Add more with `add_interaction`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact)
    """

    identifier = "minecraft:interact"

    interactions: list[Interaction] = json_field(
        default_factory=list, omit_default=True
    )

    def add_interaction(
        self,
        *,
        on_interact: EventTrigger | None = None,
        add_items: LootTable | str | None = None,
        admire: bool | None = None,
        barter: bool | None = None,
        cooldown: float | None = None,
        cooldown_after_being_attacked: float | None = None,
        drop_item_slot: Slots | str | None = None,
        drop_item_y_offset: float | None = None,
        equip_item_slot: Slots | str | None = None,
        give_item: bool | None = None,
        health_amount: int | None = None,
        hurt_item: int | None = None,
        interact_text: str | None = None,
        particle_on_start: InteractParticle | None = None,
        play_sounds: list[str] | None = None,
        repair_entity_item: RepairEntityItem | None = None,
        spawn_entities: list[str | Entity] | None = None,
        spawn_items: LootTable | str | InteractSpawnItems | None = None,
        swing: bool | None = None,
        take_item: bool | None = None,
        transform_to_item: str | None = None,
        use_item: bool | None = None,
        vibration: Vibrations | None = None,
    ) -> "EntityInteract":
        """Adds an interaction. See `Interaction` for the parameters."""
        self.interactions.append(
            Interaction(
                on_interact=on_interact,
                add_items=add_items,
                admire=admire,
                barter=barter,
                cooldown=cooldown,
                cooldown_after_being_attacked=cooldown_after_being_attacked,
                drop_item_slot=drop_item_slot,
                drop_item_y_offset=drop_item_y_offset,
                equip_item_slot=equip_item_slot,
                give_item=give_item,
                health_amount=health_amount,
                hurt_item=hurt_item,
                interact_text=interact_text,
                particle_on_start=particle_on_start,
                play_sounds=play_sounds,
                repair_entity_item=repair_entity_item,
                spawn_entities=spawn_entities,
                spawn_items=spawn_items,
                swing=swing,
                take_item=take_item,
                transform_to_item=transform_to_item,
                use_item=use_item,
                vibration=vibration,
            )
        )
        return self


class EntityInventory(JsonComponent):
    """Defines this entity's inventory properties.

    Args:
        additional_slots_per_strength (int, optional): Number of slots that this entity can gain per extra strength. Game default 0.
        can_be_siphoned_from (bool, optional): If true, the contents of this inventory can be removed by a hopper. Game default false.
        container_type (ContainerType, optional): Type of container this entity has. Game default none.
        inventory_size (int, optional): Number of slots the container has. Game default 5.
        private (bool, optional): If true, the entity will not drop its inventory on death. Game default false.
        restrict_to_owner (bool, optional): If true, the entity's inventory can only be accessed by its owner or itself. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inventory)
    """

    identifier = "minecraft:inventory"

    additional_slots_per_strength: int | None = json_field(default=None)
    can_be_siphoned_from: bool | None = json_field(default=None)
    container_type: ContainerType | None = json_field(default=None)
    inventory_size: Annotated[int, AtLeastOne] | None = json_field(default=None)
    private: bool | None = json_field(default=None)
    restrict_to_owner: bool | None = json_field(default=None)


class EntityLoot(JsonComponent):
    """Specifies the loot table that determines what items this entity drops upon death.

    Args:
        table (LootTable | str): The loot table, or its path relative to the behavior pack's root (e.g., 'loot_tables/entities/zombie.json').

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_loot)
    """

    identifier = "minecraft:loot"

    table: LootTable | str = json_field()

    def __post_init__(self) -> None:
        if isinstance(self.table, LootTable):
            self.table = self.table.table_path


class EntityManagedWanderingTrader(JsonComponent):
    """Manages the entity's ability to trade. Can only be used on the following type of entity: > * Wandering Trader (minecraft:wandering_trader) >

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_managed_wandering_trader)
    """

    identifier = "minecraft:managed_wandering_trader"


class EntityNPC(JsonComponent):
    """Makes the entity an NPC with a dialogue. Not in the Microsoft reference.

    Args:
        npc_data (NPCData, optional): The NPC's skins and offsets. Required on export. Set it with `set_npc_data`.
    """

    identifier = "minecraft:npc"
    __required__ = ("npc_data",)

    npc_data: NPCData | None = json_field(default=None)

    def set_npc_data(
        self,
        *,
        skin_list: list[int],
        portrait_offsets: NPCOffsets | None = None,
        picker_offsets: NPCOffsets | None = None,
    ) -> "EntityNPC":
        """Sets the NPC's skins and offsets. See `NPCData` for the parameters."""
        self.npc_data = NPCData(
            skin_list=skin_list,
            portrait_offsets=portrait_offsets,
            picker_offsets=picker_offsets,
        )
        return self

    def __validate__(self) -> None:
        if self.npc_data is None:
            raise ValueError(
                "EntityNPC needs `npc_data`. Set it in the constructor or with `set_npc_data`."
            )


class EntityNameable(JsonComponent):
    """Allows this entity to be named (e.g. using a name tag).

    Args:
        allow_name_tag_renaming (bool, optional): Whether name tags can rename this entity. Game default true.
        always_show (bool, optional): Whether the name is always shown. Game default false.
        default_trigger (EventTrigger | str, optional): Event to run when the entity gets named.
        name_actions (list[NameAction], optional): Special names and the events they run. Add more with `add_name_action`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_nameable)
    """

    identifier = "minecraft:nameable"

    allow_name_tag_renaming: bool | None = json_field(default=None)
    always_show: bool | None = json_field(default=None)
    default_trigger: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    name_actions: list[NameAction] = json_field(default_factory=list, omit_default=True)

    def add_name_action(
        self,
        *,
        name_filter: str | list[str],
        on_named: EventTrigger | str | None = None,
    ) -> "EntityNameable":
        """Adds a special name. See `NameAction` for the parameters."""
        self.name_actions.append(NameAction(name_filter=name_filter, on_named=on_named))
        return self


class EntityOffspring(JsonComponent):
    """Defines how the entity makes offspring.

    Args:
        blend_attributes (bool, optional): The parents' attributes are blended in the offspring. Game default true.
        deny_parents_variant (list[DenyParentsVariant], optional): How likely a baby of parents with the same variant takes another. Add more with `add_deny_parents_variant`.
        inherit_tamed (bool, optional): Babies are tamed if their parents are. Game default true.
        mutation_factor (list[MutationFactor], optional): How likely babies are not to inherit their parents' variances. Add more with `add_mutation_factor`.
        offspring_pairs (list[tuple[str | Entity, str | Entity]], optional): `(mate, offspring)` pairs: the offspring this entity makes with each mate. Written as `{mate: offspring}`.
        parent_centric_attribute_blending (list[type[JsonComponent]], optional): Attribute components blended from the parents, such as `EntityHealth`.
        property_inheritance (list[str], optional): Entity properties inherited from the parents. A name without a namespace gets the project namespace.
        random_extra_variant_mutation_interval (int | tuple[float, float], optional): Range of the random extra variant.
        random_variant_mutation_interval (int | tuple[float, float], optional): Range of the random variant.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_offspring)
    """

    identifier = "minecraft:offspring"

    blend_attributes: bool | None = json_field(default=None)
    deny_parents_variant: list[DenyParentsVariant] = json_field(
        default_factory=list, omit_default=True
    )
    inherit_tamed: bool | None = json_field(default=None)
    mutation_factor: list[MutationFactor] = json_field(
        default_factory=list, omit_default=True
    )
    offspring_pairs: (
        Annotated[
            list[
                tuple[
                    Annotated[str | Entity, EntityId], Annotated[str | Entity, EntityId]
                ]
            ],
            AsObject,
        ]
        | None
    ) = json_field(default=None)
    parent_centric_attribute_blending: list[type[JsonComponent]] | None = json_field(
        default=None
    )
    property_inheritance: list[Annotated[str, PropertyName]] | None = json_field(
        default=None
    )
    random_extra_variant_mutation_interval: (
        Annotated[int | tuple[int, int], RangeMinMax] | None
    ) = json_field(default=None)
    random_variant_mutation_interval: (
        Annotated[int | tuple[int, int], RangeMinMax] | None
    ) = json_field(default=None)

    def add_deny_parents_variant(
        self, *, chance: float, min_variant: int, max_variant: int
    ) -> "EntityOffspring":
        """Adds a variant range. See `DenyParentsVariant` for the parameters."""
        self.deny_parents_variant.append(
            DenyParentsVariant(
                chance=chance, min_variant=min_variant, max_variant=max_variant
            )
        )
        return self

    def add_mutation_factor(
        self,
        *,
        color: float | None = None,
        extra_variant: float | None = None,
        variant: float | None = None,
    ) -> "EntityOffspring":
        """Adds mutation chances. See `MutationFactor` for the parameters."""
        self.mutation_factor.append(
            MutationFactor(color=color, extra_variant=extra_variant, variant=variant)
        )
        return self


class EntityShareables(JsonComponent):
    """Defines the items the mob wants to share or pick up.

    Args:
        all_items (bool, optional): A bucket for every other item, always the lowest priority. Game default false.
        all_items_max_amount (int, optional): Maximum number of other items the mob holds. Game default -1.
        all_items_surplus_amount (int, optional): Number of other items considered extra, to share. Game default -1.
        all_items_want_amount (int, optional): Number of other items the mob wants. Game default -1.
        items (list[ShareableItem], optional): The items. Add more with `add_item`.
        singular_pickup (bool, optional): The mob cannot pick up more of an item it already holds. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shareables)
    """

    identifier = "minecraft:shareables"

    all_items: bool | None = json_field(default=None)
    all_items_max_amount: int | None = json_field(default=None)
    all_items_surplus_amount: int | None = json_field(default=None)
    all_items_want_amount: int | None = json_field(default=None)
    items: list[ShareableItem] = json_field(default_factory=list, omit_default=True)
    singular_pickup: bool | None = json_field(default=None)

    def add_item(
        self,
        *,
        item: str | Item,
        admire: bool | None = None,
        barter: bool | None = None,
        consume_item: bool | None = None,
        craft_into: str | Item | None = None,
        max_amount: int | None = None,
        pickup_limit: int | None = None,
        pickup_only: bool | None = None,
        priority: int | None = None,
        stored_in_inventory: bool | None = None,
        surplus_amount: int | None = None,
        want_amount: int | None = None,
    ) -> "EntityShareables":
        """Adds an item. See `ShareableItem` for the parameters."""
        self.items.append(
            ShareableItem(
                item=item,
                admire=admire,
                barter=barter,
                consume_item=consume_item,
                craft_into=craft_into,
                max_amount=max_amount,
                pickup_limit=pickup_limit,
                pickup_only=pickup_only,
                priority=priority,
                stored_in_inventory=stored_in_inventory,
                surplus_amount=surplus_amount,
                want_amount=want_amount,
            )
        )
        return self


class EntitySpawnEggInteraction(JsonComponent):
    """Enables interacting with this entity using its own spawn egg to spawn a born child. Runs the "minecraft:entity_born" event on the created entity as well as the defined "on_spawn" event.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_egg_interaction)
    """

    identifier = "minecraft:spawn_egg_interaction"


class EntityTameable(JsonComponent):
    """Defines the rules for an entity to be tamed.

    Args:
        tame_items (list[str | Item | TameItem], optional): Items that tame the entity. A `TameItem` also names the item it becomes. Add more with `add_tame_items`.
        tame_event (EventTrigger | str, optional): Event to run when the entity is tamed.
        probability (float, optional): The chance of taming with each item use, from 0 to 1. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tameable)
    """

    identifier = "minecraft:tameable"

    tame_items: list[Annotated[str | Item, ItemId] | TameItem] = json_field(
        default_factory=list, omit_default=True
    )
    tame_event: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    probability: Annotated[float, Chance] | None = json_field(default=None)

    def add_tame_items(self, *items: str | Item | TameItem) -> "EntityTameable":
        """Adds items that tame the entity."""
        self.tame_items.extend(items)
        return self


class EntityTamemount(JsonComponent):
    """Allows the entity to be tamed by mounting it.

    Args:
        attempt_temper_mod (int, optional): Temper gained when mounted. Game default 5.
        auto_reject_items (list[str | Item], optional): Items that anger the entity when carried while interacting.
        feed_items (list[FeedItem], optional): Items that raise the entity's temper. Add more with `add_feed_item`.
        feed_text (str, optional): Text of the feeding interact button.
        max_temper (int, optional): Maximum random starting temper. Game default 100.
        min_temper (int, optional): Minimum random starting temper. Game default 0.
        ride_text (str, optional): Text of the riding interact button. It is added to the language file.
        tame_event (EventTrigger | str, optional): Event to run when the entity becomes tamed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tamemount)
    """

    identifier = "minecraft:tamemount"

    attempt_temper_mod: int | None = json_field(default=None)
    auto_reject_items: list[Annotated[str | Item, ItemId, ItemObject]] | None = (
        json_field(default=None)
    )
    feed_items: list[FeedItem] = json_field(default_factory=list, omit_default=True)
    feed_text: str | None = json_field(default=None)
    max_temper: Annotated[int, NonNegative] | None = json_field(default=None)
    min_temper: Annotated[int, NonNegative] | None = json_field(default=None)
    ride_text: str | None = json_field(default=None)
    tame_event: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)

    def __post_init__(self) -> None:
        if self.ride_text is not None:
            self.ride_text = AnvilTranslator().localize(
                self.ride_text,
                prefix=f"action.interact.mount.{CONFIG.NAMESPACE}:{CONFIG.PROJECT_NAME}",
            )

    def add_feed_item(
        self, *, item: str | Item, temper_mod: int | None = None
    ) -> "EntityTamemount":
        """Adds an item that raises the temper. See `FeedItem`."""
        self.feed_items.append(FeedItem(item=item, temper_mod=temper_mod))
        return self


class EntityTradeResupply(JsonComponent):
    """Allows this entity to resupply the trades it has used up. Not in the Microsoft reference."""

    identifier = "minecraft:trade_resupply"


class EntityTradeTable(JsonComponent):
    """Defines this entity's ability to trade with players.

    Args:
        table (TradeTable | str): The trade table, or its path relative to the behavior pack root.
        convert_trades_economy (bool, optional): Determines when the mob transforms, if the trades should be converted when the new mob has a economy_trade_table. Game default false.
        display_name (str, optional): Name to be displayed while trading with this entity. It is added to the language file.
        new_screen (bool, optional): Used to determine if trading with entity opens the new trade screen. Game default false.
        persist_trades (bool, optional): Determines if the trades should persist when the mob transforms. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_table)
    """

    identifier = "minecraft:trade_table"

    table: TradeTable | str = json_field()
    convert_trades_economy: bool | None = json_field(default=None)
    display_name: str | None = json_field(default=None)
    new_screen: bool | None = json_field(default=None)
    persist_trades: bool | None = json_field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.table, TradeTable):
            self.table = self.table.table_path
        if self.display_name is not None:
            self.display_name = AnvilTranslator().localize(
                self.display_name,
                prefix=f"tradetable.{CONFIG.NAMESPACE}.{CONFIG.PROJECT_NAME}",
                suffix="name",
            )


class EntityTrust(JsonComponent):
    """Allows this entity to trust multiple players. Not in the Microsoft reference."""

    identifier = "minecraft:trust"


class EntityTrusting(JsonComponent):
    """Defines the rules for a mob to trust players.

    Args:
        trust_items (list[str | Item], optional): The items that can be used to get the entity to trust players. Add more with `add_trust_items`.
        trust_event (EventTrigger | str, optional): Event to run when this entity becomes trusting.
        probability (float, optional): The chance of the entity trusting with each item use between 0.0 and 1.0, where 1.0 is 100%. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trusting)
    """

    identifier = "minecraft:trusting"

    trust_items: list[Annotated[str | Item, ItemId]] = json_field(
        default_factory=list, omit_default=True
    )
    trust_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    probability: Annotated[float, Chance] | None = json_field(default=None)

    def add_trust_items(self, *items: str | Item) -> "EntityTrusting":
        """Adds items that get the entity to trust players."""
        self.trust_items.extend(items)
        return self


# endregion
