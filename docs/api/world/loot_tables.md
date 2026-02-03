# World - Loot Tables Module

::: anvil.api.world.loot_tables

## Usage Example

```python
from anvil.api.world.loot_tables import LootTable
from anvil.api.vanilla.items import MinecraftItemTypes

table = LootTable("my_loot")
pool = table.pool(rolls=1)

# Add simple items
pool.entry(MinecraftItemTypes.Apple(), weight=5)
pool.entry(MinecraftItemTypes.GoldenApple(), weight=1)

# Add complex items with functions
pool.entry(MinecraftItemTypes.DiamondSword(), weight=1).enchant_with_levels(30)

table.queue()
```
