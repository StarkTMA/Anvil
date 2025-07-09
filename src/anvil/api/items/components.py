
# Require ITEM_SERVER_VERSION >= 1.21.30
from math import inf

from anvil import ANVIL, CONFIG
from anvil.lib.enums import (Effects, EnchantsSlots, ItemCategory, ItemGroups,
                             ItemRarity, ItemVanillaTags, Slots)
from anvil.lib.format_versions import ITEM_SERVER_VERSION
from anvil.lib.lib import clamp
from anvil.lib.schemas import _BaseComponent
from anvil.lib.types import Identifier, Seconds


class ItemRarity(_BaseComponent):
    _identifier = "minecraft:rarity"

    def __init__(self, value: ItemRarity) -> None:
        """Specifies the base rarity of the item, affecting the color of its name unless overridden by
        'minecraft:hover_text_color'.

        Parameters:
            value (ItemRarity): The base rarity of the item.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_rarity
        """
        super().__init__("rarity")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")
        self._set_value("value", value)


# Require ITEM_SERVER_VERSION >= 1.21.20
class ItemCustomComponents(_BaseComponent):
    _identifier = "minecraft:custom_components"

    def __init__(self, *components: str) -> None:
        """Registers custom components for this item.

        Parameters:
            components (str): The components to register, if the namespace is not provided, the project namespace will be used.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_custom_components
        """
        super().__init__("custom_components")
        self._enforce_version(ITEM_SERVER_VERSION, "1.21.20")
        self._set_value(components)


# Require ITEM_SERVER_VERSION >= 1.20.50
class ItemTags(_BaseComponent):
    _identifier = "minecraft:tags"

    def __init__(self, *tags: ItemVanillaTags | str) -> None:
        super().__init__("tags")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.50")
        self._add_field("tags", tags)


class ItemUseModifiers(_BaseComponent):
    _identifier = "minecraft:use_modifiers"

    def __init__(self, use_duration: float, movement_modifier: float = 1.0) -> None:
        """Determines how long an item takes to use in combination with components such as Shooter, Throwable, or Food.

        Parameters:
            use_duration (float): How long the item takes to use in seconds.
            movement_modifier (float): Modifier value to scale the players movement speed when item is in use. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_modifiers?view=minecraft-bedrock-stable
        """
        super().__init__("use_modifiers")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.50")

        self._add_field("use_duration", clamp(use_duration, 0, inf))
        if not movement_modifier == 1.0:
            self._add_field("movement_modifier", movement_modifier)


# Require ITEM_SERVER_VERSION >= 1.20.30
class ItemEnchantable(_BaseComponent):
    _identifier = "minecraft:enchantable"

    def __init__(self, slot: EnchantsSlots, value: int) -> None:
        """Determines what enchantments can be applied to the item. Not all enchantments will have an effect on all item components.

        Parameters:
            type (str): What enchantments can be applied (ex. Using bow would allow this item to be enchanted as if it were a bow).
            value (int): The value of the enchantment (minimum of 0).

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable
        """
        super().__init__("enchantable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")

        self._add_field("slot", slot)
        self._add_field("value", clamp(value, 0, inf))


class ItemFood(_BaseComponent):
    _identifier = "minecraft:food"

    def __init__(
        self, can_always_eat: bool = False, nutrition: int = 0, saturation_modifier: float = 0, using_converts_to: str = None
    ) -> None:
        """Sets the item as a food component, allowing it to be edible to the player.

        Parameters:
            can_always_eat (bool, optional): If true you can always eat this item (even when not hungry).
            nutrition (int, optional): The value that is added to the actor's nutrition when the item is used. Defaults to 0.
            saturation_modifier (float, optional): Saturation Modifier is used in this formula: (nutrition saturation_modifier 2) when applying the saturation buff. Defaults to 0.
            using_converts_to (str, optional): Saturation Modifier is used in this formula: (nutrition saturation_modifier 2) when applying the saturation buff. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_food
        """
        super().__init__("food")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")
        self._require_components(ItemUseModifiers)

        self._add_field("effects", [])
        self._add_field("can_always_eat", can_always_eat)
        self._add_field("nutrition", max(0, nutrition))
        self._add_field("saturation_modifier", max(0, saturation_modifier))
        if using_converts_to:
            self._add_field("using_converts_to", using_converts_to)

    def effects(self, effect: Effects, chance: float, duration: Seconds, amplifier: int):
        """# DEPRECATED
        Sets the effects of the food item.

        Parameters:
            effect (Effects): The effect to apply.
            chance (float): The chance of the effect being applied.
            duration (Seconds): The duration of the effect.
            amplifier (int): The amplifier of the effect.
        """
        self._component["effects"].append(
            {
                "name": str(effect),
                "chance": clamp(chance, 0, 1),
                "duration": max(0, duration * 20),
                "amplifier": clamp(amplifier, 0, 255),
            }
        )
        return self


