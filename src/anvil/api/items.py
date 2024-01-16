import os

from anvil import ANVIL, CONFIG
from anvil.api.actors import Attachable, _Components
from anvil.api.commands import Effects, Slots
from anvil.api.components import _component
from anvil.api.types import Identifier, Seconds, inf
from anvil.lib.format_versions import ITEM_SERVER_VERSION
from anvil.lib.lib import clamp
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription

__all__ = [
    "Item",
    "ItemIcon",
    "ItemFuel",
    "ItemEntityPlacer",
    "ItemDurability",
    "ItemDisplayName",
    "ItemCooldown",
    "ItemRepairable",
    "ItemBlockPlacer",
    "ItemMaxStackSize",
    "ItemRecord",
    "ItemShooter",
    "ItemProjectile",
    "ItemThrowable",
    "ItemWearable",
    "ItemHandEquipped",
    "ItemGlint",
    "ItemUseModifiers",
    "ItemStackedByData",
    "ItemUseAnimation",
    "ItemAllowOffHand",
    "ItemShouldDespawn",
    "ItemLiquidClipped",
    "ItemDamage",
    "ItemDigger",
    "ItemEnchantable",
    "ItemFood",
    "ItemsInteractButton",
]


# Components
# Require ITEM_SERVER_VERSION >= 1.20.50
class ItemTags(_component):
    component_namespace = "minecraft:tags"

    def __init__(self, *tags: str) -> None:
        super().__init__("tags")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.50")
        self._component_add_field("tags", tags)


class ItemUseModifiers(_component):
    component_namespace = "minecraft:use_modifiers"

    def __init__(self, use_duration: float, movement_modifier: float = 1.0) -> None:
        """Determines how long an item takes to use in combination with components such as Shooter, Throwable, or Food.

        Args:
            use_duration (float): How long the item takes to use in seconds.
            movement_modifier (float): Modifier value to scale the players movement speed when item is in use. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_modifiers?view=minecraft-bedrock-stable
        """
        super().__init__("use_modifiers")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.50")

        self._component_add_field("use_duration", clamp(use_duration, 0, inf))
        if not movement_modifier == 1.0:
            self._component_add_field("movement_modifier", movement_modifier)


# Require ITEM_SERVER_VERSION >= 1.20.30
class ItemEnchantable(_component):
    component_namespace = "minecraft:enchantable"

    def __init__(self, type: str, value: int) -> None:
        """Determines what enchantments can be applied to the item. Not all enchantments will have an effect on all item components.

        Args:
            type (str): What enchantments can be applied (ex. Using bow would allow this item to be enchanted as if it were a bow).
            value (int): The value of the enchantment (minimum of 0).

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_enchantable
        """
        super().__init__("enchantable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")

        self._component_add_field("type", type)
        self._component_add_field("value", clamp(value, 0, inf))


class ItemFood(_component):
    component_namespace = "minecraft:food"

    def __init__(
        self, can_always_eat: bool = False, nutrition: int = 0, saturation_modifier: float = 0, using_converts_to: str = None
    ) -> None:
        """Sets the item as a food component, allowing it to be edible to the player.

        Args:
            can_always_eat (bool, optional): If true you can always eat this item (even when not hungry).
            nutrition (int, optional): The value that is added to the actor's nutrition when the item is used. Defaults to 0.
            saturation_modifier (float, optional): Saturation Modifier is used in this formula: (nutrition saturation_modifier 2) when applying the saturation buff. Defaults to 0.
            using_converts_to (str, optional): Saturation Modifier is used in this formula: (nutrition saturation_modifier 2) when applying the saturation buff. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_food
        """
        super().__init__("food")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")
        self._require_components(ItemUseModifiers)

        self._component_add_field("effects", [])
        if can_always_eat:
            self._component_add_field("can_always_eat", True)

        if nutrition > 0:
            self._component_add_field("nutrition", max(1, nutrition))

        if saturation_modifier > 0:
            self._component_add_field("saturation_modifier", max(0, saturation_modifier))

        if not using_converts_to is None:
            self._component_add_field("using_converts_to", using_converts_to)

    def effects(self, effect: Effects, chance: float, duration: Seconds, amplifier: int):
        """Sets the effects of the food item.

        Args:
            effect (Effects): The effect to apply.
            chance (float): The chance of the effect being applied.
            duration (Seconds): The duration of the effect.
            amplifier (int): The amplifier of the effect.
        """
        self[self.component_namespace]["effects"].append(
            {
                "name": effect.value,
                "chance": clamp(chance, 0, 1),
                "duration": duration,
                "amplifier": clamp(amplifier, 0, 255),
            }
        )
        return self


