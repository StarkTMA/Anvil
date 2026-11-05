"""JSON UI screens: the screen file, the built-in screens Anvil adds to (HUD, NPC, common)
and the credits builder."""

from pathlib import PurePosixPath
from typing import Annotated, Any, ClassVar

from anvil.api.ui.animations import _UIAnimation
from anvil.api.ui.elements import _keyed_schema, _merged_keys, _UIElement
from anvil.api.ui.files import _UIDefs, _UIVariables
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, json_field
from anvil.lib.jsonmodel.enums import (
    UIAnchor,
    UIAnimType,
    UIBindingType,
    UIEasing,
    UIElementTrigger,
    UIElementType,
    UIFontSize,
    UITextAlignment,
)


class _UICreditsConstructor:
    """Constructor for creating animated credits screens.

    This class provides a convenient interface for building scrolling credits
    screens with various content types including images, titles, sections, and
    spacing. It automatically handles the scrolling animation and layout.

    Attributes:
        _hud_screen (_UIScreen): Reference to the HUD screen
        _credits_panel (_UIElement): Main credits panel element
        _element_count (int): Counter for unique element naming

    Example:
        ```python
        credits = hud_screen.credits_screen_constructor(duration=45)
        credits.add_title("My Game Credits", UIFontSize.ExtraLarge)
        credits.add_space(20)
        credits.add_section("Programming", ["Alice", "Bob"],
                          title_font_size=UIFontSize.Large)
        credits.add_image("studio_logo", scale_factor=2)
        ```
    """

    def __init__(
        self,
        hud_screen: "_UIScreen",
        credits_panel: _UIElement,
        credits_duration: int = 30,
    ) -> None:
        """Initialize the credits constructor.

        Args:
            hud_screen (_UIScreen): HUD screen to add animations to
            credits_panel (_UIElement): Panel element to contain credits
            credits_duration (int, optional): Duration of scroll animation. Defaults to 30.
        """
        self._hud_screen = hud_screen

        anim = self._hud_screen._anvil_animation.add_animation("credits_scroll")
        anim.set_anim_type(UIAnimType.Offset)
        anim.set_duration(credits_duration)
        anim.set_from((0, "160%")).set_to((0, "-160%"))
        anim.set_destroy_at_end("hud_title_text")

        self._credits_panel = credits_panel.add_control(
            "credits_text@anvil_common.stack_panel"
        )
        self._credits_panel.set_offset("@anvil_animations.credits_scroll")

        self._element_count = 0

    def add_image(
        self,
        texture_name: str,
        scale_factor: int = 1,
        anchor=UIAnchor.Center,
        *nineslice_size: int,
    ):
        """Adds an image to the credits panel.

        Args:
            texture_name (str): The name of the texture.
            scale_factor (int, optional): The scale factor of the texture. Defaults to 1.
            anchor (UIAnchor, optional): The anchor of the image. Defaults to UIAnchor.Center.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        image = (
            self._credits_panel.add_control(
                f"panel_{self._element_count}@anvil_common.panel"
            )
            .set_size(("100%", "100%c"))
            .add_control(f"image_{self._element_count}@anvil_common.image")
        )
        image.set_texture(texture_name, scale_factor, *nineslice_size)
        image.set_size((50, 50))
        if anchor != UIAnchor.Center:
            image.set_anchor(anchor, anchor)

        self._element_count += 1
        return self

    def add_title(
        self,
        text: str,
        font_size: UIFontSize = UIFontSize.Normal,
        color: tuple[float] = (1, 1, 1),
        text_alignment: UITextAlignment = UITextAlignment.Center,
    ):
        """Adds a title to the credits panel.

        Args:
            text (str): The text of the title.
            font_size (UIFontSize, optional): The font size of the title. Defaults to UIFontSize.Normal.
            color (tuple[float], optional): The color of the title. Defaults to (1, 1, 1).
            text_alignment (UITextAlignment, optional): The text alignment of the title. Defaults to UITextAlignment.Center.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        title = (
            self._credits_panel.add_control(
                f"panel_{self._element_count}@anvil_common.panel"
            )
            .set_size(("100%", "100%c"))
            .add_control(f"title_{self._element_count}@anvil_common.label")
        )
        title.set_text(text)
        if font_size != UIFontSize.Normal:
            title.set_font_size(font_size)
        if color != (1, 1, 1):
            title.set_color(color)
        if text_alignment != UITextAlignment.Center:
            title.set_text_alignment(text_alignment)
            title.set_size(("100%", "default"))

        self._element_count += 1
        return self

    def add_space(self, size: int | str):
        """Adds a space to the credits panel.

        Args:
            size (int | str): The size of the space.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        space = self._credits_panel.add_control(
            f"space_{self._element_count}@anvil_common.panel"
        )
        space.set_size((0, size))
        self._element_count += 1
        return self

    def add_section(
        self,
        section_title: str,
        section_names: list[str],
        title_font_size: UIFontSize = UIFontSize.Normal,
        title_color: tuple[float] = (1, 1, 1),
        names_font_size: UIFontSize = UIFontSize.Normal,
        names_color: tuple[float] = (1, 1, 1),
    ):
        """Add a credits section with a title and list of names.

        Creates a horizontal layout with the section title on the left
        and a list of names on the right, commonly used for credits
        like "Programming: Alice, Bob, Charlie".

        Args:
            section_title (str): Title for the section (e.g., "Programming")
            section_names (list[str]): List of names to display
            title_font_size (UIFontSize, optional): Font size for title. Defaults to UIFontSize.Normal.
            title_color (tuple[float], optional): RGB color for title. Defaults to (1, 1, 1).
            names_font_size (UIFontSize, optional): Font size for names. Defaults to UIFontSize.Normal.
            names_color (tuple[float], optional): RGB color for names. Defaults to (1, 1, 1).

        Returns:
            _UICreditsConstructor: Self for method chaining
        """
        section = self._credits_panel.add_control(
            f"credits_section_{self._element_count}@anvil_common.stack_panel"
        )
        section.set_orientation("horizontal")
        section.set_size(("100%", "100%c"))

        title = (
            section.add_control(f"panel_title_{self._element_count}@anvil_common.panel")
            .set_size(("45%", "100%c"))
            .add_control(f"title_{self._element_count}@anvil_common.label")
        )
        title.set_text(section_title)
        title.set_size(("100%", "default"))
        title.set_text_alignment(UITextAlignment.Right)
        if title_font_size != UIFontSize.Normal:
            title.set_font_size(title_font_size)
        if title_color != (1, 1, 1):
            title.set_color(title_color)

        section.add_control(
            f"section_sep_{self._element_count}@anvil_common.panel"
        ).set_size(("10%", 0))

        names = section.add_control(
            f"names_{self._element_count}@anvil_common.stack_panel"
        )
        names.set_size(("45%", "100%c"))
        for i, n in enumerate(section_names):
            name = names.add_control(
                f"name_{i}_{self._element_count}@anvil_common.label"
            )
            name.set_text(n)
            name.set_text_alignment(UITextAlignment.Left)
            if names_font_size != UIFontSize.Normal:
                name.set_font_size(names_font_size)
            if names_color != (1, 1, 1):
                name.set_color(names_color)

        self._element_count += 1


class _UIScreenFile(JsonObject):
    """The content of a UI screen file: a namespace and its elements by name."""

    __required__: ClassVar[tuple[str, ...]] = ("namespace",)

    namespace: str | None = json_field(default=None)
    elements: Annotated[list[_UIElement], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True
    )

    def set_namespace(self, namespace: str) -> None:
        """Sets the namespace other files refer to this file's entries by."""
        self.namespace = namespace

    def __validate__(self) -> None:
        if self.namespace is None:
            raise ValueError("A UI file needs a namespace.")

    def __json__(self) -> Any:
        return _merged_keys(JsonObject.__json__(self), "elements")

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return _keyed_schema(
            schema,
            "elements",
            r"^(?!namespace$)",
            {"$ref": "#/$defs/_UIElement"},
        )


