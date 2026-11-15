# Adding a Custom Entity

This tutorial walks you through creating a compact **Redstone Golem** entity with **Anvil**. It targets **Anvil beginners** who already understand Minecraft concepts. Each step explicitly marks what's **necessary** and what's **optional**.

Every snippet on this page is taken from a project that compiles. Component arguments are **keyword-only**: write `EntityHealth(value=20)`, not `EntityHealth(20)`.

---

## Define the Entity

```py title="entities/redstone_golem.py"
from anvil.api.actors.entity import Entity

# Namespace is inferred from anvilconfig; only provide the short name here.
def redstone_golem():
    entity = Entity("redstone_golem")
    return entity
```

!!! warning
    Declare an `Entity` with a **unique name** (e.g., `"redstone_golem"`). The namespace comes from **anvilconfig**.

!!! warning "Export rule"
    You **must** queue the entity later with `entity.queue(...)`. If you skip this, the framework **will not export** the entity.

---

## Client Description

```py title="client visuals"
from anvil.api.pbr.texture_set import TextureComponents

# Both names point to assets/bbmodels/redstone_golem.bbmodel and a texture inside it.
entity.client.description.add_geometry("redstone_golem")
entity.client.description.add_texture(
    blockbench="redstone_golem",
    component=TextureComponents(color="redstone_golem"),
)
```

!!! info "Blockbench references"
    The first argument of `description.add_geometry`, `description.texture` and `description.animation` names a **Blockbench file** under `assets/bbmodels`. The model identifier, texture names and animation names **inside that file** must match what you reference, or Anvil raises an error at build time.

!!! tip "PBR Support"
    Add PBR maps that are also stored in the Blockbench file: `TextureComponents(color="redstone_golem", normal="redstone_golem_normal", mer="redstone_golem_mer")`. See the [PBR guide](pbr.md).

!!! tip "Material defaults"
    Anvil adds a default material named `entity_alphatest`. Add others with `description.add_material(name, material)`.

!!! failure
    **Visuals are mandatory.** Without a geometry and a texture on the client description, nothing is renderable.

!!! question "What if I want an invisible entity?"
    Use `entity.client.description.set_dummy()` for a non‑rendered, logic‑only entity.

---

## Render Controller

```py title="render controller"
rc = entity.client.description.render_controller("default")
rc.set_geometry("redstone_golem")
rc.add_texture("redstone_golem")
```

!!! warning
    A render controller is **required** for the model to **appear in‑game**. The names you pass are the short names you registered on the description.

!!! note "Optional tuning"
    Per‑part visibility, hurt and on‑fire colors, texture arrays and more are covered in [Animating an entity](entity_animations.md).

---

## Server Components

```py title="server components"
from anvil.api.actors.components import (
    EntityAILookAtPlayer,
    EntityAIRandomStroll,
    EntityCollisionBox,
    EntityHealth,
    EntityJumpStatic,
    EntityMovement,
    EntityMovementBasic,
    EntityNavigationWalk,
    EntityPhysics,
    EntityPushableByEntity,
    EntityTypeFamily,
)

entity.server.components.add(
    EntityCollisionBox(width=0.9, height=1.5),
    EntityPhysics(has_collision=True, has_gravity=True),
    EntityPushableByEntity(),
    EntityHealth(value=20, max=20),
    EntityTypeFamily(family=["golem", "mob"]),
    EntityMovement(value=0.25),
    EntityMovementBasic(),
    EntityNavigationWalk(),
    EntityJumpStatic(),
    EntityAIRandomStroll(priority=3),
    EntityAILookAtPlayer(priority=4),
)
```

!!! note
    There are **no minimum required server components**. With none, the entity has **no attributes** (no collision, physics, etc.). Add components only for the behaviors you need. An option you leave out is omitted from the JSON, so the game default applies.

!!! tip "Walking needs four components"
    A mob only moves when it has a movement speed (`EntityMovement`), a movement type (`EntityMovementBasic`), a navigation (`EntityNavigationWalk`) and an AI goal that wants to go somewhere (`EntityAIRandomStroll`).

---

## Spawning

```py title="spawning"
entity.server.description.config(is_spawnable=False)
```

