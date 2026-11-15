# Animating an Entity

This tutorial builds a **Clockwork Golem** that idles, walks, attacks and rusts over time. It covers the four moving parts of an animated entity in Anvil: **animations** from Blockbench, **client animation controllers**, **render controller arrays**, and **server-side animations and controllers** that run commands. Read [Adding a Custom Entity](adding_entity.md) first.

The whole example compiles as written. Every name passed to `client.animation(...)` must exist in `assets/bbmodels/clockwork_golem.bbmodel`.

---

## Register Animations From Blockbench

```py title="entities/clockwork_golem.py"
from anvil.api.actors.entity import Entity
from anvil.api.pbr.texture_set import TextureComponents

entity = Entity("clockwork_golem")
client = entity.client.description
server = entity.server

client.add_geometry("clockwork_golem")
client.add_texture("clockwork_golem", TextureComponents(color="clockwork_golem"))
client.add_texture("clockwork_golem", TextureComponents(color="clockwork_golem_rusted"))

client.animation("clockwork_golem", "idle")
client.animation("clockwork_golem", "walk")
client.animation("clockwork_golem", "attack")
```

`client.animation(blockbench, animation_name)` exports the animation from the Blockbench file and registers it on the client entity under its short name. Pass `animate=True` to play it unconditionally, or `condition=` with a Molang expression to play it while the expression is true. Animations driven by a controller need neither.

!!! info "Two textures, one file"
    Both textures live in the same `.bbmodel`. Each `client.texture` call registers one of them under the name it has in Blockbench.

---

## Client Animation Controller

A controller is a state machine. Each state plays animations and lists the transitions out of it, checked in order.

```py title="movement controller"
from anvil.api.logic.molang import Query

controller = client.animation_controller("movement", animate=True)
controller.add_state("default").animation("idle").transition(
    "walking", Query.GroundSpeed() > 0.1
).transition("attacking", Query.IsDelayedAttacking())
controller.add_state("walking").animation("walk").transition(
    "default", Query.GroundSpeed() < 0.1
).transition("attacking", Query.IsDelayedAttacking()).set_blend_transition(0.2)
controller.add_state("attacking").animation("attack").transition(
    "default", Query.AllAnimationsFinished()
).sound_effect("gear_clank")

client.sound_effect("gear_clank").add_sound("golem/hurt", pitch=0.7)
```

This exports to `animation_controllers/<group>/clockwork_golem.rp_ac.json`:

```json
"controller.animation.tut.clockwork_golem.movement": {
  "initial_state": "default",
  "states": {
    "default": {
      "animations": ["idle"],
      "transitions": [{"walking": "(q.ground_speed > 0.1)"}, {"attacking": "q.is_delayed_attacking"}]
    },
    "walking": {
      "animations": ["walk"],
      "transitions": [{"default": "(q.ground_speed < 0.1)"}, {"attacking": "q.is_delayed_attacking"}],
      "blend_transition": 0.2
    },
    "attacking": {
      "animations": ["attack"],
      "transitions": [{"default": "q.all_animations_finished"}],
      "sound_effects": [{"effect": "gear_clank", "locator": "root"}]
    }
  }
}
```

!!! tip "Molang in Python"
    `Query.GroundSpeed() > 0.1` builds the string `(q.ground_speed > 0.1)`. Comparison, `&`, `|` and `~` (not) all work on `Query`, `Variable` and `Math` expressions, so conditions stay readable and typo-free.

!!! note "Sounds and particles in states"
    `state.sound_effect(name)` and `state.particle(effect, locator)` play when the state is entered. `client.sound_effect(name)` registers the short name on the entity and returns its sound definition, so you can add the `.ogg` files from `assets/sounds` in the same line. See [Particles and sounds](particles_and_sounds.md).

---

## Render Controller Arrays

The render controller chooses geometry, textures and materials at render time. Arrays let a Molang expression pick an entry.