class ItemsInteractButton(_component):
    component_namespace = "minecraft:interact_button"

    def __init__(self, value: bool | str = True) -> None:
        """Is a boolean or string that determines if the interact button is shown in touch controls, and what text is displayed on the button. When set to 'true', the default 'Use Item' text will be used.

        Args:
            value (bool | str): Determines if the interact button is shown in touch controls, and what text is displayed on the button. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_interact_button
        """
        super().__init__("interact_button")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.30")

        if not value is False:
            self._component_set_value(value)


class ItemCanDestroyInCreative(_component):
    component_namespace = "minecraft:can_destroy_in_creative"

    def __init__(self, value: bool) -> None:
        """Determines if an item will break blocks in Creative Mode while swinging.

        Args:
            value (bool): If an item will break blocks in Creative Mode while swinging.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative
        """
        super().__init__("can_destroy_in_creative ")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemHoverTextColor(_component):
    component_namespace = "minecraft:hover_text_color"

    def __init__(self, color: str) -> None:
        """Determines the color of the item name when hovering over it.

        Args:
            value (bool): The color of the item name when hovering over it.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hover_text_color
        """
        super().__init__("hover_text_color")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(color)


class ItemLiquidClipped(_component):
    component_namespace = "minecraft:can_destroy_in_creative"

    def __init__(self, value: bool) -> None:
        """Determines if an item will break blocks in Creative Mode while swinging.

        Args:
            value (bool): If an item will break blocks in Creative Mode while swinging.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_can_destroy_in_creative
        """
        super().__init__("can_destroy_in_creative")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