class _UIScreen(JsonFile[_UIScreenFile]):
    """A UI screen file: a namespace and its elements.

    It also keeps the title and actionbar texts its elements react to, which `UI` gathers.

    [Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-documentation)
    """

    _extension = ".json"
    _pack = Pack.RP
    _folder = "ui"
    _object_type = "UI Screen"

    def __init__(
        self,
        name: str,
        namespace: str,
        anvil_animation: _UIAnimation,
        variables: _UIVariables,
        defs: _UIDefs,
    ) -> None:
        """Initialize the UI screen.

        Args:
            name (str): Name of the screen file
            namespace (str): Namespace for the screen
            anvil_animation (_UIAnimation): Animation manager
            variables (_UIVariables): Variables manager
            defs (_UIDefs): UI definitions manager
        """
        super().__init__(name)
        self._document.set_namespace(namespace)
        self._namespace = namespace
        self._anvil_animation = anvil_animation
        self._variables = variables
        self._defs = defs
        self._ignored_title_texts = []
        self._ignored_actionbar_texts = []
        self._hides_hud = []

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
        hides_hud: bool = False,
    ) -> _UIElement:
        """Adds an element to the screen and returns it.

        A title or actionbar trigger also adds the factory that makes the element when the
        title or actionbar shows, and with a keyword, the element only shows for that text.

        Args:
            element_name (str): Name of the element
            trigger (UIElementTrigger, optional): Trigger type for activation.
                Defaults to UIElementTrigger.NONE.
            keyword (str, optional): Keyword for trigger matching. Defaults to None.
            hides_hud (bool, optional): Whether this element hides the HUD.
                Defaults to False.
        """
        new_element = _UIElement(element_name)

        match trigger:
            case UIElementTrigger.Title:
                if not keyword is None:
                    self._variables.add_variable(
                        f"$anvil.{element_name}.text",
                        f"{CONFIG.NAMESPACE}:{keyword}",
                    )
                    self._variables.add_variable(
                        f"$anvil.{element_name}.bool",
                        f"(not ((#title_text - $anvil.{element_name}.text) = #title_text))",
                    )
                    self._ignored_title_texts.append(f"$anvil.{element_name}.text")
                    if hides_hud:
                        self._hides_hud.append(f"$anvil.{element_name}.text")

                    new_element = _UIElement(
                        f"{element_name}@anvil_common.title_binding"
                    )
                    new_element.keys("binding_text", f"$anvil.{element_name}.bool")

                factory = self.add_element(f"{element_name}_factory")
                factory.set_type(UIElementType.Panel)
                factory.set_factory(
                    "hud_title_text_factory",
                    "hud_title_text",
                    f"{element_name}_element@{self._namespace}.{element_name}",
                )

            case UIElementTrigger.Actionbar:
                if not keyword is None:
                    self._variables.add_variable(
                        f"$anvil.{element_name}.text",
                        f"{CONFIG.NAMESPACE}:{keyword}",
                    )
                    self._variables.add_variable(
                        f"$anvil.{element_name}.bool",
                        f"(not(($text - $anvil.{element_name}.text) = $text))",
                    )
                    self._ignored_actionbar_texts.append(f"$anvil.{element_name}.text")

                    new_element = _UIElement(
                        f"{element_name}@anvil_common.actionbar_binding"
                    )
                    new_element.keys("binding_text", f"$anvil.{element_name}.bool")

                factory = self.add_element(f"{element_name}_factory")
                factory.set_type(UIElementType.Panel)
                factory.set_factory(
                    "hud_actionbar_text_factory",
                    "hud_actionbar_text",
                    f"{element_name}_element@anvil_hud.{element_name}",
                )

        self._document.elements.append(new_element)
        return new_element

    def queue(self, directory: str = "") -> "_UIScreen":
        """Queues the screen file and adds it to the UI definitions, unless it has no
        elements. The textures its elements use are copied into the pack.

        Args:
            directory (str, optional): Subdirectory for the file. Defaults to "".
        """
        if not self._document.elements:
            return self
        for element in self._document.elements:
            element._copy_textures()
        self._defs.add_file(
            PurePosixPath("ui", directory, f"{self.name}{self._extension}").as_posix()
        )
        return super().queue(directory)


