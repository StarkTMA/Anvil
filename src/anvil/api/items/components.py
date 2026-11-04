from dataclasses import InitVar
from typing import Annotated

from anvil.api.actors.entity import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.items import Item
from anvil.api.logic.molang import Molang
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.api.textures import ItemTexturesObject
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.blockbench import _BlockBenchSource
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    BlockId,
    EntityId,
    Hex,
    IconTexture,
    InRange,
    ItemId,
    JsonComponent,
    JsonCustomComponent,
    JsonObject,
    JsonValueComponent,
    Length,
    MinMax,
    NonNegative,
    json_field,
)
from anvil.lib.jsonmodel.enums import DamageCause, EnchantsSlots
from anvil.lib.jsonmodel.types import (
    RGB,
    RGB255,
    RGBA,
    RGBA255,
    HexRGB,
    HexRGBA,
    ItemCooldownType,
    ItemPlantAtFace,
    ItemStartUsing,
    ItemUseAnimations,
    ItemWearableSlots,
    Rarity,
)
from anvil.lib.translator import AnvilTranslator

# region Parts: objects nested inside components


class KineticEffectConditions(JsonObject):
    """Conditions that need to be satisfied for an effect of a kinetic weapon to be applied.

    Args:
        max_duration (int, optional): Time, in ticks, during which the effect can be applied after `delay` elapses. If negative, the effect is applied indefinitely. Game default -1.
        min_relative_speed (float, optional): Minimum relative speed of the user with respect to the target, projected onto the view vector. Game default 0.
        min_speed (float, optional): Minimum speed of the user, projected onto the view vector. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_kinetic_weapon_kinetic_effect_conditions)
    """

    max_duration: int | None = json_field(default=None)
    min_relative_speed: float | None = json_field(default=None)
    min_speed: float | None = json_field(default=None)


class DurabilityThreshold(JsonObject):
    """A durability threshold, and the effects emitted when it is met.

    Args:
        durability (int): The effects are emitted when the item durability is less than or equal to this value.
        particle_type (str, optional): Particle effect to emit when the threshold is met.
        sound_event (str, optional): Sound effect to emit when the threshold is met.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor_durability_threshold)
    """

    durability: Annotated[int, NonNegative] = json_field()
    particle_type: str | None = json_field(default=None)
    sound_event: str | None = json_field(default=None)


class DestroySpeed(JsonObject):
    """How fast a digger item breaks a block.

    Args:
        block (str | Block | BlockDescriptor): The block, by descriptor, identifier or tag query.
        speed (int): Digging speed for the block.
    """

    block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    speed: int = json_field()


class RepairItem(JsonObject):
    """Items that repair an item, and how much durability they restore.

    Args:
        items (list[str | Item]): Items that may be used to repair the item.
        repair_amount (Molang | float, optional): How much the item is repaired.
    """

    items: list[Annotated[str | Item, ItemId]] = json_field()
    repair_amount: Molang | str | float | None = json_field(default=None)


class Ammunition(JsonObject):
    """An item a shooter can fire.

    Args:
        item (str | Item): The ammunition item. It needs a `minecraft:projectile` component.
        search_inventory (bool, optional): Whether the inventory is searched for the ammunition. Game default false.
        use_in_creative (bool, optional): Whether the ammunition can be used in creative mode. Game default false.
        use_offhand (bool, optional): Whether the ammunition can be used from the off hand. Game default false.
    """

    item: Annotated[str | Item, ItemId] = json_field()
    search_inventory: bool | None = json_field(default=None)
    use_in_creative: bool | None = json_field(default=None)
    use_offhand: bool | None = json_field(default=None)


# endregion

# region Components required by other components


class ItemDurability(JsonComponent):
    """Sets how much damage the item can take before breaking, and allows the item to be combined at an anvil, grindstone, or crafting table.

    Args:
        max_durability (int): The amount of damage this item can take before breaking. Minimum 0.
        damage_chance (tuple[float, float], optional): The `(min, max)` percentage chance of this item losing durability, each between 0 and 100. Game default (100, 100).

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability)
    """

    identifier = "minecraft:durability"

    max_durability: Annotated[int, NonNegative] = json_field()
    damage_chance: Annotated[tuple[int, int], InRange(0, 100), MinMax] | None = (
        json_field(default=None)
    )


