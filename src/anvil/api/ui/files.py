"""The shared JSON UI files: the global variables and the UI definitions list."""

from typing import Annotated, Any

from anvil.api.core.types import JsonSchema
from anvil.api.ui.elements import _keyed_schema, _merged_keys, _plain_value, _UIValue
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, json_field


class _UIVariablesFile(JsonObject):
    """The content of `ui/_global_variables.json`: `$variables` at the root."""

    _variables: Annotated[list[_UIValue], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True, key="$variables"
    )

    def set_variable(self, name: str, value: Any) -> None:
        """Sets a variable. A variable set again replaces the first, in its place."""
        entry = _UIValue(name=name, value=_plain_value(value))
        for index, existing in enumerate(self._variables):
            if existing.name == name:
                self._variables[index] = entry
                return
        self._variables.append(entry)

    def __json__(self) -> Any:
        return _merged_keys(JsonObject.__json__(self), "$variables")

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return _keyed_schema(schema, "$variables", r"^\$", {})


class _UIVariables(JsonFile):
    """The global UI variables of the resource pack, in `ui/_global_variables.json`.

    [Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-documentation#global-variables)
    """

    _document = _UIVariablesFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "ui"
    _object_type = "UI Variables"

    def __init__(self) -> None:
        """Initialize the global variables container."""
        super().__init__("_global_variables")

    def add_variable(self, variable: str, value: Any) -> "_UIVariables":
        """Adds a global variable. A variable added again replaces the first.

        Args:
            variable (str): The variable name, starting with `$`.
            value: Its value: a string, number, boolean, vector or expression.
        """
        self._content.set_variable(variable, value)
        return self


class _UIDefsFile(JsonObject):
    """The content of `ui/_ui_defs.json`: the UI files the game loads."""

    ui_defs: list[str] = json_field(default_factory=list, init=False)

    def add_file(self, path: str) -> None:
        """Adds a UI file, by its path from the pack root."""
        self.ui_defs.append(path)


class _UIDefs(JsonFile):
    """The list of UI files of the resource pack, in `ui/_ui_defs.json`.

    [Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-intro#ui-defs)
    """

    _document = _UIDefsFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "ui"
    _object_type = "UI Definitions"

    def __init__(self) -> None:
        """Initialize the UI definitions container."""
        super().__init__("_ui_defs")

    def add_file(self, path: str) -> "_UIDefs":
        """Adds a UI file to the definitions list.

        Args:
            path (str): The path of the UI file from the pack root.
        """
        self._content.add_file(path)
        return self
