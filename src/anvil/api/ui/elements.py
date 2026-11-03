"""JSON UI elements: `_UIElement`, with every Bedrock Wiki property as a field set by its `set_`
builder, and the parts it holds (bindings, button mappings, modifications, variables, factory).

[Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-documentation)
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Literal, Self

from PIL import Image

from anvil.api.core.types import RGB, RGBA, JsonSchema
from anvil.api.ui.enums import (
    UIAnchor,
    UIBindingType,
    UIElementType,
    UIFontSize,
    UITextAlignment,
)
from anvil.api.ui.nineslice import NinesliceJson
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    Encoded,
    JsonObject,
    JsonType,
    JsonValue,
    Keyed,
    json_field,
)
from anvil.lib.lib import AnvilFormatter, Directory


@dataclass(frozen=True, slots=True)
class _UIReferenceType(JsonType):
    """A string that stands for a property value: a `$variable`, an `@namespace.animation`,
    a `#binding` or a `(expression)`."""

    def validate(self, name: str, value: Any) -> None:
        if not value.startswith(("$", "@", "#", "(")):
            raise ValueError(
                f"'{name}' must be a value of its type, or a $variable, @animation, #binding "
                f"or (expression), got {value!r}."
            )

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return {"type": "string", "pattern": "^[$@#(]"}


_REFERENCE = _UIReferenceType()


def _ui_color(color: str | tuple[float, ...], target: Any) -> Any:
    """A color in any format as `target`, or a reference as it is."""
    if isinstance(color, str) and color.startswith(("$", "@", "(")):
        return color
    return tuple(AnvilFormatter.convert_color(color, target))


def _merged_keys(payload: dict[str, Any], key: str) -> dict[str, Any]:
    """The payload with the object under `key` merged into it."""
    payload.update(payload.pop(key, {}))
    return payload


def _keyed_schema(
    schema: JsonSchema, key: str, pattern: str, value: JsonSchema
) -> JsonSchema:
    """The schema with the `key` property replaced by keys that match `pattern`."""
    schema["properties"].pop(key, None)
    schema["patternProperties"] = {pattern: value}
    return schema


class _UIValue(JsonValue):
    """A `$variable` or `#property`, written as `name: value`.

    Args:
        name (str): The key, with its `$` or `#`.
        value: The value.
    """

    name: str = json_field(exclude=True)
    value: bool | int | float | str | tuple[bool | int | float | str, ...] = (
        json_field()
    )


class _UIControlId(JsonValue):
    """One entry of `control_ids`: a factory id and the element it makes.

    Args:
        id (str): The id the game asks the factory for.
        element (str): The element made for that id, as `name@namespace.element`.
    """

    id: str = json_field(exclude=True)
    element: str = json_field()


class _UIFactory(JsonObject):
    """The factory of a `factory` element, which makes the element the game asks for.

    Args:
        name (str): The factory name, such as `hud_title_text_factory`.
        control_name (str, optional): The one element it makes.
        control_ids (list[_UIControlId]): The element it makes for each id.
        max_children_size (int, optional): How many elements it keeps.
    """

    name: str = json_field()
    control_name: str | None = json_field(default=None)
    control_ids: Annotated[list[_UIControlId], Keyed("id")] = json_field(
        default_factory=list, omit_default=True
    )
    max_children_size: int | None = json_field(default=None)


class _UIVariableSet(JsonObject):
    """One entry of `variables`: the `$variables` set while `requires` is true.

    Args:
        requires (str): The condition, written with `$variables`.
    """

    requires: str = json_field()
    _values: Annotated[list[_UIValue], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True, key="$values"
    )

    def set_value(self, name: str, value: Any) -> Self:
        """Sets a `$variable` while the condition is true.

        Args:
            name (str): The variable, with or without its `$`.
            value: Its value.
        """
        name = f"${name.removeprefix('$')}"
        self._values[:] = [entry for entry in self._values if entry.name != name]
        self._values.append(_UIValue(name=name, value=_plain_value(value)))
        return self

    def __json__(self) -> Any:
        return _merged_keys(JsonObject.__json__(self), "$values")

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return _keyed_schema(schema, "$values", r"^\$", {})


def _plain_value(value: Any) -> Any:
    """An enum as its value, and a list as a tuple, for a `$variable` or `#property`."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return tuple(value)
    return value


class _UISound(JsonObject):
    """One entry of `sounds`.

    Args:
        sound_name (str): A sound from `sound_definitions.json`.
        sound_volume (float, optional): Its volume.
        sound_pitch (float, optional): Its pitch.
        min_seconds_between_plays (float, optional): The wait before it plays again.
    """

    sound_name: str = json_field()
    sound_volume: float | None = json_field(default=None)
    sound_pitch: float | None = json_field(default=None)
    min_seconds_between_plays: float | None = json_field(default=None)


class _UIFocusContainerCustom(JsonObject):
    """One entry of a `focus_container_custom_*` list.

    Args:
        other_focus_container_name (str): The control that receives focus.
        focus_id_inside (str, optional): The `focus_identifier` of its child that receives focus.
    """

    other_focus_container_name: str = json_field()
    focus_id_inside: str | None = json_field(default=None)


class _UIBinding(JsonObject):
    """One data binding of an element, added with `add_binding()`."""

    ignored: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    binding_type: UIBindingType | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    binding_name: str | None = json_field(default=None)
    binding_name_override: str | None = json_field(default=None)
    binding_collection_name: str | None = json_field(default=None)
    binding_collection_prefix: str | None = json_field(default=None)
    binding_condition: (
        Literal[
            "always",
            "always_when_visible",
            "visible",
            "once",
            "none",
            "visibility_changed",
        ]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    source_control_name: str | None = json_field(default=None)
    source_property_name: str | None = json_field(default=None)
    target_property_name: str | None = json_field(default=None)
    resolve_sibling_scope: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )

    def set_ignored(self, ignored: bool | str = True) -> Self:
        """Sets whether the binding is ignored.

        Args:
            ignored (bool | str): The value, or a `$variable`.
        """
        self.ignored = ignored
        return self

    def set_binding_type(
        self, binding_type: UIBindingType | str = UIBindingType.View
    ) -> Self:
        """Sets the type of the binding.

        Args:
            binding_type (UIBindingType | str): The type, or a `$variable`.
        """
        self.binding_type = binding_type
        return self

    def set_binding_name(self, binding_name: str) -> Self:
        """Sets the hardcoded binding, or a condition on it, whose value is stored.

        Args:
            binding_name (str): The binding name, such as `#hud_title_text_string`.
        """
        self.binding_name = binding_name
        return self

    def set_binding_name_override(self, binding_name_override: str) -> Self:
        """Sets the element property that receives the value of `binding_name`.

        Args:
            binding_name_override (str): The property, such as `#text`.
        """
        self.binding_name_override = binding_name_override
        return self

    def set_binding_collection_name(self, binding_collection_name: str) -> Self:
        """Sets the collection the binding reads from.

        Args:
            binding_collection_name (str): The collection name.
        """
        self.binding_collection_name = binding_collection_name
        return self

    def set_binding_collection_prefix(self, binding_collection_prefix: str) -> Self:
        """Sets the prefix of the collection.

        Args:
            binding_collection_prefix (str): The prefix.
        """
        self.binding_collection_prefix = binding_collection_prefix
        return self

    def set_binding_condition(
        self,
        binding_condition: (
            Literal[
                "always",
                "always_when_visible",
                "visible",
                "once",
                "none",
                "visibility_changed",
            ]
            | str
        ),
    ) -> Self:
        """Sets when the binding updates.

        Args:
            binding_condition (str): The condition, or a `$variable`.
        """
        self.binding_condition = binding_condition
        return self

    def set_source_control_name(self, source_control_name: str) -> Self:
        """Sets the element whose property is observed.

        Args:
            source_control_name (str): The element name.
        """
        self.source_control_name = source_control_name
        return self

    def set_source_property_name(self, source_property_name: str) -> Self:
        """Sets the observed property, or an expression on it.

        Args:
            source_property_name (str): The property or expression.
        """
        self.source_property_name = source_property_name
        return self

    def set_target_property_name(self, target_property_name: str) -> Self:
        """Sets the element property that receives the observed value.

        Args:
            target_property_name (str): The property, such as `#visible`.
        """
        self.target_property_name = target_property_name
        return self

    def set_resolve_sibling_scope(
        self, resolve_sibling_scope: bool | str = True
    ) -> Self:
        """Sets whether `source_control_name` only looks at siblings.

        Args:
            resolve_sibling_scope (bool | str): The value, or a `$variable`.
        """
        self.resolve_sibling_scope = resolve_sibling_scope
        return self