class ItemMaxStackSize(JsonValueComponent):
    """Determines how many of an item can be stacked together.

    Args:
        value (int): How many of the item can be stacked together, from 1 to 64.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size)
    """

    identifier = "minecraft:max_stack_size"

    value: Annotated[int, InRange(1, 64)] = json_field()


class ItemStorageItem(JsonComponent):
    """Enables an item to store data of the dynamic container associated with it. A dynamic container is a container for storing items that is linked to an item instead of a block or an entity.

    Args:
        allow_nested_storage_items (bool, optional): Whether another storage item is allowed inside this item. Game default true.
        allowed_items (list[str | Item], optional): Items that are exclusively allowed in this storage item. If empty, all items are allowed.
        banned_items (list[str | Item], optional): Items that are not allowed in this storage item.
        max_slots (int, optional): The maximum number of slots, from 1 to 64. Game default 64.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_item)
    """

    identifier = "minecraft:storage_item"

    allow_nested_storage_items: bool | None = json_field(default=None)
    allowed_items: list[Annotated[str | Item, ItemId]] | None = json_field(default=None)
    banned_items: list[Annotated[str | Item, ItemId]] | None = json_field(default=None)
    max_slots: Annotated[int, InRange(1, 64)] | None = json_field(default=None)


class ItemUseModifiers(JsonComponent):
    """Determines how long an item takes to use in combination with components such as Shooter, Throwable, or Food.

    Args:
        use_duration (float): Time, in seconds, that the item takes to use. Minimum 0.
        movement_modifier (float, optional): Multiplier applied to the player's movement speed while the item is in use. At most 1.
        emit_vibrations (bool, optional): Whether vibrations are emitted when the item starts or stops being used. Game default true.
        start_sound (str, optional): Sound event played when the item starts being used.
        start_using (ItemStartUsing, optional): When the player begins using the item. Game default "always". Requires format version 1.26.30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_modifiers)
    """

    identifier = "minecraft:use_modifiers"

    use_duration: Annotated[float, NonNegative] = json_field()
    movement_modifier: Annotated[float, InRange(maximum=1)] | None = json_field(
        default=None
    )
    emit_vibrations: bool | None = json_field(default=None)
    start_sound: str | None = json_field(default=None)
    start_using: ItemStartUsing | None = json_field(default=None)


# endregion

# region Components


class ItemCustomComponent(JsonCustomComponent, abstract=True):
    """Base of custom components: components registered by a script, with parameters.

    Subclass it with an `identifier` and the parameters as fields. The identifier is in the project
    namespace: a name without one gets it, any other namespace is refused.

        class Explosive(ItemCustomComponent):
            identifier = "explosive"

            power: float = json_field()

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/scripting/custom-components)
    """


class ItemAllowOffHand(JsonValueComponent):
    """Determines whether the item can be placed in the off hand slot.

    Args:
        value (bool, optional): Whether the item can be placed in the off hand slot. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand)
    """

    identifier = "minecraft:allow_off_hand"

    value: bool = json_field(default=True)


class ItemBlockPlacer(JsonComponent):
    """Sets the item as a placer item component for blocks. Items with this component will place a block when used.

    Args:
        block (str | Block | BlockDescriptor): The block that will be placed.
        replace_block_item (bool, optional): If true, the item is registered as the item for this block, and is returned when the block is broken or picked. The item identifier must match the block identifier. Game default false.
        aligned_placement (bool, optional): Whether block placement is aligned while the interaction button is held down. Requires format version 1.26.10.
        use_on (list[str | Block | BlockDescriptor], optional): Blocks this item can be used on, at most 256. If empty, all blocks are allowed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer)
    """

    identifier = "minecraft:block_placer"

    block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    replace_block_item: bool | None = json_field(default=None)
    aligned_placement: bool | None = json_field(default=None)
    use_on: (
        Annotated[
            list[Annotated[str | Block | BlockDescriptor, BlockId]], Length(maximum=256)
        ]
        | None
    ) = json_field(default=None)


