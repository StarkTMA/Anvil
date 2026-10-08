"""One self-contained file per block; none imports another.

Each exposes `create(wood, selected) -> Block`: `wood` is the set name ("rotten") and
`selected` holds the names of every block in the set ("planks", "log_stripped", ...), used
to skip recipes and features that need a block the set doesn't have. `create` builds the
block, names it, queues it and registers the recipes that make it.
"""

# The Blockbench models every wood set shares, so only the names differ between sets
MODEL = "wood_set"
"""The block collections (`assets/bbmodels/wood_set.bbmodel`). It also holds the block
textures of every wood set, named `<name>_planks`, `<name>_log` and so on."""

BOAT_MODEL = "wood_set_boat"
"""Both boats (`assets/bbmodels/wood_set_boat.bbmodel`), with the boat texture of every wood
set, named `<name>_boat`."""