!!! note
    Entities are summonable (`/summon namespace:redstone_golem`) and spawnable (they get a spawn egg) by default. Use `config(...)` to change `is_summonable`, `is_spawnable`, `is_experimental`, `runtime_identifier` or `spawn_category`. Natural spawning is covered in [Spawn rules and loot](spawning_and_loot.md).

---

## Queue the Entity

```py title="finalize"
entity.queue("misc")
return entity
```

!!! success
    **Queuing is mandatory.** If you don't call `entity.queue(...)`, the framework **will not export** the entity.

!!! tip "Queue groups"
    The argument to `queue(...)` is an export **group**. Anvil places generated files under `<group>/`. Choose any grouping string that fits your project layout. Call `entity.set_display_name(name, spawn_egg_name)` before queuing to name the entity and its egg; otherwise the name is the identifier in title case.

---

## Full Example — Redstone Golem

```py title="entities/redstone_golem.py"
from anvil.api.actors.components import (
    EntityAILookAtPlayer,
    EntityAIRandomStroll,
    EntityCollisionBox,
    EntityHealth,
    EntityJumpStatic,
    EntityMovement,
    EntityMovementBasic,
    EntityNavigationWalk,
    EntityPhysics,
    EntityPushableByEntity,
    EntityTypeFamily,
)
from anvil.api.actors.entity import Entity
from anvil.api.pbr.texture_set import TextureComponents


def redstone_golem():
    entity = Entity("redstone_golem")

    # Client visuals (mandatory)
    entity.client.description.add_geometry("redstone_golem")
    entity.client.description.add_texture(
        blockbench="redstone_golem",
        component=TextureComponents(color="redstone_golem"),
    )

    # Render (mandatory)
    rc = entity.client.description.render_controller("default")
    rc.set_geometry("redstone_golem")
    rc.add_texture("redstone_golem")

    # Server (optional)
    entity.server.components.add(
        EntityCollisionBox(width=0.9, height=1.5),
        EntityPhysics(has_collision=True, has_gravity=True),
        EntityPushableByEntity(),
        EntityHealth(value=20, max=20),
        EntityTypeFamily(family=["golem", "mob"]),
        EntityMovement(value=0.25),
        EntityMovementBasic(),
        EntityNavigationWalk(),
        EntityJumpStatic(),
        EntityAIRandomStroll(priority=3),
        EntityAILookAtPlayer(priority=4),
    )

    entity.server.description.config(is_spawnable=False)

    # Finalize (mandatory)
    entity.queue("misc")
    return entity


RedstoneGolem = redstone_golem()
```

---

## Advanced Features

### Component Groups and Events

Component groups hold components that are only active after an event adds them. Events add and remove groups, trigger other events, run commands and more.

```py title="component groups and events"
from anvil.api.actors.components import EntityHealth, EntityScale

# 1. Define component groups
entity.server.component_group("phase_1").add(EntityScale(value=1.0))
entity.server.component_group("phase_2").add(
    EntityScale(value=1.5), EntityHealth(value=100, max=100)
)

# 2. Define the transition event. Each `sequence` call adds one step.
phase_transition = entity.server.event("transform_to_phase_2")
phase_transition.add_sequence().add_component_groups(["phase_2"]).remove_component_groups(["phase_1"])
phase_transition.add_sequence().set_trigger("restore_health")

# 3. Run commands from an event
entity.server.event("restore_health").add_queue_command(["effect @s regeneration 5"])

# 4. Built-in events have their vanilla names
entity.server.event("minecraft:entity_spawned").add_component_groups(["phase_1"])
```

The event above exports as:

```json
"transform_to_phase_2": {
  "sequence": [
    {"add": {"component_groups": ["phase_2"]}, "remove": {"component_groups": ["phase_1"]}},
    {"trigger": "restore_health"}
  ]
}
```

!!! note
    Calling `entity.server.event(name)` twice returns the **same** event, so you can add to it from several places. Use `event.add_randomize().set_weight(3).add_component_groups([...])` for weighted random picks, and `entry.set_filters(Filter...)` to make a sequence step conditional.

### Related Systems

- [Animating an entity](entity_animations.md): animations, animation controllers, render controller arrays.
- [Spawn rules and loot](spawning_and_loot.md): natural spawning and drops.
- [Particles and sounds](particles_and_sounds.md): effects on the client side.
- [Trade Tables](trade_tables.md) and [NPC dialogues](dialogues.md).