class _HUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("hud_screen", "hud", anvil_animation, variables, defs)
        self.root_panel = self.add_element("root_panel")
        self.anvil_element = self.root_panel.add_modification().insert_front(
            "anvil@anvil_hud.anvil_hud"
        )

        self.hud_title_text = self.add_element("hud_title_text")
        self.hud_title_text.add_binding().set_binding_name(
            "#hud_title_text_string"
        ).set_binding_name_override("#text")
        self.hud_title_text.add_binding().set_binding_name(
            "#hud_subtitle_text_string"
        ).set_binding_name_override("#subtext")

        self.hud_actionbar_text = self.add_element("hud_actionbar_text")
        self.hud_actionbar_text.keys("text", "$actionbar_text")

        variables.add_variable("$anvil.show.text", f"{CONFIG.NAMESPACE}:show")
        variables.add_variable("$anvil.hide.text", f"{CONFIG.NAMESPACE}:hide")
        self._ignored_title_texts = ["$anvil.show.text"]
        self._ignored_actionbar_texts = ["$anvil.hide.text"]
        self._hides_hud = ["$anvil.hide.text"]

    def disable_mob_effect(self) -> "_HUDScreen":
        self.root_panel.add_modification().remove("mob_effects_renderer")
        return self

    def disable_helpers(self) -> "_HUDScreen":
        self.root_panel.add_modification().remove("left_helpers")
        self.root_panel.add_modification().remove("right_helpers")
        self.root_panel.add_modification().remove("emote_expediate_helpers")
        return self

    def disable_hotbar(self) -> "_HUDScreen":
        self.root_panel.add_modification().remove("centered_gui_elements")
        self.root_panel.add_modification().remove(
            "centered_gui_elements_at_bottom_middle"
        )
        self.root_panel.add_modification().remove(
            "centered_gui_elements_at_bottom_middle_touch"
        )
        self.root_panel.add_modification().remove("not_centered_gui_elements")
        self.root_panel.add_modification().remove("exp_rend")
        self.root_panel.add_modification().remove("exp_rend_resizable")
        return self

    def disable_sidebar(self) -> "_HUDScreen":
        self.root_panel.add_modification().remove("sidebar")
        return self

    def queue(self, directory: str = "") -> "_HUDScreen":
        return super().queue()