# Require ITEM_SERVER_VERSION >= 1.20.20
class ItemWearable(_component):
    component_namespace = "minecraft:wearable"

    def __init__(self, slot: Slots, protection: int = 0, dispensable: bool = True) -> None:
        """Sets the wearable item component.

        Args:
            slot (Slots): Determines where the item can be worn. If any non-hand slot is chosen, the max stack size is set to 1.
            protection (int, optional): How much protection the wearable has. Defaults to 0.
            dispensable (bool, optional): Whether or not the item can be dispensed from a dispenser. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_wearable
        """
        super().__init__("wearable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_add_field("slot", slot)
        self._component_add_field("protection", protection)
        self._component_add_field("dispensable", dispensable)


class ItemHandEquipped(_component):
    component_namespace = "minecraft:hand_equipped"

    def __init__(self, value: bool) -> None:
        """Determines if an item is rendered like a tool while in-hand.

        Args:
            value (bool): Determines if the item is rendered like a tool in-hand.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_hand_equipped
        """
        super().__init__("hand_equipped")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemGlint(_component):
    component_namespace = "minecraft:glint"

    def __init__(self, value: bool) -> None:
        """Determines whether the item has the enchanted glint render effect on it.

        Args:
            value (bool): Whether the item has the enchanted glint render effect.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_glint
        """
        super().__init__("glint")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemStackedByData(_component):
    component_namespace = "minecraft:stacked_by_data"

    def __init__(self, value: bool) -> None:
        """Determines if the same item with different aux values can stack. Additionally, this component defines whether the item actors can merge while floating in the world.

        Args:
            value (bool): Sets whether the same item with different aux values can stack and merge while floating in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_stacked_by_data
        """
        super().__init__("stacked_by_data")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemUseAnimation(_component):
    component_namespace = "minecraft:use_animation"

    def __init__(self, value: str) -> None:
        """Determines which animation plays when using an item.

        Args:
            value (str): Which animation to play when using an item.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_use_animation
        """
        super().__init__("use_animation")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemAllowOffHand(_component):
    component_namespace = "minecraft:allow_off_hand"

    def __init__(self, value: bool) -> None:
        """Determines whether an item can be placed in the off-hand slot of the inventory.

        Args:
            value (bool): Whether the item can be placed in the off-hand slot.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_allow_off_hand
        """
        super().__init__("allow_off_hand")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemShouldDespawn(_component):
    component_namespace = "minecraft:should_despawn"

    def __init__(self, value: bool) -> None:
        """Determines if an item should despawn while floating in the world.

        Args:
            value (bool): Sets whether the item should eventually despawn while floating in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_should_despawn
        """
        super().__init__("should_despawn")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemLiquidClipped(_component):
    component_namespace = "minecraft:liquid_clipped"

    def __init__(self, value: bool) -> None:
        """Determines whether an item interacts with liquid blocks on use.

        Args:
            value (bool): Whether an item interacts with liquid blocks on use.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_liquid_clipped
        """
        super().__init__("liquid_clipped")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemDamage(_component):
    component_namespace = "minecraft:damage"

    def __init__(self, value: bool) -> None:
        """Determines how much extra damage an item does on attack.

        Args:
            value (bool): How much extra damage the item does on attack. Note that this must be a positive value.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_damage
        """
        super().__init__("damage")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_set_value(value)


class ItemDigger(_component):
    component_namespace = "minecraft:digger"

    def __init__(self, *destroy_speeds: str) -> None:
        """Sets the item as a "Digger" item. Component put on items that dig.

        Args:
            destroy_speeds (str): Destroy speed per block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_digger
        """
        super().__init__("digger")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.20")

        self._component_add_field("destroy_speeds", destroy_speeds)

    def use_efficiency(self, use_efficiency: bool = False):
        """Toggles if the item will be used efficiently."""
        self._component_add_field("use_efficiency", use_efficiency)
        return self


# Require ITEM_SERVER_VERSION >= 1.20.10
class ItemCooldown(_component):
    component_namespace = "minecraft:cooldown"

    def __init__(self, category: str, duration: Seconds) -> None:
        """Sets an items "Cool down" time. After using an item, it becomes unusable for the duration specified by the 'duration' setting of this component.

        Args:
            category (str): The type of cool down for this item.
            duration (float): The duration of time (in seconds) items with a matching category will spend cooling down before becoming usable again.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_cooldown
        """
        super().__init__("cooldown")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("category", category)
        self._component_add_field("duration", duration)


class ItemRepairable(_component):
    component_namespace = "minecraft:repairable"

    def __init__(self, on_repaired: str = None) -> None:
        """Defines the items that can be used to repair a defined item, and the amount of durability each item restores upon repair. Each entry needs to define a list of strings for 'items' that can be used for the repair and an optional 'repair_amount' for how much durability is repaired.

        Args:
            on_repaired (str): Event that is called when this item has been repaired.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_repairable
        """
        super().__init__("repairable")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")
        self._component_add_field("repair_items", [])

        if not on_repaired is None:
            self._component_add_field("on_repaired", on_repaired)

    def add_items(self, repair_amount: int, *repair_items: str):
        """
        Args:
            repair_amount (int): How much durability is repaired.
            repair_items (str): List of repair item entries.
        """
        self[self.component_namespace]["repair_items"].append({"items": repair_items, "repair_amount": repair_amount})
        return self


class ItemMaxStackSize(_component):
    component_namespace = "minecraft:max_stack_size"

    def __init__(self, stack_size: int) -> None:
        """Determines how many of an item can be stacked together.

        Args:
            stack_size (int): How many of an item that can be stacked together.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_max_stack_size
        """
        super().__init__("max_stack_size")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_set_value(clamp(stack_size, 1, 64))


class ItemBlockPlacer(_component):
    component_namespace = "minecraft:block_placer"

    def __init__(self, block: str, *use_on: str) -> None:
        """Sets the item as a Planter item component for blocks. Planter items are items that can be planted into another block.

        Args:
            block (str): Set the placement block name for the planter item.
            use_on (str): List of block descriptors that contain blocks that this item can be used on. If left empty, all blocks will be allowed.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_block_placer
        """
        super().__init__("block_placer")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("block", block)
        self._component_add_field("use_on", use_on)


class ItemRecord(_component):
    component_namespace = "minecraft:record"

    def __init__(self, sound_event: str, duration: float, comparator_signal: int = 1) -> None:
        """Used by record items to play music.

        Args:
            sound_event (str): Set the placement block name for the planter item.
            duration (float): Duration of sound event in seconds float value.
            comparator_signal (int): Signal strength for comparator blocks to use from 1 - 13.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_record
        """
        super().__init__("record")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("sound_event", sound_event)
        self._component_add_field("duration", duration)
        self._component_add_field("comparator_signal", clamp(comparator_signal, 1, 13))


class ItemShooter(_component):
    component_namespace = "minecraft:shooter"

    def __init__(
        self,
        charge_on_draw: bool = False,
        max_draw_duration: float = 0.0,
        scale_power_by_draw_duration: bool = False,
    ) -> None:
        """Sets the shooter item component.

        Args:
            charge_on_draw (bool, optional): Sets if the item is charged when drawn (Like crossbows). Defaults to False.
            max_draw_duration (float, optional): How long can it be drawn before it will release automatically. Defaults to 0.0.
            scale_power_by_draw_duration (bool, optional): Scale the power by draw duration? When true, the longer you hold, the more power it will have when released.. Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_shooter
        """
        super().__init__("shooter")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("ammunition", [])
        if charge_on_draw:
            self._component_add_field("charge_on_draw", charge_on_draw)
        if not max_draw_duration == 0.0:
            self._component_add_field("max_draw_duration", max_draw_duration)
        if scale_power_by_draw_duration:
            self._component_add_field("scale_power_by_draw_duration", scale_power_by_draw_duration)

    def add_ammunition(
        self, ammunition: Identifier, search_inventory: bool = True, use_in_creative: bool = False, use_offhand: bool = False
    ):
        self[self.component_namespace]["ammunition"].append(
            {
                "item": ammunition,
                "search_inventory": search_inventory,
                "use_in_creative": use_in_creative,
                "use_offhand": use_offhand,
            }
        )
        return self


class ItemProjectile(_component):
    component_namespace = "minecraft:projectile"

    def __init__(self, projectile_entity: Identifier, minimum_critical_power: int) -> None:
        """Compels the item to shoot, similarly to an arrow.
        Items with minecraft:projectile can be shot from dispensers or used as ammunition for items with the minecraft:shooter item component.
        Additionally, this component sets the entity that is spawned for items that also contain the minecraft:throwable component.

        Args:
            projectile_entity (Identifier): The entity to be fired as a projectile.
            minimum_critical_power (int): Defines the time a projectile needs to charge in order to critically hit.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_projectile
        """
        super().__init__("projectile")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("projectile_entity", projectile_entity)
        self._component_add_field("minimum_critical_power", minimum_critical_power)


class ItemThrowable(_component):
    component_namespace = "minecraft:throwable"

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

        Args:
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
            self._component_add_field("do_swing_animation", do_swing_animation)
        if not launch_power_scale == 1.0:
            self._component_add_field("launch_power_scale", launch_power_scale)
        if not max_draw_duration == 0.0:
            self._component_add_field("max_draw_duration", max_draw_duration)
        if not max_launch_power == 1.0:
            self._component_add_field("max_launch_power", max_launch_power)
        if not min_draw_duration == 0.0:
            self._component_add_field("min_draw_duration", min_draw_duration)
        if scale_power_by_draw_duration:
            self._component_add_field("scale_power_by_draw_duration", scale_power_by_draw_duration)


# Require ITEM_SERVER_VERSION >= 1.19.80
class ItemDurability(_component):
    component_namespace = "minecraft:durability"

    def __init__(self, max_durability: int, damage_chance: tuple[int, int] = 100) -> None:
        """Sets how much damage the item can take before breaking, and allows the item to be combined at an anvil, grindstone, or crafting table.

        Args:
            max_durability (int): Max durability is the amount of damage that this item can take before breaking. The minimum value for this parameter is 0.
            damage_chance (int, optional): Damage chance is the percentage chance of this item losing durability. Default is set at 100 to 100.. Defaults to 100.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_durability
        """
        super().__init__("durability")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._component_add_field("max_durability", max(0, max_durability))

        if damage_chance != 100:
            self._component_add_field(
                "damage_chance",
                {
                    "min": clamp(damage_chance[0], 0, 100),
                    "max": clamp(damage_chance[1], 0, 100),
                },
            )


class ItemDisplayName(_component):
    component_namespace = "minecraft:display_name"

    def __init__(self, display_name: str, localize: bool = True) -> None:
        """Sets the item display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Args:
            display_name (str): Set the display name for an item.
            localize (bool, optional): Whether to use the name with a localization file or not. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_display_name
        """
        super().__init__("display_name")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        if localize:
            key = f'item.{CONFIG.NAMESPACE}:{display_name.lower().replace(" ", "_")}.name'
            ANVIL.definitions.register_lang(key, display_name)
            self._component_add_field("value", key)
        else:
            self._component_add_field("value", display_name)


class ItemFuel(_component):
    component_namespace = "minecraft:fuel"

    def __init__(self, duration: float) -> None:
        """Allows this item to be used as fuel in a furnace to 'cook' other items.

        Args:
            duration (float): How long in seconds will this fuel cook items for. Minimum value: 0.05.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_fuel
        """
        super().__init__("fuel")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._component_add_field("duration", clamp(duration, 0.05, inf))


class ItemEntityPlacer(_component):
    component_namespace = "minecraft:entity_placer"

    def __init__(self, entity: str) -> None:
        """Allows an item to place entities into the world. Additionally, the component allows the item to set the spawn type of a monster spawner.

        Args:
            entity (str): The entity to be placed in the world.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_entity_placer
        """
        super().__init__("entity_placer")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._component_add_field("entity", entity)

    def dispense_on(self, *blocks: str):
        """List of block descriptors that contain blocks that this item can be dispensed on."""
        self._component_add_field("dispense_on", blocks)
        return self

    def use_on(self, *blocks: str):
        """List of block descriptors that contain blocks that this item can be used on."""
        self._component_add_field("use_on", blocks)
        return self


class ItemIcon(_component):
    component_namespace = "minecraft:icon"

    def __init__(self, texture: str) -> None:
        """Sets the icon item component. Determines the icon to represent the item in the UI and elsewhere.

        Args:
            texture (str): The item texture name to be used.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon
        """
        super().__init__("icon")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        ANVIL.definitions.register_item_textures(texture, "", texture)
        self._component_add_field("texture", f"{CONFIG.NAMESPACE}:{texture}")


# Items
class _ItemServerDescription(MinecraftDescription):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._description["description"]["properties"] = {}

    def group(self, group: str):
        self._description["description"]["group"] = group
        return self

    def category(self, category: str):
        self._description["description"]["category"] = category
        return self

    @property
    def is_hidden_in_commands(self):
        self._description["description"]["is_hidden_in_commands"] = True
        return self

    @property
    def to_dict(self):
        return super().to_dict


class _ItemServer(AddonObject):
    _extension = ".item.json"
    _path = os.path.join(CONFIG.BP_PATH, "items")

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(name)
        self._name = name
        self._is_vanilla = is_vanilla
        self._server_item = JsonSchemes.server_item()
        self._description = _ItemServerDescription(name, is_vanilla)
        self._components = _Components()

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    def queue(self):
        self._server_item["minecraft:item"].update(self.description.to_dict)
        self._server_item["minecraft:item"]["components"].update(self._components._export()["components"])

        if not ItemDisplayName.component_namespace in self._server_item["minecraft:item"]["components"]:
            display_name = self._name.replace("_", " ").title()
            self._server_item["minecraft:item"]["components"][ItemDisplayName.component_namespace] = {"value": display_name}

        self.content(self._server_item)

        super().queue()


# ---------------------------


class Item:
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        self._name = name
        self._is_vanilla = is_vanilla
        self._server = _ItemServer(name, is_vanilla)
        self._attachable = None

        self._namespace_format = "minecraft" if self._is_vanilla else CONFIG.NAMESPACE

    @property
    def Server(self):
        return self._server

    @property
    def identifier(self):
        return f"{self._namespace_format}:{self._name}"

    @property
    def name(self):
        return self._name

    @property
    def attachable(self):
        if not self._attachable:
            self._attachable = Attachable(self.name)

        return self._attachable

    def queue(self):
        self.Server.queue()
        if self._attachable:
            self._attachable.queue

        if self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"].startswith("item."):
            display_name = ANVIL.definitions._language[
                self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"]
            ]

        else:
            display_name = self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"]

        CONFIG.Report.add_report(
            ReportType.ITEM,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )
