# Changelog

---

Version 0.3.5
=============
  [Anvil]
  -------
  - Updated the extensions of generated files.
  - Vanilla entities are automatically exported to the vanilla directory, regardless of the provided directory.
  - Updated to release ``1.19.81.01`` and preview ``1.20.0.20``.
  - Actors client ``scale`` values is properly set to a string.
  - ``TimedFunction`` is no longer tied to an actor and will be executed on the server fake player.
    - Tags are also no longer required.
    - To get the scoreboard objective for the TimedFunction, call it's str representation.
    - To test if the TimedFunction has finished it's run, check if the objective is equal to -1.
  - Added an error validation for path length exceeding 80 characters.
  - Anvil packaging function allows for applying an overlay to keyarts now.
  - Replaced the Exporter Parent class with ``AddonObject`` and moved extensions and paths to each individual class.
  - Moved ``LootTable``, ``Recipe``, ``Particle`` from the old ``EngineComponent`` to ``AddonObject``.
  - ``Items`` still rely on ``EngineComponent`` until the rework in ``1.20``
  - Removed unnecessary modules.
  - Added an items module in preparation for the new items.
  - Pack versioning is now supported using the ``release`` key in ``config.ini``
  
  [Components]
  ------------
  - Added ``InsideBlockNotifier()``, ``Transformation()``, ``Equipment()``, ``EquipItem()`` components
  - Added ``is_raider``, ``is_variant``, ``is_mark_variant``, ``is_skin_id`` filters.
  
  [Blocks]
  --------
  - Fully implemented ``BlockTransformation``, ``BlockDisplayName`` and ``BlockCraftingTable`` components.
  - 
  
  [Items]
  --------
  - Added the basic Items class.
  - Added ``ItemDurability``, ``ItemDisplayName``, ``ItemFuel``, ``ItemEntityPlacer``.
  - Partially added ``ItemIcon``.

  [Commands]
  ----------
  - Added ``InputPermission()`` command.
  - Added ``haspermission``, ``hasitem``, ``gamemode`` and ``scores`` arguments to the target Selector.
  - Added ``Scoreboard()`` command.
  
  [Molang]
  --------
  - `&`, `|` and `~` binary operators wrap the expression in parentheses `()`.
  - Added ``RotationToCamera()``, ``Health``, ``MaxHealth``

> <span style="color:red">**Breaking behaviour**</span>
> 
  >To ensure the interpreter functions as intended, it is recommended to wrap expressions in your own parentheses to insure a proper order of operations, as Anvil wraps expressions left to right, it may result in several bugs.
  >
  >For instance, consider the following example:
  >  
  >``Query.Property('interacted') & Query.MarkVariant == 1``
  >  
  > Although the expression may seem logical at first, it will be compiled to 
  >
  >``"(q.property('starktma:interacted') && q.mark_variant) == 1"`` which is not functioning correctly.
  >  
  >To avoid this issue, we suggest writing the expression as follows:
  >  
  >``Query.Property('interacted') & (Query.MarkVariant == 1)``

---

Version 0.3.4
=============
  [Anvil]
  -------
  - Anvil clones the bedrock samples again, untracked. `https://github.com/Mojang/bedrock-samples.git`
  - Updated to Release ``1.19.71.02``
  - Changed the CHANGELOG, README and TODO to md from rst.
  
  [Components]
  ------------
  - Added new components: `Projectile()`, `Explode()`, `KnockbackRoar()`, `MobEffect()`, `SpawnEntity()`, `AreaAttack()`, `Loot()`, `Float()`, `RandomStroll()`, `LookAtPlayer()`, `RandomLookAround()`, `HurtByTarget()`, `MeleeAttack()`, `RangedAttack()`, `Shooter()`, `SummonEntity()`, `Boss()`, `DelayedAttack()`, `MoveToBlock()`.
  - Added `actor_health`, `random_chance`, `target_distance` Filters.
  
  [Commands]
  ----------
  - The `hide_particles` argument in the 
  - Added `Playsound()`,
  
  [Molang]
  --------
  - Added `GetEquippedItemName`, `Position`, `PositionDelta`, `ItemIsCharged`, `ItemInUseDuration`, `IsRiding`, `ModifiedMoveSpeed`, `IsDelayedAttacking`, `IsCharged`, `IsCasting`, `IsRoaring`, `MarkVariant`
  - Fixed some bugs with arithmetic operations.
  - 
  
---