class _NPCScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__(
            "npc_interact_screen", "npc_interact", anvil_animation, variables, defs
        )
        self._npc_screen = self.add_element("npc_screen@common.base_screen").keys(
            "screen_content", "anvil_npc.npc_screen_chooser"
        )

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
    ) -> "_UIElement":
        return super().add_element(element_name, trigger, keyword, False)

    def queue(self, directory: str = "") -> "_NPCScreen":
        return super().queue()


class _AnvilHUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("hud", "anvil_hud", anvil_animation, variables, defs)
        self.anvil_hud: _UIElement = super().add_element("anvil_hud")
        self.anvil_hud.set_type(UIElementType.Panel)

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
        hides_hud: bool = False,
    ) -> "_UIElement":
        if not trigger is UIElementTrigger.NONE:
            self.anvil_hud.add_control(
                f"{element_name}_instance@anvil_hud.{element_name}_factory"
            )

        return super().add_element(element_name, trigger, keyword, hides_hud)

    def add_image_panel(
        self,
        name: str,
        background: str = "transparent",
        direction_out: bool = True,
        zoom_in: float = 1,
        zoom_wait: float = 6,
        zoom_out: float = 1,
    ) -> "_UIElement":
        image_element = self.add_element(name, UIElementTrigger.Title, name)
        image_element.set_type(UIElementType.Panel)
        image_element.set_size(("100%", "100%"))
        image_element.set_layer(100)
        image_element.set_anchor(UIAnchor.Center, UIAnchor.Center)

        if background != "transparent":
            background_image = image_element.add_control(f"{name}_background")
            background_image.set_type(UIElementType.Image)
            background_image.set_texture(background)
            background_image.set_size(("100%", "100%"))
            background_image.set_keep_ratio(False)

        image = image_element.add_control(f"{name}_image")
        image.set_type(UIElementType.Image)
        image.set_texture(name)
        image.set_anchor(UIAnchor.Center, UIAnchor.Center)
        image.set_offset((0, "-20px"))

        tip = image_element.add_control(f"{name}_tip")
        tip.set_type(UIElementType.Label)
        tip.set_text_alignment(UITextAlignment.Center)
        tip.set_size(("80%", "default"))
        tip.set_offset((0, "100px"))
        tip.set_text("#text").set_shadow(True).set_font_size(UIFontSize.Large)
        tip.add_binding().set_binding_name(
            "#hud_subtitle_text_string"
        ).set_binding_name_override("#text")

        zoom_steps = []
        if direction_out:
            zoom_steps = ["30%", "40%", "50%"]
        else:
            zoom_steps = ["400%", "70%", "60%"]

        self._variables.add_variable(f"$anvil.image.{name}_in", zoom_in)
        self._variables.add_variable(f"$anvil.image.{name}_wait", zoom_wait)
        self._variables.add_variable(f"$anvil.image.{name}_out", zoom_out)

        image_zoom_in = self._anvil_animation.add_animation(f"{name}_zoom_in")
        image_zoom_in.set_anim_type(UIAnimType.Size)
        image_zoom_in.set_easing(UIEasing.Linear)
        image_zoom_in.set_from((zoom_steps[0], zoom_steps[0])).set_to(
            (zoom_steps[1], zoom_steps[1])
        )
        image_zoom_in.set_duration(f"$anvil.image.{name}_in")
        image_zoom_in.set_next(f"@anvil_animations.{name}_zoom_wait")

        image_zoom_wait = self._anvil_animation.add_animation(f"{name}_zoom_wait")
        image_zoom_wait.set_anim_type(UIAnimType.Wait)
        image_zoom_wait.set_duration(f"$anvil.image.{name}_wait")
        image_zoom_wait.set_next(f"@anvil_animations.{name}_zoom_out")
        image_zoom_out = self._anvil_animation.add_animation(f"{name}_zoom_out")

        image_zoom_out.set_anim_type(UIAnimType.Size)
        image_zoom_out.set_easing(UIEasing.Linear)
        image_zoom_out.set_from((zoom_steps[1], zoom_steps[1])).set_to(
            (zoom_steps[2], zoom_steps[2])
        )
        image_zoom_out.set_duration(f"$anvil.image.{name}_out")

        image_alpha_in = self._anvil_animation.add_animation(f"{name}_alpha_in")
        image_alpha_in.set_anim_type(UIAnimType.Alpha)
        image_alpha_in.set_easing(UIEasing.OutQuad)
        image_alpha_in.set_from(0)
        image_alpha_in.set_to(1)
        image_alpha_in.set_duration(f"$anvil.image.{name}_in")
        image_alpha_in.set_next(f"@anvil_animations.{name}_alpha_wait")
        image_alpha_wait = self._anvil_animation.add_animation(f"{name}_alpha_wait")
        image_alpha_wait.set_anim_type(UIAnimType.Wait)
        image_alpha_wait.set_duration(f"$anvil.image.{name}_wait")
        image_alpha_wait.set_next(f"@anvil_animations.{name}_alpha_out")
        image_alpha_out = self._anvil_animation.add_animation(f"{name}_alpha_out")
        image_alpha_out.set_anim_type(UIAnimType.Alpha)
        image_alpha_out.set_easing(UIEasing.InOutSine)
        image_alpha_out.set_from(1)
        image_alpha_out.set_to(0)
        image_alpha_out.set_duration(f"$anvil.image.{name}_out")
        image_alpha_out.set_destroy_at_end("hud_title_text")

        image.set_size(
            f"@anvil_animations.{name}_zoom_in" if zoom_in > 0 else ("50%", "50%")
        )
        image.set_alpha(f"@anvil_animations.{name}_alpha_in" if zoom_in > 0 else 1)

        return image_element

    def add_logo(self) -> "_AnvilHUDScreen":
        self.add_image_panel("logo")
        return self

    def add_blinking_screen(self) -> "_AnvilHUDScreen":
        blink_fade_in = self._anvil_animation.add_animation("blink_fade_in")
        blink_fade_in.set_anim_type(UIAnimType.Alpha)
        blink_fade_in.set_easing(UIEasing.InOutSine)
        blink_fade_in.set_from(0).set_to(1)
        self._variables.add_variable("$anvil.blink.fade_in", 1)
        blink_fade_in.set_duration("$anvil.blink.fade_in")
        blink_fade_in.set_next("@anvil_animations.blink_fade_stay")

        blink_fade_stay = self._anvil_animation.add_animation("blink_fade_stay")
        blink_fade_stay.set_anim_type(UIAnimType.Wait)
        self._variables.add_variable("$anvil.blink.fade_stay", 1)
        blink_fade_stay.set_duration("$anvil.blink.fade_stay")
        blink_fade_stay.set_next("@anvil_animations.blink_fade_out")

        blink_fade_out = self._anvil_animation.add_animation("blink_fade_out")
        blink_fade_out.set_anim_type(UIAnimType.Alpha)
        blink_fade_out.set_easing(UIEasing.InOutSine)
        blink_fade_out.set_from(1).set_to(0)
        self._variables.add_variable("$anvil.blink.fade_out", 1)
        blink_fade_out.set_duration("$anvil.blink.fade_out")
        blink_element = self.add_element(
            "blink_element", UIElementTrigger.Title, "blink"
        )
        blink_element.set_type(UIElementType.Image)
        blink_element.set_layer(101)
        blink_element.set_texture("black_element")
        blink_element.set_anchor(UIAnchor.Center, UIAnchor.Center)
        blink_element.set_size(("300%", "300%"))
        blink_element.set_alpha("@anvil_animations.blink_fade_in")
        return self

    def add_black_bars(self) -> "_AnvilHUDScreen":
        black_bars_in = self._anvil_animation.add_animation("black_bars_in")
        black_bars_in.set_anim_type(UIAnimType.Size)
        black_bars_in.set_easing(UIEasing.InOutSine)
        black_bars_in.set_from(("300%", "300%")).set_to(("300%", "100%"))
        self._variables.add_variable("$anvil.black_bars.in", 1.6)
        black_bars_in.set_duration("$anvil.black_bars.in")
        black_bars_in.set_next("@anvil_animations.black_bars_wait")

        black_bars_wait = self._anvil_animation.add_animation("black_bars_wait")
        black_bars_wait.set_anim_type(UIAnimType.Wait)
        self._variables.add_variable("$anvil.black_bars.stay", 1)
        black_bars_wait.set_duration("$anvil.black_bars.stay")

        black_bars_out = self._anvil_animation.add_animation("black_bars_out")
        black_bars_out.set_anim_type(UIAnimType.Size)
        black_bars_out.set_easing(UIEasing.InOutSine)
        black_bars_out.set_from(("300%", "100%")).set_to(("300%", "300%"))
        self._variables.add_variable("$anvil.black_bars.out", 1.6)
        black_bars_out.set_duration("$anvil.black_bars.out")

        black_bars = self.add_element("black_bars_element", UIElementTrigger.Actionbar)
        black_bars.set_type(UIElementType.Image)
        black_bars.set_texture("black_bars")
        black_bars.set_keep_ratio(False)
        black_bars.set_anchor(UIAnchor.Center, UIAnchor.Center)
        black_bars.set_layer(101)
        black_bars.keys("anim_size", ("300%", "300%"))
        black_bars.keys("text", "$actionbar_text")
        black_bars.add_variables(
            "$anvil.black_bars_in.bool",
            anim_size="@anvil_animations.black_bars_in",
        )
        black_bars.add_variables(
            "$anvil.black_bars_out.bool",
            anim_size="@anvil_animations.black_bars_out",
        )
        black_bars.set_size("$anim_size")

        self._variables.add_variable(
            "$anvil.black_bars_in.text", f"{CONFIG.NAMESPACE}:bars_in"
        )
        self._variables.add_variable(
            "$anvil.black_bars_in.bool", "($text = $anvil.black_bars_in.text)"
        )
        self._variables.add_variable(
            "$anvil.black_bars_out.text", f"{CONFIG.NAMESPACE}:bars_out"
        )
        self._variables.add_variable(
            "$anvil.black_bars_out.bool", "($text = $anvil.black_bars_out.text)"
        )

        self._ignored_actionbar_texts.extend(
            [
                "($text = $anvil.black_bars_in.text)",
                "($text = $anvil.black_bars_out.text)",
            ]
        )
        return self

    def credits_screen_constructor(
        self, credits_duration: int = 30
    ) -> "_UICreditsConstructor":
        credits = self.add_element("credits", UIElementTrigger.Title, "credits")
        credits.set_type(UIElementType.Panel)
        credits.set_layer(100)

        background_image = credits.add_control("credits_background@anvil_common.image")
        background_image.set_texture("black_element")
        background_image.set_size(("100%", "100%"))
        background_image.set_keep_ratio(False)
        background_image.set_layer(-1)

        return _UICreditsConstructor(self, credits, credits_duration)

    def queue(self, directory: str = "") -> "_AnvilHUDScreen":
        return super().queue(directory)


