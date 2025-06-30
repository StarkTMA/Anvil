from collections import defaultdict
from enum import StrEnum


class ReportType(StrEnum):
    SOUND = "sound"
    ENTITY = "entity"
    ATTACHABLE = "attachable"
    ITEM = "item"
    BLOCK = "block"
    PARTICLE = "particle"


class ReportCollector:
    def __init__(self) -> None:
        """A dictionary where keys are ReportType and values are `list[defaultdict]`.
        These inner `defaultdict` will automatically create a key if it doesn't exist
        and initialize it to a dictionary of empty sets.

        The dictionary is later used to generate a report of what have been added to the pack.
        """
        self.dict = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

    def add_headers(self):
        self.add_report(ReportType.SOUND, col0="Sound identifier", col1="Sounds", vanilla=False)
        self.add_report(ReportType.ENTITY, col0="Entity Name", col1="Entity identifier", col2="Entity Events", vanilla=False)
        self.add_report(ReportType.ATTACHABLE, col0="Attachable Name", col1="Attachable identifier", vanilla=False)
        self.add_report(ReportType.ITEM, col0="Item Name", col1="Item identifier", vanilla=False)
        self.add_report(ReportType.BLOCK, col0="Block Name", col1="Block identifier", col2="Block States", vanilla=False)
        self.add_report(ReportType.PARTICLE, col0="Particle Name", col1="Particle identifier", vanilla=False)
        return self

    def add_report(self, report_type: ReportType, col0, **columns):
        for col_name, col_value in columns.items():
            if isinstance(col_value, tuple | set | list):
                self.dict[report_type][col0][col_name].update(col_value)
            else:
                self.dict[report_type][col0][col_name].add(str(col_value))
