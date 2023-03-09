=========
Changelog
=========

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
 - 

[Bug Fixes]
-----------
 - Fixed the ANVIL.mcworld packagin method, now output a non corrupted world.
 - Fixed the cli tool not creating the config and .gitignore files..
 - The worksapce no longer lists the Minecraft logs folder, it generally has too many files which makes the IDE slow.

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

Version 0.2.5
=============
 - Sounds ``load_on_low_memory`` is set to `False` by default.
 - UI `text_alignment` use `UITextAlignment` now instead of `UIAnchor`.

Version 0.2.4
=============
 - Expanded Molang queries.
 - Some improvements to the structure.

Version 0.2.3
=============
 - Updated the StateManager to use the new Execute commands.
 - Added Entity properties.
 - Added the Holiday Blocks, Blocks components including Experimental, Events and Event Triggers.
 - Added a Score to clock function.
 - Added some queries.

Version 0.2.2
=============
 - Updated to Python 3.11.
 - Moved away from `setup.py` to `pyproject.toml`.
 - Updated the Dialogue class.
 - Added Fog class.
 - Added Fog command.
 - Updated commands classes.

Version 0.2.1
=============
 - Untracked
 
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
 -

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
 -
 
Version 0.0.0 -> 0.1.0
======================
- Untracked