class _AnvilNPCScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("npc", "anvil_npc", anvil_animation, variables, defs)
        self._ignored_panel_texts = []

        self._npc_screen_chooser = (
            super()
            .add_element("npc_screen_chooser", True)
            .set_type(UIElementType.Panel)
        )
        vanilla = self._npc_screen_chooser.add_control(
            "vanilla@npc_interact.npc_screen_contents"
        )
        vanilla.add_binding().set_binding_type(UIBindingType.Global).set_binding_name(
            "#title_text"
        ).set_binding_name_override("#title_text")
        vanilla.add_binding().set_binding_type(UIBindingType.Global).set_binding_name(
            "#dialogtext"
        ).set_binding_name_override("#dialogtext")
        vanilla.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_property_name(
            "$anvil.npc_screen.vanilla"
        ).set_target_property_name(
            "#visible"
        )

    def add_element(
        self,
        element_name: str,
        keyword: str = None,
    ) -> "_UIElement":
        if keyword:
            self._ignored_panel_texts.append(f"$anvil.npc_screen.{element_name}.text")
            self._variables.add_variable(
                f"$anvil.npc_screen.{element_name}.text",
                keyword,
            )
            self._variables.add_variable(
                f"$anvil.npc_screen.{element_name}.bool",
                f"(#dialogtext = $anvil.npc_screen.{element_name}.text)",
            )
            custom_panel = self._npc_screen_chooser.add_control(
                f"{element_name}_instance@anvil_npc.{element_name}"
            )
            custom_panel.add_binding().set_binding_type(
                UIBindingType.Global
            ).set_binding_name("#dialogtext").set_binding_name_override("#dialogtext")
            custom_panel.add_binding().set_binding_type(
                UIBindingType.View
            ).set_source_property_name(
                f"$anvil.npc_screen.{element_name}.bool"
            ).set_target_property_name(
                "#visible"
            )

        return super().add_element(element_name, UIElementTrigger.NONE, keyword, False)

    def queue(self, directory: str = "") -> "_AnvilNPCScreen":
        self._variables.add_variable(
            "$anvil.npc_screen.vanilla",
            f"({'(' * len(self._ignored_panel_texts)}#dialogtext - "
            + " - ".join(f"{var})" for var in self._ignored_panel_texts)
            + " = #dialogtext)",
        )
        return super().queue("anvil")