class ItemBundleInteraction(JsonComponent):
    """Enables the bundle-specific interaction scheme and tooltip for an item.

    Args:
        num_viewable_slots (int, optional): The maximum number of slots in the bundle viewable by the player, from 1 to 64. Game default 12.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_bundle_interaction)
    """

    identifier = "minecraft:bundle_interaction"
    _requires = (ItemStorageItem, ItemMaxStackSize)

    num_viewable_slots: Annotated[int, InRange(1, 64)] | None = json_field(default=None)


class ItemCanDestroyInCreative(JsonValueComponent):
    """Determines whether the item can be used to destroy blocks while in creative mode.

    Args:
        value (bool, optional): Whether the item breaks blocks in creative mode while swinging. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative)
    """

    identifier = "minecraft:can_destroy_in_creative"

    value: bool = json_field(default=True)


class ItemCompostable(JsonComponent):
    """Specifies that an item is compostable and provides the chance of creating a composting layer in the composter.

    Args:
        composting_chance (int): The chance of this item to create a layer upon composting, from 1 to 100.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_compostable)
    """

    identifier = "minecraft:compostable"

    composting_chance: Annotated[int, InRange(1, 100)] = json_field()


class ItemCooldown(JsonComponent):
    """Adds a cooldown to an item, preventing it from being used again for a specified duration. Items sharing the same category enter cooldown together.

    Args:
        category (str): Groups items together. When an item is used, all items of its category enter cooldown.
        duration (int): How long, in seconds, the items of the category spend cooling down.
        type (ItemCooldownType, optional): The action that triggers the cooldown, "use" or "attack". Game default "use".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown)
    """

    identifier = "minecraft:cooldown"

    category: str = json_field()
    duration: Annotated[int | float, NonNegative] = json_field()
    type: ItemCooldownType | None = json_field(default=None)


class ItemDamage(JsonValueComponent):
    """Determines how much extra damage the item deals when attacking.

    Args:
        value (int): Extra damage added to the base attack damage, from 0 to 32767.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage)
    """

    identifier = "minecraft:damage"

    value: Annotated[int, InRange(0, 32767)] = json_field()


class ItemDamageAbsorption(JsonComponent):
    """Allows an item worn in an armor slot to absorb damage that would otherwise be dealt to its wearer. The absorbed damage reduces the item's durability.

    Args:
        absorbable_causes (list[DamageCause]): The damage causes the item can absorb, at least 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage_absorption)
    """

    identifier = "minecraft:damage_absorption"
    _requires = (ItemDurability,)

    absorbable_causes: Annotated[list[DamageCause], Length(minimum=1)] = json_field()


class ItemDigger(JsonComponent):
    """Configures an item as a digging tool, allowing it to break specific blocks faster than normal.

    Args:
        destroy_speeds (list[DestroySpeed], optional): The blocks this item digs, and how fast. Set them directly or add them with `add_destroy_speed`.
        use_efficiency (bool, optional): Whether the Efficiency enchantment increases the dig speed. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger)
    """

    identifier = "minecraft:digger"

    destroy_speeds: list[DestroySpeed] = json_field(
        default_factory=list, omit_default=True
    )
    use_efficiency: bool | None = json_field(default=None)

    def add_destroy_speed(self, *, block: str | Block | BlockDescriptor, speed: int):
        """Adds a block and its digging speed. See `DestroySpeed` for the parameters.

        Returns:
            ItemDigger: Self for method chaining.
        """
        self.destroy_speeds.append(DestroySpeed(block=block, speed=speed))
        return self


class ItemDisplayName(JsonComponent):
    """Sets the item display name. The item writes it as the localization key `item.<identifier>.name` and adds the name to the language file under that key.

    Args:
        value (str): The name shown for the item.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name)
    """

    identifier = "minecraft:display_name"

    value: str = json_field()

    def __prepare_export__(self, owner: "Item", *, root: bool = True) -> None:
        """Adds the name to the language file under `item.<identifier>.name`, then writes that key."""
        key = f"item.{owner.identifier}.name"
        if self.value == key:
            return
        AnvilTranslator().add_localization_entry(key, self.value)
        self.value = key


