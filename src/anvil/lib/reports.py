import os
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepInFrame,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from ..__version__ import __version__


class ReportType(StrEnum):
    SOUND = "sound"
    ENTITY = "entity"
    ATTACHABLE = "attachable"
    ITEM = "item"
    BLOCK = "block"
    PARTICLE = "particle"
    BIOME = "biome"


_SECTIONS: tuple[tuple[str, ReportType, dict[str, str]], ...] = (
    ("Entities:", ReportType.ENTITY, {"col3": "Property count"}),
    ("Attachables:", ReportType.ATTACHABLE, {}),
    ("Items:", ReportType.ITEM, {}),
    ("Blocks:", ReportType.BLOCK, {}),
    ("Particles:", ReportType.PARTICLE, {}),
    ("Sounds:", ReportType.SOUND, {}),
)

_TABLE_STYLE_COMMANDS: tuple[tuple, ...] = (
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("FONTSIZE", (0, 0), (-1, 0), 12),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
)


def _yes_no(value) -> str:
    return "Yes" if value else "No"


def _joined(value) -> str:
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(v) for v in value) or "N/A"
    return str(value) if value not in (None, "") else "N/A"


@dataclass
class ReportRow:
    """A single row of a report table: a name plus a set of accumulated
    values per column, and whether the row represents a vanilla (unmodified)
    entry that should be highlighted in the generated PDF."""

    name: str
    vanilla: bool = False
    columns: dict[str, set[str]] = field(default_factory=dict)

    def update_column(self, col_name: str, value) -> None:
        bucket = self.columns.setdefault(col_name, set())
        if isinstance(value, (list, tuple, set)):
            bucket.update(str(v) for v in value)
        else:
            bucket.add(str(value))


