from typing import Dict

from ..core import (ANVIL, NAMESPACE, NAMESPACE_FORMAT, PASCAL_PROJECT_NAME,
                    AddonObject, _MinecraftDescription)
from ..packages import *
from .actors import _Components
from .components import _component

#Components
class ItemDurability(_component):
    def __init__(self, max_durability: int, damage_chance: int = 100) -> None:
        """Sets how much damage the item can take before breaking."""
        super().__init__('durability')
        self._component_add_field('max_durability', max_durability)

        if damage_chance != 100:
            self._component_add_field('damage_chance', clamp(damage_chance, 0, 100))


class ItemDisplayName(_component):
    def __init__(self, display_name: str) -> None:
        """This component is specified as a Localization String. If this component is omitted, the default value for this component is the name of the item."""
        super().__init__('display_name')
        self._component_add_field('value', display_name)


class ItemFuel(_component):
    def __init__(self, duration: float) -> None:
        """Allows this item to be used as fuel in a furnace to 'cook' other items."""
        super().__init__('fuel')
        self._component_add_field('duration', clamp(duration, 0.05, inf))


class ItemEntityPlacer(_component):
    def __init__(self, entity: str) -> None:
        """Sets the item as a Planter item component for Entities. Planter items are items that can be planted into another block."""
        super().__init__('entity_placer')
        self._component_add_field('entity', entity)

    def dispense_on(self, *blocks: str):
        self._component_add_field('dispense_on', blocks)
        return self

    def use_on(self, *blocks: str):
        self._component_add_field('use_on', blocks)
        return self


class ItemIcon(_component):
    def __init__(self, texture: str, legacy_id: int = 0) -> None:
        """Sets the icon item component. Determines the icon to represent the item in the UI and elsewhere."""
        super().__init__('icon')
        self._component_add_field('texture', texture)
        if legacy_id > 0:
            self._component_add_field('legacy_id', legacy_id)

# Items
class _ItemServerDescription(_MinecraftDescription):
    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier, is_vanilla)
        self._description['description'].update({
            'properties': {},
        })

    @property
    def _export(self):
        return super()._export


class _ItemServer(AddonObject):
    _extensions = {
        0: ".item.json", 
        1: ".item.json"
    }
    
    def __init__(self, identifier: str, is_vanilla: bool) -> None:
        super().__init__(identifier, MakePath("behavior_packs", f"BP_{PASCAL_PROJECT_NAME}", "items"))
        self._identifier = identifier
        self._server_item = Schemes('server_item')
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
        self._server_item['minecraft:item'].update(self.description._export)
        self._server_item['minecraft:item']['components'].update(self._components._export()['components'])
        self.content(self._server_item)
        super().queue()


class Item():
    def _validate_name(self, identifier):
        if ':' in identifier:
            raise ValueError(NAMESPACES_NOT_ALLOWED(identifier))

    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._validate_name(identifier)

        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._server = _ItemServer(identifier, is_vanilla)

        self._namespace_format = NAMESPACE_FORMAT
        if self._is_vanilla:
            self._namespace_format = 'minecraft'

    @property
    def Server(self):
        return self._server

    @property
    def identifier(self):
        return f'{self._namespace_format}:{self._identifier}'

    @property
    def queue(self):
        display_name = RawText(self._identifier)[1]
        ANVIL.localize(f'item.{NAMESPACE_FORMAT}:{self._identifier}.name={display_name}')
        ANVIL._items.update({f'{self._namespace_format}:{self._identifier}': {"Display Name": display_name}})
        self.Server.queue