class ItemInteractButton(_BaseComponent):
    _identifier = "minecraft:interact_button"

    def __init__(self, value: bool | str = True) -> None:
        """Is a boolean or string that determines if the interact button is shown in touch controls, and what text is displayed on the button. When set to 'true', the default 'Use Item' text will be used.

        Parameters:
            value (bool | str): Determines if the interact button is shown in touch controls, and what text is displayed on the button. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button
        """
        super().__init__("interact_button")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")

        if not value is False:
            self._set_value(value)


class ItemCanDestroyInCreative(_BaseComponent):
    _identifier = "minecraft:can_destroy_in_creative"

    def __init__(self, value: bool) -> None:
        """Determines if an item will break blocks in Creative Mode while swinging.

        Parameters:
            value (bool): If an item will break blocks in Creative Mode while swinging.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative
        """
        super().__init__("can_destroy_in_creative ")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemHoverTextColor(_BaseComponent):
    _identifier = "minecraft:hover_text_color"

    def __init__(self, color: str) -> None:
        """Determines the color of the item name when hovering over it.

        Parameters:
            value (bool): The color of the item name when hovering over it.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color
        """
        super().__init__("hover_text_color")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(color)


class ItemLiquidClipped(_BaseComponent):
    _identifier = "minecraft:can_destroy_in_creative"

    def __init__(self, value: bool) -> None:
        """Determines if an item will break blocks in Creative Mode while swinging.

        Parameters:
            value (bool): If an item will break blocks in Creative Mode while swinging.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative
        """
        super().__init__("can_destroy_in_creative")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


# Require ITEM_SERVER_VERSION >= 1.20.20
class ItemWearable(_BaseComponent):
    _identifier = "minecraft:wearable"

    def __init__(self, slot: Slots, protection: int = 0) -> None:
        """Sets the wearable item component.

        Parameters:
            slot (Slots): Determines where the item can be worn. If any non-hand slot is chosen, the max stack size is set to 1.
            protection (int, optional): How much protection the wearable has. Defaults to 0.
            dispensable (bool, optional): Whether or not the item can be dispensed from a dispenser. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable
        """
        super().__init__("wearable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.70")

        self._add_field("slot", slot)
        self._add_field("protection", protection)
        # self._add_field("dispensable", dispensable)


class ItemHandEquipped(_BaseComponent):
    _identifier = "minecraft:hand_equipped"

    def __init__(self, value: bool) -> None:
        """Determines if an item is rendered like a tool while in-hand.

        Parameters:
            value (bool): Determines if the item is rendered like a tool in-hand.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped
        """
        super().__init__("hand_equipped")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._add_field("value", value)


