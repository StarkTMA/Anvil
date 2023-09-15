from anvil.api.actors import _Components
from anvil.api.components import _component
from anvil.core import ANVIL, AddonObject, _MinecraftDescription
from anvil.lib import *
from anvil.lib import _JsonSchemes

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
    "LEGACYItemFood",
    "LEGACYItemUseDuration",
    "LEGACYItemStackedByData",
    "LEGACYItemFoil",
    "LEGACYItemHandEquipped",
]


# LEGACY COMPONENTS
class LEGACYItemHandEquipped(_component):
    component_namespace = "minecraft:hand_equipped"
    def __init__(self) -> None:
        super().__init__("hand_equipped")
        self._component_set_value(True)


class LEGACYItemFoil(_component):
    component_namespace = "minecraft:foil"
    def __init__(self) -> None:
        super().__init__("foil")
        self._component_set_value(True)


class LEGACYItemStackedByData(_component):
    component_namespace = "minecraft:stacked_by_data"
    def __init__(self) -> None:
        super().__init__("stacked_by_data")
        self._component_set_value(True)


class LEGACYItemUseDuration(_component):
    component_namespace = "minecraft:use_duration"
    def __init__(self, use_duration: Seconds) -> None:
        super().__init__("use_duration")
        self._component_set_value(clamp(use_duration, 0, inf))


class LEGACYItemFood(_component):
    component_namespace = "minecraft:food"
    def __init__(self, can_always_eat: bool = False) -> None:
        super().__init__("food")
        self._component_add_field("effects", [])
        if can_always_eat:
            self._component_add_field("can_always_eat", True)

    def nutrition(self, nutrition: int):
        self._component_add_field("nutrition", max(1, nutrition))
        return self

    def saturation_modifier(self, saturation_modifier: float):
        self._component_add_field("saturation_modifier", max(0, saturation_modifier))
        return self

    def cooldown(self, cooldown_time: Seconds, cooldown_type: str):
        self._component_add_field("cooldown_time", clamp(cooldown_time * 20, 1, inf))
        self._component_add_field("cooldown_type", cooldown_type)
        return self

    def effects(self, effect: Effects, chance: float, duration: Seconds, amplifier: int):
        self[self.component_namespace]["effects"].append(
            {
                "name": effect.value,
                "chance": clamp(chance, 0, 1),
                "duration": duration,
                "amplifier": clamp(amplifier, 0, 255),
            }
        )
        return self


# Require ITEM_SERVER_VERSION >= 1.20.10
class ItemCooldown(_component):
    component_namespace = "minecraft:cooldown"
    def __init__(self, category: str, duration: float) -> None:
        """Sets an items "Cool down" time. After using an item, it becomes unusable for the duration specified by the 'duration' setting of this component.

        Args:
            category (str): The type of cool down for this item.
            duration (float): The duration of time (in seconds) items with a matching category will spend cooling down before becoming usable again.
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
        self[self.component_namespace]["repair_items"].append(
            {"items": repair_items, "repair_amount": repair_amount}
        )
        return self


class ItemMaxStackSize(_component):
    component_namespace = "minecraft:max_stack_size"
    def __init__(self, stack_size: int) -> None:
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
        """
        super().__init__("block_placer")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("block", block)
        self._component_add_field("use_on", use_on)


class ItemRecord(_component):
    component_namespace = "minecraft:record"
    def __init__(
        self, sound_event: str, duration: float, comparator_signal: int = 1
    ) -> None:
        """Used by record items to play music.

        Args:
            sound_event (str): Set the placement block name for the planter item.
            duration (float): Duration of sound event in seconds float value.
            comparator_signal (int): Signal strength for comparator blocks to use from 1 - 13.
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
            charge_on_draw (bool, optional): Sets if the item is charged when drawn. Defaults to False.
            max_draw_duration (float, optional): How long can it be drawn before it will release automatically. Defaults to 0.0.
            scale_power_by_draw_duration (bool, optional): Scale the power by draw duration? When true, the longer you hold, the more power it will have when released.. Defaults to False.
        """
        super().__init__("shooter")
        self._enforce_version(ITEM_SERVER_VERSION, "1.20.10")

        self._component_add_field("ammunition", [])
        if charge_on_draw:
            self._component_add_field("charge_on_draw", charge_on_draw)
        if not max_draw_duration == 0.0:
            self._component_add_field("max_draw_duration", max_draw_duration)
        if scale_power_by_draw_duration:
            self._component_add_field(
                "scale_power_by_draw_duration", scale_power_by_draw_duration
            )
    
    def add_ammunition(self, ammunition: Identifier, search_inventory: bool = True, use_in_creative: bool = False, use_offhand: bool = False):
        self[self.component_namespace]['ammunition'].append({
            "item": ammunition,
            "search_inventory": search_inventory,
            "use_in_creative": use_in_creative,
            "use_offhand": use_offhand
        })
        return self