class ItemDurabilitySensor(JsonComponent):
    """Enables an item to emit effects when it receives damage.

    Args:
        durability_thresholds (list[DurabilityThreshold]): The thresholds and their effects, at least 1. Set them directly or add them with `add_durability_threshold`. When several thresholds are met, only the one with the lowest durability is used.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability_sensor)
    """

    identifier = "minecraft:durability_sensor"
    _requires = (ItemDurability,)

    durability_thresholds: Annotated[list[DurabilityThreshold], Length(minimum=1)] = (
        json_field(default_factory=list)
    )

    def add_durability_threshold(
        self,
        *,
        durability: int,
        particle_type: str | None = None,
        sound_event: str | None = None,
    ):
        """Adds a durability threshold. See `DurabilityThreshold` for the parameters.

        Returns:
            ItemDurabilitySensor: Self for method chaining.
        """
        self.durability_thresholds.append(
            DurabilityThreshold(
                durability=durability,
                particle_type=particle_type,
                sound_event=sound_event,
            )
        )
        return self


class ItemDyeable(JsonComponent):
    """Enables players to dye this item, like leather armor.

    Args:
        default_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): The color of the item when undyed. Written as a hex color. Game default white.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_dyeable)
    """

    identifier = "minecraft:dyeable"

    default_color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None
    ) = json_field(default=None)


class ItemEnchantable(JsonComponent):
    """Determines what enchantments can be applied to the item. Not all enchantments will have an effect on all item components.

    Args:
        slot (EnchantsSlots): Which types of enchantments can be applied. For example, `bow` lets the item be enchanted as if it were a bow.
        value (int): The enchantability of the item. Minimum 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable)
    """

    identifier = "minecraft:enchantable"

    slot: EnchantsSlots = json_field()
    value: Annotated[int, NonNegative] = json_field()


class ItemEntityPlacer(JsonComponent):
    """Allows an item to place entities into the world, and to set the spawn type of a monster spawner.

    Args:
        entity (str | Entity): The entity to be placed in the world.
        dispense_on (list[str | Block | BlockDescriptor], optional): Blocks this item can be dispensed on. If empty, all blocks are allowed.
        use_on (list[str | Block | BlockDescriptor], optional): Blocks this item can be used on. If empty, all blocks are allowed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer)
    """

    identifier = "minecraft:entity_placer"

    entity: Annotated[str | Entity, EntityId] = json_field()
    dispense_on: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = (
        json_field(default=None)
    )
    use_on: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = json_field(
        default=None
    )


class ItemFireResistant(JsonComponent):
    """Determines whether the item is immune to burning when dropped in fire or lava.

    Args:
        value (bool, optional): Whether the item is immune to burning. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fire_resistant)
    """

    identifier = "minecraft:fire_resistant"

    value: bool = json_field(default=True)


class ItemFood(JsonComponent):
    """Sets the item as a food component, allowing it to be edible to the player.

    Args:
        can_always_eat (bool, optional): Whether the item can be eaten even when not hungry. Game default false.
        nutrition (int, optional): The value added to the entity's nutrition when the item is used. Game default 0.
        saturation_modifier (float, optional): Used in `nutrition * saturation_modifier * 2` to compute the saturation buff. Game default 0.6.
        using_converts_to (str | Item, optional): The item this one converts to when used.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_food)
    """

    identifier = "minecraft:food"
    _requires = (ItemUseModifiers,)

    can_always_eat: bool | None = json_field(default=None)
    nutrition: Annotated[int, NonNegative] | None = json_field(default=None)
    saturation_modifier: Annotated[float, NonNegative] | None = json_field(default=None)
    using_converts_to: Annotated[str | Item, ItemId] | None = json_field(default=None)


class ItemFuel(JsonComponent):
    """Allows this item to be used as fuel in a furnace to 'cook' other items.

    Args:
        duration (int): How long, in seconds, this fuel cooks items for. Minimum 0.05.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel)
    """

    identifier = "minecraft:fuel"

    duration: Annotated[int | float, InRange(minimum=0.05)] = json_field()


