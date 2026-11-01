from anvil.api.core.components import EventTrigger
from anvil.api.core.enums import DamageCause
from anvil.api.core.filters import Filter
from anvil.lib.jsonmodel import JsonComponent
from anvil.lib.jsonmodel.validators import (
    all_of,
    each,
    in_range,
    instance_of,
    length,
    one_of,
    one_or_many,
    subclass_of,
)
from anvil.lib.schemas import (
    MinecraftBlockDescriptor,
    MinecraftEntityDescriptor,
    MinecraftItemDescriptor,
)

# region Validators

_boolean = instance_of(bool)
_string = instance_of(str)
_number = instance_of(int, float)
_integer = instance_of(int)
_positive = in_range(minimum=0)
_chance = in_range(0.0, 1.0)
_molang = instance_of(str, int, float)
_item = instance_of(str, MinecraftItemDescriptor)
_items = each(_item)
_block = instance_of(str, MinecraftBlockDescriptor)
_blocks = each(_block)
_filter = instance_of(Filter)
_event = instance_of(EventTrigger, str)
_entity = instance_of(str, MinecraftEntityDescriptor)
_damage_cause = one_of(*DamageCause)
_entity_pair = all_of(length(2, 2), each(_entity))
_component_class = subclass_of(JsonComponent)
_events = one_or_many(_event)

# endregion
