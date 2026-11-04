# Particles and Sounds

This tutorial adds a particle burst and sounds to the **Ember Moth** from [Spawn rules and loot](spawning_and_loot.md): a **particle** from `assets/particles`, **sound definitions** from `assets/sounds`, **entity sound events**, and **block sounds**.

Every snippet compiles as written.

---

## Particles

Particles are JSON files you author in a particle editor and drop in `assets/particles/<name>.particle.json`, next to their texture `<name>.png`. Anvil reads the file into its typed particle format, checks that the identifier inside matches the file name, and exports the file and the texture. A key or component the format does not have stops the build with the file and key named. `Particle.__schema__()` returns the JSON Schema of the format, which an editor can use to check particle files.

```py title="particle"
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.world.particles import Particle

Particle("ember_burst", TextureComponents(color="ember_burst")).queue()
```

A particle can then be referenced from an entity, an animation controller state or a `/particle` command as `<namespace>:ember_burst`.

```py title="particle on the entity"
from anvil.api.logic.molang import Query

client = entity.client.description
client.particle_effect("ember_burst", TextureComponents(color="ember_burst"))
sparks = client.animation_controller("sparks", animate=True)
sparks.add_state("default").transition("hurt", Query.HurtTime() > 0)
sparks.add_state("hurt").particle("ember_burst", locator="root").transition(
    "default", ~(Query.HurtTime() > 0)
)
```

```json
"controller.animation.tut.ember_moth.sparks": {
  "initial_state": "default",
  "states": {
    "default": {"transitions": [{"hurt": "(q.hurt_time > 0)"}]},
    "hurt": {
      "transitions": [{"default": "!((q.hurt_time > 0))"}],
      "particle_effects": [{"effect": "ember_burst", "locator": "root"}]
    }
  }
}
```

!!! tip "PBR particles"
    `TextureComponents(color="ember_burst", mer="ember_burst_mer")` exports a texture set for the particle when PBR is enabled.

---

## Sound Definitions

A sound definition is a named list of `.ogg` files from `assets/sounds`. The name gets the project namespace.

```py title="sound definitions"
from anvil.lib.jsonmodel.enums import SoundCategory
from anvil.api.sounds.sound_definitions import SoundDefinition


def ember_moth_sounds():
    sounds = SoundDefinition()
    flutter = sounds.sound_reference("mob.ember_moth.flutter", SoundCategory.Neutral)
    flutter.add_sound("golem/idle_0", volume=0.6, pitch=1.4)
    flutter.add_sound("golem/idle_1", volume=0.6, pitch=1.6)
    sounds.sound_reference("mob.ember_moth.hurt", SoundCategory.Neutral).add_sound(
        "golem/hurt"
    )
    sounds.sound_reference("mob.ember_moth.death", SoundCategory.Neutral).add_sound(
        "golem/death"
    )
    sounds.queue()
```

```json
"tut:mob.ember_moth.flutter": {
  "category": "neutral",
  "sounds": [
    {"name": "sounds/tut/golem/idle_0", "volume": 0.6, "pitch": 1.4},
    {"name": "sounds/tut/golem/idle_1", "volume": 0.6, "pitch": 1.6}
  ]
}
```

!!! note
    `add_sound("golem/idle_0")` reads `assets/sounds/golem/idle_0.ogg`. Several sounds under one reference are picked at random, weighted by `weight`. `SoundDefinition()` is a single shared file, so call it from anywhere.

---

## Entity Sound Events

Sound events connect the game's events (`ambient`, `hurt`, `death`, `step`...) to a sound definition.

```py title="sound events"
from anvil.api.actors.components import EntityAmbientSoundInterval
from anvil.lib.jsonmodel.enums import EntitySoundEvent

client.sound_event("mob.ember_moth.flutter", EntitySoundEvent.Ambient, volume=0.8)
client.sound_event("mob.ember_moth.hurt", EntitySoundEvent.Hurt)
client.sound_event("mob.ember_moth.death", EntitySoundEvent.Death)

server.components.add(
    EntityAmbientSoundInterval(value=4, range=8, event_name="ambient"),
)
```

```json
"tut:ember_moth": {
  "events": {
    "ambient": {"sound": "tut:mob.ember_moth.flutter", "pitch": [0.8, 1.2], "volume": 0.8},
    "hurt": {"sound": "tut:mob.ember_moth.hurt", "pitch": [0.8, 1.2], "volume": 1.0},
    "death": {"sound": "tut:mob.ember_moth.death", "pitch": [0.8, 1.2], "volume": 1.0}
  }
}
```

!!! note
    The `ambient` event only plays when the server component `EntityAmbientSoundInterval` is present; `value` is the seconds between sounds and `range` the random extra.

!!! tip "Sounds from controllers"
    For a sound played by an animation controller state use `client.sound_effect(name)`, which registers the short name on the entity and returns its sound definition. See [Animating an entity](entity_animations.md).

---

## Block Sounds

```py title="block sounds"
from anvil.lib.jsonmodel.enums import BlockSoundEvent, BlockSoundGroup

block.client.sound_group(BlockSoundGroup.Chain)
block.client.block_sound("block.brass_lantern.hit", BlockSoundEvent.Hit).add_sound(
    "golem/hurt"
)
```

A sound group reuses a vanilla block's sounds. `block_sound(reference, event)` maps one of the block's events to your own definition and returns it, so the files are added in place.