class ItemGlint(JsonValueComponent):
    """Determines whether the item has the enchanted glint render effect on it.

    Args:
        value (bool, optional): Whether the item has the enchanted glint. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint)
    """

    identifier = "minecraft:glint"

    value: bool = json_field(default=True)


class ItemHandEquipped(JsonValueComponent):
    """Determines whether the item is rendered like a tool while in the player's hand.

    Args:
        value (bool, optional): Whether the item is rendered like a tool. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped)
    """

    identifier = "minecraft:hand_equipped"

    value: bool = json_field(default=True)


class ItemHoverTextColor(JsonValueComponent):
    """Determines the color of the item name when hovering over it.

    Args:
        value (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The color of the item hover text. Written as a hex color.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color)
    """

    identifier = "minecraft:hover_text_color"

    value: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] = (
        json_field()
    )


class ItemIcon(JsonComponent):
    """Determines the icon that represents the item in the UI and elsewhere. The texture is added to the resource pack and to `item_texture.json`.

    Args:
        textures (TextureComponents): The icon texture and its PBR maps. Written as `{"default": "<namespace>:<color>"}`.
        blockbench (str, optional): The Blockbench project to take the textures from. Not written to the JSON.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon)
    """

    identifier = "minecraft:icon"

    textures: Annotated[TextureComponents, IconTexture] = json_field()
    blockbench: InitVar[str | None] = None

    def __post_init__(self, blockbench: str | None) -> None:
        color = self.textures.color
        ItemTexturesObject().add_item(
            item_name=color, sprites=[color], blockbench=blockbench
        )
        texture_set = TextureSet(color, _BlockBenchSource.ITEM)
        if blockbench:
            texture_set.set_blockbench_textures(blockbench, self.textures)
        else:
            texture_set.set_item_textures(self.textures)
        texture_set.queue()


class ItemInteractButton(JsonValueComponent):
    """Determines whether the interact button is shown in touch controls, and the text on it.

    Args:
        value (bool | str, optional): True shows the default "Use Item" text. A string is added to the language file and shown instead. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button)
    """

    identifier = "minecraft:interact_button"

    value: bool | str = json_field(default=True)

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            self.value = AnvilTranslator().localize(
                self.value, prefix=f"key.{CONFIG.NAMESPACE}:{CONFIG.PROJECT_NAME}"
            )


class ItemKineticWeapon(JsonComponent):
    """Allows an item to deal kinetic damage and its effects every tick while in use, along the user's view vector. Damage depends on the user's and the target's velocity.

    Args:
        reach (tuple[float, float], optional): The `(min, max)` range, in blocks, along the view vector where entities can be hit. Game default (0, 3).
        creative_reach (tuple[float, float], optional): The reach in Creative mode. Defaults to `reach`.
        damage_modifier (float, optional): Value added to the scaled dot product, after `damage_multiplier`. Game default 0.
        damage_multiplier (float, optional): Value the sum of the projected velocities is multiplied by. Game default 1.
        delay (int, optional): Time, in ticks, after which kinetic damage and its effects start being applied. Game default 0.
        hitbox_margin (float, optional): Added tolerance to the view vector raycast. Game default 0.
        damage_conditions (KineticEffectConditions, optional): Conditions for damage to be applied. If not set, damage is not applied.
        knockback_conditions (KineticEffectConditions, optional): Conditions for knockback to be applied. If not set, knockback is not applied.
        dismount_conditions (KineticEffectConditions, optional): Conditions for riders to be dismounted. If not set, riders cannot be dismounted.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_kinetic_weapon)
    """

    identifier = "minecraft:kinetic_weapon"
    _requires = (ItemUseModifiers,)

    reach: Annotated[tuple[float, float], MinMax] | None = json_field(default=None)
    creative_reach: Annotated[tuple[float, float], MinMax] | None = json_field(
        default=None
    )
    damage_modifier: float | None = json_field(default=None)
    damage_multiplier: float | None = json_field(default=None)
    delay: Annotated[int, NonNegative] | None = json_field(default=None)
    hitbox_margin: float | None = json_field(default=None)
    damage_conditions: KineticEffectConditions | None = json_field(default=None)
    knockback_conditions: KineticEffectConditions | None = json_field(default=None)
    dismount_conditions: KineticEffectConditions | None = json_field(default=None)

    def set_damage_conditions(
        self,
        *,
        max_duration: int | None = None,
        min_relative_speed: float | None = None,
        min_speed: float | None = None,
    ):
        """Sets the conditions for damage to be applied. See `KineticEffectConditions` for the parameters.

        Returns:
            ItemKineticWeapon: Self for method chaining.
        """
        self.damage_conditions = KineticEffectConditions(
            max_duration=max_duration,
            min_relative_speed=min_relative_speed,
            min_speed=min_speed,
        )
        return self

    def set_knockback_conditions(
        self,
        *,
        max_duration: int | None = None,
        min_relative_speed: float | None = None,
        min_speed: float | None = None,
    ):
        """Sets the conditions for knockback to be applied. See `KineticEffectConditions` for the parameters.

        Returns:
            ItemKineticWeapon: Self for method chaining.
        """
        self.knockback_conditions = KineticEffectConditions(
            max_duration=max_duration,
            min_relative_speed=min_relative_speed,
            min_speed=min_speed,
        )
        return self

    def set_dismount_conditions(
        self,
        *,
        max_duration: int | None = None,
        min_relative_speed: float | None = None,
        min_speed: float | None = None,
    ):
        """Sets the conditions for riders to be dismounted. See `KineticEffectConditions` for the parameters.

        Returns:
            ItemKineticWeapon: Self for method chaining.
        """
        self.dismount_conditions = KineticEffectConditions(
            max_duration=max_duration,
            min_relative_speed=min_relative_speed,
            min_speed=min_speed,
        )
        return self


class ItemLiquidClipped(JsonValueComponent):
    """Determines whether the item interacts with liquid blocks on use.

    Args:
        value (bool, optional): Whether the item interacts with liquid blocks on use. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped)
    """

    identifier = "minecraft:liquid_clipped"

    value: bool = json_field(default=True)


class ItemPiercingWeapon(JsonComponent):
    """Allows an item to deal damage to all entities detected in a straight line along the user's view vector. Items with this component cannot destroy blocks.

    Args:
        reach (tuple[float, float], optional): The `(min, max)` range, in blocks, along the view vector where entities can be hit. Game default (0, 3).
        creative_reach (tuple[float, float], optional): The reach in Creative mode. Defaults to `reach`.
        hitbox_margin (float, optional): Added tolerance to the view vector raycast. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_piercing_weapon)
    """

    identifier = "minecraft:piercing_weapon"

    reach: Annotated[tuple[float, float], MinMax] | None = json_field(default=None)
    creative_reach: Annotated[tuple[float, float], MinMax] | None = json_field(
        default=None
    )
    hitbox_margin: float | None = json_field(default=None)


class ItemProjectile(JsonComponent):
    """Defines an item as a projectile that can be shot from dispensers or used as ammunition by `minecraft:shooter`. With `minecraft:throwable`, sets the entity spawned when the item is thrown.

    Args:
        projectile_entity (str | Entity): The entity fired as a projectile. A spawn event can be added as `"entity<event>"`.
        minimum_critical_power (float, optional): How long the projectile must be charged to critically hit. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile)
    """

    identifier = "minecraft:projectile"

    projectile_entity: Annotated[str | Entity, EntityId] = json_field()
    minimum_critical_power: float | None = json_field(default=None)


class ItemRarity(JsonValueComponent):
    """Specifies the base rarity of the item, and so the color of its name when hovered. Overridden by `minecraft:hover_text_color`.

    Args:
        value (Rarity): The base rarity. It rises when the item is enchanted.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_rarity)
    """

    identifier = "minecraft:rarity"

    value: Rarity = json_field()


class ItemRecord(JsonComponent):
    """Used by record items to play music.

    Args:
        sound_event (str): The sound event played.
        duration (int, optional): Duration of the sound event, in seconds. Game default 0.
        comparator_signal (int, optional): Signal strength for comparator blocks, from 1 to 13. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record)
    """

    identifier = "minecraft:record"

    sound_event: str = json_field()
    duration: Annotated[int | float, NonNegative] | None = json_field(default=None)
    comparator_signal: Annotated[int, InRange(1, 13)] | None = json_field(default=None)


