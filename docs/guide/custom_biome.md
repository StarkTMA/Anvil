# Creating a Biome

This tutorial creates the **Ember Fields**, a hot overworld biome with its own terrain, colors, fog, sky, lighting and water. A biome has a **server** side (where and how it generates) and a **client** side (how it looks), and the client side points at the **Vibrant Visuals** settings files: fog, atmosphere, lighting and water.

Every snippet compiles as written. PBR must be enabled in `anvilconfig.json` for the lighting, atmosphere and water files.

---

## Server: Generation

```py title="worldgen/ember_fields.py"
from anvil.api.biomes.biomes import Biome
from anvil.api.biomes.components import (
    BiomeClimate,
    BiomeMapTints,
    BiomeOverworldGenerationRules,
    BiomeOverworldHeight,
    BiomeSurfaceBuilder,
    BiomeTags,
)
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.vanilla.blocks import MinecraftBlockTypes

biome = Biome("ember_fields")

biome.server.components.add(
    BiomeClimate(temperature=1.4, downfall=0.1),
    BiomeTags(
        tags=[MinecraftBiomeTags.Overworld, MinecraftBiomeTags.Monster, "ember_fields"]
    ),
    BiomeOverworldHeight(noise_params=(0.3, 0.4)),
    BiomeOverworldGenerationRules(generate_for_climates=[("warm", 2)]),
    BiomeSurfaceBuilder().set_overworld_builder(
        top_material=MinecraftBlockTypes.Basalt(),
        mid_material=MinecraftBlockTypes.Blackstone(),
        foundation_material=MinecraftBlockTypes.Deepslate(),
        sea_floor_material=MinecraftBlockTypes.Gravel(),
        sea_material=MinecraftBlockTypes.Water(),
    ),
    BiomeMapTints(foliage="#b35a2a").set_grass(tint="#c96b3a"),
)
```

```json
"components": {
  "minecraft:climate": {"temperature": 1.4, "downfall": 0.1},
  "minecraft:tags": {"tags": ["overworld", "monster", "ember_fields"]},
  "minecraft:overworld_height": {"noise_params": [0.3, 0.4]},
  "minecraft:overworld_generation_rules": {"generate_for_climates": [["warm", 2]]},
  "minecraft:surface_builder": {"builder": {"type": "minecraft:overworld", "foundation_material": "minecraft:deepslate", "mid_material": "minecraft:blackstone", "top_material": "minecraft:basalt", "sea_floor_material": "minecraft:gravel", "sea_material": "minecraft:water"}},
  "minecraft:map_tints": {"foliage": "#b35a2a", "grass": {"tint": "#c96b3a"}}
}
```

- `BiomeTags` is how everything else finds the biome: spawn rules, feature rules and structures filter on `Filter.has_biome_tag("ember_fields")`. Keep the vanilla tags the biome should still count as (`Overworld`, `Monster`, `Animal`...).
- `BiomeOverworldGenerationRules` places the biome in the overworld climate bands; `BiomeMultiNoiseGenerationRules` is the alternative for custom dimensions.
- The surface builder chooses the blocks; `BiomeSurfaceMaterialAdjustments` layers more blocks by height or noise.

!!! warning "Addons"
    A package of type `addon` cannot override a vanilla biome (`Biome("plains", is_vanilla=True)` raises). Custom biomes are fine.

---

## Vibrant Visuals Settings

The client biome references settings files by identifier. Build them first and pass the objects, so the identifiers never go out of sync.

```py title="visual settings"
from anvil.lib.jsonmodel.enums import FogCameraLocation, RenderDistanceType
from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.lighting import LightingSettings, LocalLighting
from anvil.api.pbr.water import WaterSettings

fog = FogSettings("ember_fog")
fog.add_distance_location("#c9663a", 8, 96, RenderDistanceType.Fixed)
fog.add_distance_location(
    "#3b1a0e", 0, 12, RenderDistanceType.Fixed, FogCameraLocation.Water
)
fog.air_density(0.25, zero_density_height=120, max_density_height=60)
fog.queue()

sky = AtmosphericSettings("ember_sky")
sky.sky_zenith_color([(0.0, "#7a2a14"), (0.5, "#ff9a4d"), (1.0, "#7a2a14")])
sky.sky_horizon_color("#ffb070")
sky.sun_glare_shape(0.6)
sky.queue()

light = LightingSettings("ember_lighting")
light.orbital_lights(sun_illuminance=80000, sun_color="#ffc078", moon_illuminance=0.4)
light.ambient(4, "#ff8040")
light.emissive(0.2)
light.queue()

water = WaterSettings("ember_water")
water.particle_concentrations(cdom=2.0, chlorophyll=0.1, suspended_sediment=40)
water.waves(enabled=True, depth=0.3, frequency=0.8)
water.queue()

lights = LocalLighting()
lights.add_point_light("tut:brass_lantern", "#ffb347")
lights.queue()
```

!!! note "Keyframes"
    Any value that can change over the day takes a list of `(time, value)` tuples with `time` from 0 (midnight) to 1, or a single value for a constant.

!!! note "Colors"
    Colors are hex strings (`"#ff8040"`), `(r, g, b)` floats from 0 to 1 or `(r, g, b)` integers from 0 to 255, with an optional alpha. They are written as hex.

---

## Client: Appearance

