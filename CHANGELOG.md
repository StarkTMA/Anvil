# Changelog

## Table of Contents

### Latest Releases

- [**Version 0.9.4.1**](#version-0941)
- [Version 0.9.4](#version-094)
- [Version 0.9.3.1](#version-0931)
- [Version 0.9.3](#version-093)
- [Version 0.9.2](#version-092)
- [Version 0.9.1](#version-091)
- [**Version 0.9.0** - _Modular Architecture_](#version-090)

### Version 0.8.x Series

- [Version 0.8.4](#version-084)
- [Version 0.8.3](#version-083)
- [Version 0.8.2](#version-082)
- [Version 0.8.1](#version-081)
- [**Version 0.8.0** - _The Blockbench Update_](#version-080---the-blockbench-update)

### Version 0.7.x Series

- [Version 0.7.3](#version-073)
- [Version 0.7.2](#version-072)
- [Version 0.7.1](#version-071)
- [**Version 0.7.0** - _Guidelines & Addon Support_](#version-070)

### Version 0.6.x Series

- [**Version 0.6.0** - _Configuration Overhaul_](#version-060)

### Version 0.5.x Series

- [Version 0.5.4](#version-054)
- [Version 0.5.3](#version-053)
- [Version 0.5.2](#version-052)
- [Version 0.5.1](#version-051)
- [**Version 0.5.0** - _Documentation & Tools_](#version-050)

### Version 0.4.x Series

- [Version 0.4.2 - 0.4.2.6](#version-042---04226)
- [Version 0.4.1](#version-041)
- [**Version 0.4.0** - _ScriptAPI & PBR Support_](#version-040)

### Version 0.3.x Series

- [Version 0.3.5](#version-035)
- [Version 0.3.4](#version-034)
- [Version 0.3.3](#version-033)
- [Version 0.3.2](#version-032)
- [Version 0.3.1](#version-031)
- [**Version 0.3.0** - _Materials System_](#version-030)

### Version 0.2.x Series

- [Version 0.2.6](#version-026)
- [Version 0.2.5](#version-025)
- [Version 0.2.4](#version-024)
- [Version 0.2.3](#version-023)
- [Version 0.2.2](#version-022)
- [Version 0.2.1](#version-021)
- [**Version 0.2.0** - _Major Architecture Rewrite_](#version-020)

### Early Development

- [**Version 0.1.0** - _Core Foundation_](#version-010)
- [Version 0.0.0 → 0.1.0](#version-000--010)

---

## Version 0.9.4.1

### Anvil
- Added a new cli command `anvil export-world` to export the world from the `.mcworld` file to the `world` directory. this works exactly like the `extract_world` argument in the `Anvil.compile()` method.

### Actors
- Added `EntityPersistent`, `EntityAIMoveToRandomBlock` components.

### Blocks
- Added `block_culling` method to the `BlockGeometry` component.


## Version 0.9.4

### Anvil

- Preparing for Full Anvil Release.
- Moved the Filters class from api.actors.components to lib.filters.
- Added all missing filters.

### Biomes

- Added a new api to manage biome components.
- Added Biomes server components.
- Moved BiomeCustomization class to the Biomes api, the customization options are now more accessible through the Biome Client property, similar to Entities and Blocks.

### Recipes
- Added support for Potion Brewing Recipes.
- Added support for Shapeless, Shaped, and Stonecutter custom block tags.

## Loot Tables
- The loot table classes are now up to date with the current Anvil API architecture.
- Added missing loot table functions.

## Actors
- Separated the Spawn Rule classes from the actors classes, now you can write spawn rules without needing to create an entity.

## Version 0.9.3.1

- Fixed some templates.
- Fixed "en_US" lang files not exporting.
- Cleaned up some CLI print statements during compilation.

## Version 0.9.3

- PyPI version fix

## Version 0.9.2

### Anvil

- Cleaned up the codebase, removed unused imports and files.
- Removed the Logger class as the code now relies heavily on exceptions.
- Added 3 new entries to the anvilConfig file:
  - **ENTRY_POINT**: This is the entry point for the Anvil CLI, it can be used to run Anvil from a specific python file.
    - **NOTE**: The `anvil run` still requires the `anvilconfig.json` file to be present in the working directory.
  - **SCRIPT_BUNDLE_SCRIPT**: This is the javascript compilation/bundling script that will be used to bundle the TypeScript/JavaScript files.
  - **MINIFY**: This option enables/disables minification of json files.
- Changed the anvil project hierarchy.
  - The new hierarchy is designed to be more intuitive and easier to navigate.
  - The new hierarchy is as follows:
    ```
    project/
    ├── assets/
    │   ├── bbmodels/
    │   ├── particles/
    │   ├── textures/
    │   └── sounds/
    ├── marketing/
    ├── output/
    ├── scripts/
    │   ├── javascript/
    │   └── python/
    ├── world/
    │   └── structures/
    ├── anvilconfig.json
    ├── esbuild.js
    ├── package.json
    └── tsconfig.json
    ```
- Anvil now uses esbuild by default to bundle the TypeScript files into JavaScript files.
  - esbuild is recommended by Microsoft for bundling TypeScript files for Minecraft Bedrock Edition.
  - The Compiling/Bundling script can be changed in the `anvilconfig.json` file. So you can use your own bundling script if you wish.
- Updated format versions.
- Anvil now uses Templates for file generation instead of hardcoded jsons.
- Added a new translator module, this new module shouldn't effect your existing code at all. However it introduced a new localization.xlsx file for managing translations. Now you can choose to manually translate your strings using this, automatically translate them using the Google Translate API, or a combination of both. You can also choose to only compile and translate specific languages.
  - The file is generated automatically in the root directory of your projects and is populated with all the localization keys from your code.
  - If you already manually or automatically translated your strings, and then changed a value in your code, the translation of that string will be removed and that language will not be exported unless the key is updated.

### Blockbench

- Blockbench API can now export Generic models containing meshes. This is not a fully supported feature, and likely will not be supported in the future. The API expects meshes containing Minecraft like cubic clusters with a Cubic scale of 1 meters squared.
  - This was tested with .OBJ files exported from Minecraft using Mineways.
- Blockbench can export global animation rotation.
- Added `override_bounding_box` argument to geometry registration in Entity and Block descriptions.

### Kit

- Added a new module `anvil.kit`.
  - The module contains useful functions and classes used for different purposes across different projects by startkma.
- Added `ldtk()` class `anvil.kit.world`. This class can be used to load and parse LDtk files then convert them to Minecraft worlds.
  - ldtk can be a little confusing to work with here, but it was powerful for the creation of [Beyond: Platformer](https://www.minecraft.net/en-us/marketplace/pdp/starktma/beyond:-platformer/f1ecf12b-1b6f-4794-a8de-24dfb82e6f25).
  - A tutorial on how to use the `ldtk()` class will be available in the documentation sometime in the future.
- Added `add_entity_outline()` function to the `anvil.kit.actors.materials` module. This function can be used to add 2 materials used for entity outlines.
  - The function will add the `base` and `outline` materials to the entity.materials file.
  - The `base` material is used for the base model, while the `outline` material is used for the outline of entities.

### Actors

- Added `is_moving` filter.
- Added `EntityAITakeBlocks()`, `EntityAIPlaceBlock()` components.

### Items

- Added `ItemStorageItem`, `ItemStorageWeightLimit`, `ItemStorageWeightModifier` and `ItemBundleInteraction` components.

### Blocks

- Added `BlockMovable()`, `BlockDestructionParticles()` component.

## Version 0.9.1

### Anvil

- Improved Type Hints and IDE autocompletion. Although much more work is needed.
- Improved error handling and raised errors.
- Improved class inheritance and modularity for AddonObjects and Descriptors.
- Exposed the `CustomComponent` from the `anvil.lib.schemas` module, enabling users to define custom components with support for inheritance.
- Relocated many classes for better organization and modularity, your code should be minimally affected by this change.
- Component Groups now validates component dependencies and clashes within the same group or permutation.

## Version 0.9.0 - Modular Architecture

### Anvil

- Updated to release `1.21.90`.
- Refactored and rearranged the Anvil codebase to use a more modular approach.
- Creating a new project will no longer generate the folder in "com.mojang/minecraftWorlds", instead the working directory will be used.
- Added a new "assets/world" to host and ".mcworld file" with the same name as the project.
- "assets/world" will now be used to host ".mcstructures" files instead of "assets/structures".
- Added a new argument "extract_world" to Anvil.compile() method, this will extract the world from the ".mcworld" file and place it in the world directory.
- Added a new `JigsawStructureSet()` and `JigsawStructureTemplatePool()` classes to the `anvil.api.structures` module, `JigsawStructure` and `JigsawStructureProcess` can be initialized from within `JigsawStructureSet` and `JigsawStructureTemplatePool`.
- Started moving away from `Enums` to new `types` and `Literals` to better support type checking and IDE autocompletion.

### PBR

- Added `AtmosphericSettings()`, `FogSettings()`, `ShadowSettings()`, `WaterSettings()`, `ColorGradingSettings()`, `BiomeCustomization()`, `LightingSettings()`, `PointLights()`, `PBRFallback()`.
- Integrated Texture Sets with Entities and BlockMaterialInstances.

### Blockbench

- Blockbench no longer exports cube faces that have texture disabled.

## Version 0.8.4

### Anvil

- Added Recipe unlocking context to the `Recipe()` class.

### Blocks

- Added `BlockTick()` component.

## Version 0.8.3

### Anvil

- Updated `MODULE_MINECRAFT_SERVER` to `[1.17.0]`.
- Added Aim Assist and Focus Target to the `CameraPreset()` class.
- Added `Glyph()` enum.
- Entity Sound Events now support variants.
- Animation controller sound effects now support locators.

### Blocks

- Block groups are now namespaced, for example `starktma:group_name`.
- Added `BlockItemVisual()`, `BlockLiquidDetection()`, `BlockDestructionParticles()` component.

### Items

- Item groups are now namespaced, for example `starktma:group_name`.

### Components

- Added `MovementSoundDistanceOffset()`, `RendersWhenInvisible()`, `Breedable()`, `IsCollidable()`, `BodyRotationAxisAligned()`, `InputAirControlled()` components.
- Added `home_distance`, `is_bound_to_creaking_heart` Filters.

### Molang

- Added `LastInputModeIsAny()` and `TouchOnlyAffectsHotbar()` queries.

## Version 0.8.2

### Anvil

- Updated `MODULE_MINECRAFT_SERVER` to `[1.16.0]`.
- Updated `MODULE_MINECRAFT_SERVER_UI` to `[1.3.0]`.

### Blocks

- Added `BlockRedstoneConductivity()` components.

### Components

- Added `DimensionBound()`, `Transient()`, `CannotBeAttacked()`, `IgnoreCannotBeAttacked()`, `LookedAt()` components.

### Vanilla

- Added new blocks: `CreakingHeart()`, `ClosedEyeBlossom()`, `OpenEyeBlossom()`, `PaleHangingMoss()`, `PaleMossBlock()`.
- Added new entities: `Creaking`.

### Actors

- Added `play_sound` and `emit_particle` to Entity Events.

### Molang

- Added `ClientMemoryTier`, `ServerMemoryTier` and `ClientMaxRenderDistance` queries.

## Version 0.8.1

### Anvil

- Updated `GEOMETRY_VERSION` to `[1.21.0]`.
- Updated `MODULE_MINECRAFT_SERVER` to `[1.13.0]`.
- Updated `MODULE_MINECRAFT_SERVER_UI` to `[1.2.0]`.

### Vanilla

- Added 2 new mobs: Bogged and Breeze
- Added new items: `Mace`, `OminousBottle`, `WindCharge`, `TrialKey`, `OminousTrialKey`, `BreezeRod`, `TrialSpawner`, `FlowPotteryShard`, `GusterPotteryShard`, `ScrapePotteryShard`, `FlowBannerPattern`, `GlobeBannerPattern`, `GusterBannerPattern`, `BoltArmorTrim`, `FlowArmorTrim`, `MusicDiscCreator`, `MusicDiscCreatorMusicBox`, `MusicDiscPrecipice`.
- Added new blocks: `Crafter()`, `TrialSpawner()`, `Vault()`, `HeavyCore()`.
- Expanded the copper family with all the Oxidized and waxed variants of the following blocks: `ChiseledCopper()`, `CopperGrate()`, `CopperBulb()`, `CopperDoor()`, `CopperTrapdoor()`

### Commands

- Added new effects to the `Effects` enum: `Infested`, `Oozing`, `Weaving`, `WindCharged`, `RaidOmen`, `TrailOmen`.

### Blockbench

- Added support for UV rotations.
- Added support for Item Display Transformation.

### Blocks

- Added `scale_pivot` and `rotation_pivot` to `BlockTransformation()`.
- Added `BlockCustomComponents()`.

### Items

- Added `ItemCustomComponents()`, `ItemRarity()` components.

## Version 0.8.0 - The Blockbench Update

### Blockbench

- Added support for Blockbench files. Entities attachables and blocks no longer require a dedicated model, animation and texture files, instead a single bbmodel must be added to the `assets/bbmodels` folder.
  - A blockbench file can store a model and all of its relative textures and animations.
  - For instance, if you have an entity named `starktma:vehicle` that references a model called `truck`, you must add a model file named `truck.bbmodel` to the `assets/bbmodels` folder. For example:
    - `player.Client.description.geometry("energy_beam")`. Anvil will check for a file named `energy_beam.bbmodel` in the `assets/bbmodels` directory and extract the model from it.
    - `player.Client.description.texture("energy_beam", "energy_beam_blue")`. Anvil will check for a file named `energy_beam.bbmodel` in the `assets/bbmodels` directory and extract the texture `energy_beam_blue` from it.
    - `player.Client.description.animation("energy_beam", "energy_beam_charging")`. Anvil will check for a file named `energy_beam.bbmodel` in the `assets/bbmodels` directory and extract the animation `energy_beam_charging` from it.
- Blockbench file identifiers should use a namespace prefix, for example `starktma:truck.bbmodel`. Anvil will automatically add the namespace to the identifier.
- Blockbench animations should contain their name. For example, `energy_beam_charging` instead of `animation.stark_ap.player.energy_beam`. Anvil will automatically format them properly.
- Blockbench textures should contain their name. For example, `energy_beam_blue` instead of `texture.stark_ap.player.energy_beam`. Anvil will automatically format them properly.
- Blockbench animation controllers are not currently supported. the animation controllers must be added manually through Anvil.
- Blockbench `Bézier` keyframes are not supported. Anvil will treat them as `linear` keyframes.

### Actors

- Actors will no longer support a texture and geometry shortnames instead the full name will be used. **Breaking**
- Actors will now require a `blockbench_filename` property to reference the blockbench file, in addition to the target texture and animation. **Breaking**

### Anvil

- Resource and behavior packs are now generated in the `development_behavior_packs` and `development_resource_packs` directories instead of the project root folder, this improves the development experience and reduces the commit changes as the packs can be regenerated at any point.
- Added a new enumerator `ItemVanillaTags` for item tags.
- Added a new enumerator `BlockVanillaTags` for block tags.

### Features

- Added `SmithingTrimRecipe()` class.

### Blocks

- Added Block tag to Components and Permutations. `block.server.components.tag()` or `block.server.permutation("permutation_name").tag()`.

## Version 0.7.3

### Anvil

- Added `behavior_description` and `resource_description` to `anvilconfig.json`.
- Fixed addons packaging issue.
- Updated `MANIFEST_BUILD` to `1.20.80`.
- Updated `ENTITY_SERVER_VERSION` to `1.20.80`.
- Updated `MODULE_MINECRAFT_SERVER` to `1.10.0`.
- Updated `ITEM_SERVER_VERSION` to `1.20.70`.
- Updated `CAMERA_PRESET_VERSION` to `1.20.80`.

### Actors

- Added a `reuse_assets` property to the `EntityClient` description, this property will allow you to manually enter animation, geometry and controller IDs without Anvil checking for a match in the `assets` directory.
- Added `queryable_geometry` property to the `EntityClient` description.
- Added `should_update_bones_and_effects_offscreen` and `should_update_effects_offscreen` properties to the `EntityClient` description.
- Updated the `get_vanilla()` `EntityClient` function, the change will fixes some issues with retrieving the proper vanilla entity from the public repository.
- Added a placeholder `spawn_category()` function to the `EntityServer` description. This is not functional in Minecraft at the moment therefore it has no effect.
- `EntityClient` `spawn_egg()` function now supports an index number.
- Added `spawn_egg_color()` function to the `EntityClient` description.

### Commands

- Added the `Hud` command.
- Added a `remove()` function to the `Effect()` class, this function will remove specific effects from the target.

### Components

- Added `has_tag()`, `is_difficulty()`, `is_sitting()` and `has_damaged_equipment()` filters.
- Updated the `Interact()` component.
- Added `Inventory()`, `Dash()`, `VariableMaxAutoStep()`, `RiseToLiquidLevel()`, `Buoyant()`, `LavaMovement()`, `ExperienceReward()`, `Equippable()`, `Color()`, `Color2()`, `BurnsInDaylight()`, `Boss()`, `Sittable()`, `FlyingSpeedMeters()`, `ConditionalBandwidthOptimization()`, `ItemHopper()`, and `BodyRotationBlocked()` components.

### Features

- Added `extend_player_rendering()` to the `CameraPreset()` class.

### Molang

- Added `ArmorSlotDamage()` query.
- `BoneOrientationTrs()` and `BoneOrientationMatrix()` queries now return an object with `position`, `rotation` and `scale` properties.

## Version 0.7.2

### Anvil

- Added an `anvilConstans.ts` to the `assets/javascript` directory. This file will be regenerated on every run of the script and is means to sync the project configuration with ScriptingAPI.
- Updated `MANIFEST_BUILD` to `1.20.70`.
- Updated `ENTITY_SERVER_VERSION` to `1.20.70`.
- Updated `MODULE_MINECRAFT_SERVER` to `1.9.0`.

### Blocks

- Added a menu category and group Enums to block description.
- Added `is_hidden_in_commands` property to block description.
- Added `AlphaTestSingleSided` variable to the `BlockMaterial` enum.

### Features

- Rewrote the Recipe class.
- Added `SmeltingRecipe()`, `SmithingRecipe()`, `ShapelessRecipe()`, `StoneCutterRecipe()`, `ShapedCraftingRecipe()` classes.

### Vanilla

- Remove the `LEGACYItems()` class and added the rest of the items to the `Items()` class.
- Renamed `Grass()` block class to `GrassBlock()`.
- Split `Leaves()` and `Leaves2()` block classes to `AcaciaLeaves()`, `BirchLeaves()`, `DarkOakLeaves()`, `JungleLeaves()`, `OakLeaves()`, `SpruceLeaves()`.
- Split `DoubleWoodenSlab()` block class to `AcaciaDoubleSlab()`, `BirchDoubleSlab()`, `DarkOakDoubleSlab()`, `JungleDoubleSlab()`, `OakDoubleSlab()`, `SpruceDoubleSlab()`.
- Split `WoodenSlab()` block class to `AcaciaSlab()`, `BirchSlab()`, `DarkOakSlab()`, `JungleSlab()`, `OakSlab()`, `SpruceSlab()`.
- Split `Wood()` block class to `AcaciaWood()`, `BirchWood()`, `DarkOakWood()`, `JungleWood()`, `OakWood()`, `SpruceWood()`, `StrippedOakWood()`, `StrippedSpruceWood()`, `StrippedBirchWood()`, `StrippedJungleWood()`, `StrippedAcaciaWood()`, `StrippedDarkOakWood()`.

### Commands

- Added `has_property()` method to the `TargetSelector()` class.
- Replace the `Suicide` DamageCause enum variable with `SelfDestruct`.

### Components

- `EntitySensor()` range parameter now accepts a tuple for horizontal and vertical range.
- Added `was_last_hurt_by()` filter.

### Molang

- Due to the deprecation of class properties in Python 3.13, all class properties are now converted to methods.
- Added `IsAttached()`, `HasPlayerRider()`, `Scoreboard()`, `RideBodyXRotation()`, `RideBodyYRotation()`, `RideHeadXRotation()`, `RideHeadYRotation()`, `RiderBodyXRotation()`, `RiderBodyYRotation()`, `RiderHeadXRotation()` and `RiderHeadYRotation()` queries.

## Version 0.7.1

### Anvil

- Updated `MODULE_MINECRAFT_SERVER` to `1.8.0`.
- Updated `MANIFEST_BUILD` to `1.20.60`
- Music now references the correct sound definitions.

### Actors

- Added `queue_command` and `emit_vibration` to Actor events.
- Actors can now reference the same animations, same as geometries and textures.

### Components

- Added `is_panicking` and `is_sprinting` filters.
- Updated `Ageable()` component.
- `EntitySensor()` now support multiple sensors.
- Added `SlimeKeepOnJumping()` component.

### Molang

- Added `IsCooldownType`, `CooldownTime`, `CooldownTimeRemaining`, `RelativeBlockHasAnyTags`, `RelativeBlockHasAllTags`, `BlockNeighborHasAnyTags`, `BlockNeighborHasAllTags`, `BlockHasAllTags`, `BlockHasAnyTags`, `BoneOrientationTrs` and `BoneOrientationMatrix` queries.

## Version 0.7.0 - Guidelines & Addon Support

### Guidelines

- New packaging type: Addon
- Anvil raises an error when using experimental features in packages of type Addon.
- Anvil raises an error when total block permutations exceed 10,000 in packages of type Addon, and a warning otherwise.
- Anvil raises an error when overriding a vanilla feature (items and entities, including the player) in packages of type Addon.
- All textures are now placed 2 folders deep in the RP directory, this is to avoid overriding 3rd party textures. `RP/textures/namespace/project_name/`
- Texture references are now in the format `namespace:texture_name`. This is done automatically.
- Scores are now enforced to start with `namespace.` for packages of type Addon. added a new method `get_new_score` to anvil definition to generate scores.
- Tags are now enforced to start with `namespace.` for packages of type Addon.
- Loot Tables are now placed 2 folders deep in the BP directory, this is to avoid conflicting with 3rd party loot tables. `BP/loot_tables/namespace/project_name/`.
- Functions are now placed 2 folders deep in the BP directory, this is to avoid conflicting with 3rd party functions. `BP/functions/namespace/project_name/`.
- Sound references are now in the format `namespace:sound_name`. This is done automatically.
- Materials now follow the format `namespace.material_name:base_material`.

### Anvil

- Split the `core.py` file into multiple files. This shouldn't cause any issues.
- Removed the `fullns` cli option, a universal format is now enforced.
- Added `addon` cli option to set the packaging target. Can be changed from `anvilconfig.json`.
- Missing config options are now handled on runtime.
- `AddonObjects` now all have a single extension format.
- Refactored a lot of code, split a lot classes into smaller modules.
- Most of the functionalities are now required to manually import from their respective modules.
- Anvil now flags experimental entities on non experimental environments.
- Resource packs and behavior Packs always have dependencies on each other
- Reimplemented the `get_vanilla` method in Entity clients, work with vanilla entities only. The method retrieves the latest version of the `client_entity` from the official `bedrock_samples` github repository.
- Implemented a basic caching system to store retrieved vanilla data, the cached data will be updated in case there is newer release.
- Added a new `identifier` property to the `Materials()` class.

### Blocks

- Added a new `BlockDefault()` component that allows you to use the blocks.json file to define block visuals. This is a workaround until `BlockUnitCube()` is out of experimental.
- `BlockGeometry()` and `BlockMaterialInstance()` are no longer required when using `BlockDefault()`.
- If a display name is not supplied using `BlockDisplayName()`, the name will be inferred from the block identifier. Not localized.

### Items

- If a display name is not supplied using `ItemDisplayName()`, the name will be inferred from the item identifier. Not localized.
- Added an `attachable` property to items to quickly add attachables to items.

### Molang

- Added `Context` to the molang module.
- Fixed an error that treated some molang expressions as string literals and wrapped them with single quotes.

### Blockbench

- As an effort to move towards using `.bbmodel` files natively, there has been a change to how models and textures are referenced.
  - Entities and attachables no longer require a dedicated model file, instead a referenced models must be added to the `assets/models` folder under their own name.
    - For instance, if you have an entity named `starktma:vehicle` that references a model called `truck`, you must add a model file named `truck.geo.json` to the `assets/models/actors` folder.
  - Entities and attachables no longer require a dedicated texture file, instead a referenced textures must be added to the `assets/textures` folder under their own name.
    - For instance, if you have an entity named `starktma:vehicle` that references a texture called `truck`, you must add a texture file named `truck.png` to the `assets/textures/actors` folder.
  - Entities and attachables textures and models are now placed in the same `actors` folder.
  - Entities and attachables no longer exports their models and texture into queued folders, instead everything is exported under the `actors` folder.
- Adopting blockbench files will facilitate working with assets, additionally the folder structure can no longer be supported with the new enforced guidelines due to the file path limit.

### Components

- Added `Tameable()` component.

## Version 0.6.0 - Configuration Overhaul

### Anvil

- Changed the directory configuration of some files to support the new Addons program.
- Changed `Config.ini` to `anvilconfig.json`. This is done so it's much easier to integrate with the Scripting API.
- A newer guidelines have been introduced to Anvil. Namespaces now require an additional abbreviation of the project name. For instance, if the namespace is `starktma` and the project name is `Beyond: Platformer`, the namespace will be `starktma_bp`. This is done to avoid conflicts with other projects.
- Item Texture and Terrain Texture references are now in this format `namespace:name`. This change does not require your attention as it's done automatically.
- Item and block textures are now save under `RP/textures/namespace/`. previously they were saved under `RP/textures/`.
- Added sounds and music will now use `RP/sounds/namespace/` instead of `RP/sounds/`.
- Sounds now use the format `namespace:sound_reference` instead of `sound_reference`. This is does not require your attention as it's done automatically.
- Calling `identifier` on a sound definitions will return the Sound reference in the format `namespace:sound_reference`.
- Moved `Dialogue()`, `Fog()`, `LootTable()`, `Recipe()`, `Function()`, `Particle()`, `CameraPreset()`, `Structure()`, `Fonts()` and `SkinPack()` classes to `anvil.api.features`.
- Dialogue scene tags now use the format `namespace:scene_tag` instead of `scene_tag`. This is does not require your attention as it's done automatically.
- Calling `identifier` on a dialogue scene will return the scene tag in the format `namespace:scene_tag`.
- Calling `identifier` on a fog instance will return its identifier.
- Moved `Geometry()` and `Animations()` classes to `anvil.api.blockbench`, this is in preparation to integrate `.bbmodel` files directly into Anvil without splitting them into multiple json files.
- LootTables will be exported to `BP/loot_tables/namespace/`
- Calling `path` on a loot table will return its execution path that can be used in Components or Commands. (Must be queued first)
- Particle textures will no be copied to `RP/textures/particle/namespace/`.
- Actor textures are now copied into `RP/textures/namespace/[entity-attachable]/` instead of `RP/textures/[entity-attachable]/`

### Components

- Added `FlyingSpeed()`, `RandomHover()`, `Interact()`, `AngerLevel()`, `Roar()`, `FloatWander()`, `LayDown()`, `MeleeBoxAttack()`, `CanJoinRaid()`, `TimerFlag1()`, `TimerFlag2()`, `TimerFlag3()` components.
- Updated `ENTITY_SERVER_VERSION` to `[1.20.50]`.

### Vanilla

- Split the Planks block into 6 individual blocks.
- Split the Stone block into 7 individual blocks.

### Items

- Renamed `ItemUseDuration()` to `ItemUseModifiers()`.
- Added `ItemTags()` component.
- Updated `ITEM_SERVER_VERSION` to `[1.20.50]`.

### Molang

- Added `timer_flag_1`, `timer_flag_2`, `timer_flag_3` queries.

## Version 0.5.4

### Anvil

- Updated `MODULE_MINECRAFT_SERVER` to `[1.6.0]`.
- Updated `ITEM_SERVER_VERSION` to `[1.20.40]`.
- tsc now runs using `tsconfig.json`. The tsconfig options can be added and/or changed but `outDir` and `include` will be overwritten by Anvil.
- Added a `launch.json` for script debugging.
- Added `node_modules/` to default `.gitignore`.
- Added `scriptui` option to `config.ini`.

### Components

- Added `MovementMeters()` component that takes speed in m/s instead of whatever Minecraft is using.
- Added `MovementMeters()`, `FollowParent()`, `PlayerRideTamed()`, `InputGroundControlled()`, `FollowOwner()`, `WaterMovement()`, `Panic()`, `ChargeAttack()`, `RamAttack()`, `AvoidMobType()`, `LeapAtTarget()`, `OcelotAttack()`, `Angry()`, `OwnerHurtByTarget()`, `OwnerHurtTarget()`, `RandomSearchAndDig()`, `StompAttack()`, `FollowMob()`, `RandomSwim()`, `RandomBreach()` components.
- Added `has_damage()`, `is_daytime()`, `rider_count()` filters.

## Version 0.5.3

### Anvil

- Renamed `seed` cli option to `random_seed`.
- Updated `ITEM_SERVER_VERSION` to `[1.20.30]`.
- Added a new `generate_technical_notes()` method to `Anvil` class, the method will generate a pdf file containing a list of every entity, block, attachable, item, particle and sounds that were exported.
- `compile()`, `mcworld()`, `mcaddon()` are now proper methods instead of properties.
- Removed the `scipy` requirement from `setup.cfg`.
- Removed and/or replaced rarely used library imports.
- Added a new `CameraPreset()` class that creates new camera presets.
- Removed the `vanilla` folder from the `assets` directory, this is a step forward towards removing support for cloning vanilla packs.
- Scripting API files are now hosted in the `assets/javascript` directory, a quality of life improvement towards full support of js scripting.
- Anvil CLI will install both `@minecraft/server` and `@minecraft/serve-ui` modules if the `scriptapi` flag is set.
- Anvil will automatically run `tsc <filename>` on every `.ts` file in `assets/javascript` and copies every `.js` files preserving the relative paths in `BP/scripts`.
- Moved the scripts folder to host all Python files to `assets/python`, you can place your files anywhere you wish to but this is done to keep inline with javascript files.
- Anvil now support multiple packs, generation will still take place in a single pack but if you wish to include other packs, add the uuid to `config.ini` separating by a `,` and copy your pack to their respective locations.

### Blocks

- Renamed `FacingDirections`, `BlockFaces` and `VerticalHalf` to `FacingDirectionsTrait`, `BlockFacesTrait` and `VerticalHalfTrait`.
- Renames properties to states in Block Description.

### Commands

- Fixed an issue with `Camera()` command where the keyword `ease` was not parsed.
- Added `Time()`, `Stopsound()` commands.

### Components

- Added `is_biome()`, `is_underwater()`, `on_ground()`, `in_water()` filters.
- Added `Biomes` enum.
- Added `RandomSitting()`, `StayWhileSitting()`, `UnderwaterMovement()`, `RandomSwim()`, `RandomBreach()`, `MoveToWater()`, `MoveToLand()`, `MoveToLava()`, `LookAtTarget()` components.
- `Rideable()` family types are now added by passing family strings using `family_types()`.

### Items

- Added `ItemCanDestroyInCreative()` and `ItemHoverTextColor()` components.

### Tools

- `StateMachine()`:
  - `active_player` counter now runs all the time regardless of the max player count.

## Version 0.5.2

### Anvil

- Split `StainedHardenedClay()` block into 16 individual blocks.
- Split `StainedGlass()` block into 16 individual blocks.
- Split `StainedGlassPane()` block into 16 individual blocks.
- Split `ConcretePowder()` block into 16 individual blocks.
- Entity names starting with a digit will raise an error.
- Updated the `SOUND_DEFINITIONS_VERSION` format version to `[1.20.20]`.
- Updated `BLOCK_SERVER_VERSION` to `[1.20.20]`.
- sound_definitions now accept both float and integer values for min_distance and max_distance.
- Added support of Random Seed Generation to both CLI and core Anvil.
- Updated some vanilla blocks to use `BlockStates.CardinalDirection` instead of `BlockStates.Direction`.

### Components

- Added `can_spread_on_fire` parameter to both `DelayedAttack()` `MeleeAttack()`.

### Molang

- Renamed `block_property` to `block_state`.
- Renamed `has_block_property` to `has_block_state`.

### Commands

- Added `PlayerSleepingPercentage()` to the `Gamerule` command.
- Added `ScriptEvent()`.
- Added `CameraPresets()` and `CameraEasing()` enums.
- Added `Camera()` command.

### Items

- Added `group`, `category` and `is_hidden_in_commands` to Item Server description.
- Added `ItemWearable()` component.
- Added `ItemHandEquipped()` component.
- Added `ItemGlint()` component.
- Added `ItemUseDuration()` component.
- Added `ItemStackedByData()` component.
- Added `ItemUseAnimation()` component.
- Added `ItemAllowOffHand()` component.
- Added `ItemShouldDespawn()` component.
- Added `ItemLiquidClipped()` component.
- Added `ItemDamage()` component.
- Added `ItemDigger()` component.
- Added `ItemEnchantable()` component.
- Added `ItemFood()` component.
- Added `ItemsInteractButton()` component.
- Removed `LEGACYItemHandEquipped()` component.
- Removed `LEGACYItemFoil()` component.
- Removed `LEGACYItemStackedByData()` component.
- Removed `LEGACYItemUseDuration()` component.
- Removed `LEGACYItemFood()` component.
- Removed the `_ItemClient()` class.

### Blocks

- Added `BlockFace` and `VerticalHalf` block states.
- Removed `_BlockClient()` class.
- Added `traits` property to blocks server description.
- Added the following enums: `PlacementDirectionTrait`, `PlacementPositionTrait`, `CardinalDirections`, `FacingDirections`, `BlockFaces`, `VerticalHalf`.
- Renamed `property` keys to `state`.

### Documentation

- Exposed more APIs.

## Version 0.5.1

### Anvil

- Added workflows to publish to pypi and testpypi.
- Gone Public!!!!!!!!

## Version 0.5.0 - Documentation & Tools

### Anvil

- Docs are now build when pushing to the main branch.
- Added a universal way to require project specific configuration.
  - To use call `ANVIL.require_config()` and pass the required configs as arguments.
- Additional work on documentation.
- Fonts can now generate a 'numbers' particle texture that contains numbers from 0-999.
- Replaced `dependecies` with `capabilities` in resource pack manifest.
- Added a new API module `texture_pack` (WIP).
- Added `GlobalLighting` and `Atmospherics` to the `texture_pack` module to support the new PBR pipeline.
- A `version` function will now generate every time there is a compilation, includes the time, Minecraft version and the build version.
- Rolled `ITEM_SERVER_VERSION` back to `[1.16.0]`, a lot of necessary functionalities are missing, waiting for `[1.12.40]`.
- Added a new module, `anvil.tools.functions`
- Added 3 new systems to `anvil.tools.functions`: `StateMachine`, `TimedFunction` and `StepTimedFunction`.
- Added a new property to Anvil Core `ANVIL.new_score`, this will register and return a new incremental score every time it's called. (Improved the score creation in `TimedFunction`)

### Components

- Added and `_ai_goal()` parent class.
- Added new components: `MoveTowardsTarget()`, `EntitySensor()`, `AmbientSoundInterval()`.
- Slightly modified the way components are coded, this allows for much easier use of the `remove` method from events.
- Fixed a bug that wrapped filters in additional brackets for `all_of`, `any_of` and `none_of` conditions.
- Fixed a bug with `SendEvent()` that caused it to not write some important data to the json file therefore causing it to not work.

### Actors

- Similar to geometries, animations can now be referenced from other entities, reducing redundancy.
- Entity Sound Events can now specify a min and max distance of a sound.

### Commands

- Fixed a bug with the `CameraShake()` command returning `None` on export.

### UI

- Added a `Credits Constructor` class method to `AnvilHUDScreen` to facilitate creating UI based credits.
- Titles and Actionbars will now ignore keywords created in screens other that `anvil_hud`.

### Documentation

- Finished the tutorial for adding an entity.
- Added a documentation for adding a block.
- Added a tutorial for creating a One Block SkyBlock map.

## Version 0.4.2 - 0.4.2.6

### Anvil

- Updated to release `1.20.11`.
- Updated `ITEM_SERVER_VERSION` to `[1.12.10]`
- Added lots of docstrings
- Changed README from rst to md.
- Added basic documentations.

### Items

- Added `ItemCooldown`, `ItemRepairable`, `ItemMaxStackSize`, `ItemBlockPlacer`, `ItemRecord`, `ItemShooter`, `ItemProjectile`, `ItemThrowable`.

### Commands

- Block states in commands will use equals instead of colon.

### UI

- Rewrote the UI trigger mechanic to allow for more complex ui elements.

## Version 0.4.1

### Anvil

- Added a proper integration of vanilla blocks.
- Added a proper `Blocks()` class and `BlockStates` Enumerator to the `vanilla` api. The vanilla blocks will allow you to customize them using their block states.
- Components and Commands will only accept `vanilla.Blocks()`, `str()` and `Block()` as inputs and will raise an error otherwise.
- Fixed an issue that caused music and sound to not be compiled.
- Classes use proper Enumerators.
- Added `_debug` a rawtext attribute to ANVIL. this can be useful to display score and debug text as actionbar if DEBUG = 1.
- Added a `_SoundEvent()` class to `core.py`. This call will serve as sound manager for Minecraft Vanilla sound event triggers.
  - Sound Events are only supported for Entities as of now, a new method was added to `Entity.Client.description` that allows adding default sound triggers.

### Components

- Components that have block inputs will only accept `vanilla.Blocks()`, `str()` and `Block()` instances as inputs and will raise an error otherwise.

### Items

- Rolled `ITEM_SERVER_VERSION` back to `[1.12.1]`.
- Added a `Client` property to items, used to set the `Name` and `Icon` of an item as a temporary solution until the full list of item components leave experimental.

### Commands

- Added `Setblock()` command.
- Added `Fill()` command.
- Added `Music()` command.
- Updated `Execute().If/Unless.Block()` to use block states instead of legacy data values.
- Commands that have block inputs will only accept `vanilla.Blocks()`, `str()` and `Block()` instances as inputs and will raise an error otherwise.
- `Playsound()` no longer appends position by default.
- `Say()` now wraps all texts with "" by default.

### Molang

- Added the rest of the molang queries.
  - Some queries need more information to properly implement therefore they may not work.

## Version 0.4.0 - ScriptAPI & PBR Support

### Anvil

- Added support for ScriptAPI
  - To include scripting in your project use the flag `--scriptapi` when creating a new project.
  - Scripts can be added or removed anytime from `config.ini`.
- Added support for PBR
  - To include pbr in your project use the flag `--pbr` when creating a new project.
  - PBR can be added or removed anytime from `config.ini`.
- Removed the #packaging comment from the generated python script, it's outdated and doesn't represent the functionality of the method anymore.
- Updated to release `1.20.1.0`.
- Preview builds are no longer tracked, instead focusing solely on releases.
- Reusable geometries no longer make copies of the same geometry files, instead only reference them. Referenced entities must be queues before the referencing entity.
- Renamed `Permission` enumerator to `InputPermissions`.
- `package.py` changes:
  - Added a lot of docstring.
  - Removed `RawText`, `random_character_generator`, `CreateImage`, `GetColors`, `CreateTreeFromPath`, `GetPathFromTree`, `MoveFiles`, `DownloadFile`.
  - Moved `CreateDirectoriesFromTree` to `cli.py`
  - Moved `ShortenDict` inside the `AddonObject` class.
- Added docstrings to the `cli` tool.
- Started moving from the basic `RaiseError` to proper Errors.
- Removing a component from an Actor no longer results in an error if the component doesn't exist.
- Empty functions will no longer be exported.
- Restructured the Schemes function, now it's a proper class.
- Created a Logger class to track error and operations.
- Removed type subdirectory from RP animation and render controllers.
- Added a version enforcing method to components.
  - Implemented the enforcements in the items components.
  - Components that require a minimum format version will raise an error if Anvil format version is not equal or higher.
  - This change will allow us to work on implementing experimental features safely.
- Added the new Items and Blocks to the vanilla module.
- Added `all_slots_empty` and `any_slots_empty` filters.
- Added the `spawn_item_event` key to the `SpawnEntity` component class.
- Formatted some Logger error messages.
- Updated `ITEM_SERVER_VERSION` to `1.20.0`

> <span style="color:red">**Breaking behavior**</span>
>
> - Config file is no longer automatically initialized, instead it's an `ANVIL` property.
> - The gloabl variables such as `NAMESPACE` and `PROJECTNAME` are now accessible through the `ANVIL` instance.
>   - `NAMESPACE -> ANVIL.NAMESPACE`
> - Localizing uses a key_value arguments instead of a manual string now

### Components

- Added `InsideBlockNotifier()`, `Transformation()`, `Equipment()`, `EquipItem()`, `FireImmune()`, `SendEvent()` components.
- Added `is_raider`, `is_variant`, `is_mark_variant`, `is_skin_id` filters.
- Removed the `particle` argument from the `Particle` component, use `particle_on_hit` method instead.

### Blocks

- Custom blocks textures are moved inside an `anvil` folder to separate them from vanilla textures.

### Commands

- `Give` command always includes the amount and data, this is done to account for possible use of item components.
- `Summon` command now always wraps nametags inside additional double quotes.
- `name` argument in the target selectors wraps names inside additional double quotes.

### UI

- New UI screen will automatically populate the `_ui_defs.json` file.
- Added an `anvil_common` screen to host common elements.

## Version 0.3.5

### Anvil

- Updated the extensions of generated files.
- Vanilla entities are automatically exported to the vanilla directory, regardless of the provided directory.
- Updated to release `1.19.81.01` and preview `1.20.0.20`.
- Actors client `scale` values is properly set to a string.
- `TimedFunction` is no longer tied to an actor and will be executed on the server fake player.
  - Tags are also no longer required.
  - To get the scoreboard objective for the TimedFunction, call it's str representation.
  - To test if the TimedFunction has finished it's run, check if the objective is equal to -1.
- Added an error validation for path length exceeding 80 characters.
- Anvil packaging function allows for applying an overlay to keyarts now.
- Replaced the Exporter Parent class with `AddonObject` and moved extensions and paths to each individual class.
- Moved `LootTable`, `Recipe`, `Particle` from the old `EngineComponent` to `AddonObject`.
- `Items` still rely on `EngineComponent` until the rework in `1.20`
- Removed unnecessary modules.
- Added an items module in preparation for the new items.
- Pack versioning is now supported using the `release` key in `config.ini`

### Components

- Added `InsideBlockNotifier()`, `Transformation()`, `Equipment()`, `EquipItem()` components
- Added `is_raider`, `is_variant`, `is_mark_variant`, `is_skin_id` filters.

### Blocks

- Fully implemented `BlockTransformation`, `BlockDisplayName` and `BlockCraftingTable` components.

### Items

- Added the basic Items class.
- Added `ItemDurability`, `ItemDisplayName`, `ItemFuel`, `ItemEntityPlacer`.
- Partially added `ItemIcon`.

### Commands

- Added `InputPermission()` command.
- Added `haspermission`, `hasitem`, `gamemode` and `scores` arguments to the target Selector.
- Added `Scoreboard()` command.

### Molang

- `&`, `|` and `~` binary operators wrap the expression in parentheses `()`.
- Added `RotationToCamera()`, `Health`, `MaxHealth`

> <span style="color:red">**Breaking behavior**</span>
>
> To ensure the interpreter functions as intended, it is recommended to wrap expressions in your own parentheses to insure a proper order of operations, as Anvil wraps expressions left to right, it may result in several bugs.
>
> For instance, consider the following example:
>
> `Query.Property('interacted') & Query.MarkVariant == 1`
>
> Although the expression may seem logical at first, it will be compiled to
>
> `"(q.property('starktma:interacted') && q.mark_variant) == 1"` which is not functioning correctly.
>
> To avoid this issue, we suggest writing the expression as follows:
>
> `Query.Property('interacted') & (Query.MarkVariant == 1)`

## Version 0.3.4

### Anvil

- Anvil clones the bedrock samples again, untracked. `https://github.com/Mojang/bedrock-samples.git`
- Updated to Release `1.19.71.02`
- Changed the CHANGELOG, README and TODO to md from rst.

### Components

- Added new components: `Projectile()`, `Explode()`, `KnockbackRoar()`, `MobEffect()`, `SpawnEntity()`, `AreaAttack()`, `Loot()`, `Float()`, `RandomStroll()`, `LookAtPlayer()`, `RandomLookAround()`, `HurtByTarget()`, `MeleeAttack()`, `RangedAttack()`, `Shooter()`, `SummonEntity()`, `Boss()`, `DelayedAttack()`, `MoveToBlock()`.
- Added `actor_health`, `random_chance`, `target_distance` Filters.

### Commands

- The `hide_particles` argument in particle commands has been improved.
- Added `Playsound()` command.

### Molang

- Added `GetEquippedItemName`, `Position`, `PositionDelta`, `ItemIsCharged`, `ItemInUseDuration`, `IsRiding`, `ModifiedMoveSpeed`, `IsDelayedAttacking`, `IsCharged`, `IsCasting`, `IsRoaring`, `MarkVariant`
- Fixed some bugs with arithmetic operations.

## Version 0.3.3

### Anvil

- Fixed the attachables class not copying the models to `RP/models/entity`.
- Updated to Release `1.19.70.02`
- Updated to Preview `1.19.80.20`
- Fixed a bug with Anvil UI where it caused asserts if no actionbar visibility condition was added.
- Fixed some bugs with the generated font characters clipping into each other.

### Blocks

- Updated `BlockSelectionBox()`.
- Removed `_BlockRotation()` and `_BlockPartVisibility()`.
- Added `_BlockTransformation()`.
- Added `permutation(condition)` to block servers.

### Components

- Added `Rideable()` Component.
- Added `is_riding` Filter.

### Commands

- Added the `ReplaceItem` command.

### Molang

- Expanded operation support to use Python operation natively.
  - Division: **a/b**
  - Floor Division: **a//b** → **math.floor(a/b)**
  - Modulo: **a%b** → **math.mod(a, b)**
  - Power: **a**b** → **math.pow(a, b)\*\*
  - Absolute value: **abs(a)** → **math.abs(a)**
  - Rounded value: **round(a)** → **math.round(a)**
- Added `BlockProperty`.

## Version 0.3.2

### Anvil

- Added a public to-do list.
- Added a basic `Animation()` class to create animations within Anvil.

### Molang

- Added `HeadXRotation`, `HeadYRotation`, `IsLocalPlayer`, `IsItemNameAny` queries.
- Values negation is now supported, `-Query.HeadXRotation`.
- Arithmetic operations now return a str wrapped in brackets, this is to avoid unintended behavior that may arise because of expressions like this:
  `q.life_time >= v.timer + 2` → `q.life_time >= (v.timer + 2)`

### Commands

- Expanded commands to support nbt.
- Added the Give command class with its nbt components.
- Added the `family` argument to the Target Selector.

### Blocks

- Added new components: `BlockCollisionBox`, `BlockCraftingTable`, `BlockPlacementFilter`.

## Version 0.3.1

### New

- Added `generate_font()` to the `Fonts()` class. Now you'll be able to generate the `default8` texture using a ttf/otf files.
- Added `PreferredPath`, `TargetNearbySensor`, `NearestAttackableTarget`, `RandomLookAround`, and `Timer` components.
- Added a basic `Geometry()` class to create models within Anvil.
- Added the filters `is_block`
- Molang now support subtraction and multiplication.
- Added a snippets module to serve as a host for useful and quick functions.

### Bug Fixes

- Fixed the ANVIL.mcworld packaging method, now outputs a non corrupted world.
- Fixed the cli tool not creating the config and .gitignore files.
- The workspace no longer lists the Minecraft logs folder, it generally has too many files which makes the IDE slow.

## Version 0.3.0 - Materials System

### New

- Added a basic Materials class.
- Molang variables can now access initiated variables, else throw errors.
- Added more queries.

### Bug Fixes

- 'enum' properties use the 'values' key instead of 'range'.

## Version 0.2.6

- Switch to use ConfigParser for the configuration instead of a simple json file.
- Added basic Filters class with few filters.
- Added `EnvironmentSensor` class.
- Removed automatic imports from `anvil.__init__` , now requires a manual import from `anvil.api` module.
- Added `DistanceFromCamera` to Query class.
- Updated the Query, Variable and Math classes methods to @staticmethods and @classmethods.
- Removed the requirement of using a block geometry in Blocks as the 16x cube is used by default.
- Removed the oldBlock class.
- Molang now support native comparison operators (==, !=, <, >, <=, >=), wrapping in strings is no longer necessary. `f'{Query.DistanceFromCamera} <= {sensor_range}'` is the same as `Query.DistanceFromCamera <= sensor_range`

## Version 0.2.5

- Sounds `load_on_low_memory` is set to `False` by default.
- UI `text_alignment` use `UITextAlignment` now instead of `UIAnchor`.

## Version 0.2.4

- Expanded Molang queries.
- Some improvements to the structure.

## Version 0.2.3

- Updated the StateManager to use the new Execute commands.
- Added Entity properties.
- Added the Holiday Blocks, Blocks components including Experimental, Events and Event Triggers.
- Added a Score to clock function.
- Added some queries.

## Version 0.2.2

- Updated to Python 3.11.
- Moved away from `setup.py` to `pyproject.toml`.
- Updated the Dialogue class.
- Added Fog class.
- Added Fog command.
- Updated commands classes.

## Version 0.2.1

- Untracked

## Version 0.2.0 - Major Architecture Rewrite

- Updated the Exporter to include file extension formats.
- Added a `TerrainTextures()` class to manage block textures.
- Added Music class to manage music, accessible through `ANVIL.music()`.
- Updated base classes `_Entity` to `_Actor`.
- Added `Attachables()` class.
- Added mcaddon function to ANVIL. compiles the project and exports as an `.mcaddon`.
- Exposed more Minecraft entity components.
- FileExtensions are now namespace_format dependent.
- Added a Tools script to host the new `StateManager()`, `Cinematics()` and `TimedFunction()`.
- Due to the change to the source of Vanilla asset packs, Anvil now relies on the Public Mojang repository `Mojang/bedrock-samples` instead of a local download.
- Updated Vanilla Items, Blocks and Entities identifiers to `release 1.19.31` and `preview 1.19.50.21`.
- Implemented a basic UI class with support for element triggers with `title` command and HUD modifications.
- UI implementations are moved to their own submodule `submodules/ui`.
- Moved all Actors classes `Entity and Attachable` to it's own submodule `submodules/actors`.
- Removed the option to download vanilla RP and BP. Vanilla assets are now hosted and maintained by Mojang on GitHub.
- `get_vanilla` method of entities now pulls directly from GitHub instead of relying on a local copy of Vanilla assets.
- Exposed more Minecraft entity components.

## Version 0.1.0 - Core Foundation

- Fixed incorrect names for White Dye, Black Dye,
- Updated boats icons.
- Finished adding the new spawn rules conditions.
- Updated StateManager.
- Functions with more than 10000 lines of code are now split into multiple functions.
- Entity events now append new entries instead of overwriting them if not called in the same line.
- Added (_run_command) to Entity Events, proceeded with `_`.
- Added a command validator to the commands namespace.
- Server animations now append new commands instead of overwriting them if not called in the same line.
- Reformatted Tellraw and Titleraw to support text, selector, score and translate of the rawtext components.
- Updated the Exported class to use the os.path.join function.
- Integrated AddDespawnMechanic and OptimizeEntity to the NewEntity class, now included with all entities.

## Version 0.0.0 -> 0.1.0

- Anvil was a collection of individual generator scripts with no unified structure or design.