class _AnvilCommon(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("common", "anvil_common", anvil_animation, variables, defs)
        self.basic_components()
        self.image_label()
        self.title_actionbar()
        self.scoreboard_retrieve()
        self.complex_components()

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
    ) -> "_UIElement":
        return super().add_element(element_name, trigger, keyword, False)

    def basic_components(self) -> "_AnvilCommon":
        label = self.add_element("label")
        label.set_type(UIElementType.Label)
        label.set_text_alignment(UITextAlignment.Center)

        image = self.add_element("image")
        image.set_type(UIElementType.Image)

        stack_panel = self.add_element("stack_panel")
        stack_panel.set_type(UIElementType.StackPanel)

        panel = self.add_element("panel")
        panel.set_type(UIElementType.Panel)
        return self

    def complex_components(self) -> "_AnvilCommon":
        npc_renderer = self.add_element("npc_renderer")
        npc_renderer.set_type(UIElementType.Panel)
        npc_renderer.set_size(("100%", "100%"))
        npc_renderer.set_clips_children(True)
        npc_model = npc_renderer.add_control("npc_model")
        npc_model.set_type(UIElementType.Custom)
        npc_model.set_layer(5)
        npc_model.set_renderer("actor_portrait_renderer")
        npc_model.set_size(("120%", "120%"))
        npc_model.set_enable_scissor_test()
        npc_model.add_binding().set_binding_type(
            UIBindingType.Collection
        ).set_binding_collection_name("skins_collection").set_binding_name(
            "#skin_index"
        )

        player_renderer = self.add_element("player_renderer")
        player_renderer.set_type(UIElementType.Panel)
        player_renderer.set_size(("80%", "80%"))
        player_renderer.set_clips_children(True)
        player_model = player_renderer.add_control("player_model")
        player_model.set_type(UIElementType.Custom)
        player_model.set_renderer("live_player_renderer")
        player_model.set_size(("80%", "80%"))
        player_model.set_enable_scissor_test()
        player_model.set_offset((0, "50%y"))
        return self

    def image_label(self) -> "_AnvilCommon":
        image_label = self.add_element("image_label@anvil_common.image")
        image_label.set_size(("100%c + 8px", "100%c + 4px"))
        image_label.keys("text", "PLACEHOLDER TEXT")
        image_label.keys("localize", False)
        image_label.keys("text_color", "#0f0f0f")

        label = image_label.add_control("label@anvil_common.label")
        label.set_text("$text")
        label.set_localize("$localize")
        label.set_color("$text_color")

        image_label_binding = self.add_element("image_label_binding@anvil_common.image")
        image_label_binding.set_size(("100%c + 8px", "100%c + 4px"))
        image_label_binding.keys("text_color", "#0f0f0f")

        label_binding = image_label_binding.add_control("text@anvil_common.label")
        label_binding.set_text("#text")
        label_binding.set_layer(1)
        label_binding.set_color("$text_color")
        label_binding.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_control_name("$control_name").set_source_property_name(
            "#text"
        ).set_target_property_name(
            "#text"
        )
        return self

    def title_actionbar(self) -> "_AnvilCommon":
        title_binding = self.add_element("title_binding")
        title_binding.set_property_bag(title_text="", subtitle_text="")
        title_binding.add_binding().set_binding_name(
            "#hud_title_text_string"
        ).set_binding_name_override("#title_text")
        title_binding.add_binding().set_binding_name(
            "#hud_subtitle_text_string"
        ).set_binding_name_override("#subtitle_text")
        title_binding.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_property_name("$binding_text").set_target_property_name("#visible")

        actionbar_binding = self.add_element("actionbar_binding")
        actionbar_binding.keys("text", "$actionbar_text")
        actionbar_binding.set_visible("$binding_text")
        return self

    def scoreboard_retrieve(self) -> "_AnvilCommon":
        """Use ``retrieve_score`` as the element. A few variables must be passed.
        To retrieve the score value, you must call the source_control_name using the element based on ``retrieve_score``,
        then call the property ``score`` for the int value, or ``text`` for the string value.

        - index: this is the index of the score in the sidebar scoreboard.
        - score_offset: the number to subtract from the score.
        - color [optional]: The RGB tuple color of the text.
        """
        scoreboard_score = self.add_element(
            "scoreboard_score_element@anvil_common.label"
        )
        scoreboard_score.set_text("#score_string")
        scoreboard_score.set_color("$color")
        scoreboard_score.set_shadow("$shadow")
        scoreboard_score.set_layer(1)

        binding = scoreboard_score.add_binding().set_binding_type(
            UIBindingType.Collection
        )
        binding.set_binding_name("#player_score_sidebar")
        binding.set_binding_collection_name("scoreboard_scores")

        binding = scoreboard_score.add_binding().set_binding_type(UIBindingType.View)
        binding.set_source_property_name("(0 + #player_score_sidebar - $score_offset)")
        binding.set_target_property_name("#score_integer")

        binding = scoreboard_score.add_binding().set_binding_type(UIBindingType.View)
        binding.set_source_property_name("('§z' + #score_integer)")
        binding.set_target_property_name("#score_string")

        retrieve_score = self.add_element("retrieve_score@anvil_common.stack_panel")
        retrieve_score.set_size(("100%c", "100%c"))
        retrieve_score.keys("index", 0)
        retrieve_score.keys("shadow", False)
        retrieve_score.keys("score_offset", 0)
        retrieve_score.keys("color", (1, 1, 1))
        retrieve_score.keys("name", "('score_text_' + $index)")
        retrieve_score.set_collection_name("scoreboard_scores")
        retrieve_score.add_control(
            "$name@scoreboard_score_element"
        ).set_collection_index("$index")
        retrieve_score.set_visible(False)
        retrieve_score.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_control_name("$name").set_source_property_name(
            "#score_string"
        ).set_target_property_name(
            "#score_string"
        )
        retrieve_score.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_control_name("$name").set_source_property_name(
            "#score_integer"
        ).set_target_property_name(
            "#score_integer"
        )
        return self

    def queue(self, directory: str = "") -> "_AnvilCommon":
        return super().queue("anvil")
