"""One self-contained file per block; none imports another.

Each exposes `create(wood, selected) -> Block`: `wood` is the set name ("rotten") and
`selected` holds the names of every block in the set ("planks", "log_stripped", ...), used
to skip recipes and features that need a block the set doesn't have. `create` builds the
block, names it, queues it and registers the recipes that make it.
"""