class ItemGlint(_BaseComponent):
    _identifier = "minecraft:glint"

    def __init__(self, value: bool) -> None:
        """Determines whether the item has the enchanted glint render effect on it.

        Parameters:
            value (bool): Whether the item has the enchanted glint render effect.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint
        """
        super().__init__("glint")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemStackedByData(_BaseComponent):
    _identifier = "minecraft:stacked_by_data"

    def __init__(self, value: bool) -> None:
        """Determines if the same item with different aux values can stack. Additionally, this component defines whether the item actors can merge while floating in the world.

        Parameters:
            value (bool): Sets whether the same item with different aux values can stack and merge while floating in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data
        """
        super().__init__("stacked_by_data")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemUseAnimation(_BaseComponent):
    _identifier = "minecraft:use_animation"

    def __init__(self, value: str) -> None:
        """Determines which animation plays when using an item.

        Parameters:
            value (str): Which animation to play when using an item.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation
        """
        super().__init__("use_animation")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemAllowOffHand(_BaseComponent):
    _identifier = "minecraft:allow_off_hand"

    def __init__(self, value: bool) -> None:
        """Determines whether an item can be placed in the off-hand slot of the inventory.

        Parameters:
            value (bool): Whether the item can be placed in the off-hand slot.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand
        """
        super().__init__("allow_off_hand")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemShouldDespawn(_BaseComponent):
    _identifier = "minecraft:should_despawn"

    def __init__(self, value: bool) -> None:
        """Determines if an item should despawn while floating in the world.

        Parameters:
            value (bool): Sets whether the item should eventually despawn while floating in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn
        """
        super().__init__("should_despawn")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemLiquidClipped(_BaseComponent):
    _identifier = "minecraft:liquid_clipped"

    def __init__(self, value: bool) -> None:
        """Determines whether an item interacts with liquid blocks on use.

        Parameters:
            value (bool): Whether an item interacts with liquid blocks on use.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped
        """
        super().__init__("liquid_clipped")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemDamage(_BaseComponent):
    _identifier = "minecraft:damage"

    def __init__(self, value: bool) -> None:
        """Determines how much extra damage an item does on attack.

        Parameters:
            value (bool): How much extra damage the item does on attack. Note that this must be a positive value.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage
        """
        super().__init__("damage")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._set_value(value)


class ItemDigger(_BaseComponent):
    _identifier = "minecraft:digger"

    def __init__(self, *destroy_speeds: str) -> None:
        """Sets the item as a "Digger" item. Component put on items that dig.

        Parameters:
            destroy_speeds (str): Destroy speed per block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger
        """
        super().__init__("digger")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._add_field("destroy_speeds", destroy_speeds)

    def use_efficiency(self, use_efficiency: bool = False):
        """Toggles if the item will be used efficiently."""
        self._add_field("use_efficiency", use_efficiency)
        return self


# Require ITEM_SERVER_VERSION >= 1.20.10
class ItemCooldown(_BaseComponent):
    _identifier = "minecraft:cooldown"

    def __init__(self, category: str, duration: Seconds) -> None:
        """Sets an items "Cool down" time. After using an item, it becomes unusable for the duration specified by the 'duration' setting of this component.

        Parameters:
            category (str): The type of cool down for this item.
            duration (float): The duration of time (in Seconds) items with a matching category will spend cooling down before becoming usable again.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown
        """
        super().__init__("cooldown")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._add_field("category", category)
        self._add_field("duration", duration)


class ItemRepairable(_BaseComponent):
    _identifier = "minecraft:repairable"

    def __init__(self, on_repaired: str = None) -> None:
        """Defines the items that can be used to repair a defined item, and the amount of durability each item restores upon repair. Each entry needs to define a list of strings for 'items' that can be used for the repair and an optional 'repair_amount' for how much durability is repaired.

        Parameters:
            on_repaired (str): Event that is called when this item has been repaired.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable
        """
        super().__init__("repairable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")
        self._add_field("repair_items", [])

        if not on_repaired is None:
            self._add_field("on_repaired", on_repaired)

    def add_items(self, repair_amount: int, *repair_items: str):
        """
        Parameters:
            repair_amount (int): How much durability is repaired.
            repair_items (str): List of repair item entries.
        """
        self._component["repair_items"].append(
            {"items": [str(i) for i in repair_items], "repair_amount": repair_amount}
        )
        return self


class ItemMaxStackSize(_BaseComponent):
    _identifier = "minecraft:max_stack_size"

    def __init__(self, stack_size: int) -> None:
        """Determines how many of an item can be stacked together.

        Parameters:
            stack_size (int): How many of an item that can be stacked together.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size
        """
        super().__init__("max_stack_size")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._set_value(clamp(stack_size, 1, 64))