```py title="render controller"
rc = client.render_controller("default")
rc.set_geometry("clockwork_golem")
rc.texture_array(
    "skins", ["clockwork_golem", "clockwork_golem_rusted"], Query.Variant()
)
rc.add_part_visibility("crown", Query.Variant() == 1)
rc.set_is_hurt_color(0.5, 1, 0.2, 0.2)
```

```json
"controller.render.tut.clockwork_golem.default": {
  "arrays": {"textures": {"array.skins": ["Texture.clockwork_golem", "Texture.clockwork_golem_rusted"]}},
  "geometry": "Geometry.clockwork_golem",
  "textures": ["array.skins[q.variant]"],
  "part_visibility": [{"crown": "(q.variant == 1)"}],
  "is_hurt_color": {"r": 1, "g": 0.2, "b": 0.2, "a": 0.5},
  "materials": [{"*": "material.default"}]
}
```

!!! note
    `add_part_visibility(bone, condition)` toggles a bone of the model. `geometry_array` and `material_array` work like `texture_array`. `set_on_fire_color`, `set_overlay_color`, `set_ignore_lighting()` and `set_uv_anim(...)` are the other common tweaks.

---

## Server Components for the Behaviour

The golem fights monsters, so the attack animation has something to react to. `EntityAIDelayedAttack` is what makes `Query.IsDelayedAttacking()` true.

```py title="server components"
from anvil.api.actors.components import (
    EntityAIDelayedAttack,
    EntityAIHurtByTarget,
    EntityAILookAtPlayer,
    EntityAINearestAttackableTarget,
    EntityAIRandomStroll,
    EntityAttack,
    EntityCollisionBox,
    EntityHealth,
    EntityJumpStatic,
    EntityMovement,
    EntityMovementBasic,
    EntityNavigationWalk,
    EntityPhysics,
    EntityVariant,
)
from anvil.api.actors.components.ai_goals import GoalEntityType
from anvil.api.core.filters import Filter

server.components.add(
    EntityCollisionBox(width=1.0, height=1.8),
    EntityPhysics(has_collision=True, has_gravity=True),
    EntityHealth(value=40, max=40),
    EntityMovement(value=0.2),
    EntityMovementBasic(),
    EntityNavigationWalk(can_path_over_water=True),
    EntityJumpStatic(),
    EntityAttack(damage=5),
    EntityAIDelayedAttack(priority=2, attack_duration=0.75, hit_delay_pct=0.5),
    EntityAIHurtByTarget(priority=1),
    EntityAINearestAttackableTarget(
        priority=3,
        must_see=True,
        entity_types=[GoalEntityType(filters=Filter.is_family("monster"), max_dist=16)],
    ),
    EntityAIRandomStroll(priority=5),
    EntityAILookAtPlayer(priority=6),
)

server.component_group("rusted").add(EntityVariant(value=1))
server.event("rust").add_component_groups(["rusted"])
```

!!! tip "Nested parts"
    Components with lists of structured entries take small objects, such as `GoalEntityType`, or have an `add_` builder for them (`EntityDamageSensor().add_trigger(...)`). Filters come from `anvil.api.core.filters.Filter`; combine them with `Filter.all_of([...])` and `Filter.any_of([...])`.

---

## Server Animations and Controllers

Behaviour-pack animations run **commands** on a timeline. Behaviour-pack controllers run commands when a state is entered or left.

```py title="server animations"
wind_down = server.description.animation("wind_down", loop=False)
wind_down.set_animation_length(3)
wind_down.add_timeline(0, ["playsound random.click @a[r=8]"])
wind_down.add_timeline(2.5, ["event entity @s rust"])

guard = server.description.animation_controller("guard", animate=True)
guard.add_state("default").transition("alert", Query.HasTarget())
guard.add_state("alert").add_on_entry("playsound note.bell @a[r=16]").transition(
    "default", ~Query.HasTarget()
)

entity.queue("golems")
```

```json
"animation.tut.clockwork_golem.wind_down": {
  "loop": false,
  "animation_length": 3,
  "timeline": {"0": ["/playsound random.click @a[r=8]"], "2.5": ["/event entity @s rust"]}
}
```

