# NPC Dialogues

This tutorial creates a **Tinker** NPC with a two-scene **dialogue**: a greeting and a trade screen. Dialogues are behaviour-pack files opened on an NPC entity with the `/dialogue` command; every string becomes a localization key.

Every snippet compiles as written.

---

## The Dialogue

```py title="npc/tinker.py"
from anvil.api.world.dialogue import Dialogue


def tinker_dialogue():
    dialogue = Dialogue("tinker")

    welcome = dialogue.add_scene("welcome")
    welcome.properties("Tinker", "Need a lantern? I trade brass for ember dust.")
    welcome.button("Trade", ["/dialogue open @s @initiator tut:tinker_trade"])
    welcome.button("Not now", ["/dialogue close @initiator"])
    welcome.set_on_open_commands(["/playsound note.chime @initiator"])

    trade = dialogue.add_scene("tinker_trade")
    trade.properties("Tinker", "Four ember dust for one brass lantern.")
    trade.button(
        "Deal",
        [
            "/clear @initiator tut:ember_dust 0 4",
            "/give @initiator tut:brass_lantern",
            "/dialogue open @s @initiator tut:welcome",
        ],
    )
    trade.button("Back", ["/dialogue open @s @initiator tut:welcome"])
    return dialogue.queue()
```

The scene tags get the project namespace, so commands refer to them as `tut:welcome`. The exported scene:

```json
{
  "scene_tag": "tut:welcome",
  "npc_name": {"rawtext": [{"translate": "dialogue.tut:tutorial.npc_name.tinker"}]},
  "text": {"rawtext": [{"translate": "dialogue.tut:tutorial.text.need_a_lantern_i_trade_brass_for_ember_dust"}]},
  "on_open_commands": ["/playsound note.chime @initiator"],
  "buttons": [
    {"name": {"rawtext": [{"translate": "dialogue.tut:tutorial.button.trade"}]}, "commands": ["/dialogue open @s @initiator tut:tinker_trade"]},
    {"name": {"rawtext": [{"translate": "dialogue.tut:tutorial.button.not_now"}]}, "commands": ["/dialogue close @initiator"]}
  ]
}
```

- `scene.properties(npc_name, text)` sets the title and the body.
- `scene.button(name, commands)` adds up to six buttons.
- `set_on_open_commands` and `set_on_close_commands` run when the scene is shown or dismissed.

!!! tip
    `@initiator` is the player who opened the dialogue and `@s` the NPC. Keep the scene names unique across the whole pack.

---

## The NPC

An entity shows dialogues when it has the `EntityNPC` component. Everything else is a normal entity.

```py title="npc entity"
from anvil.api.actors.components import (
    EntityAILookAtPlayer,
    EntityCollisionBox,
    EntityHealth,
    EntityKnockbackResistance,
    EntityNPC,
    EntityPersistent,
    EntityPhysics,
    EntityTypeFamily,
)
from anvil.api.actors.entity import Entity
from anvil.api.pbr.texture_set import TextureComponents


def tinker():
    entity = Entity("tinker")
    client = entity.client.description
    client.add_geometry("tinker")
    client.add_texture("tinker", TextureComponents(color="tinker"))
    client.render_controller("default").set_geometry("tinker").add_texture("tinker")

    entity.server.components.add(
        EntityCollisionBox(width=0.6, height=1.9),
        EntityPhysics(has_collision=True, has_gravity=True),
        EntityHealth(value=20, max=20),
        EntityKnockbackResistance(value=1),
        EntityTypeFamily(family=["npc", "tinker"]),
        EntityPersistent(),
        EntityNPC().set_npc_data(skin_list=[0]),
        EntityAILookAtPlayer(priority=1, look_distance=8),
    )
    entity.server.description.config(is_spawnable=False)
    entity.server.event("minecraft:entity_spawned").add_queue_command(
        ["dialogue change @s tut:welcome"]
    )

    tinker_dialogue()
    entity.queue("npc")
    return entity


Tinker = tinker()
```

!!! note
    `EntityNPC` needs its `npc_data`; `set_npc_data(skin_list=[0])` is the minimum. The spawn event binds the default scene with `dialogue change`, so right-clicking the NPC opens it without a command block.

!!! tip "Trading instead of talking"
    For a villager-style trade screen use a [trade table](trade_tables.md) with `EntityEconomyTradeTable` rather than a dialogue.