class ItemBlockPlacer(_BaseComponent):
    _identifier = "minecraft:block_placer"

    def __init__(self, block: str, replace_block_item: bool = False) -> None:
        """Sets the item as a Planter item component for blocks. Planter items are items that can be planted into another block.

        Parameters:
            block (str): Set the placement block name for the planter item.
            use_on (str): List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer
        """
        super().__init__(
            "block_placer",
        )
        self._enforce_version(ITEM_SERVER_VERSION, "1.21.50")

        self._add_field("block", block)
        if replace_block_item:
            self._add_field("replace_block_item", replace_block_item)

    def use_on(self, *blocks: str):
        """List of block descriptors that contain blocks that this item can be used on."""
        self._add_field("use_on", blocks)
        return self


class ItemRecord(_BaseComponent):
    _identifier = "minecraft:record"

    def __init__(self, sound_event: str, duration: float, comparator_signal: int = 1) -> None:
        """Used by record items to play music.

        Parameters:
            sound_event (str): Set the placement block name for the planter item.
            duration (float): Duration of sound event in Seconds float value.
            comparator_signal (int): Signal strength for comparator blocks to use from 1 - 13.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record
        """
        super().__init__("record")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._add_field("sound_event", sound_event)
        self._add_field("duration", duration)
        self._add_field("comparator_signal", clamp(comparator_signal, 1, 13))


class ItemShooter(_BaseComponent):
    _identifier = "minecraft:shooter"

    def __init__(
        self,
        charge_on_draw: bool = False,
        max_draw_duration: float = 0.0,
        scale_power_by_draw_duration: bool = False,
    ) -> None:
        """Sets the shooter item component.

        Parameters:
            charge_on_draw (bool, optional): Sets if the item is charged when drawn (Like crossbows). Defaults to False.
            max_draw_duration (float, optional): How long can it be drawn before it will release automatically. Defaults to 0.0.
            scale_power_by_draw_duration (bool, optional): Scale the power by draw duration? When true, the longer you hold, the more power it will have when released.. Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter
        """
        super().__init__("shooter")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._add_field("ammunition", [])
        if charge_on_draw:
            self._add_field("charge_on_draw", charge_on_draw)
        if not max_draw_duration == 0.0:
            self._add_field("max_draw_duration", max_draw_duration)
        if scale_power_by_draw_duration:
            self._add_field("scale_power_by_draw_duration", scale_power_by_draw_duration)

    def add_ammunition(
        self, ammunition: Identifier, search_inventory: bool = True, use_in_creative: bool = False, use_offhand: bool = False
    ):
        self._component["ammunition"].append(
            {
                "item": ammunition,
                "search_inventory": search_inventory,
                "use_in_creative": use_in_creative,
                "use_offhand": use_offhand,
            }
        )
        return self


class ItemProjectile(_BaseComponent):
    _identifier = "minecraft:projectile"

    def __init__(self, projectile_entity: Identifier, minimum_critical_power: int) -> None:
        """Compels the item to shoot, similarly to an arrow.
        Items with minecraft:projectile can be shot from dispensers or used as ammunition for items with the minecraft:shooter item component.
        Additionally, this component sets the entity that is spawned for items that also contain the minecraft:throwable component.

        Parameters:
            projectile_entity (Identifier): The entity to be fired as a projectile.
            minimum_critical_power (int): Defines the time a projectile needs to charge in order to critically hit.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile
        """
        super().__init__("projectile")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._add_field("projectile_entity", projectile_entity)
        self._add_field("minimum_critical_power", minimum_critical_power)


