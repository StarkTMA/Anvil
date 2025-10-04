# Adding a Custom Entity

This tutorial walks you through creating a compact **Redstone Golem** entity with **Anvil**. It targets **Anvil beginners** who already understand Minecraft concepts. Each step explicitly marks what's **necessary** and what's **optional**.

---

## Define the Entity

```py title="entities/redstone_golem.py"
from anvil.api.actors.actors import Entity

# Namespace is inferred from your anvilconfig; only provide the short name here.
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
# These identifiers must exist in your Blockbench asset and match internal names.
entity.client.description.geometry(entity.name)
entity.client.description.texture(entity.name, "redstone_golem")
```

!!! info "Blockbench references"
The first argument in `description.geometry`, `description.texture`, and `description.animation` points to a **Blockbench file** under `assets/blockbench`. The **geometry/texture names inside that file must match what's being referenced** or Anvil raises an error.

!!! tip "Material defaults"
Anvil automatically adds a default material named `entity_alphatest`. You can define additional materials as needed.

!!! failure
**Visuals are mandatory.** Without a geometry + texture defined on the client description, nothing is renderable and the export is skipped.

!!! question "What if I want an invisible entity?"
Use `entity.client.description.dummy()` for a non‑rendered, logic‑only entity.

![Redstone Golem Blockbench preview](/assets/redstone_golem_blockbench.png)

---

## Render Controller

```py title="render controller"
rc = entity.client.description.render_controller("default")
rc.geometry(entity.name)
rc.textures("redstone_golem")
```

!!! warning
A render controller is **required** for the model to **appear in‑game**.

!!! note "Optional tuning"
You can later add per‑part visibility, hurt/on‑fire colors, or other visual tweaks. These are **optional**.

---

## Server Components

```py title="server components"
from anvil.api.actors.components import (
    EntityCollisionBox,
    EntityPhysics,
    EntityPushable,
    EntityHealth,
)

entity.server.components.add(
    EntityCollisionBox(1.5, 0.9),   # compact golem hitbox
    EntityPhysics(True, True),      # affected by gravity + can move
    EntityPushable(True, True),     # can push/be pushed
    EntityHealth(20, 20),           # 20 HP (10 hearts)
)
```

!!! note
There are **no minimum required server components**. With none, the entity has **no attributes** (no collision, physics, etc.). Add components only for the behaviors you need.

![Hitbox diagram placeholder](/assets/redstone_golem_hitbox.png)

---

## Summonable

```py title="summoning"
entity.server.description.Summonable
```

!!! note
Marking the entity **Summonable** lets you it with commands `/summon namespace:redstone_golem`.

---

## Queue the Entity

```py title="finalize"
entity.queue("misc")
return entity
```

!!! success
**Queuing is mandatory.** If you don't call `entity.queue(...)`, the framework will **not export** the entity.

!!! tip "Queue groups"
The argument to `queue(...)` is an export **group**. Anvil places generated files under `<group>/`. Choose any grouping string that fits your project layout.

---

## Full Example — Redstone Golem

```py title="entities/redstone_golem.py"
from anvil.api.actors.actors import Entity
from anvil.api.actors.components import (
    EntityCollisionBox,
    EntityPhysics,
    EntityPushable,
    EntityHealth,
)


def redstone_golem():
    entity = Entity("redstone_golem")

    # Client visuals (mandatory)
    entity.client.description.geometry(entity.name)
    entity.client.description.texture(entity.name, "redstone_golem")

    # Render (mandatory)
    rc = entity.client.description.render_controller("default")
    rc.geometry(entity.name)
    rc.textures("redstone_golem")

    # Server (optional)
    entity.server.description.Summonable
    entity.server.components.add(
        EntityCollisionBox(1.5, 0.9),
        EntityPhysics(True, True),
        EntityPushable(True, True),
        EntityHealth(20, 20),
    )

    # Finalize (mandatory)
    entity.queue("misc")
    return entity


RedstoneGolem = redstone_golem()
```

---
