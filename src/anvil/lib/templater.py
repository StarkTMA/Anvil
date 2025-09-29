from __future__ import annotations

import json
import os
import pprint
import re
from typing import Any, Callable, Dict, Optional

_TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z_]\w*)\s*(?:\|([A-Za-z_]\w*))?\s*\}\}")

_DEFAULT_FILTERS: Dict[str, Callable[[object], str]] = {
    "upper": lambda v: str(v).upper(),
    "lower": lambda v: str(v).lower(),
    "json": lambda v: json.dumps(v, ensure_ascii=False),
    "path": lambda v: str(v).replace("\\", "/"),
    "dquote": lambda v: str(v).replace("'", '"'),
}
_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")


def load_file(
    file_path: str, vars: Dict[str, object] = {}, *, on_missing: str = "empty", is_json: bool = False
) -> str | Any:  # "keep" | "empty" | "error"
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

    with open(os.path.join(_TEMPLATES_DIR, file_path), "r", encoding="utf-8") as file:
        text = file.read()

    result = _TOKEN_RE.sub(replace, text)
    if is_json:
        try:
            return json.loads(result)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON", e)
    return result