```py title="client biome"
from anvil.lib.jsonmodel.enums import MusicCategory

client = biome.client
client.sky_color("#e07a3f")
client.fog_appearance(fog)
client.atmosphere_identifier(sky)
client.lighting_identifier(light)
client.water_identifier(water)
client.grass_appearance("#c96b3a")
client.foliage_appearance("#b35a2a")
client.water_appearance("#5a2b14", surface_opacity=0.9)
client.precipitation(ash=0.4)
client.biome_music(music_definition=MusicCategory.Soulsand_valley, volume_multiplier=0.6)

biome.queue()
```

```json
"minecraft:client_biome": {
  "description": {"identifier": "tut:ember_fields"},
  "components": {
    "minecraft:sky_color": {"sky_color": "#e07a3f"},
    "minecraft:fog_appearance": {"fog_identifier": "tut:ember_fog"},
    "minecraft:atmosphere_identifier": {"atmosphere_identifier": "tut:ember_sky"},
    "minecraft:lighting_identifier": {"lighting_identifier": "tut:ember_lighting"},
    "minecraft:water_identifier": {"water_identifier": "tut:ember_water"},
    "minecraft:grass_appearance": {"color": "#c96b3a"},
    "minecraft:foliage_appearance": {"color": "#b35a2a"},
    "minecraft:water_appearance": {"surface_color": "#5a2b14", "surface_opacity": 0.9},
    "minecraft:precipitation": {"ash": 0.4},
    "minecraft:biome_music": {"music_definition": "soulsand_valley", "volume_multiplier": 0.6}
  }
}
```

- The builders on `biome.client` add the client components for you; `biome.client.components.add(BiomeClientSkyColor(...))` is the same thing spelled out.
- `grass_appearance` and `foliage_appearance` also accept a vanilla color map name such as `"swamp_grass"`.
- `ambient_sounds(addition=, loop=, mood=)` returns sound definitions to add `.ogg` files to, exactly like [sound definitions](particles_and_sounds.md).

!!! tip "Only the sides you use"
    `biome.queue()` exports the server file and the client file only when you touched them. A biome used for a feature filter alone needs neither.

---

## Full Example — Ember Fields

```py title="worldgen/ember_fields.py"
from anvil.api.biomes.biomes import Biome
from anvil.api.biomes.components import (
    BiomeClimate,
    BiomeMapTints,
    BiomeOverworldGenerationRules,
    BiomeOverworldHeight,
    BiomeSurfaceBuilder,
    BiomeTags,
)
from anvil.lib.jsonmodel.enums import FogCameraLocation, MusicCategory, RenderDistanceType
from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.lighting import LightingSettings, LocalLighting
from anvil.api.pbr.water import WaterSettings
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.vanilla.blocks import MinecraftBlockTypes


def ember_visuals():
    fog = FogSettings("ember_fog")
    fog.add_distance_location("#c9663a", 8, 96, RenderDistanceType.Fixed)
    fog.add_distance_location(
        "#3b1a0e", 0, 12, RenderDistanceType.Fixed, FogCameraLocation.Water
    )
    fog.air_density(0.25, zero_density_height=120, max_density_height=60)
    fog.queue()

    sky = AtmosphericSettings("ember_sky")
    sky.sky_zenith_color([(0.0, "#7a2a14"), (0.5, "#ff9a4d"), (1.0, "#7a2a14")])
    sky.sky_horizon_color("#ffb070")
    sky.sun_glare_shape(0.6)
    sky.queue()

    light = LightingSettings("ember_lighting")
    light.orbital_lights(sun_illuminance=80000, sun_color="#ffc078", moon_illuminance=0.4)
    light.ambient(4, "#ff8040")
    light.emissive(0.2)
    light.queue()

    water = WaterSettings("ember_water")
    water.particle_concentrations(cdom=2.0, chlorophyll=0.1, suspended_sediment=40)
    water.waves(enabled=True, depth=0.3, frequency=0.8)
    water.queue()

    lights = LocalLighting()
    lights.add_point_light("tut:brass_lantern", "#ffb347")
    lights.queue()
    return fog, sky, light, water


def ember_fields():
    fog, sky, light, water = ember_visuals()
    biome = Biome("ember_fields")

    biome.server.components.add(
        BiomeClimate(temperature=1.4, downfall=0.1),
        BiomeTags(
            tags=[MinecraftBiomeTags.Overworld, MinecraftBiomeTags.Monster, "ember_fields"]
        ),
        BiomeOverworldHeight(noise_params=(0.3, 0.4)),
        BiomeOverworldGenerationRules(generate_for_climates=[("warm", 2)]),
        BiomeSurfaceBuilder().set_overworld_builder(
            top_material=MinecraftBlockTypes.Basalt(),
            mid_material=MinecraftBlockTypes.Blackstone(),
            foundation_material=MinecraftBlockTypes.Deepslate(),
            sea_floor_material=MinecraftBlockTypes.Gravel(),
            sea_material=MinecraftBlockTypes.Water(),
        ),
        BiomeMapTints(foliage="#b35a2a").set_grass(tint="#c96b3a"),
    )

    client = biome.client
    client.sky_color("#e07a3f")
    client.fog_appearance(fog)
    client.atmosphere_identifier(sky)
    client.lighting_identifier(light)
    client.water_identifier(water)
    client.grass_appearance("#c96b3a")
    client.foliage_appearance("#b35a2a")
    client.water_appearance("#5a2b14", surface_opacity=0.9)
    client.precipitation(ash=0.4)
    client.biome_music(music_definition=MusicCategory.Soulsand_valley, volume_multiplier=0.6)

    return biome.queue()


EmberFields = ember_fields()
```

Fill the biome with ores, lanterns and trees in [Generating features](world_features.md).