class ItemProjectile(_component):
    component_namespace = "minecraft:projectile"
    def __init__(
        self, projectile_entity: Identifier, minimum_critical_power: int
    ) -> None:
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
            self._component_add_field(
                "scale_power_by_draw_duration", scale_power_by_draw_duration
            )


# Components
# Require ITEM_SERVER_VERSION >= 1.19.80
class ItemDurability(_component):
    component_namespace = "minecraft:durability"
    def __init__(
        self, max_durability: int, damage_chance: int | tuple[int, int] = 100
    ) -> None:
        """Sets how much damage the item can take before breaking, and allows the item to be combined at an anvil, grindstone, or crafting table.

        Args:
            max_durability (int): Max durability is the amount of damage that this item can take before breaking. The minimum value for this parameter is 0.
            damage_chance (int, optional): Damage chance is the percentage chance of this item losing durability. Default is set at 100 to 100.. Defaults to 100.
        """
        super().__init__("durability")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._component_add_field("max_durability", max(0, max_durability))

        if damage_chance != 100:
            if type(damage_chance) is int:
                self._component_add_field("damage_chance", clamp(damage_chance, 0, 100))
            else:
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
        """
        super().__init__("display_name")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        if localize:
            key = (
                f'item.{ANVIL.NAMESPACE}:{display_name.lower().replace(" ", "_")}.name'
            )
            ANVIL.localize(key, display_name)
            self._component_add_field("value", key)
        else:
            self._component_add_field("value", display_name)


class ItemFuel(_component):
    component_namespace = "minecraft:fuel"
    def __init__(self, duration: float) -> None:
        """Allows this item to be used as fuel in a furnace to 'cook' other items.

        Args:
            duration (float): How long in seconds will this fuel cook items for. Minimum value: 0.05.
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
        """
        super().__init__("icon")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        ANVIL._item_texture.add_item(texture, "", texture)
        self._component_add_field("texture", texture)


# Items
class _ItemServerDescription(_MinecraftDescription):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._description["description"]["properties"] = {}

    @property
    def _export(self):
        return super()._export


class _ItemServer(AddonObject):
    _extensions = {0: ".item.json", 1: ".item.json"}

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(
            name,
            os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "items"),
        )
        self._name = name
        self._is_vanilla = is_vanilla
        self._server_item = _JsonSchemes.server_item()
        self._description = _ItemServerDescription(name, is_vanilla)
        self._components = _Components()

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    @property
    def queue(self):
        self._server_item["minecraft:item"].update(self.description._export)
        self._server_item["minecraft:item"]["components"].update(
            self._components._export()["components"]
        )
        self.content(self._server_item)
        super().queue()


# To be removed after 1.20.30
class _ItemClient(AddonObject):
    _extensions = {0: ".item.json", 1: ".item.json"}

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(
            name,
            os.path.join("resource_packs", f"RP_{ANVIL.PASCAL_PROJECT_NAME}", "items"),
        )
        self._name = name
        self._is_vanilla = is_vanilla
        self._client_item = _JsonSchemes.client_item()
        self._description = _MinecraftDescription(name, is_vanilla)

        key = f"item.{ANVIL.NAMESPACE}:{self._name}.name"
        ANVIL.localize(key, name.replace("_", " ").title())

        ANVIL._item_texture.add_item(name, "", name)

    @property
    def queue(self):
        self._client_item["minecraft:item"].update(self._description._export)
        self._client_item["minecraft:item"]["components"].update(
            {"minecraft:icon": self._name}
        )
        self.content(self._client_item)
        super().queue()


# ---------------------------


class Item:
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        self._name = name
        self._is_vanilla = is_vanilla
        self._server = _ItemServer(name, is_vanilla)
        self._client = _ItemClient(name, is_vanilla)

        self._namespace_format = "minecraft" if self._is_vanilla else ANVIL.NAMESPACE

    @property
    def Server(self):
        return self._server

    @property
    def Client(self):
        return self._client

    @property
    def identifier(self):
        return f"{self._namespace_format}:{self._name}"

    @property
    def queue(self):
        if ITEM_SERVER_VERSION <= "1.16.0":
            self.Client.queue
        self.Server.queue