class ItemRepairable(JsonComponent):
    """Defines the items that can repair this item, and how much durability each restores.

    Args:
        repair_items (list[RepairItem], optional): The repair entries. Set them directly or add them with `add_repair_item`.
        on_repaired (str, optional): Event triggered when this item has been repaired, for example "minecraft:celebrate".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable)
    """

    identifier = "minecraft:repairable"

    repair_items: list[RepairItem] = json_field(default_factory=list, omit_default=True)
    on_repaired: str | None = json_field(default=None)

    def add_repair_item(
        self,
        *,
        items: list[str | Item],
        repair_amount: Molang | str | float | None = None,
    ):
        """Adds a repair entry. See `RepairItem` for the parameters.

        Returns:
            ItemRepairable: Self for method chaining.
        """
        self.repair_items.append(RepairItem(items=items, repair_amount=repair_amount))
        return self


class ItemSeed(JsonComponent):
    """Sets the item as a seed that can be planted to grow crops.

    Args:
        crop_result (str | Block | BlockDescriptor): The block placed when the seed is planted.
        plant_at (list[str | Block | BlockDescriptor], optional): Blocks this seed can be planted on or attached to. If not set, standard farmland rules apply.
        plant_at_any_solid_surface (bool, optional): Deprecated. Has no effect from format version 1.19.0.
        plant_at_face (ItemPlantAtFace, optional): Deprecated. Has no effect from format version 1.19.0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_seed)
    """

    identifier = "minecraft:seed"

    crop_result: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    plant_at: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = (
        json_field(default=None)
    )
    plant_at_any_solid_surface: bool | None = json_field(default=None)
    plant_at_face: ItemPlantAtFace | None = json_field(default=None)


class ItemShooter(JsonComponent):
    """Compels an item to shoot projectiles, like a bow or crossbow.

    Args:
        ammunition (list[Ammunition], optional): The items that can be fired. Set them directly or add them with `add_ammunition`.
        charge_on_draw (bool, optional): Whether the shooter charges when the player starts drawing, like a crossbow. Game default false.
        max_draw_duration (int, optional): How long, in seconds, the shooter can be drawn before it fires or reaches full power. Game default 0.
        scale_power_by_draw_duration (bool, optional): Whether launch power grows with draw time. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter)
    """

    identifier = "minecraft:shooter"
    _requires = (ItemUseModifiers,)

    ammunition: list[Ammunition] = json_field(default_factory=list, omit_default=True)
    charge_on_draw: bool | None = json_field(default=None)
    max_draw_duration: Annotated[int | float, NonNegative] | None = json_field(
        default=None
    )
    scale_power_by_draw_duration: bool | None = json_field(default=None)

    def add_ammunition(
        self,
        *,
        item: str | Item,
        search_inventory: bool | None = None,
        use_in_creative: bool | None = None,
        use_offhand: bool | None = None,
    ):
        """Adds an ammunition entry. See `Ammunition` for the parameters.

        Returns:
            ItemShooter: Self for method chaining.
        """
        self.ammunition.append(
            Ammunition(
                item=item,
                search_inventory=search_inventory,
                use_in_creative=use_in_creative,
                use_offhand=use_offhand,
            )
        )
        return self


class ItemShouldDespawn(JsonValueComponent):
    """Determines whether the item should eventually despawn while floating in the world.

    Args:
        value (bool, optional): Whether the item despawns. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn)
    """

    identifier = "minecraft:should_despawn"

    value: bool = json_field(default=True)


class ItemStackedByData(JsonValueComponent):
    """Determines whether the same item with different aux values can stack, and whether the item entities can merge while floating in the world.

    Args:
        value (bool, optional): Whether items with different aux values stack and merge. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data)
    """

    identifier = "minecraft:stacked_by_data"

    value: bool = json_field(default=True)


class ItemStorageWeightLimit(JsonComponent):
    """Specifies the maximum weight limit that a storage item can hold.

    Args:
        max_weight_limit (int, optional): The maximum allowed weight of the sum of all contained items, at most 64. Game default 64.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_limit)
    """

    identifier = "minecraft:storage_weight_limit"

    max_weight_limit: Annotated[int, InRange(0, 64)] | None = json_field(default=None)


