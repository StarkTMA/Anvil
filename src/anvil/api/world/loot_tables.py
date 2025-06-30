import os

from anvil import CONFIG
from anvil.lib.enums import LootPoolType, PotionId
from anvil.lib.lib import clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


# Legacy code, must improve
class _LootPool:
    class _entry:
        class _Functions:
            def __init__(self) -> None:
                pass

            def SetBookContent(self, author: str, title: str, *pages: str):
                self._func = {
                    "author": author,
                    "title": title,
                    "pages": [str(p) for p in pages],
                    "function": "set_book_contents",
                }
                return self

            def SetName(self, name: str):
                self._func = {"function": "set_name", "name": name}
                return self

            def SetLore(self, *lore: str):
                self._func = {"function": "set_lore", "lore": [lore]}
                return self

            def SpecificEnchants(self, *enchants: tuple[str, int]):
                self._func = {
                    "function": "specific_enchants",
                    "enchants": [{"id": enchant[0], "level": enchant[1]} for enchant in enchants],
                }
                return self

            def SetDamage(self, damage: tuple[float, float]):
                self._func = {
                    "function": "set_damage",
                    "damage": {
                        "min": clamp(damage[0], 0, 1),
                        "max": clamp(damage[1], 0, 1),
                    },
                }
                return self

            def SetCount(self, count: int | tuple[int, int]):
                if type(count) is tuple:
                    self._func = {
                        "function": "set_count",
                        "count": {"min": count[0], "max": count[1]},
                    }
                elif type(count) is int:
                    self._func = {"function": "set_count", "count": count}
                return self

            def SetData(self, data: int | tuple[int, int]):
                if type(data) is tuple:
                    self._func = {
                        "function": "set_data",
                        "data": {"min": data[0], "max": data[1]},
                    }
                elif type(data) is int:
                    self._func = {"function": "set_data", "data": data}
                return self

            def EnchantRandomly(self):
                self._func = {"function": "enchant_randomly"}
                return self

            def SetPotion(self, id: PotionId):
                self._func = {"function": "set_potion", "id": id}
                return self

            def _export(self):
                return self._func

        def __init__(
            self,
            name: str,
            count: int = 1,
            weight: int = 1,
            entry_type: LootPoolType = LootPoolType.Item,
        ) -> None:
            self._entry = {
                "type": entry_type.value,
                "name": name,
                "count": count,
                "weight": weight,
            }
            self._functions = []

        def quality(self, quality: int):
            self._entry.update({"quality": quality})

        @property
        def functions(self):
            function = self._Functions()
            self._functions.append(function)
            return function

        def _export(self):
            for function in self._functions:
                if "functions" not in self._entry:
                    self._entry.update({"functions": []})
                self._entry["functions"].append(function._export())
            return self._entry

    def __init__(
        self,
        rolls: int | list[int, int] = 1,
        loot_type: LootPoolType = LootPoolType.Item,
    ):
        self._pool = {}
        self._entries = []
        if type(rolls) is int:
            self._pool.update({"rolls": rolls})
        elif type(rolls) is tuple:
            self._pool.update({"rolls": {rolls[0], rolls[1]}})
        self._pool.update({"type": loot_type.value})

    def tiers(self, bonus_chance: int = 0, bonus_rolls: int = 0, initial_range: int = 0):
        self._pool.update({"tiers": {}})
        if bonus_chance != 0:
            self._pool["tiers"].update({"bonus_chance": bonus_chance})
        if bonus_rolls != 0:
            self._pool["tiers"].update({"bonus_rolls": bonus_rolls})
        if initial_range != 0:
            self._pool["tiers"].update({"initial_range": initial_range})

    def entry(
        self,
        name: str,
        count: int = 1,
        weight: int = 1,
        entry_type: LootPoolType = LootPoolType.Item,
    ):
        entry = self._entry(str(name), count, weight, entry_type)
        self._entries.append(entry)
        return entry

    def _export(self):
        for entry in self._entries:
            if "entries" not in self._pool:
                self._pool.update({"entries": []})
            self._pool["entries"].append(entry._export())
        return self._pool


class LootTable(AddonObject):
    """A class representing a LootTable."""

    _extension = ".loot_table.json"
    _path = os.path.join(CONFIG.BP_PATH, "loot_tables", CONFIG.NAMESPACE)

    def __init__(self, name: str):
        """Initializes a LootTable instance.

        Parameters:
            name (str): The name of the LootTable.
        """
        super().__init__(name)
        self._content = JsonSchemes.loot_table()
        self._pools = []

    def pool(
        self,
        rolls: int | list[int, int] = 1,
        loot_type: LootPoolType = LootPoolType.Item,
    ):
        pool = _LootPool(rolls, loot_type)
        self._pools.append(pool)
        return pool

    @property
    def path(self):
        return os.path.join("loot_tables", CONFIG.NAMESPACE, self._directory, self._name + self._extension)

    def queue(self, directory: str = ""):
        for pool in self._pools:
            self._content["pools"].append(pool._export())
        self.content(self._content)
        self._directory = directory
        return super().queue(directory=directory)
