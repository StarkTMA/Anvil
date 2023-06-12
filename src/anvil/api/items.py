from ..core import ANVIL, AddonObject, _MinecraftDescription
from ..lib import *
from ..lib import _JsonSchemes
from .actors import _Components
from .components import _component


# LEGACY COMPONENTS
class LEGACYItemHandEquipped(_component):
    def __init__(self) -> None:
        super().__init__("hand_equipped")
        self._component_set_value(True)


class LEGACYItemFoil(_component):
    def __init__(self) -> None:
        super().__init__("foil")
        self._component_set_value(True)


class LEGACYItemStackedByData(_component):
    def __init__(self) -> None:
        super().__init__("stacked_by_data")
        self._component_set_value(True)


class LEGACYItemMaxStackSize(_component):
    def __init__(self, stack_size: int) -> None:
        super().__init__("max_stack_size")
        self._component_set_value(clamp(stack_size, 1, 64))


class LEGACYItemUseDuration(_component):
    def __init__(self, use_duration: Seconds) -> None:
        super().__init__("use_duration")
        self._component_set_value(clamp(use_duration, 0, inf))


class LEGACYItemFood(_component):
    def __init__(self, can_always_eat: bool = False) -> None:
        super().__init__("use_duration")
        self._component_add_field("effects", [])
        if can_always_eat:
            self._component_add_field("can_always_eat", True)

    def nutrition(self, nutrition: int):
        self._component_add_field("nutrition", max(1, nutrition))

    def saturation_modifier(self, saturation_modifier: float):
        self._component_add_field("saturation_modifier", max(0, saturation_modifier))

    def cooldown(self, cooldown_time: Seconds, cooldown_type: str):
        self._component_add_field("cooldown_time", clamp(cooldown_time, 1, inf))
        self._component_add_field("cooldown_type", cooldown_type)

    def effects(self, effect: Effects, chance: float, duration: Seconds, amplifier):
        self[self._component_namespace]["effects"].append(
            {
                "name": effect,
                "chance": clamp(chance, 0, 1),
                "duration": duration,
                "amplifier": amplifier,
            }
        )


# Components
class ItemDisplayName(_component):
    def __init__(self, display_name: str, localize: bool = True) -> None:
        """Sets the item display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Args:
            display_name (str): Set the display name for an item.
            localize (bool, optional): Whether to use the name with a localization file or not. Defaults to True.
        """
        super().__init__("display_name")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        if localize:
            key = f'item.{display_name.lower().replace(" ", "_")}.name'
            ANVIL.localize(key, display_name)
            self._component_add_field("value", key)
        else:
            self._component_add_field("value", display_name)


class ItemDurability(_component):
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


class ItemEntityPlacer(_component):
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


class ItemFuel(_component):
    def __init__(self, duration: float) -> None:
        """Allows this item to be used as fuel in a furnace to 'cook' other items.

        Args:
            duration (float): How long in seconds will this fuel cook items for. Minimum value: 0.05.
        """
        super().__init__("fuel")
        self._enforce_version(ITEM_SERVER_VERSION, "1.19.80")
        self._component_add_field("duration", clamp(duration, 0.05, inf))


class ItemIcon(_component):
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
    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier, is_vanilla)
        self._description["description"]["properties"] = {}

    @property
    def _export(self):
        return super()._export


class _ItemServer(AddonObject):
    _extensions = {0: ".item.json", 1: ".item.json"}

    def __init__(self, identifier: str, is_vanilla: bool) -> None:
        super().__init__(
            identifier,
            os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "items"),
        )
        self._identifier = identifier
        self._server_item = _JsonSchemes.server_item()
        self._description = _ItemServerDescription(identifier, is_vanilla)
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


class Item:
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._server = _ItemServer(identifier, is_vanilla)

        self._namespace_format = (
            "minecraft" if self._is_vanilla else ANVIL.NAMESPACE_FORMAT
        )

    @property
    def Server(self):
        return self._server

    @property
    def identifier(self):
        return f"{self._namespace_format}:{self._identifier}"

    @property
    def queue(self):
        display_name = self._identifier.replace("_", " ").title()
        ANVIL.localize(
            f"item.{self._namespace_format}:{self._identifier}.name", display_name
        )
        self.Server.queue