---

## Music

```py title="music"
from anvil.lib.jsonmodel.enums import MusicCategory
from anvil.api.sounds.music_definitions import MusicDefinition

music = MusicDefinition()
music.music_definition(MusicCategory.Creative, min_delay=30, max_delay=120).add_sound(
    "music/ember_theme", stream=True
)
music.queue()
```

A biome plays its own music through `biome.client.biome_music(music_definition=...)`, see [Creating a biome](custom_biome.md).

---

## Full Example — Ember Moth

```py title="entities/ember_moth.py"
from anvil.api.actors.components import (
    EntityAIRandomHover,
    EntityAmbientSoundInterval,
    EntityCollisionBox,
    EntityDespawn,
    EntityFireImmune,
    EntityFlyingSpeed,
    EntityHealth,
    EntityLoot,
    EntityMovementBasic,
    EntityNavigationFly,
    EntityPhysics,
    EntityTypeFamily,
)
from anvil.api.actors.entity import Entity
from anvil.lib.jsonmodel.enums import (
    Difficulty,
    EntitySoundEvent,
    Population,
    SoundCategory,
)
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.sounds.sound_definitions import SoundDefinition
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.api.world.loot_tables import LootTable
from anvil.api.world.particles import Particle


def ember_moth_loot():
    table = LootTable("ember_moth")
    pool = table.pool(rolls=1)
    pool.entry("tut:ember_dust", count=1, weight=4)
    pool.entry(MinecraftItemTypes.Gunpowder(), count=1, weight=1)
    pool.entry(None, weight=2)

    rare = table.pool(rolls=1)
    rare.conditions.killed_by_player().random_chance_with_looting(0.05, 0.02)
    rare.entry(MinecraftItemTypes.BlazePowder(), count=1)
    table.queue()
    return table


def ember_moth_sounds():
    sounds = SoundDefinition()
    flutter = sounds.sound_reference("mob.ember_moth.flutter", SoundCategory.Neutral)
    flutter.add_sound("golem/idle_0", volume=0.6, pitch=1.4)
    flutter.add_sound("golem/idle_1", volume=0.6, pitch=1.6)
    sounds.sound_reference("mob.ember_moth.hurt", SoundCategory.Neutral).add_sound(
        "golem/hurt"
    )
    sounds.sound_reference("mob.ember_moth.death", SoundCategory.Neutral).add_sound(
        "golem/death"
    )
    sounds.queue()


def ember_moth():
    entity = Entity("ember_moth")
    client = entity.client.description
    server = entity.server

    client.add_geometry("ember_moth")
    client.add_texture("ember_moth", TextureComponents(color="ember_moth"))
    client.animation("ember_moth", "fly", animate=True)
    rc = client.render_controller("default")
    rc.set_geometry("ember_moth")
    rc.add_texture("ember_moth")
    rc.set_ignore_lighting()

    Particle("ember_burst", TextureComponents(color="ember_burst")).queue()
    client.particle_effect("ember_burst", TextureComponents(color="ember_burst"))
    sparks = client.animation_controller("sparks", animate=True)
    sparks.add_state("default").transition("hurt", Query.HurtTime() > 0)
    sparks.add_state("hurt").particle("ember_burst", locator="root").transition(
        "default", ~(Query.HurtTime() > 0)
    )

    client.sound_event("mob.ember_moth.flutter", EntitySoundEvent.Ambient, volume=0.8)
    client.sound_event("mob.ember_moth.hurt", EntitySoundEvent.Hurt)
    client.sound_event("mob.ember_moth.death", EntitySoundEvent.Death)

    server.components.add(
        EntityCollisionBox(width=0.5, height=0.4),
        EntityPhysics(has_collision=True, has_gravity=False),
        EntityHealth(value=6, max=6),
        EntityTypeFamily(family=["ember_moth", "ambient", "mob"]),
        EntityFireImmune(),
        EntityFlyingSpeed(value=0.15),
        EntityMovementBasic(),
        EntityNavigationFly(can_path_from_air=True),
        EntityAIRandomHover(priority=1, hover_height=(2, 6), xz_dist=8, y_dist=6),
        EntityAmbientSoundInterval(value=4, range=8, event_name="ambient"),
        EntityDespawn(despawn_from_distance=(32, 64)),
        EntityLoot(table=ember_moth_loot()),
    )

    spawn = server.spawn_rule
    spawn.description.set_population_control(Population.Ambient)
    spawn.add_condition.spawns_on_surface().brightness_filter(0, 7).weight(8).herd(
        2, 5
    ).biome_filter(
        [
            Filter.any_of(
                [
                    Filter.has_biome_tag(MinecraftBiomeTags.Savanna),
                    Filter.has_biome_tag(MinecraftBiomeTags.Mesa),
                ]
            )
        ]
    ).spawns_above_block_filter([MinecraftBlockTypes.Magma()], distance=4)
    spawn.add_condition.spawns_underground().difficulty_filter(
        Difficulty.Easy, Difficulty.Hard
    ).weight(2).biome_filter([Filter.has_biome_tag(MinecraftBiomeTags.Nether)])

    ember_moth_sounds()
    entity.set_display_name("Ember Moth", "Ember Moth Egg").queue("ambient")
    return entity


EmberMoth = ember_moth()
```