Version 0.3.3
=============
  [Anvil]
  --------
  - Fixed the attachables class not  copying the models to `RP/models/entity`.
  - Updated to Release 1.19.70.02
  - Updated to Preview 1.19.80.20
  - Fixed a bug with Anvil UI where it caused asserts if no actionbar visibility condition was added.
  - Fixed some bugs with the generated font characters clipping into each other.
  
  [Blocks]
  --------
  - Updated `BlockSelectionBox()`.
  - Removed `_BlockRotation()` and `_BlockPartVisibility()`.
  - Added `_BlockTransformation()`.
  - Added `permutation(condition)` to block servers.
  
  [Components]
  ------------
  - Added `Rideable()` Component.
  - Added `is_riding` Filter.
  
  [Commands]
  ----------
  - Added the `ReplaceItem` command.
  
  [Molang]
  --------
  - Expanded operation support to use Python operation natively.
     - Division: **a/b** 
     - Floor Division: **a//b** => **math.floor(a/b)**
     - Modulo: **a%b** => **math.mod(a, b)**
     - Power: **a**b** => **math.pow(a, b)**
     - Absolute value: **abs(a)** => **math.abs(a)**
     - Rounded value: **round(a)** => **math.round(a)**
  - Added `BlockProperty`.
  
---

Version 0.3.2
=============
  [Anvil]
  --------
  - Added a public to-do list.
  - Added a basic `Animation()` class to create animations within Anvil.
  
  [Molang]
  --------
  - Added `HeadXRotation`, `HeadYRotation`, `IsLocalPlayer`, `IsItemNameAny` queries.
  - Values negation is now supported, `-Query.HeadXRotation`.
  - Arithmitic operations now return a str wrapped in brackets, this is to avoid unintended behaviour that may arise because of expressions like this:
      `q.life_time >= v.timer + 2` => `q.life_time >= (v.timer + 2)`
  
  [Commands]
  ----------
  - Expanded commands to support nbt.
  - Added the Give command class with its nbt components.
  - Added the `family` argument to the Target Selector.
  
  [Blocks]
  --------
    - Added new components: `BlockCollisionBox`, `BlockCraftingTable`, `BlockPlacementFilter`.
  
---

Version 0.3.1
=============
  [New]
  -----
  - Added `generate_font()` to the `Fonts()` class. Now you'll be able to generate the `default8` texture using a ttf/otf files.
  - Added `PreferredPath`, `TargetNearbySensor`, `NearestAttackableTarget`, `RandomLookAround`, and `Timer` components.
  - Added a basic `Geometry()` class to create models within Anvil.
  - Added the filters `is_block`, 
  - Molangs now support subtraction and multiplication.
  - Added a snippets module to serve as a host for useful and quick functions.
  [Bug Fixes]
  -----------
  - Fixed the ANVIL.mcworld packagin method, now output a non corrupted world.
  - Fixed the cli tool not creating the config and .gitignore files..
  - The worksapce no longer lists the Minecraft logs folder, it generally has too many files which makes the IDE slow.

---

Version 0.3.0
=============
  [New]
  -----
  - Added a basic Materials class.
  - Molang variables can now access initiated variables, else throw errors.
  - Added more queries.
  
  [Bug Fixes]
  -----------
  - 'enum' properties use the 'values' key instead of 'range'.
  
---

Version 0.2.6
=============
  - Switch to use ConfigParser for the configuration instead of a simple json file.
  - Added basic Filters class with few filters.
  - Added `EnvironmentSensor` class.
  - Removed automatic imports from `anvil.__init__` , now requires a manual import from `anvil.api` module.
  - Added `DistanceFromCamera` to Query class.
  - Updated the Query, Variable and Math classes methods to @staticmethods and @classmethods.
  - Removed the requirement of using a block geometry in Blocks as the 16x cube is used by default.
  - Removed the oldBlock class.
  - Molang now support native comparison operators (==, !=, <, >, <=, >=), wrapping in strings is no longer necessary. f'{Query.DistanceFromCamera} <= {sensor_range}' is that same as Query.DistanceFromCamera <= sensor_range

---

Version 0.2.5
=============
  - Sounds ``load_on_low_memory`` is set to `False` by default.
  - UI `text_alignment` use `UITextAlignment` now instead of `UIAnchor`.
  
---

Version 0.2.4
=============
  - Expanded Molang queries.
  - Some improvements to the structure.
  
---

Version 0.2.3
=============
  - Updated the StateManager to use the new Execute commands.
  - Added Entity properties.
  - Added the Holiday Blocks, Blocks components including Experimental, Events and Event Triggers.
  - Added a Score to clock function.
  - Added some queries.

---

Version 0.2.2
=============
  - Updated to Python 3.11.
  - Moved away from `setup.py` to `pyproject.toml`.
  - Updated the Dialogue class.
  - Added Fog class.
  - Added Fog command.
  - Updated commands classes.
  
---

Version 0.2.1
=============
  - Untracked
  
---
   
Version 0.2.0
=============
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

---

Version 0.1.0
=============
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
  - Updated the Exported class to use the MakePath function.
  - Integrated AddDespawnMechanic and OptimizeEntity to the NewEntity class, now included with all entities.
   
---

Version 0.0.0 -> 0.1.0
======================
  - Untracked
  
---