class _UIButtonMapping(JsonObject):
    """One button mapping of an element, added with `add_button_mapping()`."""

    ignored: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    from_button_id: str | None = json_field(default=None)
    to_button_id: str | None = json_field(default=None)
    mapping_type: (
        Literal["global", "pressed", "double_pressed", "focused"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    scope: Literal["view", "controller"] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    input_mode_condition: (
        Literal["not_gaze", "not_gamepad", "gamepad_and_not_gaze"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    ignore_input_scope: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    consume_event: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    handle_select: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    handle_deselect: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    button_up_right_of_first_refusal: bool | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )

    def set_ignored(self, ignored: bool | str = True) -> Self:
        """Sets whether the mapping is ignored.

        Args:
            ignored (bool | str): The value, or a `$variable`.
        """
        self.ignored = ignored
        return self

    def set_from_button_id(self, from_button_id: str) -> Self:
        """Sets the button that fires the mapping.

        Args:
            from_button_id (str): The button id, such as `button.menu_select`.
        """
        self.from_button_id = from_button_id
        return self

    def set_to_button_id(self, to_button_id: str) -> Self:
        """Sets the button the mapping fires.

        Args:
            to_button_id (str): The button id.
        """
        self.to_button_id = to_button_id
        return self

    def set_mapping_type(
        self,
        mapping_type: Literal["global", "pressed", "double_pressed", "focused"] | str,
    ) -> Self:
        """Sets when the mapping fires.

        Args:
            mapping_type (str): The mapping type, or a `$variable`.
        """
        self.mapping_type = mapping_type
        return self

    def set_scope(self, scope: Literal["view", "controller"] | str) -> Self:
        """Sets the scope of the mapping.

        Args:
            scope (str): The scope, or a `$variable`.
        """
        self.scope = scope
        return self

    def set_input_mode_condition(
        self,
        input_mode_condition: (
            Literal["not_gaze", "not_gamepad", "gamepad_and_not_gaze"] | str
        ),
    ) -> Self:
        """Sets the input mode the mapping needs.

        Args:
            input_mode_condition (str): The input mode, or a `$variable`.
        """
        self.input_mode_condition = input_mode_condition
        return self

    def set_ignore_input_scope(self, ignore_input_scope: bool | str = True) -> Self:
        """Sets `ignore_input_scope`.

        Args:
            ignore_input_scope (bool | str): The value, or a `$variable`.
        """
        self.ignore_input_scope = ignore_input_scope
        return self

    def set_consume_event(self, consume_event: bool | str = True) -> Self:
        """Sets `consume_event`.

        Args:
            consume_event (bool | str): The value, or a `$variable`.
        """
        self.consume_event = consume_event
        return self

    def set_handle_select(self, handle_select: bool | str = True) -> Self:
        """Sets `handle_select`.

        Args:
            handle_select (bool | str): The value, or a `$variable`.
        """
        self.handle_select = handle_select
        return self

    def set_handle_deselect(self, handle_deselect: bool | str = True) -> Self:
        """Sets `handle_deselect`.

        Args:
            handle_deselect (bool | str): The value, or a `$variable`.
        """
        self.handle_deselect = handle_deselect
        return self

    def set_button_up_right_of_first_refusal(
        self, button_up_right_of_first_refusal: bool | str = True
    ) -> Self:
        """Sets `button_up_right_of_first_refusal`.

        Args:
            button_up_right_of_first_refusal (bool | str): The value, or a `$variable`.
        """
        self.button_up_right_of_first_refusal = button_up_right_of_first_refusal
        return self


def _one_element(element: "_UIElement") -> dict[str, "_UIElement"]:
    return {element.name: element}


def _each_element(elements: list["_UIElement"]) -> list[dict[str, "_UIElement"]]:
    return [{element.name: element} for element in elements]


_ELEMENT_ENTRY: JsonSchema = {
    "type": "object",
    "minProperties": 1,
    "maxProperties": 1,
    "additionalProperties": {"$ref": "#/$defs/_UIElement"},
}


class _UIModification(JsonObject):
    """One change to an element of a pack below, added with `add_modification()`.

    Finish it with `remove()` or `insert_front()`.
    """

    array_name: str | None = json_field(default=None)
    operation: (
        Literal[
            "insert_back",
            "insert_front",
            "insert_after",
            "insert_before",
            "move_back",
            "move_front",
            "move_after",
            "move_before",
            "swap",
            "replace",
            "remove",
        ]
        | None
    ) = json_field(default=None)
    control_name: str | None = json_field(default=None)
    value: Annotated[_UIElement, Encoded(_one_element, _ELEMENT_ENTRY)] | None = (
        json_field(default=None)
    )

    def remove(self, control_name: str) -> Self:
        """Removes a control.

        Args:
            control_name (str): The control to remove.
        """
        self.control_name = control_name
        self.operation = "remove"
        return self

    def insert_front(self, control_name: str) -> "_UIElement":
        """Inserts a new control at the front of `controls`, and returns it.

        Args:
            control_name (str): The new control, as `name@namespace.element`.
        """
        self.array_name = "controls"
        self.operation = "insert_front"
        self.value = _UIElement(control_name)
        return self.value


class _UIElement(JsonObject):
    """A JSON UI element: a control, its children, bindings and `$variables`.

    Every property from the Bedrock Wiki's JSON UI documentation is a field set with its
    `set_` builder. Fields also take a `$variable`, and animated ones an `@namespace.animation`.

    Example:
        ```python
        panel = screen.add_element("my_panel")
        panel.set_type(UIElementType.Panel).set_size(("100%", "50px"))
        panel.set_anchor(UIAnchor.Center, UIAnchor.Center)

        label = panel.add_control("my_label")
        label.set_type(UIElementType.Label).set_text("Hello World")
        ```

    Args:
        name (str): The element name, as `name` or `name@namespace.parent`.
    """

    name: str = json_field(exclude=True, positional=True)
    _keys: Annotated[list[_UIValue], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True, key="$keys"
    )
    _textures: list[str] = json_field(default_factory=list, init=False, exclude=True)

    type: UIElementType | Annotated[str, _REFERENCE] | None = json_field(default=None)
    controls: Annotated[
        list[_UIElement],
        Encoded(
            _each_element, lambda inner: {"type": "array", "items": _ELEMENT_ENTRY}
        ),
    ] = json_field(default_factory=list, init=False, omit_default=True)
    bindings: list[_UIBinding] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    button_mappings: list[_UIButtonMapping] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    modifications: list[_UIModification] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    variables: list[_UIVariableSet] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    property_bag: Annotated[list[_UIValue], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    factory: _UIFactory | None = json_field(default=None)
    control_ids: Annotated[list[_UIControlId], Keyed("id")] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    sounds: list[_UISound] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    focus_container_custom_left: list[_UIFocusContainerCustom] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    focus_container_custom_right: list[_UIFocusContainerCustom] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    focus_container_custom_down: list[_UIFocusContainerCustom] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    focus_container_custom_up: list[_UIFocusContainerCustom] = json_field(
        default_factory=list, init=False, omit_default=True
    )
    visible: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    enabled: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    layer: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    alpha: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    propagate_alpha: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    clips_children: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    allow_clipping: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    clip_offset: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    clip_state_change_event: str | None = json_field(default=None)
    enable_scissor_test: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    selected: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    use_child_anchors: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    anims: list[str] | Annotated[str, _REFERENCE] | None = json_field(default=None)
    disable_anim_fast_forward: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    animation_reset_name: str | None = json_field(default=None)
    ignored: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    grid_position: tuple[int, int] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    collection_index: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    size: tuple[float | str, float | str] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    max_size: tuple[float | str, float | str] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    min_size: tuple[float | str, float | str] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    offset: tuple[float | str, float | str] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    anchor_from: UIAnchor | Annotated[str, _REFERENCE] | None = json_field(default=None)
    anchor_to: UIAnchor | Annotated[str, _REFERENCE] | None = json_field(default=None)
    inherit_max_sibling_width: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    inherit_max_sibling_height: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    use_anchored_offset: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    contained: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    draggable: (
        Literal["vertical", "horizontal", "both"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    follows_cursor: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    orientation: (
        Literal["vertical", "horizontal"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    grid_dimensions: tuple[int, int] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    maximum_grid_items: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    grid_dimension_binding: str | None = json_field(default=None)
    grid_rescaling_type: (
        Literal["vertical", "horizontal", "none"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    grid_fill_direction: (
        Literal["vertical", "horizontal", "none"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    grid_item_template: str | None = json_field(default=None)
    precached_grid_item_count: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    text: str | None = json_field(default=None)
    color: tuple[float, float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    locked_color: tuple[float, float, float] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    shadow: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    hide_hyphen: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    notify_on_ellipses: list[str] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    enable_profanity_filter: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    locked_alpha: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    font_size: UIFontSize | Annotated[str, _REFERENCE] | None = json_field(default=None)
    font_scale_factor: float | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    localize: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    line_padding: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    font_type: (
        Literal["default", "rune", "unicode", "smooth", "MinecraftTen"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    backup_font_type: (
        Literal["default", "rune", "unicode", "smooth", "MinecraftTen"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    text_alignment: UITextAlignment | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    texture: str | None = json_field(default=None)
    allow_debug_missing_texture: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    uv: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    uv_size: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    texture_file_system: (
        Literal[
            "InUserPackage",
            "InAppPackage",
            "RawPath",
            "RawPersistent",
            "InSettingsDir",
            "InExternalDir",
            "InServerPackage",
            "InDataDir",
            "InUserDir",
            "InWorldDir",
            "StoreCache",
        ]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    nineslice_size: (
        int | tuple[int, int, int, int] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    tiled: bool | Literal["x", "y"] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tiled_scale: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    clip_direction: (
        Literal["left", "right", "up", "down", "center"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    clip_ratio: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    clip_pixelperfect: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    keep_ratio: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    bilinear: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    fill: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    zip_folder: str | None = json_field(default=None)
    grayscale: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    force_texture_reload: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    base_size: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    modal: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    inline_modal: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    always_listen_to_input: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    always_handle_pointer: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    always_handle_controller_direction: bool | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    hover_enabled: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    prevent_touch_input: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    consume_event: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    consume_hover_events: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    gesture_tracking_button: str | None = json_field(default=None)
    default_focus_precedence: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    focus_enabled: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    focus_wrap_enabled: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    focus_magnet_enabled: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    focus_identifier: str | None = json_field(default=None)
    focus_change_down: str | None = json_field(default=None)
    focus_change_up: str | None = json_field(default=None)
    focus_change_left: str | None = json_field(default=None)
    focus_change_right: str | None = json_field(default=None)
    focus_container: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    use_last_focus: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    focus_navigation_mode_left: (
        Literal["none", "stop", "custom", "contained"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    focus_navigation_mode_right: (
        Literal["none", "stop", "custom", "contained"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    focus_navigation_mode_down: (
        Literal["none", "stop", "custom", "contained"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    focus_navigation_mode_up: (
        Literal["none", "stop", "custom", "contained"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    default_control: str | None = json_field(default=None)
    hover_control: str | None = json_field(default=None)
    pressed_control: str | None = json_field(default=None)
    locked_control: str | None = json_field(default=None)
    radio_toggle_group: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    toggle_name: str | None = json_field(default=None)
    toggle_default_state: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    toggle_group_forced_index: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    toggle_group_default_selected: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    reset_on_focus_lost: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    toggle_on_hover: str | None = json_field(default=None)
    toggle_on_button: str | None = json_field(default=None)
    toggle_off_button: str | None = json_field(default=None)
    enable_directional_toggling: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    toggle_grid_collection_name: str | None = json_field(default=None)
    checked_control: str | None = json_field(default=None)
    unchecked_control: str | None = json_field(default=None)
    checked_hover_control: str | None = json_field(default=None)
    unchecked_hover_control: str | None = json_field(default=None)
    checked_locked_control: str | None = json_field(default=None)
    unchecked_locked_control: str | None = json_field(default=None)
    checked_locked_hover_control: str | None = json_field(default=None)
    unchecked_locked_hover_control: str | None = json_field(default=None)
    dropdown_name: str | None = json_field(default=None)
    dropdown_content_control: str | None = json_field(default=None)
    dropdown_area: str | None = json_field(default=None)
    sound_name: str | None = json_field(default=None)
    sound_volume: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    sound_pitch: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    collection_name: str | None = json_field(default=None)
    text_box_name: str | None = json_field(default=None)
    text_edit_box_grid_collection_name: str | None = json_field(default=None)
    constrain_to_rect: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    enabled_newline: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    text_type: (
        Literal["ExtendedASCII", "IdentifierChars", "NumberChars"]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    max_length: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    text_control: str | None = json_field(default=None)
    place_holder_control: str | None = json_field(default=None)
    can_be_deselected: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    always_listening: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    virtual_keyboard_buffer_control: str | None = json_field(default=None)
    slider_track_button: str | None = json_field(default=None)
    slider_small_decrease_button: str | None = json_field(default=None)
    slider_small_increase_button: str | None = json_field(default=None)
    slider_steps: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    slider_direction: (
        Literal["vertical", "horizontal"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    slider_timeout: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    slider_collection_name: str | None = json_field(default=None)
    slider_name: str | None = json_field(default=None)
    slider_select_on_hover: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    slider_selected_button: str | None = json_field(default=None)
    slider_deselected_button: str | None = json_field(default=None)
    slider_box_control: str | None = json_field(default=None)
    background_control: str | None = json_field(default=None)
    background_hover_control: str | None = json_field(default=None)
    progress_control: str | None = json_field(default=None)
    progress_hover_control: str | None = json_field(default=None)
    scrollbar_track_button: str | None = json_field(default=None)
    scrollbar_touch_button: str | None = json_field(default=None)
    scroll_speed: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    gesture_control_enabled: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    always_handle_scrolling: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    touch_mode: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    scrollbar_box: str | None = json_field(default=None)
    scrollbar_track: str | None = json_field(default=None)
    scroll_view_port: str | None = json_field(default=None)
    scroll_content: str | None = json_field(default=None)
    scroll_box_and_track_panel: str | None = json_field(default=None)
    jump_to_bottom_on_update: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    renderer: (
        Literal[
            "hover_text_renderer",
            "3d_structure_renderer",
            "splash_text_renderer",
            "ui_holo_cursor",
            "trial_time_renderer",
            "panorama_renderer",
            "actor_portrait_renderer",
            "banner_pattern_renderer",
            "live_player_renderer",
            "web_view_renderer",
            "hunger_renderer",
            "bubbles_renderer",
            "mob_effects_renderer",
            "cursor_renderer",
            "progress_indicator_renderer",
            "camera_renderer",
            "horse_jump_renderer",
            "armor_renderer",
            "horse_heart_renderer",
            "heart_renderer",
            "hotbar_cooldown_renderer",
            "hotbar_renderer",
            "hud_player_renderer",
            "live_horse_renderer",
            "holographic_postrenderer",
            "enchanting_book_renderer",
            "debug_screen_renderer",
            "gradient_renderer",
            "paper_doll_renderer",
            "name_tag_renderer",
            "flying_item_renderer",
            "inventory_item_renderer",
            "credits_renderer",
            "vignette_renderer",
            "progress_bar_renderer",
            "debug_overlay_renderer",
            "background_renderer",
            "bohr_model_renderer",
            "equipment_preview_renderer",
            "experience_renderer",
            "menu_background_renderer",
        ]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    gradient_direction: (
        Literal["vertical", "horizontal"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    color1: tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    color2: tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    text_color: (
        tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    background_color: (
        tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    primary_color: (
        tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    secondary_color: (
        tuple[float, float, float, float] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    camera_tilt_degrees: float | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    starting_rotation: float | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    use_selected_skin: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    use_uuid: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    use_skin_gui_scale: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    use_player_paperdoll: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    rotation: (
        Literal["auto", "gesture_x", "custom_y"] | Annotated[str, _REFERENCE] | None
    ) = json_field(default=None)
    end_event: str | None = json_field(default=None)
    item_id_aux: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    item_custom_color: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    armor_trim_material: (
        Literal[
            "amethyst",
            "copper",
            "diamond",
            "emerald",
            "gold",
            "iron",
            "lapis",
            "netherite",
            "quartz",
            "redstone",
            "resin",
        ]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    armor_trim_pattern: (
        Literal[
            "coast",
            "dune",
            "eye",
            "host",
            "raiser",
            "rib",
            "sentry",
            "shaper",
            "silence",
            "snout",
            "spire",
            "tide",
            "vex",
            "ward",
            "wayfinder",
            "wild",
            "bolt",
            "flow",
        ]
        | Annotated[str, _REFERENCE]
        | None
    ) = json_field(default=None)
    render_only_when_topmost: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    screen_not_flushable: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    always_accepts_input: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    render_game_behind: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    absorbs_input: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    is_showing_menu: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    is_modal: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    should_steal_mouse: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    low_frequency_rendering: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    screen_draws_last: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    vr_mode: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    force_render_below: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    send_telemetry: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    close_on_player_hurt: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    cache_screen: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    load_screen_immediately: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    gamepad_cursor: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    gamepad_cursor_deflection_mode: bool | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    should_be_skipped_during_automation: bool | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    inner_radius: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    outer_radius: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    state_controls: list[str] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    slice_count: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    button_name: str | None = json_field(default=None)
    iterate_left_button_name: str | None = json_field(default=None)
    iterate_right_button_name: str | None = json_field(default=None)
    initial_button_slice: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_name: str | None = json_field(default=None)
    tts_control_header: str | None = json_field(default=None)
    tts_section_header: str | None = json_field(default=None)
    tts_control_type_order_priority: int | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    tts_index_priority: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_toggle_on: str | None = json_field(default=None)
    tts_toggle_off: str | None = json_field(default=None)
    tts_override_control_value: str | None = json_field(default=None)
    tts_inherit_siblings: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_value_changed: str | None = json_field(default=None)
    ttsSectionContainer: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_ignore_count: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_skip_message: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_value_order_priority: int | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    tts_play_on_unchanged_focus_control: bool | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    tts_ignore_subsections: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    text_tts: str | None = json_field(default=None)
    use_priority: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    priority: bool | int | Annotated[str, _REFERENCE] | None = json_field(default=None)

    def __json__(self) -> Any:
        payload = _merged_keys(JsonObject.__json__(self), "$keys")
        return payload or {"$skip_shortening": True}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return _keyed_schema(schema, "$keys", r"^\$", {})

    def _copy_textures(self) -> None:
        """Copies the textures of this element and its children into the pack."""
        for texture in self._textures:
            Directory.copy_files(
                Path("assets", "textures", "ui"),
                CONFIG.RP_PATH / "textures" / "ui",
                f"{texture}.png",
            )
        for control in self.controls:
            control._copy_textures()
        for modification in self.modifications:
            if modification.value is not None:
                modification.value._copy_textures()

    def inherit(self, element_name: str) -> Self:
        """Inherits the properties of another element, as `name@element_name`.

        Args:
            element_name (str): The element to inherit from, as `namespace.element`.
        """
        self.name = f"{self.name}@{element_name}"
        return self

    def set_type(self, type: UIElementType | str) -> Self:
        """Sets the element type.

        Args:
            type (UIElementType | str): The type, or a `$variable`.
        """
        self.type = type
        return self

    def set_anchor(
        self, anchor_from: UIAnchor | str, anchor_to: UIAnchor | str
    ) -> Self:
        """Sets the anchor point in the parent and in the element.

        Args:
            anchor_from (UIAnchor | str): The point in the parent, or a `$variable`.
            anchor_to (UIAnchor | str): The point in the element, or a `$variable`.
        """
        self.anchor_from = anchor_from
        self.anchor_to = anchor_to
        return self

    def keys(self, key: str, value: Any) -> Self:
        """Sets a `$variable` of the element. A variable set again replaces the first.

        Args:
            key (str): The variable, with or without its `$`, such as `size|default`.
            value: Its value.
        """
        name = f"${key.removeprefix('$')}"
        self._keys[:] = [entry for entry in self._keys if entry.name != name]
        self._keys.append(_UIValue(name=name, value=_plain_value(value)))
        return self

    def set_property_bag(self, **properties: Any) -> Self:
        """Sets `#properties` in the property bag. A property set again replaces the first.

        Args:
            **properties: The properties, without their `#`.
        """
        for key, value in properties.items():
            name = f"#{key}"
            self.property_bag[:] = [
                entry for entry in self.property_bag if entry.name != name
            ]
            self.property_bag.append(_UIValue(name=name, value=_plain_value(value)))
        return self

    def add_variables(self, requires: str, **values: Any) -> Self:
        """Adds `$variables` that apply while a condition is true.

        Args:
            requires (str): The condition, written with `$variables`.
            **values: The variables, without their `$`.
        """
        variable_set = _UIVariableSet(requires=requires)
        for name, value in values.items():
            variable_set.set_value(name, value)
        self.variables.append(variable_set)
        return self

    def add_binding(self) -> _UIBinding:
        """Adds a data binding and returns it."""
        binding = _UIBinding()
        self.bindings.append(binding)
        return binding

    def add_button_mapping(self) -> _UIButtonMapping:
        """Adds a button mapping and returns it."""
        mapping = _UIButtonMapping()
        self.button_mappings.append(mapping)
        return mapping

    def add_modification(self) -> _UIModification:
        """Adds a modification of an element from a pack below and returns it."""
        modification = _UIModification()
        self.modifications.append(modification)
        return modification

    def add_control(self, element_name: str) -> "_UIElement":
        """Adds a child element and returns it.

        Args:
            element_name (str): The child name, as `name` or `name@namespace.parent`.
        """
        control = _UIElement(element_name)
        self.controls.append(control)
        return control

    def add_control_id(self, id: str, element: str) -> Self:
        """Adds the element a factory makes for an id.

        Args:
            id (str): The id.
            element (str): The element, as `name@namespace.element`.
        """
        self.control_ids.append(_UIControlId(id=id, element=element))
        return self

    def set_factory(self, name: str, id: str, element: str) -> Self:
        """Sets the factory that makes this element's children.

        Args:
            name (str): The factory name.
            id (str): The id the element is made for, or `control_name` for the only one.
            element (str): The element made, as `name@namespace.element`.
        """
        if id == "control_name":
            self.factory = _UIFactory(name=name, control_name=element)
        else:
            self.factory = _UIFactory(
                name=name, control_ids=[_UIControlId(id=id, element=element)]
            )
        return self

    def add_sound(
        self,
        sound_name: str,
        sound_volume: float | None = None,
        sound_pitch: float | None = None,
        min_seconds_between_plays: float | None = None,
    ) -> Self:
        """Adds a sound played when the element is pressed.

        Args:
            sound_name (str): A sound from `sound_definitions.json`.
            sound_volume (float, optional): Its volume.
            sound_pitch (float, optional): Its pitch.
            min_seconds_between_plays (float, optional): The wait before it plays again.
        """
        self.sounds.append(
            _UISound(
                sound_name=sound_name,
                sound_volume=sound_volume,
                sound_pitch=sound_pitch,
                min_seconds_between_plays=min_seconds_between_plays,
            )
        )
        return self

    def add_focus_container_custom_left(
        self, other_focus_container_name: str, focus_id_inside: str | None = None
    ) -> Self:
        """Adds a control that receives focus on `button.menu_left`.

        Args:
            other_focus_container_name (str): The control.
            focus_id_inside (str, optional): The `focus_identifier` of its child.
        """
        self.focus_container_custom_left.append(
            _UIFocusContainerCustom(
                other_focus_container_name=other_focus_container_name,
                focus_id_inside=focus_id_inside,
            )
        )
        return self

    def add_focus_container_custom_right(
        self, other_focus_container_name: str, focus_id_inside: str | None = None
    ) -> Self:
        """Adds a control that receives focus on `button.menu_right`.

        Args:
            other_focus_container_name (str): The control.
            focus_id_inside (str, optional): The `focus_identifier` of its child.
        """
        self.focus_container_custom_right.append(
            _UIFocusContainerCustom(
                other_focus_container_name=other_focus_container_name,
                focus_id_inside=focus_id_inside,
            )
        )
        return self

    def add_focus_container_custom_down(
        self, other_focus_container_name: str, focus_id_inside: str | None = None
    ) -> Self:
        """Adds a control that receives focus on `button.menu_down`.

        Args:
            other_focus_container_name (str): The control.
            focus_id_inside (str, optional): The `focus_identifier` of its child.
        """
        self.focus_container_custom_down.append(
            _UIFocusContainerCustom(
                other_focus_container_name=other_focus_container_name,
                focus_id_inside=focus_id_inside,
            )
        )
        return self

    def add_focus_container_custom_up(
        self, other_focus_container_name: str, focus_id_inside: str | None = None
    ) -> Self:
        """Adds a control that receives focus on `button.menu_up`.

        Args:
            other_focus_container_name (str): The control.
            focus_id_inside (str, optional): The `focus_identifier` of its child.
        """
        self.focus_container_custom_up.append(
            _UIFocusContainerCustom(
                other_focus_container_name=other_focus_container_name,
                focus_id_inside=focus_id_inside,
            )
        )
        return self

    def _ui_texture(self, texture: str) -> str:
        """The pack path of a texture in `assets/textures/ui`, kept for copying at export."""
        if not (Path("assets", "textures", "ui") / f"{texture}.png").exists():
            raise FileNotFoundError(
                f"{texture}.png not found in {Path('assets', 'textures', 'ui')}. "
                "Please ensure the file exists."
            )
        self._textures.append(texture)
        return Path("textures", "ui", texture).as_posix()

    def _nineslice(
        self,
        texture: str,
        scale_factor: int,
        nineslice_size: int | tuple[int, int, int, int] | None,
    ) -> None:
        """Queues the nineslice file of a scaled or nine-sliced texture."""
        if not nineslice_size and scale_factor == 1:
            return
        if nineslice_size and scale_factor != 1:
            if isinstance(nineslice_size, int):
                nineslice_size = nineslice_size * scale_factor
            else:
                nineslice_size = tuple(size * scale_factor for size in nineslice_size)
        image_size = Image.open(Path("assets", "textures", "ui", f"{texture}.png")).size
        nineslice = NinesliceJson(texture).base_size(
            *(size * scale_factor for size in image_size)
        )
        if nineslice_size:
            nineslice.nineslice_size(nineslice_size)
        nineslice.queue()

    def set_texture(
        self,
        texture: str,
        scale_factor: int = 1,
        nineslice_size: int | tuple[int, int, int, int] | None = None,
        tiled: bool = False,
        tiled_scale: float | tuple[float, float] = 1,
    ) -> Self:
        """Sets the texture from `assets/textures/ui`, copied into the pack on export.

        A scaled or nine-sliced texture also gets its nineslice file.

        Args:
            texture (str): The texture name without `.png`, or a `$variable`.
            scale_factor (int): The scale of the texture's base and nineslice size.
            nineslice_size (int | tuple[int, int, int, int], optional): The nineslice size.
            tiled (bool): Whether the texture tiles.
            tiled_scale (float | tuple[float, float]): The scale of the tiles.
        """
        if "$" in texture:
            self.texture = texture
        else:
            self.texture = self._ui_texture(texture)
        if not nineslice_size and scale_factor == 1:
            return self
        if tiled:
            self.set_tiled(tiled)
        if tiled_scale != 1:
            self.set_tiled_scale(tiled_scale)
        self._nineslice(texture, scale_factor, nineslice_size)
        return self

    def texture_key(
        self,
        key: str,
        texture: str,
        scale_factor: int = 1,
        nineslice_size: int | tuple[int, int, int, int] | None = None,
    ) -> Self:
        """Sets a `$variable` to a texture from `assets/textures/ui`, copied into the pack on
        export. A scaled or nine-sliced texture also gets its nineslice file.

        Args:
            key (str): The variable, without its `$`.
            texture (str): The texture name without `.png`.
            scale_factor (int): The scale of the texture's base and nineslice size.
            nineslice_size (int | tuple[int, int, int, int], optional): The nineslice size.
        """
        self.keys(key, self._ui_texture(texture))
        self._nineslice(texture, scale_factor, nineslice_size)
        return self

    def aseprite_texture(self, texture: str) -> Self:
        """Sets an Aseprite texture from `assets/textures/ui`, with its `.json` sheet.

        Args:
            texture (str): The texture name without `.png`.
        """
        self.set_texture(texture)
        Directory.copy_files(
            Path("assets", "textures", "ui"),
            CONFIG.RP_PATH / "textures" / "ui",
            f"{texture}.json",
        )
        return self

    def aseprite_key(self, key: str, texture: str) -> Self:
        """Sets a `$variable` to an Aseprite texture from `assets/textures/ui`, with its `.json`
        sheet.

        Args:
            key (str): The variable, without its `$`.
            texture (str): The texture name without `.png`.
        """
        self.keys(key, self._ui_texture(texture))
        Directory.copy_files(
            Path("assets", "textures", "ui"),
            CONFIG.RP_PATH / "textures" / "ui",
            f"{texture}.json",
        )
        return self

    def set_visible(self, visible: bool | str = True) -> Self:
        """Sets `visible`. If the UI element should be visible.

        Args:
            visible (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.visible = visible
        return self

    def set_enabled(self, enabled: bool | str = True) -> Self:
        """Sets `enabled`. If true and if the UI element or any of its children have the locked state then they will be in the locked.

        Args:
            enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.enabled = enabled
        return self

    def set_layer(self, layer: int | str) -> Self:
        """Sets `layer`. Z-Index/Layer (like z-index in CSS) is relative to the parent element. Higher values render above, while negative values render below the parent element.

        Args:
            layer (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.layer = layer
        return self

    def set_alpha(self, alpha: float | str) -> Self:
        """Sets `alpha`. Alpha/transparency of the element. It will only affect the UI element. Its children will be unaffected. If you want the alpha to apply for both the parent and children also use `propagate_alpha`.

        Args:
            alpha (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.alpha = alpha
        return self

    def set_propagate_alpha(self, propagate_alpha: bool | str = True) -> Self:
        """Sets `propagate_alpha`. If `alpha` should not only apply to the parent if possible but also all its children.

        Args:
            propagate_alpha (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.propagate_alpha = propagate_alpha
        return self

    def set_clips_children(self, clips_children: bool | str = True) -> Self:
        """Sets `clips_children`. Cuts off visually and interactively everything beyond the boundaries of the UI element.

        Args:
            clips_children (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.clips_children = clips_children
        return self

    def set_allow_clipping(self, allow_clipping: bool | str = True) -> Self:
        """Sets `allow_clipping`. If `clips_children` works in the UI element. Otherwise, it won't have any effect.

        Args:
            allow_clipping (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.allow_clipping = allow_clipping
        return self

    def set_clip_offset(self, clip_offset: tuple[float, float] | str) -> Self:
        """Sets `clip_offset`. Offset from the start of the clipping.

        Args:
            clip_offset (tuple[float, float] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.clip_offset = clip_offset
        return self

    def set_clip_state_change_event(self, clip_state_change_event: str) -> Self:
        """Sets `clip_state_change_event`.

        Args:
            clip_state_change_event (str): The value.
        """
        self.clip_state_change_event = clip_state_change_event
        return self

    def set_enable_scissor_test(self, enable_scissor_test: bool | str = True) -> Self:
        """Sets `enable_scissor_test`.

        Args:
            enable_scissor_test (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.enable_scissor_test = enable_scissor_test
        return self

    def set_selected(self, selected: bool | str = True) -> Self:
        """Sets `selected`. If the text box is selected by default.

        Args:
            selected (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.selected = selected
        return self

    def set_use_child_anchors(self, use_child_anchors: bool | str = True) -> Self:
        """Sets `use_child_anchors`. Use the `anchor_from` and`anchor_to` of the child of the UI element.

        Args:
            use_child_anchors (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_child_anchors = use_child_anchors
        return self

    def set_anims(self, anims: list[str] | str) -> Self:
        """Sets `anims`. Array of the animation names.

        Args:
            anims (list[str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.anims = anims
        return self

    def set_disable_anim_fast_forward(
        self, disable_anim_fast_forward: bool | str = True
    ) -> Self:
        """Sets `disable_anim_fast_forward`.

        Args:
            disable_anim_fast_forward (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.disable_anim_fast_forward = disable_anim_fast_forward
        return self

    def set_animation_reset_name(self, animation_reset_name: str) -> Self:
        """Sets `animation_reset_name`.

        Args:
            animation_reset_name (str): The value.
        """
        self.animation_reset_name = animation_reset_name
        return self

    def set_ignored(self, ignored: bool | str = True) -> Self:
        """Sets `ignored`. If the UI element should be ignored.

        Args:
            ignored (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.ignored = ignored
        return self

    def set_grid_position(self, grid_position: tuple[int, int] | str) -> Self:
        """Sets `grid_position`. Position that the control will take inside the grid. This also allows to modify specific grid items of a hardcoded grid.

        Args:
            grid_position (tuple[int, int] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.grid_position = grid_position
        return self

    def set_collection_index(self, collection_index: int | str) -> Self:
        """Sets `collection_index`. Index that the control takes in the collection.

        Args:
            collection_index (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.collection_index = collection_index
        return self

    def set_size(self, size: tuple[float | str, float | str] | str) -> Self:
        """Sets `size`. Size of the UI element.

        Args:
            size (tuple[float | str, float | str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.size = size
        return self

    def set_max_size(self, max_size: tuple[float | str, float | str] | str) -> Self:
        """Sets `max_size`. Maximum size of the UI element can have.

        Args:
            max_size (tuple[float | str, float | str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.max_size = max_size
        return self

    def set_min_size(self, min_size: tuple[float | str, float | str] | str) -> Self:
        """Sets `min_size`. Minimum size of the UI element can have.

        Args:
            min_size (tuple[float | str, float | str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.min_size = min_size
        return self

    def set_offset(self, offset: tuple[float | str, float | str] | str) -> Self:
        """Sets `offset`. Position of the UI element relative to the parent UI element. It's TopLeft based meaning the coordinates [0, 0] start at the top left of the screen.

        Args:
            offset (tuple[float | str, float | str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.offset = offset
        return self

    def set_anchor_from(self, anchor_from: UIAnchor | str) -> Self:
        """Sets `anchor_from`. Anchor point in the parent element.

        Args:
            anchor_from (UIAnchor | str): The value, or a `$variable` or `@animation` reference.
        """
        self.anchor_from = anchor_from
        return self

    def set_anchor_to(self, anchor_to: UIAnchor | str) -> Self:
        """Sets `anchor_to`. Anchor point in the element.

        Args:
            anchor_to (UIAnchor | str): The value, or a `$variable` or `@animation` reference.
        """
        self.anchor_to = anchor_to
        return self

    def set_inherit_max_sibling_width(
        self, inherit_max_sibling_width: bool | str = True
    ) -> Self:
        """Sets `inherit_max_sibling_width`. Use the maximum width of the sibling element.

        Args:
            inherit_max_sibling_width (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.inherit_max_sibling_width = inherit_max_sibling_width
        return self

    def set_inherit_max_sibling_height(
        self, inherit_max_sibling_height: bool | str = True
    ) -> Self:
        """Sets `inherit_max_sibling_height`. Use the maximum height of the sibling element.

        Args:
            inherit_max_sibling_height (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.inherit_max_sibling_height = inherit_max_sibling_height
        return self

    def set_use_anchored_offset(self, use_anchored_offset: bool | str = True) -> Self:
        """Sets `use_anchored_offset`.

        Args:
            use_anchored_offset (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_anchored_offset = use_anchored_offset
        return self

    def set_contained(self, contained: bool | str = True) -> Self:
        """Sets `contained`.

        Args:
            contained (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.contained = contained
        return self

    def set_draggable(
        self, draggable: Literal["vertical", "horizontal", "both"] | str
    ) -> Self:
        """Sets `draggable`. Makes the element draggable through cursor. The element should be able to accept input in order to be draggable (`input_panel`, `button`, etc.) and must have the required button mappings.

        Args:
            draggable (Literal["vertical", "horizontal", "both"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.draggable = draggable
        return self

    def set_follows_cursor(self, follows_cursor: bool | str = True) -> Self:
        """Sets `follows_cursor`. Follows the cursor.

        Args:
            follows_cursor (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.follows_cursor = follows_cursor
        return self

    def set_orientation(
        self, orientation: Literal["vertical", "horizontal"] | str
    ) -> Self:
        """Sets `orientation`. Direction the elements stack inside `stack_panel`.

        Args:
            orientation (Literal["vertical", "horizontal"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.orientation = orientation
        return self

    def set_grid_dimensions(self, grid_dimensions: tuple[int, int] | str) -> Self:
        """Sets `grid_dimensions`. Number of columns and rows the grid has.

        Args:
            grid_dimensions (tuple[int, int] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.grid_dimensions = grid_dimensions
        return self

    def set_maximum_grid_items(self, maximum_grid_items: int | str) -> Self:
        """Sets `maximum_grid_items`. Maximum number of items the grid will generate.

        Args:
            maximum_grid_items (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.maximum_grid_items = maximum_grid_items
        return self

    def set_grid_dimension_binding(self, grid_dimension_binding: str) -> Self:
        """Sets `grid_dimension_binding`. Binding name for grid dimensions.

        Args:
            grid_dimension_binding (str): The value.
        """
        self.grid_dimension_binding = grid_dimension_binding
        return self

    def set_grid_rescaling_type(
        self, grid_rescaling_type: Literal["vertical", "horizontal", "none"] | str
    ) -> Self:
        """Sets `grid_rescaling_type`. Grid rescaling orientation.

        Args:
            grid_rescaling_type (Literal["vertical", "horizontal", "none"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.grid_rescaling_type = grid_rescaling_type
        return self

    def set_grid_fill_direction(
        self, grid_fill_direction: Literal["vertical", "horizontal", "none"] | str
    ) -> Self:
        """Sets `grid_fill_direction`.

        Args:
            grid_fill_direction (Literal["vertical", "horizontal", "none"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.grid_fill_direction = grid_fill_direction
        return self

    def set_grid_item_template(self, grid_item_template: str) -> Self:
        """Sets `grid_item_template`. An element capable of handling collections.

        Args:
            grid_item_template (str): The value.
        """
        self.grid_item_template = grid_item_template
        return self

    def set_precached_grid_item_count(
        self, precached_grid_item_count: int | str
    ) -> Self:
        """Sets `precached_grid_item_count`.

        Args:
            precached_grid_item_count (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.precached_grid_item_count = precached_grid_item_count
        return self

    def set_text(self, text: str) -> Self:
        """Sets `text`. Text content.

        Args:
            text (str): The value.
        """
        self.text = text
        return self

    def set_color(self, color: str | tuple[float, ...]) -> Self:
        """Sets `color`. Text color. RGB value from 0.0 to 1.0.

        Args:
            color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.color = _ui_color(color, RGB)
        return self

    def set_locked_color(self, locked_color: str | tuple[float, ...]) -> Self:
        """Sets `locked_color`. Text color when a parent has `enabled: false`.

        Args:
            locked_color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.locked_color = _ui_color(locked_color, RGB)
        return self

    def set_shadow(self, shadow: bool | str = True) -> Self:
        """Sets `shadow`. Text shadow.

        Args:
            shadow (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.shadow = shadow
        return self

    def set_hide_hyphen(self, hide_hyphen: bool | str = True) -> Self:
        """Sets `hide_hyphen`. Hide hyphen caused by word breaking.

        Args:
            hide_hyphen (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.hide_hyphen = hide_hyphen
        return self

    def set_notify_on_ellipses(self, notify_on_ellipses: list[str] | str) -> Self:
        """Sets `notify_on_ellipses`. Array of names of the controls to notify when text gets or loses ellipses.

        Args:
            notify_on_ellipses (list[str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.notify_on_ellipses = notify_on_ellipses
        return self

    def set_enable_profanity_filter(
        self, enable_profanity_filter: bool | str = True
    ) -> Self:
        """Sets `enable_profanity_filter`. If "bad" words should be censored.

        Args:
            enable_profanity_filter (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.enable_profanity_filter = enable_profanity_filter
        return self

    def set_locked_alpha(self, locked_alpha: float | str) -> Self:
        """Sets `locked_alpha`. Alpha/transparency of label when a parent has `enabled: false`.

        Args:
            locked_alpha (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.locked_alpha = locked_alpha
        return self

    def set_font_size(self, font_size: UIFontSize | str) -> Self:
        """Sets `font_size`. Size of the text.

        Args:
            font_size (UIFontSize | str): The value, or a `$variable` or `@animation` reference.
        """
        self.font_size = font_size
        return self

    def set_font_scale_factor(self, font_scale_factor: float | str) -> Self:
        """Sets `font_scale_factor`. Scale of the text.

        Args:
            font_scale_factor (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.font_scale_factor = font_scale_factor
        return self

    def set_localize(self, localize: bool | str = True) -> Self:
        """Sets `localize`. If `text` should be able to be translated.

        Args:
            localize (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.localize = localize
        return self

    def set_line_padding(self, line_padding: float | str) -> Self:
        """Sets `line_padding`. Space between lines.

        Args:
            line_padding (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.line_padding = line_padding
        return self

    def set_font_type(
        self,
        font_type: (
            Literal["default", "rune", "unicode", "smooth", "MinecraftTen"] | str
        ),
    ) -> Self:
        """Sets `font_type`. Font of the text.

        Args:
            font_type (Literal["default", "rune", "unicode", "smooth", "MinecraftTen"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.font_type = font_type
        return self

    def set_backup_font_type(
        self,
        backup_font_type: (
            Literal["default", "rune", "unicode", "smooth", "MinecraftTen"] | str
        ),
    ) -> Self:
        """Sets `backup_font_type`. Font used if `font_type` didn't work.

        Args:
            backup_font_type (Literal["default", "rune", "unicode", "smooth", "MinecraftTen"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.backup_font_type = backup_font_type
        return self

    def set_text_alignment(self, text_alignment: UITextAlignment | str) -> Self:
        """Sets `text_alignment`. Text alignment direction. If it's not defined it will adjust automatically based on `anchor_from` and `anchor_to`.

        Args:
            text_alignment (UITextAlignment | str): The value, or a `$variable` or `@animation` reference.
        """
        self.text_alignment = text_alignment
        return self

    def set_allow_debug_missing_texture(
        self, allow_debug_missing_texture: bool | str = True
    ) -> Self:
        """Sets `allow_debug_missing_texture`. Display the missing_texture if the texture is not found.

        Args:
            allow_debug_missing_texture (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.allow_debug_missing_texture = allow_debug_missing_texture
        return self

    def set_uv(self, uv: tuple[float, float] | str) -> Self:
        """Sets `uv`. Start position of the texture mapping.

        Args:
            uv (tuple[float, float] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.uv = uv
        return self

    def set_uv_size(self, uv_size: tuple[float, float] | str) -> Self:
        """Sets `uv_size`. Size of the texture mapping.

        Args:
            uv_size (tuple[float, float] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.uv_size = uv_size
        return self

    def set_texture_file_system(
        self,
        texture_file_system: (
            Literal[
                "InUserPackage",
                "InAppPackage",
                "RawPath",
                "RawPersistent",
                "InSettingsDir",
                "InExternalDir",
                "InServerPackage",
                "InDataDir",
                "InUserDir",
                "InWorldDir",
                "StoreCache",
            ]
            | str
        ),
    ) -> Self:
        """Sets `texture_file_system`. Source to get the texture.

        Args:
            texture_file_system (Literal["InUserPackage", "InAppPackage", "RawPath", "RawPersistent", "InSettingsDir", "InExternalDir", "InServerPackage", "InDataDir", "InUserDir", "InWorldDir", "StoreCache"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.texture_file_system = texture_file_system
        return self

    def set_nineslice_size(
        self, nineslice_size: int | tuple[int, int, int, int] | str
    ) -> Self:
        """Sets `nineslice_size`. 9-slice. A method that divides an texture into 9 pieces. When resized the corners will stay in place and the rest will stretch.

        Args:
            nineslice_size (int | tuple[int, int, int, int] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.nineslice_size = nineslice_size
        return self

    def set_tiled(self, tiled: bool | Literal["x", "y"] | str = True) -> Self:
        """Sets `tiled`. If the texture will tile when the size of the UI element is bigger than the texture size.

        Args:
            tiled (bool | Literal["x", "y"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tiled = tiled
        return self

    def set_tiled_scale(self, tiled_scale: float | tuple[float, float] | str) -> Self:
        """Sets `tiled_scale`. Scale of the tile textures.

        Args:
            tiled_scale (float | tuple[float, float] | str): One scale for both axes, an `(x, y)` pair, or a `$variable`.
        """
        self.tiled_scale = (
            (tiled_scale, tiled_scale)
            if isinstance(tiled_scale, (int, float))
            else tiled_scale
        )
        return self

    def set_clip_direction(
        self, clip_direction: Literal["left", "right", "up", "down", "center"] | str
    ) -> Self:
        """Sets `clip_direction`. Start point position for the `clip_ratio`. If `down`, the image will begin to appear from the bottom.

        Args:
            clip_direction (Literal["left", "right", "up", "down", "center"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.clip_direction = clip_direction
        return self

    def set_clip_ratio(self, clip_ratio: float | str) -> Self:
        """Sets `clip_ratio`. How much to clip. From 0.0 to 1.0.

        Args:
            clip_ratio (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.clip_ratio = clip_ratio
        return self

    def set_clip_pixelperfect(self, clip_pixelperfect: bool | str = True) -> Self:
        """Sets `clip_pixelperfect`. If the clip should try to be the most pixel accurate possible.

        Args:
            clip_pixelperfect (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.clip_pixelperfect = clip_pixelperfect
        return self

    def set_keep_ratio(self, keep_ratio: bool | str = True) -> Self:
        """Sets `keep_ratio`. Keep ratio when resizing image.

        Args:
            keep_ratio (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.keep_ratio = keep_ratio
        return self

    def set_bilinear(self, bilinear: bool | str = True) -> Self:
        """Sets `bilinear`. Use the bilinear function when resizing the image.

        Args:
            bilinear (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.bilinear = bilinear
        return self

    def set_fill(self, fill: bool | str = True) -> Self:
        """Sets `fill`. Stretch the image to the size.

        Args:
            fill (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.fill = fill
        return self

    def set_zip_folder(self, zip_folder: str) -> Self:
        """Sets `zip_folder`.

        Args:
            zip_folder (str): The value.
        """
        self.zip_folder = zip_folder
        return self

    def set_grayscale(self, grayscale: bool | str = True) -> Self:
        """Sets `grayscale`. Render image in black and white.

        Args:
            grayscale (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.grayscale = grayscale
        return self

    def set_force_texture_reload(self, force_texture_reload: bool | str = True) -> Self:
        """Sets `force_texture_reload`. Reload image when the texture path is changed.

        Args:
            force_texture_reload (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.force_texture_reload = force_texture_reload
        return self

    def set_base_size(self, base_size: tuple[float, float] | str) -> Self:
        """Sets `base_size`.

        Args:
            base_size (tuple[float, float] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.base_size = base_size
        return self

    def set_modal(self, modal: bool | str = True) -> Self:
        """Sets `modal`.

        Args:
            modal (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.modal = modal
        return self

    def set_inline_modal(self, inline_modal: bool | str = True) -> Self:
        """Sets `inline_modal`.

        Args:
            inline_modal (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.inline_modal = inline_modal
        return self

    def set_always_listen_to_input(
        self, always_listen_to_input: bool | str = True
    ) -> Self:
        """Sets `always_listen_to_input`.

        Args:
            always_listen_to_input (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_listen_to_input = always_listen_to_input
        return self

    def set_always_handle_pointer(
        self, always_handle_pointer: bool | str = True
    ) -> Self:
        """Sets `always_handle_pointer`.

        Args:
            always_handle_pointer (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_handle_pointer = always_handle_pointer
        return self

    def set_always_handle_controller_direction(
        self, always_handle_controller_direction: bool | str = True
    ) -> Self:
        """Sets `always_handle_controller_direction`.

        Args:
            always_handle_controller_direction (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_handle_controller_direction = always_handle_controller_direction
        return self

    def set_hover_enabled(self, hover_enabled: bool | str = True) -> Self:
        """Sets `hover_enabled`.

        Args:
            hover_enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.hover_enabled = hover_enabled
        return self

    def set_prevent_touch_input(self, prevent_touch_input: bool | str = True) -> Self:
        """Sets `prevent_touch_input`.

        Args:
            prevent_touch_input (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.prevent_touch_input = prevent_touch_input
        return self

    def set_consume_event(self, consume_event: bool | str = True) -> Self:
        """Sets `consume_event`.

        Args:
            consume_event (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.consume_event = consume_event
        return self

    def set_consume_hover_events(self, consume_hover_events: bool | str = True) -> Self:
        """Sets `consume_hover_events`. When set to false, it prevents the element from being hovered.

        Args:
            consume_hover_events (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.consume_hover_events = consume_hover_events
        return self

    def set_gesture_tracking_button(self, gesture_tracking_button: str) -> Self:
        """Sets `gesture_tracking_button`.

        Args:
            gesture_tracking_button (str): The value.
        """
        self.gesture_tracking_button = gesture_tracking_button
        return self

    def set_default_focus_precedence(self, default_focus_precedence: int | str) -> Self:
        """Sets `default_focus_precedence`. Precedence over the other inputs on screen for being selected once the screen is opened.

        Args:
            default_focus_precedence (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.default_focus_precedence = default_focus_precedence
        return self

    def set_focus_enabled(self, focus_enabled: bool | str = True) -> Self:
        """Sets `focus_enabled`. If the arrow keys or controller can focus the element.

        Args:
            focus_enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_enabled = focus_enabled
        return self

    def set_focus_wrap_enabled(self, focus_wrap_enabled: bool | str = True) -> Self:
        """Sets `focus_wrap_enabled`.

        Args:
            focus_wrap_enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_wrap_enabled = focus_wrap_enabled
        return self

    def set_focus_magnet_enabled(self, focus_magnet_enabled: bool | str = True) -> Self:
        """Sets `focus_magnet_enabled`.

        Args:
            focus_magnet_enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_magnet_enabled = focus_magnet_enabled
        return self

    def set_focus_identifier(self, focus_identifier: str) -> Self:
        """Sets `focus_identifier`. Focus identifier for this element.

        Args:
            focus_identifier (str): The value.
        """
        self.focus_identifier = focus_identifier
        return self

    def set_focus_change_down(self, focus_change_down: str) -> Self:
        """Sets `focus_change_down`. Identifier (`focus_identifier`) of the focusable element that will receive focus when on button.menu_down. If you want to prevent the focus to escape from the bottom use `FOCUS_OVERRIDE_STOP`.

        Args:
            focus_change_down (str): The value.
        """
        self.focus_change_down = focus_change_down
        return self

    def set_focus_change_up(self, focus_change_up: str) -> Self:
        """Sets `focus_change_up`. Identifier (`focus_identifier`) of the focusable element that will receive focus when on button.menu_up. If you want to prevent the focus to escape from the top use `FOCUS_OVERRIDE_STOP`.

        Args:
            focus_change_up (str): The value.
        """
        self.focus_change_up = focus_change_up
        return self

    def set_focus_change_left(self, focus_change_left: str) -> Self:
        """Sets `focus_change_left`. Identifier (`focus_identifier`) of the focusable element that will receive focus when on button.menu_left. If you want to prevent the focus to escape from the left use `FOCUS_OVERRIDE_STOP`.

        Args:
            focus_change_left (str): The value.
        """
        self.focus_change_left = focus_change_left
        return self

    def set_focus_change_right(self, focus_change_right: str) -> Self:
        """Sets `focus_change_right`. Identifier (`focus_identifier`) of the focusable element that will receive focus when on button.menu_right. If you want to prevent the focus to escape from the right use `FOCUS_OVERRIDE_STOP`.

        Args:
            focus_change_right (str): The value.
        """
        self.focus_change_right = focus_change_right
        return self

    def set_focus_container(self, focus_container: bool | str = True) -> Self:
        """Sets `focus_container`.

        Args:
            focus_container (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_container = focus_container
        return self

    def set_use_last_focus(self, use_last_focus: bool | str = True) -> Self:
        """Sets `use_last_focus`.

        Args:
            use_last_focus (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_last_focus = use_last_focus
        return self

    def set_focus_navigation_mode_left(
        self,
        focus_navigation_mode_left: (
            Literal["none", "stop", "custom", "contained"] | str
        ),
    ) -> Self:
        """Sets `focus_navigation_mode_left`.

        Args:
            focus_navigation_mode_left (Literal["none", "stop", "custom", "contained"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_navigation_mode_left = focus_navigation_mode_left
        return self

    def set_focus_navigation_mode_right(
        self,
        focus_navigation_mode_right: (
            Literal["none", "stop", "custom", "contained"] | str
        ),
    ) -> Self:
        """Sets `focus_navigation_mode_right`.

        Args:
            focus_navigation_mode_right (Literal["none", "stop", "custom", "contained"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_navigation_mode_right = focus_navigation_mode_right
        return self

    def set_focus_navigation_mode_down(
        self,
        focus_navigation_mode_down: (
            Literal["none", "stop", "custom", "contained"] | str
        ),
    ) -> Self:
        """Sets `focus_navigation_mode_down`.

        Args:
            focus_navigation_mode_down (Literal["none", "stop", "custom", "contained"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_navigation_mode_down = focus_navigation_mode_down
        return self

    def set_focus_navigation_mode_up(
        self,
        focus_navigation_mode_up: Literal["none", "stop", "custom", "contained"] | str,
    ) -> Self:
        """Sets `focus_navigation_mode_up`.

        Args:
            focus_navigation_mode_up (Literal["none", "stop", "custom", "contained"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.focus_navigation_mode_up = focus_navigation_mode_up
        return self

    def set_default_control(self, default_control: str) -> Self:
        """Sets `default_control`. Name of the child control that will be displayed only in the default state.

        Args:
            default_control (str): The value.
        """
        self.default_control = default_control
        return self

    def set_hover_control(self, hover_control: str) -> Self:
        """Sets `hover_control`. Name of the child control that will be displayed only in the hover state.

        Args:
            hover_control (str): The value.
        """
        self.hover_control = hover_control
        return self

    def set_pressed_control(self, pressed_control: str) -> Self:
        """Sets `pressed_control`. Name of the child control that will be displayed only in the pressed state.

        Args:
            pressed_control (str): The value.
        """
        self.pressed_control = pressed_control
        return self

    def set_locked_control(self, locked_control: str) -> Self:
        """Sets `locked_control`. Name of the child control that will be displayed only in the locked state.

        Args:
            locked_control (str): The value.
        """
        self.locked_control = locked_control
        return self

    def set_radio_toggle_group(self, radio_toggle_group: bool | str = True) -> Self:
        """Sets `radio_toggle_group`.

        Args:
            radio_toggle_group (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.radio_toggle_group = radio_toggle_group
        return self

    def set_toggle_name(self, toggle_name: str) -> Self:
        """Sets `toggle_name`. Identifier for the toggle group it belongs to. It can be a custom one.

        Args:
            toggle_name (str): The value.
        """
        self.toggle_name = toggle_name
        return self

    def set_toggle_default_state(self, toggle_default_state: bool | str = True) -> Self:
        """Sets `toggle_default_state`.

        Args:
            toggle_default_state (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.toggle_default_state = toggle_default_state
        return self

    def set_toggle_group_forced_index(
        self, toggle_group_forced_index: int | str
    ) -> Self:
        """Sets `toggle_group_forced_index`. Index of the toggle in its group.

        Args:
            toggle_group_forced_index (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.toggle_group_forced_index = toggle_group_forced_index
        return self

    def set_toggle_group_default_selected(
        self, toggle_group_default_selected: int | str
    ) -> Self:
        """Sets `toggle_group_default_selected`. Index of the default toggle of the its group.

        Args:
            toggle_group_default_selected (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.toggle_group_default_selected = toggle_group_default_selected
        return self

    def set_reset_on_focus_lost(self, reset_on_focus_lost: bool | str = True) -> Self:
        """Sets `reset_on_focus_lost`.

        Args:
            reset_on_focus_lost (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.reset_on_focus_lost = reset_on_focus_lost
        return self

    def set_toggle_on_hover(self, toggle_on_hover: str) -> Self:
        """Sets `toggle_on_hover`.

        Args:
            toggle_on_hover (str): The value.
        """
        self.toggle_on_hover = toggle_on_hover
        return self

    def set_toggle_on_button(self, toggle_on_button: str) -> Self:
        """Sets `toggle_on_button`.

        Args:
            toggle_on_button (str): The value.
        """
        self.toggle_on_button = toggle_on_button
        return self

    def set_toggle_off_button(self, toggle_off_button: str) -> Self:
        """Sets `toggle_off_button`.

        Args:
            toggle_off_button (str): The value.
        """
        self.toggle_off_button = toggle_off_button
        return self

    def set_enable_directional_toggling(
        self, enable_directional_toggling: bool | str = True
    ) -> Self:
        """Sets `enable_directional_toggling`.

        Args:
            enable_directional_toggling (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.enable_directional_toggling = enable_directional_toggling
        return self

    def set_toggle_grid_collection_name(self, toggle_grid_collection_name: str) -> Self:
        """Sets `toggle_grid_collection_name`. Name of the collection the toggle belongs to.

        Args:
            toggle_grid_collection_name (str): The value.
        """
        self.toggle_grid_collection_name = toggle_grid_collection_name
        return self

    def set_checked_control(self, checked_control: str) -> Self:
        """Sets `checked_control`. Name of the child control that will be displayed only in the checked state.

        Args:
            checked_control (str): The value.
        """
        self.checked_control = checked_control
        return self

    def set_unchecked_control(self, unchecked_control: str) -> Self:
        """Sets `unchecked_control`. Name of the child control that will be displayed only in the unchecked state.

        Args:
            unchecked_control (str): The value.
        """
        self.unchecked_control = unchecked_control
        return self

    def set_checked_hover_control(self, checked_hover_control: str) -> Self:
        """Sets `checked_hover_control`. Name of the child control that will be displayed only in the checked hover state.

        Args:
            checked_hover_control (str): The value.
        """
        self.checked_hover_control = checked_hover_control
        return self

    def set_unchecked_hover_control(self, unchecked_hover_control: str) -> Self:
        """Sets `unchecked_hover_control`. Name of the child control that will be displayed only in the unchecked hover state.

        Args:
            unchecked_hover_control (str): The value.
        """
        self.unchecked_hover_control = unchecked_hover_control
        return self

    def set_checked_locked_control(self, checked_locked_control: str) -> Self:
        """Sets `checked_locked_control`. Name of the child control that will be displayed only in the checked locked state.

        Args:
            checked_locked_control (str): The value.
        """
        self.checked_locked_control = checked_locked_control
        return self

    def set_unchecked_locked_control(self, unchecked_locked_control: str) -> Self:
        """Sets `unchecked_locked_control`. Name of the child control that will be displayed only in the unchecked locked state.

        Args:
            unchecked_locked_control (str): The value.
        """
        self.unchecked_locked_control = unchecked_locked_control
        return self

    def set_checked_locked_hover_control(
        self, checked_locked_hover_control: str
    ) -> Self:
        """Sets `checked_locked_hover_control`. Name of the child control that will be displayed only in the checked locked hover state.

        Args:
            checked_locked_hover_control (str): The value.
        """
        self.checked_locked_hover_control = checked_locked_hover_control
        return self

    def set_unchecked_locked_hover_control(
        self, unchecked_locked_hover_control: str
    ) -> Self:
        """Sets `unchecked_locked_hover_control`. Name of the child control that will be displayed only in the unchecked locked hover state.

        Args:
            unchecked_locked_hover_control (str): The value.
        """
        self.unchecked_locked_hover_control = unchecked_locked_hover_control
        return self

    def set_dropdown_name(self, dropdown_name: str) -> Self:
        """Sets `dropdown_name`. Identifier for the dropdown.

        Args:
            dropdown_name (str): The value.
        """
        self.dropdown_name = dropdown_name
        return self

    def set_dropdown_content_control(self, dropdown_content_control: str) -> Self:
        """Sets `dropdown_content_control`. Name of the child control that will behave as the root content panel.

        Args:
            dropdown_content_control (str): The value.
        """
        self.dropdown_content_control = dropdown_content_control
        return self

    def set_dropdown_area(self, dropdown_area: str) -> Self:
        """Sets `dropdown_area`. Name of the child control that will behave as the inside content.

        Args:
            dropdown_area (str): The value.
        """
        self.dropdown_area = dropdown_area
        return self

    def set_sound_name(self, sound_name: str) -> Self:
        """Sets `sound_name`. Name of the sound defined in the `RP/sounds/sound_definitions.json` file that plays when the pressed event is fired.

        Args:
            sound_name (str): The value.
        """
        self.sound_name = sound_name
        return self

    def set_sound_volume(self, sound_volume: float | str) -> Self:
        """Sets `sound_volume`. Volume of the sound.

        Args:
            sound_volume (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.sound_volume = sound_volume
        return self

    def set_sound_pitch(self, sound_pitch: float | str) -> Self:
        """Sets `sound_pitch`. Pitch of the sound.

        Args:
            sound_pitch (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.sound_pitch = sound_pitch
        return self

    def set_collection_name(self, collection_name: str) -> Self:
        """Sets `collection_name`. Name of the collection to be used.

        Args:
            collection_name (str): The value.
        """
        self.collection_name = collection_name
        return self

    def set_text_box_name(self, text_box_name: str) -> Self:
        """Sets `text_box_name`. Identifier for text box.

        Args:
            text_box_name (str): The value.
        """
        self.text_box_name = text_box_name
        return self

    def set_text_edit_box_grid_collection_name(
        self, text_edit_box_grid_collection_name: str
    ) -> Self:
        """Sets `text_edit_box_grid_collection_name`. Name of the collection the `edit_box` belongs to.

        Args:
            text_edit_box_grid_collection_name (str): The value.
        """
        self.text_edit_box_grid_collection_name = text_edit_box_grid_collection_name
        return self

    def set_constrain_to_rect(self, constrain_to_rect: bool | str = True) -> Self:
        """Sets `constrain_to_rect`.

        Args:
            constrain_to_rect (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.constrain_to_rect = constrain_to_rect
        return self

    def set_enabled_newline(self, enabled_newline: bool | str = True) -> Self:
        """Sets `enabled_newline`. Allows multiline text.

        Args:
            enabled_newline (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.enabled_newline = enabled_newline
        return self

    def set_text_type(
        self,
        text_type: Literal["ExtendedASCII", "IdentifierChars", "NumberChars"] | str,
    ) -> Self:
        """Sets `text_type`. Type of characters that the user is allowed to type in th text field.

        Args:
            text_type (Literal["ExtendedASCII", "IdentifierChars", "NumberChars"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.text_type = text_type
        return self

    def set_max_length(self, max_length: int | str) -> Self:
        """Sets `max_length`. Maximum number of characters allow in the text field.

        Args:
            max_length (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.max_length = max_length
        return self

    def set_text_control(self, text_control: str) -> Self:
        """Sets `text_control`. Name of the child control that will be used for displaying the text.

        Args:
            text_control (str): The value.
        """
        self.text_control = text_control
        return self

    def set_place_holder_control(self, place_holder_control: str) -> Self:
        """Sets `place_holder_control`. Name of the child control that will be used for display the placeholder text.

        Args:
            place_holder_control (str): The value.
        """
        self.place_holder_control = place_holder_control
        return self

    def set_can_be_deselected(self, can_be_deselected: bool | str = True) -> Self:
        """Sets `can_be_deselected`.

        Args:
            can_be_deselected (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.can_be_deselected = can_be_deselected
        return self

    def set_always_listening(self, always_listening: bool | str = True) -> Self:
        """Sets `always_listening`.

        Args:
            always_listening (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_listening = always_listening
        return self

    def set_virtual_keyboard_buffer_control(
        self, virtual_keyboard_buffer_control: str
    ) -> Self:
        """Sets `virtual_keyboard_buffer_control`.

        Args:
            virtual_keyboard_buffer_control (str): The value.
        """
        self.virtual_keyboard_buffer_control = virtual_keyboard_buffer_control
        return self

    def set_slider_track_button(self, slider_track_button: str) -> Self:
        """Sets `slider_track_button`. ID of the action for the slider track.

        Args:
            slider_track_button (str): The value.
        """
        self.slider_track_button = slider_track_button
        return self

    def set_slider_small_decrease_button(
        self, slider_small_decrease_button: str
    ) -> Self:
        """Sets `slider_small_decrease_button`. ID of the action for the decrease slider.

        Args:
            slider_small_decrease_button (str): The value.
        """
        self.slider_small_decrease_button = slider_small_decrease_button
        return self

    def set_slider_small_increase_button(
        self, slider_small_increase_button: str
    ) -> Self:
        """Sets `slider_small_increase_button`. ID of the action for the increase slider.

        Args:
            slider_small_increase_button (str): The value.
        """
        self.slider_small_increase_button = slider_small_increase_button
        return self

    def set_slider_steps(self, slider_steps: int | str) -> Self:
        """Sets `slider_steps`. How many steps (or values) does the slider have.

        Args:
            slider_steps (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.slider_steps = slider_steps
        return self

    def set_slider_direction(
        self, slider_direction: Literal["vertical", "horizontal"] | str
    ) -> Self:
        """Sets `slider_direction`. Orientation of the slider movement.

        Args:
            slider_direction (Literal["vertical", "horizontal"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.slider_direction = slider_direction
        return self

    def set_slider_timeout(self, slider_timeout: float | str) -> Self:
        """Sets `slider_timeout`.

        Args:
            slider_timeout (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.slider_timeout = slider_timeout
        return self

    def set_slider_collection_name(self, slider_collection_name: str) -> Self:
        """Sets `slider_collection_name`. Name of the collection the slider belongs to.

        Args:
            slider_collection_name (str): The value.
        """
        self.slider_collection_name = slider_collection_name
        return self

    def set_slider_name(self, slider_name: str) -> Self:
        """Sets `slider_name`. Identifier for the slider.

        Args:
            slider_name (str): The value.
        """
        self.slider_name = slider_name
        return self

    def set_slider_select_on_hover(
        self, slider_select_on_hover: bool | str = True
    ) -> Self:
        """Sets `slider_select_on_hover`. Focus slider when it's hovered.

        Args:
            slider_select_on_hover (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.slider_select_on_hover = slider_select_on_hover
        return self

    def set_slider_selected_button(self, slider_selected_button: str) -> Self:
        """Sets `slider_selected_button`. ID of the action for when the slider is selected.

        Args:
            slider_selected_button (str): The value.
        """
        self.slider_selected_button = slider_selected_button
        return self

    def set_slider_deselected_button(self, slider_deselected_button: str) -> Self:
        """Sets `slider_deselected_button`. ID of the action for when the slider is deselected.

        Args:
            slider_deselected_button (str): The value.
        """
        self.slider_deselected_button = slider_deselected_button
        return self

    def set_slider_box_control(self, slider_box_control: str) -> Self:
        """Sets `slider_box_control`. Name of the child control that will behave as the slider thumb.

        Args:
            slider_box_control (str): The value.
        """
        self.slider_box_control = slider_box_control
        return self

    def set_background_control(self, background_control: str) -> Self:
        """Sets `background_control`. Name of the child control that will behave as the slider background.

        Args:
            background_control (str): The value.
        """
        self.background_control = background_control
        return self

    def set_background_hover_control(self, background_hover_control: str) -> Self:
        """Sets `background_hover_control`. Name of the child control that will behave as the slider background on hover.

        Args:
            background_hover_control (str): The value.
        """
        self.background_hover_control = background_hover_control
        return self

    def set_progress_control(self, progress_control: str) -> Self:
        """Sets `progress_control`. Name of the child control that will behave as the slider background overlay for the slider progress.

        Args:
            progress_control (str): The value.
        """
        self.progress_control = progress_control
        return self

    def set_progress_hover_control(self, progress_hover_control: str) -> Self:
        """Sets `progress_hover_control`. Name of the child control that will behave as the slider background overlay for the slider progress on hover.

        Args:
            progress_hover_control (str): The value.
        """
        self.progress_hover_control = progress_hover_control
        return self

    def set_scrollbar_track_button(self, scrollbar_track_button: str) -> Self:
        """Sets `scrollbar_track_button`. ID of the action for the track button.

        Args:
            scrollbar_track_button (str): The value.
        """
        self.scrollbar_track_button = scrollbar_track_button
        return self

    def set_scrollbar_touch_button(self, scrollbar_touch_button: str) -> Self:
        """Sets `scrollbar_touch_button`. ID of the action for the touch input.

        Args:
            scrollbar_touch_button (str): The value.
        """
        self.scrollbar_touch_button = scrollbar_touch_button
        return self

    def set_scroll_speed(self, scroll_speed: float | str) -> Self:
        """Sets `scroll_speed`. Scrolling speed.

        Args:
            scroll_speed (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.scroll_speed = scroll_speed
        return self

    def set_gesture_control_enabled(
        self, gesture_control_enabled: bool | str = True
    ) -> Self:
        """Sets `gesture_control_enabled`.

        Args:
            gesture_control_enabled (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.gesture_control_enabled = gesture_control_enabled
        return self

    def set_always_handle_scrolling(
        self, always_handle_scrolling: bool | str = True
    ) -> Self:
        """Sets `always_handle_scrolling`.

        Args:
            always_handle_scrolling (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_handle_scrolling = always_handle_scrolling
        return self

    def set_touch_mode(self, touch_mode: bool | str = True) -> Self:
        """Sets `touch_mode`.

        Args:
            touch_mode (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.touch_mode = touch_mode
        return self

    def set_scrollbar_box(self, scrollbar_box: str) -> Self:
        """Sets `scrollbar_box`. Name of child UI element or nested UI element that will behave as the scrollbar thumb.

        Args:
            scrollbar_box (str): The value.
        """
        self.scrollbar_box = scrollbar_box
        return self

    def set_scrollbar_track(self, scrollbar_track: str) -> Self:
        """Sets `scrollbar_track`. Name of child UI element or nested UI element that will behave as the scrollbar track.

        Args:
            scrollbar_track (str): The value.
        """
        self.scrollbar_track = scrollbar_track
        return self

    def set_scroll_view_port(self, scroll_view_port: str) -> Self:
        """Sets `scroll_view_port`. Name of child UI element that will behave as the view port.

        Args:
            scroll_view_port (str): The value.
        """
        self.scroll_view_port = scroll_view_port
        return self

    def set_scroll_content(self, scroll_content: str) -> Self:
        """Sets `scroll_content`. Name of child UI element that will behave as the content root parent.

        Args:
            scroll_content (str): The value.
        """
        self.scroll_content = scroll_content
        return self

    def set_scroll_box_and_track_panel(self, scroll_box_and_track_panel: str) -> Self:
        """Sets `scroll_box_and_track_panel`. Name of child UI element that will contain the scrolling and track controls.

        Args:
            scroll_box_and_track_panel (str): The value.
        """
        self.scroll_box_and_track_panel = scroll_box_and_track_panel
        return self

    def set_jump_to_bottom_on_update(
        self, jump_to_bottom_on_update: bool | str = True
    ) -> Self:
        """Sets `jump_to_bottom_on_update`. Jump to the bottom when the scrolling panel has an update. For example, adds more children to it.

        Args:
            jump_to_bottom_on_update (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.jump_to_bottom_on_update = jump_to_bottom_on_update
        return self

    def set_renderer(
        self,
        renderer: (
            Literal[
                "hover_text_renderer",
                "3d_structure_renderer",
                "splash_text_renderer",
                "ui_holo_cursor",
                "trial_time_renderer",
                "panorama_renderer",
                "actor_portrait_renderer",
                "banner_pattern_renderer",
                "live_player_renderer",
                "web_view_renderer",
                "hunger_renderer",
                "bubbles_renderer",
                "mob_effects_renderer",
                "cursor_renderer",
                "progress_indicator_renderer",
                "camera_renderer",
                "horse_jump_renderer",
                "armor_renderer",
                "horse_heart_renderer",
                "heart_renderer",
                "hotbar_cooldown_renderer",
                "hotbar_renderer",
                "hud_player_renderer",
                "live_horse_renderer",
                "holographic_postrenderer",
                "enchanting_book_renderer",
                "debug_screen_renderer",
                "gradient_renderer",
                "paper_doll_renderer",
                "name_tag_renderer",
                "flying_item_renderer",
                "inventory_item_renderer",
                "credits_renderer",
                "vignette_renderer",
                "progress_bar_renderer",
                "debug_overlay_renderer",
                "background_renderer",
                "bohr_model_renderer",
                "equipment_preview_renderer",
                "experience_renderer",
                "menu_background_renderer",
            ]
            | str
        ),
    ) -> Self:
        """Sets `renderer`.

        Args:
            renderer (Literal["hover_text_renderer", "3d_structure_renderer", "splash_text_renderer", "ui_holo_cursor", "trial_time_renderer", "panorama_renderer", "actor_portrait_renderer", "banner_pattern_renderer", "live_player_renderer", "web_view_renderer", "hunger_renderer", "bubbles_renderer", "mob_effects_renderer", "cursor_renderer", "progress_indicator_renderer", "camera_renderer", "horse_jump_renderer", "armor_renderer", "horse_heart_renderer", "heart_renderer", "hotbar_cooldown_renderer", "hotbar_renderer", "hud_player_renderer", "live_horse_renderer", "holographic_postrenderer", "enchanting_book_renderer", "debug_screen_renderer", "gradient_renderer", "paper_doll_renderer", "name_tag_renderer", "flying_item_renderer", "inventory_item_renderer", "credits_renderer", "vignette_renderer", "progress_bar_renderer", "debug_overlay_renderer", "background_renderer", "bohr_model_renderer", "equipment_preview_renderer", "experience_renderer", "menu_background_renderer"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.renderer = renderer
        return self

    def set_gradient_direction(
        self, gradient_direction: Literal["vertical", "horizontal"] | str
    ) -> Self:
        """Sets `gradient_direction`.

        Args:
            gradient_direction (Literal["vertical", "horizontal"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.gradient_direction = gradient_direction
        return self

    def set_color1(self, color1: str | tuple[float, ...]) -> Self:
        """Sets `color1`.

        Args:
            color1 (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.color1 = _ui_color(color1, RGBA)
        return self

    def set_color2(self, color2: str | tuple[float, ...]) -> Self:
        """Sets `color2`.

        Args:
            color2 (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.color2 = _ui_color(color2, RGBA)
        return self

    def set_text_color(self, text_color: str | tuple[float, ...]) -> Self:
        """Sets `text_color`.

        Args:
            text_color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.text_color = _ui_color(text_color, RGBA)
        return self

    def set_background_color(self, background_color: str | tuple[float, ...]) -> Self:
        """Sets `background_color`.

        Args:
            background_color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.background_color = _ui_color(background_color, RGBA)
        return self

    def set_primary_color(self, primary_color: str | tuple[float, ...]) -> Self:
        """Sets `primary_color`.

        Args:
            primary_color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.primary_color = _ui_color(primary_color, RGBA)
        return self

    def set_secondary_color(self, secondary_color: str | tuple[float, ...]) -> Self:
        """Sets `secondary_color`.

        Args:
            secondary_color (str | tuple[float, ...]): A color in any format, or a `$variable`.
        """
        self.secondary_color = _ui_color(secondary_color, RGBA)
        return self

    def set_camera_tilt_degrees(self, camera_tilt_degrees: float | str) -> Self:
        """Sets `camera_tilt_degrees`.

        Args:
            camera_tilt_degrees (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.camera_tilt_degrees = camera_tilt_degrees
        return self

    def set_starting_rotation(self, starting_rotation: float | str) -> Self:
        """Sets `starting_rotation`.

        Args:
            starting_rotation (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.starting_rotation = starting_rotation
        return self

    def set_use_selected_skin(self, use_selected_skin: bool | str = True) -> Self:
        """Sets `use_selected_skin`.

        Args:
            use_selected_skin (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_selected_skin = use_selected_skin
        return self

    def set_use_uuid(self, use_uuid: bool | str = True) -> Self:
        """Sets `use_uuid`.

        Args:
            use_uuid (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_uuid = use_uuid
        return self

    def set_use_skin_gui_scale(self, use_skin_gui_scale: bool | str = True) -> Self:
        """Sets `use_skin_gui_scale`.

        Args:
            use_skin_gui_scale (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_skin_gui_scale = use_skin_gui_scale
        return self

    def set_use_player_paperdoll(self, use_player_paperdoll: bool | str = True) -> Self:
        """Sets `use_player_paperdoll`.

        Args:
            use_player_paperdoll (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_player_paperdoll = use_player_paperdoll
        return self

    def set_rotation(
        self, rotation: Literal["auto", "gesture_x", "custom_y"] | str
    ) -> Self:
        """Sets `rotation`.

        Args:
            rotation (Literal["auto", "gesture_x", "custom_y"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.rotation = rotation
        return self

    def set_end_event(self, end_event: str) -> Self:
        """Sets `end_event`.

        Args:
            end_event (str): The value.
        """
        self.end_event = end_event
        return self

    def set_item_id_aux(self, item_id_aux: int | str) -> Self:
        """Sets `item_id_aux`. Item id aux of the equipment you want display.

        Args:
            item_id_aux (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.item_id_aux = item_id_aux
        return self

    def set_item_custom_color(self, item_custom_color: int | str) -> Self:
        """Sets `item_custom_color`. Dyed Leather Armor Colors ID.

        Args:
            item_custom_color (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.item_custom_color = item_custom_color
        return self

    def set_armor_trim_material(
        self,
        armor_trim_material: (
            Literal[
                "amethyst",
                "copper",
                "diamond",
                "emerald",
                "gold",
                "iron",
                "lapis",
                "netherite",
                "quartz",
                "redstone",
                "resin",
            ]
            | str
        ),
    ) -> Self:
        """Sets `armor_trim_material`.

        Args:
            armor_trim_material (Literal["amethyst", "copper", "diamond", "emerald", "gold", "iron", "lapis", "netherite", "quartz", "redstone", "resin"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.armor_trim_material = armor_trim_material
        return self

    def set_armor_trim_pattern(
        self,
        armor_trim_pattern: (
            Literal[
                "coast",
                "dune",
                "eye",
                "host",
                "raiser",
                "rib",
                "sentry",
                "shaper",
                "silence",
                "snout",
                "spire",
                "tide",
                "vex",
                "ward",
                "wayfinder",
                "wild",
                "bolt",
                "flow",
            ]
            | str
        ),
    ) -> Self:
        """Sets `armor_trim_pattern`.

        Args:
            armor_trim_pattern (Literal["coast", "dune", "eye", "host", "raiser", "rib", "sentry", "shaper", "silence", "snout", "spire", "tide", "vex", "ward", "wayfinder", "wild", "bolt", "flow"] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.armor_trim_pattern = armor_trim_pattern
        return self

    def set_render_only_when_topmost(
        self, render_only_when_topmost: bool | str = True
    ) -> Self:
        """Sets `render_only_when_topmost`. Only render the screen if it's the most top screen in the screen stack.

        Args:
            render_only_when_topmost (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.render_only_when_topmost = render_only_when_topmost
        return self

    def set_screen_not_flushable(self, screen_not_flushable: bool | str = True) -> Self:
        """Sets `screen_not_flushable`.

        Args:
            screen_not_flushable (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.screen_not_flushable = screen_not_flushable
        return self

    def set_always_accepts_input(self, always_accepts_input: bool | str = True) -> Self:
        """Sets `always_accepts_input`.

        Args:
            always_accepts_input (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.always_accepts_input = always_accepts_input
        return self

    def set_render_game_behind(self, render_game_behind: bool | str = True) -> Self:
        """Sets `render_game_behind`. Doesn't prevent screen below of being able to receive input from the user.

        Args:
            render_game_behind (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.render_game_behind = render_game_behind
        return self

    def set_absorbs_input(self, absorbs_input: bool | str = True) -> Self:
        """Sets `absorbs_input`.

        Args:
            absorbs_input (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.absorbs_input = absorbs_input
        return self

    def set_is_showing_menu(self, is_showing_menu: bool | str = True) -> Self:
        """Sets `is_showing_menu`.

        Args:
            is_showing_menu (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.is_showing_menu = is_showing_menu
        return self

    def set_is_modal(self, is_modal: bool | str = True) -> Self:
        """Sets `is_modal`. It's a screen modal.

        Args:
            is_modal (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.is_modal = is_modal
        return self

    def set_should_steal_mouse(self, should_steal_mouse: bool | str = True) -> Self:
        """Sets `should_steal_mouse`. Captures the cursor and hides it.

        Args:
            should_steal_mouse (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.should_steal_mouse = should_steal_mouse
        return self

    def set_low_frequency_rendering(
        self, low_frequency_rendering: bool | str = True
    ) -> Self:
        """Sets `low_frequency_rendering`. Uses less memory to render the screen.

        Args:
            low_frequency_rendering (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.low_frequency_rendering = low_frequency_rendering
        return self

    def set_screen_draws_last(self, screen_draws_last: bool | str = True) -> Self:
        """Sets `screen_draws_last`. It's the last screen to be drawn/rendered.

        Args:
            screen_draws_last (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.screen_draws_last = screen_draws_last
        return self

    def set_vr_mode(self, vr_mode: bool | str = True) -> Self:
        """Sets `vr_mode`.

        Args:
            vr_mode (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.vr_mode = vr_mode
        return self

    def set_force_render_below(self, force_render_below: bool | str = True) -> Self:
        """Sets `force_render_below`. Renders bottom screens below current screen in the screen stack.

        Args:
            force_render_below (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.force_render_below = force_render_below
        return self

    def set_send_telemetry(self, send_telemetry: bool | str = True) -> Self:
        """Sets `send_telemetry`.

        Args:
            send_telemetry (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.send_telemetry = send_telemetry
        return self

    def set_close_on_player_hurt(self, close_on_player_hurt: bool | str = True) -> Self:
        """Sets `close_on_player_hurt`. Close the screen is the player takes damage.

        Args:
            close_on_player_hurt (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.close_on_player_hurt = close_on_player_hurt
        return self

    def set_cache_screen(self, cache_screen: bool | str = True) -> Self:
        """Sets `cache_screen`.

        Args:
            cache_screen (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.cache_screen = cache_screen
        return self

    def set_load_screen_immediately(
        self, load_screen_immediately: bool | str = True
    ) -> Self:
        """Sets `load_screen_immediately`.

        Args:
            load_screen_immediately (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.load_screen_immediately = load_screen_immediately
        return self

    def set_gamepad_cursor(self, gamepad_cursor: bool | str = True) -> Self:
        """Sets `gamepad_cursor`.

        Args:
            gamepad_cursor (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.gamepad_cursor = gamepad_cursor
        return self

    def set_gamepad_cursor_deflection_mode(
        self, gamepad_cursor_deflection_mode: bool | str = True
    ) -> Self:
        """Sets `gamepad_cursor_deflection_mode`.

        Args:
            gamepad_cursor_deflection_mode (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.gamepad_cursor_deflection_mode = gamepad_cursor_deflection_mode
        return self

    def set_should_be_skipped_during_automation(
        self, should_be_skipped_during_automation: bool | str = True
    ) -> Self:
        """Sets `should_be_skipped_during_automation`.

        Args:
            should_be_skipped_during_automation (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.should_be_skipped_during_automation = should_be_skipped_during_automation
        return self

    def set_inner_radius(self, inner_radius: float | str) -> Self:
        """Sets `inner_radius`.

        Args:
            inner_radius (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.inner_radius = inner_radius
        return self

    def set_outer_radius(self, outer_radius: float | str) -> Self:
        """Sets `outer_radius`.

        Args:
            outer_radius (float | str): The value, or a `$variable` or `@animation` reference.
        """
        self.outer_radius = outer_radius
        return self

    def set_state_controls(self, state_controls: list[str] | str) -> Self:
        """Sets `state_controls`.

        Args:
            state_controls (list[str] | str): The value, or a `$variable` or `@animation` reference.
        """
        self.state_controls = state_controls
        return self

    def set_slice_count(self, slice_count: int | str) -> Self:
        """Sets `slice_count`.

        Args:
            slice_count (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.slice_count = slice_count
        return self

    def set_button_name(self, button_name: str) -> Self:
        """Sets `button_name`.

        Args:
            button_name (str): The value.
        """
        self.button_name = button_name
        return self

    def set_iterate_left_button_name(self, iterate_left_button_name: str) -> Self:
        """Sets `iterate_left_button_name`.

        Args:
            iterate_left_button_name (str): The value.
        """
        self.iterate_left_button_name = iterate_left_button_name
        return self

    def set_iterate_right_button_name(self, iterate_right_button_name: str) -> Self:
        """Sets `iterate_right_button_name`.

        Args:
            iterate_right_button_name (str): The value.
        """
        self.iterate_right_button_name = iterate_right_button_name
        return self

    def set_initial_button_slice(self, initial_button_slice: int | str) -> Self:
        """Sets `initial_button_slice`.

        Args:
            initial_button_slice (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.initial_button_slice = initial_button_slice
        return self

    def set_tts_name(self, tts_name: str) -> Self:
        """Sets `tts_name`.

        Args:
            tts_name (str): The value.
        """
        self.tts_name = tts_name
        return self

    def set_tts_control_header(self, tts_control_header: str) -> Self:
        """Sets `tts_control_header`.

        Args:
            tts_control_header (str): The value.
        """
        self.tts_control_header = tts_control_header
        return self

    def set_tts_section_header(self, tts_section_header: str) -> Self:
        """Sets `tts_section_header`.

        Args:
            tts_section_header (str): The value.
        """
        self.tts_section_header = tts_section_header
        return self

    def set_tts_control_type_order_priority(
        self, tts_control_type_order_priority: int | str
    ) -> Self:
        """Sets `tts_control_type_order_priority`.

        Args:
            tts_control_type_order_priority (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_control_type_order_priority = tts_control_type_order_priority
        return self

    def set_tts_index_priority(self, tts_index_priority: int | str) -> Self:
        """Sets `tts_index_priority`.

        Args:
            tts_index_priority (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_index_priority = tts_index_priority
        return self

    def set_tts_toggle_on(self, tts_toggle_on: str) -> Self:
        """Sets `tts_toggle_on`. Use by the `toggle` type.

        Args:
            tts_toggle_on (str): The value.
        """
        self.tts_toggle_on = tts_toggle_on
        return self

    def set_tts_toggle_off(self, tts_toggle_off: str) -> Self:
        """Sets `tts_toggle_off`. Use by the `toggle` type.

        Args:
            tts_toggle_off (str): The value.
        """
        self.tts_toggle_off = tts_toggle_off
        return self

    def set_tts_override_control_value(self, tts_override_control_value: str) -> Self:
        """Sets `tts_override_control_value`.

        Args:
            tts_override_control_value (str): The value.
        """
        self.tts_override_control_value = tts_override_control_value
        return self

    def set_tts_inherit_siblings(self, tts_inherit_siblings: bool | str = True) -> Self:
        """Sets `tts_inherit_siblings`.

        Args:
            tts_inherit_siblings (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_inherit_siblings = tts_inherit_siblings
        return self

    def set_tts_value_changed(self, tts_value_changed: str) -> Self:
        """Sets `tts_value_changed`.

        Args:
            tts_value_changed (str): The value.
        """
        self.tts_value_changed = tts_value_changed
        return self

    def set_ttsSectionContainer(self, ttsSectionContainer: bool | str = True) -> Self:
        """Sets `ttsSectionContainer`.

        Args:
            ttsSectionContainer (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.ttsSectionContainer = ttsSectionContainer
        return self

    def set_tts_ignore_count(self, tts_ignore_count: bool | str = True) -> Self:
        """Sets `tts_ignore_count`.

        Args:
            tts_ignore_count (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_ignore_count = tts_ignore_count
        return self

    def set_tts_skip_message(self, tts_skip_message: bool | str = True) -> Self:
        """Sets `tts_skip_message`.

        Args:
            tts_skip_message (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_skip_message = tts_skip_message
        return self

    def set_tts_value_order_priority(self, tts_value_order_priority: int | str) -> Self:
        """Sets `tts_value_order_priority`.

        Args:
            tts_value_order_priority (int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_value_order_priority = tts_value_order_priority
        return self

    def set_tts_play_on_unchanged_focus_control(
        self, tts_play_on_unchanged_focus_control: bool | str = True
    ) -> Self:
        """Sets `tts_play_on_unchanged_focus_control`.

        Args:
            tts_play_on_unchanged_focus_control (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_play_on_unchanged_focus_control = tts_play_on_unchanged_focus_control
        return self

    def set_tts_ignore_subsections(
        self, tts_ignore_subsections: bool | str = True
    ) -> Self:
        """Sets `tts_ignore_subsections`.

        Args:
            tts_ignore_subsections (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.tts_ignore_subsections = tts_ignore_subsections
        return self

    def set_text_tts(self, text_tts: str) -> Self:
        """Sets `text_tts`.

        Args:
            text_tts (str): The value.
        """
        self.text_tts = text_tts
        return self

    def set_use_priority(self, use_priority: bool | str = True) -> Self:
        """Sets `use_priority`. If the `priority` property will be use to determine the TTS priority of each child control.

        Args:
            use_priority (bool | str): The value, or a `$variable` or `@animation` reference.
        """
        self.use_priority = use_priority
        return self

    def set_priority(self, priority: bool | int | str) -> Self:
        """Sets `priority`. Order/index of priority that the element has on TTS.

        Args:
            priority (bool | int | str): The value, or a `$variable` or `@animation` reference.
        """
        self.priority = priority
        return self
