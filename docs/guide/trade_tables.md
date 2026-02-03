# Creating Trade Tables

This guide explains how to define trading options for villagers using the `TradeTable` API. Trade tables allow you to customize what items entities buy and sell, organize them into unlockable tiers, and group them for randomized selection.

---

## Direct API Usage

The `TradeTable` API uses a fluent interface, allowing you to chain methods to build your hierarchy of tiers, groups, and trades.

```python title="trading/my_trader.py"
from anvil.api.world.trade_tables import TradeTable
from anvil.api.vanilla.items import MinecraftItemTypes

# 1. Create the table
table = TradeTable("my_trader")

# 2. Add a Tier (Level 1, 0 XP required)
tier_1 = table.tier(total_exp_required=0)

# 3. Add a Group (Selects 1 trade from the list)
group_1 = tier_1.group(num_to_select=1)

# 4. Add a specific Trade
# Wants 1 Emerald -> Gives 5 Apples
group_1.trade(max_uses=7, reward_exp=True).wants(
    MinecraftItemTypes.Emerald(), quantity=1
).gives(
    MinecraftItemTypes.Apple(), quantity=5
)

# You can also chain everything in one go:
table.tier(total_exp_required=10).group(num_to_select=2).trade(
    max_uses=5
).wants(
    MinecraftItemTypes.Diamond(), 1
).gives(
    "my_custom:sword", 1
)

# 5. Queue for export
table.queue()
```

!!! warning "Export rule"
    You **must** call `.queue()` on your `TradeTable` object. If you skip this, Anvil **will not export** the JSON file to your behavior pack.

!!! tip "Items"
    You can use string identifiers (e.g. `"minecraft:apple"`), `Identifier` objects, or Anvil's typed helpers (like `MinecraftItemTypes.Apple()`) for items.

---

## Data-Driven Approach

For complex traders with many tiers and options, defining trades in a dictionary and looping through it can be cleaner and more maintainable.

```python title="trading/harbour_folk_trades.py"
from anvil.api.world.trade_tables import TradeTable
from anvil.api.vanilla.items import MinecraftItemTypes

def create_trades():
    # Define your data structure
    trades_data = {
        "novice": {
            "min_experience": 0,
            "groups": [
                {
                    "select": 1,
                    "trades": [
                        {
                            "wants": [{"item": MinecraftItemTypes.Emerald(), "count": 1}],
                            "gives": [{"item": MinecraftItemTypes.Bread(), "count": 6}],
                            "stock": 16,
                            "xp": 2
                        }
                    ]
                }
            ]
        },
        "apprentice": {
            "min_experience": 10,
            "groups": [
                {
                    "select": 1,
                    "trades": [
                        {
                            "wants": [{"item": MinecraftItemTypes.IronIngot(), "count": 4}],
                            "gives": [{"item": MinecraftItemTypes.Emerald(), "count": 1}],
                            "stock": 12,
                            "xp": 10
                        }
                    ]
                }
            ]
        }
    }

    # Create the table object
    trade_table = TradeTable("harbour_folk_resource_trader")

    # Loop through the data to build the table
    for level, data in trades_data.items():
        # Create the tier
        tier = trade_table.tier(data["min_experience"])

        for group_data in data["groups"]:
            # Create a group within the tier
            trade_group = tier.group(group_data["select"])

            for trade_def in group_data["trades"]:
                # Create the trade
                trade = trade_group.trade(
                    max_uses=trade_def.get("stock", 10),
                    reward_exp=True,
                    trader_exp=trade_def.get("xp", 1),
                )

                # Add 'wants' (Cost)
                for want in trade_def["wants"]:
                    trade.wants(
                        item=want["item"],
                        quantity=want["count"],
                        price_multiplier=0.05
                    )

                # Add 'gives' (Reward)
                for give in trade_def["gives"]:
                    trade.gives(
                        item=give["item"],
                        quantity=give["count"]
                    )

    # Queue the table for export
    trade_table.queue()
    return trade_table
```

!!! info "Structure"
    The hierarchy is always **Table -> Tiers -> Groups -> Trades**. - **Tiers** unlock based on villager XP. - **Groups** determine how many trades are picked from a pool (useful for RNG). - **Trades** define the actual exchange (inputs/outputs).

---

## Modifying Trades

The `.gives()` method returns a `_TradeItemGives` object which inherits from loot pool functions. This allows you to add modifiers like enchantments to the traded item.

```python
# Trade that gives an enchanted sword
trade.gives(MinecraftItemTypes.IronSword(), 1).enchant_with_levels(
    levels=30,
    treasure=True
)
```

!!! check "Efficiency"
    Using the loop approach is recommended for entities with standard profession hierarchies (Novice, Apprentice, Journeyman, etc.) to keep your code DRY (Don't Repeat Yourself).
