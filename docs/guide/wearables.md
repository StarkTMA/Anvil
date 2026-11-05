# Wearables and Attachables

This tutorial makes an **Iron Crown**: a helmet item with durability, enchantability and repair, rendered on the player's head by an **attachable**. The attachable is the item's client and uses the same API as an entity client.

Every snippet compiles as written.

---

## The Item

```py title="items/iron_crown.py"
from anvil.lib.jsonmodel.enums import EnchantsSlots, ItemCategory, ItemGroups, Slots
from anvil.api.items.components import (
    ItemDurability,
    ItemEnchantable,
    ItemIcon,
    ItemRarity,
    ItemRepairable,
    ItemWearable,
)
from anvil.api.items.items import Item
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.items import MinecraftItemTypes

item = Item("iron_crown")
item.server.description.set_menu_category(ItemCategory.Equipment, ItemGroups.Helmet)
item.server.components.add(
    ItemIcon(textures=TextureComponents(color="iron_crown")),
    ItemWearable(slot=Slots.Head, protection=2),
    ItemDurability(max_durability=180),
    ItemEnchantable(slot=EnchantsSlots.ArmorHead, value=10),
    ItemRepairable().add_repair_item(
        items=[MinecraftItemTypes.IronIngot()],
        repair_amount="context.other->query.remaining_durability + 45",
    ),
    ItemRarity(value="rare"),
)
```

```json
"components": {
  "minecraft:icon": {"textures": {"default": "tut:iron_crown"}},
  "minecraft:wearable": {"slot": "slot.armor.head", "protection": 2},
  "minecraft:durability": {"max_durability": 180},
  "minecraft:enchantable": {"slot": "armor_head", "value": 10},
  "minecraft:repairable": {"repair_items": [{"items": ["minecraft:iron_ingot"], "repair_amount": "context.other->query.remaining_durability + 45"}]},
  "minecraft:rarity": "rare",
  "minecraft:display_name": {"value": "item.tut:iron_crown.name"}
}
```

- `ItemWearable(slot=Slots.Head)` makes the item equippable; `Slots.Chest`, `Slots.Legs`, `Slots.Feet`, `Slots.Body` and `Slots.Offhand` are the others. `protection` is the armor value.
- `ItemEnchantable` uses the enchantment slot names (`EnchantsSlots.ArmorHead`, `Sword`, `Bow`...).
- `repair_amount` can be a number or Molang.

---

## The Attachable

```py title="attachable"
client = item.client.description
client.add_geometry("iron_crown")
client.add_texture("iron_crown", TextureComponents(color="iron_crown"))
client.animation("iron_crown", "offset", animate=True)
client.render_controller("default").set_geometry("iron_crown").add_texture(
    "iron_crown"
)

item.queue()
```

```json
"minecraft:attachable": {
  "description": {
    "identifier": "tut:iron_crown",
    "materials": {"default": "entity_alphatest"},
    "textures": {"iron_crown": "textures/tut/tutorial/actors/iron_crown/iron_crown"},
    "geometry": {"iron_crown": "geometry.tut.iron_crown"},
    "animations": {"offset": "animation.tut.iron_crown.offset"},
    "scripts": {"animate": ["offset"]},
    "render_controllers": ["controller.render.tut.iron_crown.default"]
  }
}
```

!!! info "Model and animation"
    Build the crown in Blockbench on the player's `head` bone, so it follows the head. The `offset` animation is how the model is positioned when worn; it is also where first-person and third-person differences go, with `Query.IsFirstPerson()` conditions, as in [Adding a Custom Item](adding_item.md).

!!! tip "Hiding the vanilla armor"
    When the attachable replaces an armor piece, add a material such as `client.add_material("default", "armor")` and use the vanilla `armor` render controller behaviour: `client.render_controller("default").set_geometry(...)` with part visibility tied to `Query.IsItemNameAny(...)`.

---

## Full Example — Iron Crown

```py title="items/iron_crown.py"
from anvil.lib.jsonmodel.enums import EnchantsSlots, ItemCategory, ItemGroups, Slots
from anvil.api.items.components import (
    ItemDurability,
    ItemEnchantable,
    ItemIcon,
    ItemRarity,
    ItemRepairable,
    ItemWearable,
)
from anvil.api.items.items import Item
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.items import MinecraftItemTypes


def iron_crown():
    item = Item("iron_crown")
    item.server.description.set_menu_category(ItemCategory.Equipment, ItemGroups.Helmet)
    item.server.components.add(
        ItemIcon(textures=TextureComponents(color="iron_crown")),
        ItemWearable(slot=Slots.Head, protection=2),
        ItemDurability(max_durability=180),
        ItemEnchantable(slot=EnchantsSlots.ArmorHead, value=10),
        ItemRepairable().add_repair_item(
            items=[MinecraftItemTypes.IronIngot()],
            repair_amount="context.other->query.remaining_durability + 45",
        ),
        ItemRarity(value="rare"),
    )

    client = item.client.description
    client.add_geometry("iron_crown")
    client.add_texture("iron_crown", TextureComponents(color="iron_crown"))
    client.animation("iron_crown", "offset", animate=True)
    client.render_controller("default").set_geometry("iron_crown").add_texture(
        "iron_crown"
    )

    item.queue()
    return item


IronCrown = iron_crown()
```
