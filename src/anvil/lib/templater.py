from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable, Dict

import orjson

_TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z_]\w*)\s*(?:\|([A-Za-z_]\w*))?\s*\}\}")

_DEFAULT_FILTERS: Dict[str, Callable[[object], str]] = {
    "upper": lambda v: str(v).upper(),
    "lower": lambda v: str(v).lower(),
    "json": lambda v: orjson.dumps(v, option=orjson.OPT_NON_STR_KEYS).decode(),
    "path": lambda v: str(v).replace("\\", "/"),
    "dquote": lambda v: str(v).replace("'", '"'),
}
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def load_file(
    file_path: str,
    vars: Dict[str, object] = {},
    *,
    on_missing: str = "empty",  # "keep" | "empty" | "error"
    is_json: bool = False,
) -> Any:
    def replace(match: re.Match) -> str:
        var_name, filter_name = match.group(1), match.group(2)
        if var_name not in vars:
            if on_missing == "keep":
                return match.group(0)
            if on_missing == "empty":
                return ""
            raise KeyError(f"Missing variable: {var_name}")
        value = vars[var_name]
        if filter_name:
            filter_func = _DEFAULT_FILTERS.get(filter_name)
            if not filter_func:
                raise ValueError(f"Unknown filter: {filter_name}")
            return str(filter_func(value))
        # Apply dquote filter by default
        return str(value).replace("'", '"')

    with (_TEMPLATES_DIR / file_path).open("r", encoding="utf-8") as file:
        text = file.read()

    result = _TOKEN_RE.sub(replace, text)

    if is_json:
        return orjson.loads(result)

    return str(result)
