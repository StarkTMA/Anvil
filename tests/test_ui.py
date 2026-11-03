"""Tests for the typed JSON UI and dialogue files."""

import pytest

from anvil.api.ui.animations import _UIAnimation
from anvil.api.ui.elements import _UIElement
from anvil.api.ui.files import _UIDefs, _UIVariables
from anvil.api.ui.screens import _UIScreen, _UIScreenFile
from anvil.api.ui.ui import UIAnchor, UIAnimType, UIBindingType, UIElementType
from anvil.api.world.dialogue import Dialogue
from anvil.lib.lib import AnvilIO

jsonschema = pytest.importorskip("jsonschema")


def _json(value):
    return AnvilIO._normalize_json_like(value)


def _check(document):
    schema = type(document).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = _json(document)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def _screen(name="screen", namespace="test_ns"):
    defs = _UIDefs()
    variables = _UIVariables()
    animation = _UIAnimation("animations", "test_animations", defs)
    return _UIScreen(name, namespace, animation, variables, defs)


def test_empty_element_skips_shortening():
    assert _json(_UIElement("empty")) == {"$skip_shortening": True}


def test_element_writes_fields_parts_and_variables():
    element = _UIElement("panel")
    element.set_type(UIElementType.Panel).set_size(("100%", "50px"))
    element.set_anchor(UIAnchor.Center, UIAnchor.TopLeft).keys("$size|default", (1, 2))
    element.add_control("label@common.label").set_text("#text").set_shadow()
    element.add_binding().set_binding_type(UIBindingType.Global).set_binding_name(
        "#hud_title_text_string"
    )
    element.add_variables("$touch", size=["100%", 10])
    element.set_property_bag(title_text="none")
    element.add_modification().insert_front("anvil@anvil_hud.anvil_hud").set_layer(2)
    element.add_modification().remove("sidebar")

    assert _json(element) == {
        "type": "panel",
        "size": ["100%", "50px"],
        "anchor_from": "center",
        "anchor_to": "top_left",
        "$size|default": [1, 2],
        "controls": [{"label@common.label": {"text": "#text", "shadow": True}}],
        "bindings": [
            {"binding_type": "global", "binding_name": "#hud_title_text_string"}
        ],
        "variables": [{"requires": "$touch", "$size": ["100%", 10]}],
        "property_bag": {"#title_text": "none"},
        "modifications": [
            {
                "array_name": "controls",
                "operation": "insert_front",
                "value": {"anvil@anvil_hud.anvil_hud": {"layer": 2}},
            },
            {"operation": "remove", "control_name": "sidebar"},
        ],
    }


def test_keys_and_property_bag_replace_their_value():
    element = _UIElement("panel").keys("index", 0).keys("$index", 1)
    element.set_property_bag(a=1).set_property_bag(a=2)
    assert _json(element) == {"$index": 1, "property_bag": {"#a": 2}}


def test_factory_with_one_control_or_control_ids():
    single = _UIElement("a").set_factory("f", "control_name", "x@y.z")
    keyed = _UIElement("b").set_factory("f", "hud_title_text", "x@y.z")
    assert _json(single) == {"factory": {"name": "f", "control_name": "x@y.z"}}
    assert _json(keyed) == {
        "factory": {"name": "f", "control_ids": {"hud_title_text": "x@y.z"}}
    }


def test_color_is_converted_but_references_are_kept():
    assert _json(_UIElement("a").set_color("#ff0000")) == {"color": [1.0, 0.0, 0.0]}
    assert _json(_UIElement("b").set_color("$text_color")) == {"color": "$text_color"}


@pytest.mark.parametrize(
    "value", ["$visible", "@anvil_animations.fade", "#visible", "(not $touch)"]
)
def test_properties_take_references(value):
    assert _json(_UIElement("a").set_visible(value)) == {"visible": value}


def test_wrong_values_raise_on_export():
    with pytest.raises(ValueError):
        _json(_UIElement("a").set_orientation("sideways"))
    with pytest.raises(ValueError):
        _json(_UIElement("a").set_visible("yes"))
    with pytest.raises(TypeError):
        _json(_UIElement("a").set_layer(1.5))


def test_inherit_renames_the_element():
    assert _UIElement("a").inherit("common.button").name == "a@common.button"


def test_screen_file():
    screen = _screen()
    panel = screen.add_element("panel").set_type(UIElementType.Panel)
    panel.add_control("child").set_layer(1)
    exported = _check(screen._content)
    assert exported == {
        "namespace": "test_ns",
        "panel": {"type": "panel", "controls": [{"child": {"layer": 1}}]},
    }


def test_screen_refuses_two_elements_with_one_name():
    screen = _screen()
    screen.add_element("panel")
    screen.add_element("panel")
    with pytest.raises(ValueError):
        _json(screen._content)


def test_title_trigger_adds_the_factory_once():
    screen = _screen()
    screen.add_element("logo", trigger="title", keyword="logo")
    exported = _json(screen._content)
    assert list(exported) == [
        "namespace",
        "logo_factory",
        "logo@anvil_common.title_binding",
    ]
    assert exported["logo_factory"]["factory"] == {
        "name": "hud_title_text_factory",
        "control_ids": {"hud_title_text": "logo_element@test_ns.logo"},
    }
    variables = _json(screen._variables._content)
    assert variables["$anvil.logo.text"] == "test:logo"


def test_animation_file():
    animations = _UIAnimation("animations", "test_animations", _UIDefs())
    fade = animations.add_animation("fade")
    fade.set_anim_type(UIAnimType.Alpha).set_from(0).set_to(1).set_duration(
        "$fade_time"
    )
    animations.add_animation("move").set_anim_type(UIAnimType.Offset).set_from(
        (0, "100%")
    ).set_to((0, 0))
    exported = _check(animations._content)
    assert exported == {
        "namespace": "test_animations",
        "fade": {"anim_type": "alpha", "duration": "$fade_time", "from": 0, "to": 1},
        "move": {"anim_type": "offset", "from": [0, "100%"], "to": [0, 0]},
    }
    assert str(fade) == "fade"


def test_variables_and_defs_files():
    variables = _UIVariables()
    variables.add_variable("$a", 1).add_variable("$b", "x").add_variable("$a", 2)
    assert _check(variables._content) == {"$a": 2, "$b": "x"}

    defs = _UIDefs().add_file("ui/anvil/common.json")
    assert _check(defs._content) == {"ui_defs": ["ui/anvil/common.json"]}


def test_ui_file_needs_a_namespace():
    with pytest.raises(ValueError):
        _json(_UIScreenFile())


def test_dialogue_file():
    dialogue = Dialogue("intro")
    scene = dialogue.add_scene("start").properties("Guide", "Hello there")
    scene.button("Next", ["say hi", "/tp @s 0 0 0"]).set_on_open_commands(["/say open"])
    dialogue.add_scene("silent")
    exported = _check(dialogue._content)
    scenes = exported["minecraft:npc_dialogue"]["scenes"]
    assert scenes[0]["scene_tag"] == "test:start"
    assert scenes[0]["buttons"][0]["commands"] == ["/say hi", "/tp @s 0 0 0"]
    assert scenes[0]["on_open_commands"] == ["/say open"]
    assert scenes[1] == {"scene_tag": "test:silent"}


def test_dialogue_allows_six_buttons():
    scene = Dialogue("many").add_scene("start")
    for index in range(7):
        scene.button(f"Button {index}", ["/say hi"])
    with pytest.raises(ValueError):
        _json(scene)