class ItemStorageWeightModifier(JsonComponent):
    """Specifies the weight of this item when inside another storage item.

    Args:
        weight_in_storage_item (int, optional): The weight of this item inside another storage item. 0 means the item is not allowed in one. Game default 4.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_storage_weight_modifier)
    """

    identifier = "minecraft:storage_weight_modifier"

    weight_in_storage_item: Annotated[int, NonNegative] | None = json_field(
        default=None
    )


class ItemSwingDuration(JsonComponent):
    """Duration, in seconds, of the item's swing animation when mining or attacking. Affects visuals only.

    Args:
        value (int, optional): The swing duration in seconds. Game default 0.3.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_duration)
    """

    identifier = "minecraft:swing_duration"

    value: Annotated[int | float, NonNegative] | None = json_field(default=None)


class ItemSwingSounds(JsonComponent):
    """Overrides the swing sounds emitted by the user. Each field takes a sound event from `sound_definitions.json`, including vanilla ones.

    Args:
        attack_critical_hit (str, optional): Sound played when an attack hits and deals critical damage.
        attack_hit (str, optional): Sound played when an attack hits.
        attack_miss (str, optional): Sound played when an attack misses or deals no damage due to invulnerability.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_swing_sounds)
    """

    identifier = "minecraft:swing_sounds"

    attack_critical_hit: str | None = json_field(default=None)
    attack_hit: str | None = json_field(default=None)
    attack_miss: str | None = json_field(default=None)


class ItemTags(JsonComponent):
    """Determines which tags are included on the item.

    Args:
        tags (list[MinecraftItemTags | str]): The item tags.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_tags)
    """

    identifier = "minecraft:tags"

    tags: list[MinecraftItemTags | str] = json_field()


class ItemThrowable(JsonComponent):
    """Makes an item throwable by the player, like a snowball or ender pearl. Use with `minecraft:projectile` to set the entity spawned.

    Args:
        do_swing_animation (bool, optional): Whether the item uses the swing animation when thrown. Game default false.
        launch_power_scale (float, optional): The scale at which the power of the throw increases. Game default 1.0.
        max_draw_duration (int, optional): The maximum duration to draw the item. Game default 0.
        max_launch_power (float, optional): The maximum launch power. Game default 1.0.
        min_draw_duration (int, optional): The minimum duration to draw the item. Game default 0.
        scale_power_by_draw_duration (bool, optional): Whether the power of the throw grows with draw time. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_throwable)
    """

    identifier = "minecraft:throwable"

    do_swing_animation: bool | None = json_field(default=None)
    launch_power_scale: float | None = json_field(default=None)
    max_draw_duration: Annotated[int | float, NonNegative] | None = json_field(
        default=None
    )
    max_launch_power: float | None = json_field(default=None)
    min_draw_duration: Annotated[int | float, NonNegative] | None = json_field(
        default=None
    )
    scale_power_by_draw_duration: bool | None = json_field(default=None)


class ItemUseAnimation(JsonValueComponent):
    """Specifies which animation is played when the player uses the item.

    Args:
        value (ItemUseAnimations): The animation played when the item is used.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation)
    """

    identifier = "minecraft:use_animation"

    value: ItemUseAnimations = json_field()


class ItemWearable(JsonComponent):
    """Allows an item to be worn by a player in an equipment slot. A non-hand slot sets the max stack size to 1.

    Args:
        slot (ItemWearableSlots): Where the item can be worn.
        protection (int, optional): How much protection the item provides. Game default 0.
        hides_player_location (bool, optional): Whether the wearer is hidden on locator maps and the locator bar. Game default false.
        dispensable (bool, optional): Whether the item can be equipped by a dispenser.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable)
    """

    identifier = "minecraft:wearable"

    slot: ItemWearableSlots = json_field()
    protection: Annotated[int, NonNegative] | None = json_field(default=None)
    hides_player_location: bool | None = json_field(default=None)
    dispensable: bool | None = json_field(default=None)


# endregion
