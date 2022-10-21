=========
Changelog
=========

Version 0.2.0
===========
 - Updated the Exporter to include file extension formats.
 - Added a `TerrainTextures()` class to manage block textures.
 - Added Music class to manage music, accessible through `ANVIL.music()`.
 - Updated base classes `_Entity` to `_Actor`.
 - Added `Attachables()` class.
 - Added mcaddon function to ANVIL. compiles the project and exports as an `.mcaddon`.
 - Exposed more Minecraft entity components.
 - FileExtensions are now namespace_format dependent.
 - Added a Tools script to host the new `State_Manager()`, `Cinematics()` and `TimedFunction()`.
 - Due to the change to the source of Vanilla asset packs, Anvil now relies on the Public Mojang repository `Mojang/bedrock-samples` instead of a local download.
 - Updated Vanilla Items, Blocks and Entities identifiers to `release 1.19.31` and `preview 1.19.50.21`.
 - Implemented a basic UI class with support for element triggers with `title` command and HUD modifications.
 - UI implementations are moved to their own submodule `submodules/ui`.
 - Moved all Actors classes `Entity and Attachable` to it's own submodule `submodules/actors`.
 - Removed the option to download vanilla RP and BP. Vanilla assets are now hosted and maintained by Mojang on GitHub.
 - `get_vanilla` method of entities now pulls directly from GitHub instead of relying on a local copy of Vanilla assets.
 - Exposed more Minecraft entity components.

Version 0.1.0
===========
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

Version 0.0.0 -> 0.1.0
===========
- Untracked