!!! note "Playing a server animation"
    `server.description.animation(name, animate=True)` plays it from spawn. With `animate=False` (the default) it is only registered, and a controller state or an event can start it: add `state.animation("wind_down")` to a behaviour-pack controller state.

---

## Full Example — Clockwork Golem

```py title="entities/clockwork_golem.py"
from anvil.api.actors.components import (
    EntityAIDelayedAttack,
    EntityAIHurtByTarget,
    EntityAILookAtPlayer,
    EntityAINearestAttackableTarget,
    EntityAIRandomStroll,
    EntityAttack,
    EntityCollisionBox,
    EntityHealth,
    EntityJumpStatic,
    EntityMovement,
    EntityMovementBasic,
    EntityNavigationWalk,
    EntityPhysics,
    EntityVariant,
)
from anvil.api.actors.components.ai_goals import GoalEntityType
from anvil.api.actors.entity import Entity
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents


def clockwork_golem():
    entity = Entity("clockwork_golem")
    client = entity.client.description
    server = entity.server

    client.add_geometry("clockwork_golem")
    client.add_texture("clockwork_golem", TextureComponents(color="clockwork_golem"))
    client.add_texture("clockwork_golem", TextureComponents(color="clockwork_golem_rusted"))

    client.animation("clockwork_golem", "idle")
    client.animation("clockwork_golem", "walk")
    client.animation("clockwork_golem", "attack")

    controller = client.animation_controller("movement", animate=True)
    controller.add_state("default").animation("idle").transition(
        "walking", Query.GroundSpeed() > 0.1
    ).transition("attacking", Query.IsDelayedAttacking())
    controller.add_state("walking").animation("walk").transition(
        "default", Query.GroundSpeed() < 0.1
    ).transition("attacking", Query.IsDelayedAttacking()).set_blend_transition(0.2)
    controller.add_state("attacking").animation("attack").transition(
        "default", Query.AllAnimationsFinished()
    ).sound_effect("gear_clank")

    client.sound_effect("gear_clank").add_sound("golem/hurt", pitch=0.7)

    rc = client.render_controller("default")
    rc.set_geometry("clockwork_golem")
    rc.texture_array(
        "skins", ["clockwork_golem", "clockwork_golem_rusted"], Query.Variant()
    )
    rc.add_part_visibility("crown", Query.Variant() == 1)
    rc.set_is_hurt_color(0.5, 1, 0.2, 0.2)

    server.components.add(
        EntityCollisionBox(width=1.0, height=1.8),
        EntityPhysics(has_collision=True, has_gravity=True),
        EntityHealth(value=40, max=40),
        EntityMovement(value=0.2),
        EntityMovementBasic(),
        EntityNavigationWalk(can_path_over_water=True),
        EntityJumpStatic(),
        EntityAttack(damage=5),
        EntityAIDelayedAttack(priority=2, attack_duration=0.75, hit_delay_pct=0.5),
        EntityAIHurtByTarget(priority=1),
        EntityAINearestAttackableTarget(
            priority=3,
            must_see=True,
            entity_types=[GoalEntityType(filters=Filter.is_family("monster"), max_dist=16)],
        ),
        EntityAIRandomStroll(priority=5),
        EntityAILookAtPlayer(priority=6),
    )

    server.component_group("rusted").add(EntityVariant(value=1))
    server.event("rust").add_component_groups(["rusted"])

    wind_down = server.description.animation("wind_down", loop=False)
    wind_down.set_animation_length(3)
    wind_down.add_timeline(0, ["playsound random.click @a[r=8]"])
    wind_down.add_timeline(2.5, ["event entity @s rust"])

    guard = server.description.animation_controller("guard", animate=True)
    guard.add_state("default").transition("alert", Query.HasTarget())
    guard.add_state("alert").add_on_entry("playsound note.bell @a[r=16]").transition(
        "default", ~Query.HasTarget()
    )

    entity.queue("golems")
    return entity


ClockworkGolem = clockwork_golem()
```