class ReportCollector:
    def __init__(self) -> None:
        # ReportType -> row name -> ReportRow
        self.dict: defaultdict[ReportType, dict[str, ReportRow]] = defaultdict(dict)

        self.styles = getSampleStyleSheet()
        self.normal_style = self.styles["Normal"]
        self.title_style = self.styles["Heading1"]
        self.body_style = self.styles["BodyText"]
        self.bullet_style = self.styles["Bullet"]

        self.title_style.spaceBefore = 0
        self.title_style.fontSize = 14
        self.title_style.textColor = colors.royalblue

        self.elements = []

    def add_headers(self):
        self.add_report(
            ReportType.SOUND, col0="Sound identifier", col1="Sounds", vanilla=False
        )
        self.add_report(
            ReportType.ENTITY,
            col0="Entity Name",
            col1="Entity identifier",
            col2="Entity Events",
            col3="Entity Properties",
            vanilla=False,
        )
        self.add_report(
            ReportType.ATTACHABLE,
            col0="Attachable Name",
            col1="Attachable identifier",
            vanilla=False,
        )
        self.add_report(
            ReportType.ITEM, col0="Item Name", col1="Item identifier", vanilla=False
        )
        self.add_report(
            ReportType.BLOCK,
            col0="Block Name",
            col1="Block identifier",
            col2="Block States",
            vanilla=False,
        )
        self.add_report(
            ReportType.PARTICLE,
            col0="Particle Name",
            col1="Particle identifier",
            vanilla=False,
        )
        self.add_report(
            ReportType.BIOME, col0="Biome Name", col1="Biome identifier", vanilla=False
        )
        return self

    def add_report(
        self, report_type: ReportType, col0: str, vanilla: bool = False, **columns
    ) -> None:
        rows = self.dict[report_type]
        row = rows.setdefault(col0, ReportRow(name=col0))
        row.vanilla = bool(vanilla)
        for col_name, col_value in columns.items():
            row.update_column(col_name, col_value)

    @staticmethod
    def _column_widths(doc_width: float, num_cols: int) -> list[float]:
        if num_cols <= 1:
            return [doc_width]
        first = doc_width / (num_cols + 1)
        rest = (doc_width - first) / (num_cols - 1)
        return [first] + [rest] * (num_cols - 1)

    def _make_table(
        self,
        rows: list[list[str]],
        doc_width: float,
        doc_height: float,
        highlight_rows: frozenset[int] = frozenset(),
    ) -> Table:
        col_widths = self._column_widths(doc_width, len(rows[0]))
        max_cell_height = max(doc_height - 4 * cm, 4 * cm)
        normal_style = self.normal_style

        def cell(text: str, width: float) -> KeepInFrame:
            return KeepInFrame(
                width,
                max_cell_height,
                [Paragraph(text, normal_style)],
                mode="shrink",
            )

        data = [
            [cell(value, width) for value, width in zip(row, col_widths)]
            for row in rows
        ]

        table = Table(data, hAlign="LEFT", colWidths=col_widths)
        style_commands = list(_TABLE_STYLE_COMMANDS)
        style_commands.extend(
            ("BACKGROUND", (0, row), (-1, row), colors.lightgreen)
            for row in highlight_rows
        )
        table.setStyle(TableStyle(style_commands))
        return table

    def add_table(
        self,
        doc_width: float,
        doc_height: float,
        section_name: str,
        rows: dict[str, ReportRow],
        count_labels: dict[str, str] = {},
    ):
        if not rows:
            return []

        # Keep the header row (added by add_headers) first, then sort the
        # remaining rows alphabetically by their display name.
        header_row, *data_rows = rows.values()
        data_rows.sort(key=lambda row: row.name.casefold())
        ordered_rows = [header_row, *data_rows]

        table_rows: list[list[str]] = []
        highlight_rows: set[int] = set()

        for idx, row in enumerate(ordered_rows):
            if row.vanilla:
                highlight_rows.add(idx)

            values = []
            for col_name, col_values in row.columns.items():
                value_string = "<br/>".join(sorted(col_values, key=str.casefold))
                label = count_labels.get(col_name)
                if label and idx > 0:
                    value_string = f"{label} ({len(col_values)}):<br/>{value_string}"
                values.append(value_string)
            table_rows.append([row.name, *values])

        title = Paragraph(section_name, self.title_style)
        table = self._make_table(
            table_rows, doc_width, doc_height, frozenset(highlight_rows)
        )
        return [title, Spacer(1, 0.3 * cm), table, Spacer(1, 1 * cm)]

    def _project_info_rows(self, CONFIG) -> list[list[str]]:
        return [
            ["Anvil Version", __version__],
            ["Project Name", _joined(getattr(CONFIG, "PROJECT_NAME", None))],
            ["Namespace", _joined(getattr(CONFIG, "NAMESPACE", None))],
            ["Display Name", _joined(getattr(CONFIG, "DISPLAY_NAME", None))],
            ["Company", _joined(getattr(CONFIG, "COMPANY", None))],
            ["Package Target", _joined(getattr(CONFIG, "_TARGET", None))],
            ["Release Version", _joined(getattr(CONFIG, "_RELEASE", None))],
            [
                "Vanilla Version Target",
                _joined(getattr(CONFIG, "_VANILLA_VERSION", None)),
            ],
            ["Preview Build", _yes_no(getattr(CONFIG, "_PREVIEW", False))],
            ["Script API", _yes_no(getattr(CONFIG, "_SCRIPT_API", False))],
            ["Script UI", _yes_no(getattr(CONFIG, "_SCRIPT_UI", False))],
            ["PBR", _yes_no(getattr(CONFIG, "PBR", False))],
            ["Random Seed", _yes_no(getattr(CONFIG, "_RANDOM_SEED", False))],
            ["Experimental Features", _yes_no(getattr(CONFIG, "_EXPERIMENTAL", False))],
            ["Resource Pack UUID", _joined(getattr(CONFIG, "_RP_UUID", None))],
            ["Behavior Pack UUID", _joined(getattr(CONFIG, "_BP_UUID", None))],
            ["Pack UUID", _joined(getattr(CONFIG, "_PACK_UUID", None))],
        ]

    def generate_report(self) -> None:
        from anvil.lib.config import CONFIG

        self.doc = SimpleDocTemplate(
            os.path.join("output", "technical_notes.pdf"),
            pagesize=A4,
            leftMargin=1 * cm,
            rightMargin=1 * cm,
            topMargin=1 * cm,
            bottomMargin=1 * cm,
            title=f"{CONFIG.DISPLAY_NAME} Technical Notes",
            author=CONFIG.COMPANY,
            subject=f"{CONFIG.DISPLAY_NAME} Technical Notes",
            creator=f"Anvil@StarkTMA {__version__}",
        )

        doc_width, doc_height = self.doc.width, self.doc.height

        info_table = self._make_table(
            self._project_info_rows(CONFIG), doc_width, doc_height
        )

        self.elements = [
            Paragraph(f"{CONFIG.DISPLAY_NAME}:", self.title_style),
            Paragraph(f"Developed by: {CONFIG.COMPANY}", self.body_style),
            Paragraph(
                f'Generated with <a href="https://github.com/StarkTMA/Anvil"><u><font color="blue">StarkTMA/Anvil {__version__}</font></u></a>',
                self.body_style,
            ),
            Spacer(1, 1 * cm),
            info_table,
            Spacer(1, 1 * cm),
            Paragraph("General information:", self.title_style),
            Paragraph(
                "The following technical notes have been entirely generated from source code using Anvil.",
                self.body_style,
            ),
            Paragraph(
                "Features overwriting vanilla defaults will be highlighted in green.",
                self.bullet_style,
                "*",
            ),
            Spacer(1, 1 * cm),
        ]

        for section_name, report_type, count_labels in _SECTIONS:
            section = self.add_table(
                doc_width,
                doc_height,
                section_name,
                CONFIG.Report.dict[report_type],
                count_labels,
            )
            if not section:
                continue
            self.elements.append(PageBreak())
            self.elements.extend(section)

        self.doc.build(self.elements)