class ItemThrowable(_BaseComponent):
    _identifier = "minecraft:throwable"

    def __init__(
        self,
        do_swing_animation: bool = False,
        launch_power_scale: float = 1.0,
        max_draw_duration: float = 0.0,
        max_launch_power: float = 1.0,
        min_draw_duration: float = 0.0,
        scale_power_by_draw_duration: bool = False,
    ) -> None:
        """Sets the throwable item component.

        Parameters:
            do_swing_animation (bool, optional): Whether the item should use the swing animation when thrown. Defaults to False.
            launch_power_scale (float, optional): The scale at which the power of the throw increases. Defaults to 1.0.
            max_draw_duration (float, optional): The maximum duration to draw a throwable item. Defaults to 0.0.
            max_launch_power (float, optional): The maximum power to launch the throwable item. Defaults to 1.0.
            min_draw_duration (float, optional): The minimum duration to draw a throwable item. Defaults to 0.0.
            scale_power_by_draw_duration (bool, optional): Whether or not the power of the throw increases with duration charged. When true, The longer you hold, the more power it will have when released. Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_throwable
        """
        super().__init__("throwable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        if do_swing_animation:
            self._add_field("do_swing_animation", do_swing_animation)
        if not launch_power_scale == 1.0:
            self._add_field("launch_power_scale", launch_power_scale)
        if not max_draw_duration == 0.0:
            self._add_field("max_draw_duration", max_draw_duration)
        if not max_launch_power == 1.0:
            self._add_field("max_launch_power", max_launch_power)
        if not min_draw_duration == 0.0:
            self._add_field("min_draw_duration", min_draw_duration)
        if scale_power_by_draw_duration:
            self._add_field("scale_power_by_draw_duration", scale_power_by_draw_duration)


# Require ITEM_SERVER_VERSION >= 1.19.80
class ItemDurability(_BaseComponent):
    _identifier = "minecraft:durability"

    def __init__(self, max_durability: int, damage_chance: tuple[int, int] = 100) -> None:
        """Sets how much damage the item can take before breaking, and allows the item to be combined at an anvil, grindstone, or crafting table.

        Parameters:
            max_durability (int): Max durability is the amount of damage that this item can take before breaking. The minimum value for this parameter is 0.
            damage_chance (int, optional): Damage chance is the percentage chance of this item losing durability. Default is set at 100 to 100.. Defaults to 100.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability
        """
        super().__init__("durability")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._add_field("max_durability", max(0, max_durability))

        if damage_chance != 100:
            self._add_field(
                "damage_chance",
                {
                    "min": clamp(damage_chance[0], 0, 100),
                    "max": clamp(damage_chance[1], 0, 100),
                },
            )


class ItemDisplayName(_BaseComponent):
    _identifier = "minecraft:display_name"

    def __init__(self, display_name: str, localize: bool = True) -> None:
        """Sets the item display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Parameters:
            display_name (str): Set the display name for an item.
            localize (bool, optional): Whether to use the name with a localization file or not. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name
        """
        super().__init__("display_name")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        if localize:
            key = f'item.{CONFIG.NAMESPACE}:{display_name.lower().replace(" ", "_").replace("\\n", "_")}.name'
            ANVIL.definitions.register_lang(key, display_name)
            self._add_field("value", key)
        else:
            self._add_field("value", display_name)


class ItemFuel(_BaseComponent):
    _identifier = "minecraft:fuel"

    def __init__(self, duration: float) -> None:
        """Allows this item to be used as fuel in a furnace to 'cook' other items.

        Parameters:
            duration (float): How long in seconds will this fuel cook items for. Minimum value: 0.05.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel
        """
        super().__init__("fuel")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._add_field("duration", clamp(duration, 0.05, inf))


class ItemEntityPlacer(_BaseComponent):
    _identifier = "minecraft:entity_placer"

    def __init__(self, entity: str) -> None:
        """Allows an item to place entities into the world. Additionally, the component allows the item to set the spawn type of a monster spawner.

        Parameters:
            entity (str): The entity to be placed in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer
        """
        super().__init__("entity_placer")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._add_field("entity", entity)

    def dispense_on(self, *blocks: str):
        """List of block descriptors that contain blocks that this item can be dispensed on."""
        self._add_field("dispense_on", blocks)
        return self

    def use_on(self, *blocks: str):
        """List of block descriptors that contain blocks that this item can be used on."""
        self._add_field("use_on", blocks)
        return self


class ItemIcon(_BaseComponent):
    _identifier = "minecraft:icon"

    def __init__(self, texture: str) -> None:
        """Sets the icon item component. Determines the icon to represent the item in the UI and elsewhere.

        Parameters:
            texture (str): The item texture name to be used.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon
        """
        super().__init__("icon")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        ANVIL.definitions.register_item_textures(texture, "", texture)
        self._component["textures"] = {
            "default": f"{CONFIG.NAMESPACE}:{texture}",
        }
