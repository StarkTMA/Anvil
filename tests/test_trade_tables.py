import jsonschema
import pytest

from anvil.api.world.trade_tables import TradeTable
from anvil.lib.lib import AnvilIO


def _json(file):
    return AnvilIO._normalize_json_like(file._document)


def test_trade_table():
    table = TradeTable("fisher")
    trade = table.tier(0).group(2).trade(max_uses=12, trader_exp=5)
    trade.add_wants("minecraft:cod", (6, 10)).add_wants("minecraft:emerald", 1, 0.2)
    trade.add_gives("minecraft:fishing_rod").EnchantWithLevels((5, 19)).SetDamage(0.5)

    assert _json(table) == {
        "tiers": [
            {
                "total_exp_required": 0,
                "groups": [
                    {
                        "num_to_select": 2,
                        "trades": [
                            {
                                "wants": [
                                    {
                                        "item": "minecraft:cod",
                                        "quantity": {"min": 6, "max": 10},
                                        "price_multiplier": 0.05,
                                    },
                                    {
                                        "item": "minecraft:emerald",
                                        "quantity": 1,
                                        "price_multiplier": 0.2,
                                    },
                                ],
                                "gives": [
                                    {
                                        "item": "minecraft:fishing_rod",
                                        "quantity": 1,
                                        "functions": [
                                            {
                                                "function": "enchant_with_levels",
                                                "levels": {"min": 5, "max": 19},
                                                "treasure": False,
                                            },
                                            {"function": "set_damage", "damage": 0.5},
                                        ],
                                    }
                                ],
                                "trader_exp": 5,
                                "max_uses": 12,
                                "reward_exp": True,
                            }
                        ],
                    }
                ],
            }
        ]
    }
    assert table.table_path.startswith("trading/")
    jsonschema.validate(_json(table), TradeTable.__schema__())


def test_trade_item_needs_an_item():
    trade = TradeTable("empty").tier(0).group().trade()
    with pytest.raises(ValueError, match="cannot be None"):
        trade.add_wants(None)
