# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

MANIFEST_VERSION: int = 3
MANIFEST_BUILD: str = "1.26.10"
MANIFEST_BUILD_PREVIEW: str = "1.26.20"

# ---------------------------------------------------------------------------
# Content-type format versions (all currently track MANIFEST_BUILD)
# ---------------------------------------------------------------------------

BLOCK_SERVER_VERSION: str = MANIFEST_BUILD
ENTITY_SERVER_VERSION: str = MANIFEST_BUILD
ENTITY_CLIENT_VERSION: str = MANIFEST_BUILD
ITEM_SERVER_VERSION: str = MANIFEST_BUILD
RECIPE_JSON_FORMAT_VERSION: str = MANIFEST_BUILD
SPAWN_RULES_VERSION: str = "1.8.0"
SOUND_DEFINITIONS_VERSION: str = MANIFEST_BUILD
FOG_VERSION: str = MANIFEST_BUILD
JIGSAW_VERSION: str = MANIFEST_BUILD
BIOME_SERVER_VERSION: str = MANIFEST_BUILD
BIOME_CLIENT_VERSION: str = MANIFEST_BUILD
PBR_SETTINGS_VERSION: str = MANIFEST_BUILD

# ---------------------------------------------------------------------------
# Animation / rendering
# ---------------------------------------------------------------------------

ANIMATION_CONTROLLERS_VERSION: str = "1.10.0"
BP_ANIMATION_VERSION: str = "1.10.0"
RP_ANIMATION_VERSION: str = "1.10.0"
RENDER_CONTROLLER_VERSION: str = "1.10.0"
GEOMETRY_VERSION: str = "1.21.20"
MATERIALS_VERSION: str = "1.0.0"
CAMERA_PRESET_VERSION: str = "1.21.0"
BLOCK_CULLING_VERSION: str = "1.20.80"
TEXTURE_SET_VERSION: str = "1.21.30"

# ---------------------------------------------------------------------------
# Block / item / world JSON format versions
# ---------------------------------------------------------------------------

BLOCK_JSON_FORMAT_VERSION: str = "1.21.40"
CRAFTING_ITEMS_CATALOG: str = "1.21.60"
DIALOGUE_VERSION: str = "1.18.0"

# ---------------------------------------------------------------------------
# Script API module versions
# ---------------------------------------------------------------------------

MODULE_MINECRAFT_SERVER: str = "2.6.0"
MODULE_MINECRAFT_SERVER_UI: str = "2.0.0"
MODULE_MINECRAFT_SERVER_PREVIEW: str = "2.8.0-beta"
MODULE_MINECRAFT_SERVER_UI_PREVIEW: str = "2.1.0-beta"
MODULE_MINECRAFT_SERVER_EDITOR: str = "0.1.0"
MODULE_MINECRAFT_SERVER_GAMETEST: str = "1.0.0"
MODULE_MINECRAFT_SERVER_GRAPHICS: str = "1.0.0-beta"
