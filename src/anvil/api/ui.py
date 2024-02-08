from anvil import ANVIL, CONFIG
from anvil.lib.lib import *
from anvil.lib.schemas import AddonObject
from PIL import Image

__all__ = [
    "UIBindingType",
    "UIElementType",
    "UIAnchor",
    "UITextAlignment",
    "UIAnimType",
    "UIEasing",
    "UIElementTrigger",
    "UIFontSize",
    "UI",
]

class UIBindingType(StrEnum):
    View = "view"
    Global = "global"
    Collection = "collection"
    CollectionDetails = "collection_details"
    NONE = "none"


class UIElementType(StrEnum):
    Image = "image"
    Panel = "panel"
    Label = "label"
    Screen = "screen"
    Factory = "factory"
    StackPanel = "stack_panel"
    Grid = "grid"
    Custom = "custom"
    Button = "button"


class UIAnchor(StrEnum):
    Center = "center"
    TopLeft = "top_left"
    TopMiddle = "top_middle"
    TopRight = "top_right"
    LeftMiddle = "left_middle"
    RightMiddle = "right_middle"
    BottomLeft = "bottom_left"
    BottomMiddle = "bottom_middle"
    BottomRight = "bottom_right"


class UITextAlignment(StrEnum):
    Center = "center"
    Left = "left"
    Right = "right"


class UIAnimType(StrEnum):
    Alpha = "alpha"
    Clip = "clip"
    Color = "color"
    Flip_book = "flip_book"
    Offset = "offset"
    Size = "size"
    UV = "uv"
    Wait = "wait"
    Aseprite_flip_book = "aseprite_flip_book"


class UIEasing(StrEnum):
    Linear = "linear"
    Spring = "spring"
    InQuad = "in_quad"
    OutQuad = "out_quad"
    InOutQuad = "in_out_quad"
    InCubic = "in_cubic"
    OutCubic = "out_cubic"
    InOutCubic = "in_out_cubic"
    InQuart = "in_quart"
    OutQuart = "out_quart"
    InOutQuart = "in_out_quart"
    InQuint = "in_quint"
    OutQuint = "out_quint"
    InOutQuint = "in_out_quint"
    InSine = "in_sine"
    OutSine = "out_sine"
    InOutSine = "in_out_sine"
    InExpo = "in_expo"
    OutExpo = "out_expo"
    InOutExpo = "in_out_expo"
    InCirc = "in_circ"
    OutCirc = "out_circ"
    InOutCirc = "in_out_circ"
    InBounce = "in_bounce"
    OutBounce = "out_bounce"
    InOutBounce = "in_out_bounce"
    InBack = "in_back"
    OutBack = "out_back"
    InOutBack = "in_out_back"
    InElastic = "in_elastic"
    OutElastic = "out_elastic"
    InOutElastic = "in_out_elastic"


class UIElementTrigger(StrEnum):
    Title = "title"
    Actionbar = "actionbar"
    NONE = "None"


class UIFontSize(StrEnum):
    Normal = "normal"
    Small = "small"
    Large = "large"
    ExtraLarge = "extra_large"


# Subclasses ==========================================================


class _UIBinding:
    def __init__(self) -> None:
        self._content = {}

    def binding_name(self, binding_name: str):
        self._content["binding_name"] = binding_name
        return self

    def binding_name_override(self, binding_name_override: str):
        self._content["binding_name_override"] = binding_name_override
        return self

    def binding_type(self, binding_type: UIBindingType = UIBindingType.View):
        self._content["binding_type"] = binding_type.value
        return self

    def binding_collection_name(self, binding_collection_name: str):
        self._content["binding_collection_name"] = binding_collection_name
        return self

    def binding_collection_prefix(self, binding_collection_prefix: str):
        self._content["binding_collection_prefix"] = binding_collection_prefix
        return self

    def source_control_name(self, source_control_name: str):
        self._content["source_control_name"] = source_control_name
        return self

    def source_property_name(self, source_property_name: str):
        self._content["source_property_name"] = source_property_name
        return self

    def target_property_name(self, target_property_name: str):
        self._content["target_property_name"] = target_property_name
        return self

    @property
    def resolve_sibling_scope(
        self,
    ):
        self._content["resolve_sibling_scope"] = True
        return self

    def binding_condition(self, binding_condition: str):
        self._content["binding_condition"] = binding_condition
        return self


class _UIButtonMapping:
    def __init__(self) -> None:
        self._content = {}

    def from_button_id(self, from_button_id: str):
        self._content["from_button_id"] = from_button_id
        return self

    def to_button_id(self, to_button_id: str):
        self._content["to_button_id"] = to_button_id
        return self

    def mapping_type(self, mapping_type: str):
        self._content["mapping_type"] = mapping_type
        return self

    def ignored(self, ignored: bool):
        self._content["ignored"] = ignored
        return self

    @property
    def button_up_right_of_first_refusal(self):
        self._content["button_up_right_of_first_refusal"] = True
        return self


class _UIModifications:
    def __init__(self) -> None:
        self._content = {}

    def remove(self, control_name: str):
        self._content["control_name"] = control_name
        self._content["operation"] = "remove"
        return self

    def insert_front(self, control_name: str):
        element = _UIElement(control_name)
        self._content["array_name"] = "controls"
        self._content["operation"] = "insert_front"
        self._content["value"] = element
        return element


class _UIElement:
    def __init__(self, element_name: str) -> None:
        self._element_name = element_name
        self._textures = []
        self.element = {}
        self._buttons: list[_UIButtonMapping] = []
        self._bindings: list[_UIBinding] = []
        self._controls: list[_UIElement] = []
        self._modifications: list[_UIModifications] = []

    @property
    def should_steal_mouse(self):
        self.element["should_steal_mouse"] = True
        return self

    @property
    def absorbs_input(self):
        self.element["absorbs_input"] = True
        return self

    def visible(self, visible: bool | str):
        self.element["visible"] = visible
        return self

    def fill(self, fill: bool | str):
        self.element["fill"] = fill
        return self

    def ignored(self, ignored: bool | str):
        self.element["ignored"] = ignored
        return self

    def enabled(self, enabled: bool | str):
        self.element["enabled"] = enabled
        return self

    def text(self, text: str):
        self.element["text"] = text
        return self

    def localize(self, localize: bool):
        self.element["localize"] = localize
        return self

    def renderer(self, renderer: str):
        self.element["renderer"] = renderer
        return self

    def type(self, type: UIElementType):
        self.element["type"] = type.value
        return self

    def orientation(self, orientation: str):
        self.element["orientation"] = orientation
        return self

    def anchor(self, anchor_from: UIAnchor, anchor_to: UIAnchor):
        self.element["anchor_from"] = anchor_from.value if isinstance(anchor_from, UIAnchor) else anchor_from
        self.element["anchor_to"] = anchor_to.value if isinstance(anchor_to, UIAnchor) else anchor_to
        return self

    def text_alignment(self, text_alignment: UITextAlignment):
        self.element["text_alignment"] = text_alignment.value
        return self

    def color(self, color: tuple[float, float, float]):
        self.element["color"] = color
        return self

    def font_size(self, font_size: UIFontSize):
        self.element["font_size"] = font_size.value
        return self

    def layer(self, layer: int):
        self.element["layer"] = layer
        return self

    def locked_control(self, locked_control: str):
        self.element["locked_control"] = locked_control
        return self

    def font_scale_factor(self, font_scale_factor: int):
        self.element["font_scale_factor"] = font_scale_factor
        return self

    def texture(self, texture: str, scale_factor: int = 1, *nineslice_size: int):
        if not "$" in texture:
            if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
                self.element["texture"] = os.path.join("textures", "ui", texture)
                self._textures.append(texture)
            else:
                ANVIL.config.Logger.file_exist_error(f"{texture}.png", os.path.join("assets", "textures", "ui"))
        else:
            self.element["texture"] = texture

        if len(nineslice_size) > 0 or scale_factor != 1:
            File(
                f"{texture}.json",
                {
                    "nineslice_size": nineslice_size[0] * scale_factor if len(nineslice_size) == 1 else [i * scale_factor for i in nineslice_size],
                    "base_size": [i * scale_factor for i in Image.open(os.path.join("assets", "textures", "ui", f"{texture}.png")).size],
                },
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                "w",
            )
        return self

    def texture_key(self, key: str, texture: str, scale_factor: int = 1, *nineslice_size: int):
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.element[f"${key}"] = os.path.join("textures", "ui", texture)
            self._textures.append(texture)
            if len(nineslice_size) > 0 or scale_factor != 1:
                File(
                    f"{texture}.json",
                    {
                        "nineslice_size": nineslice_size,
                        "base_size": [i * scale_factor for i in Image.open(os.path.join("assets", "textures", "ui", f"{texture}.png")).size],
                    },
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "w",
                )
        else:
            ANVIL.config.Logger.file_exist_error(f"{texture}.png", os.path.join("assets", "textures", "ui"))
        return self

    def aseprite_texture(self, texture: str):
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.texture(texture)
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                f"{texture}.json",
            )
        else:
            ANVIL.config.Logger.file_exist_error(f"{texture}.png", os.path.join("assets", "textures", "ui"))
        return self

    def aseprite_key(self, key: str, texture: str):
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.element[f"${key}"] = os.path.join("textures", "ui", texture)
            self._textures.append(texture)
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                f"{texture}.json",
            )
        else:
            ANVIL.config.Logger.file_exist_error(f"{texture}.png", os.path.join("assets", "textures", "ui"))
        return self

    def keys(self, key, value):
        self.element[f"${key}"] = value.value if isinstance(value, StrEnum) else value
        return self

    def property_bag(self, **properties):
        if "property_bag" not in self.element:
            self.element["property_bag"] = {}
        self.element["property_bag"].update({f"#{k}": v for k, v in properties.items()})
        return self

    @property
    def binding(self):
        if "bindings" not in self.element:
            self.element["bindings"] = []
        bind = _UIBinding()
        self._bindings.append(bind)
        return bind

    @property
    def button_mapping(self):
        if "button_mappings" not in self.element:
            self.element["button_mappings"] = []
        bind = _UIButtonMapping()
        self._buttons.append(bind)
        return bind

    @property
    def modification(self):
        if "modifications" not in self.element:
            self.element["modifications"] = []
        mod = _UIModifications()
        self._modifications.append(mod)
        return mod

    def control_ids(self, id: str, element: str):
        if "control_ids" not in self.element:
            self.element["control_ids"] = {}
        self.element["control_ids"][id] = element

        return self

    def controls(self, element_name: str):
        if "controls" not in self.element:
            self.element["controls"] = []

        ctrl = _UIElement(element_name)
        self._controls.append(ctrl)
        return ctrl

    def factory(self, name, id, element):
        if not id == "control_name":
            self.element["factory"] = {"name": name, "control_ids": {id: element}}
        else:
            self.element["factory"] = {"name": name, id: element}

        return self

    def size(self, size: str | tuple):
        self.element["size"] = size
        return self

    def tiled(self, bool: bool | str):
        self.element["tiled"] = bool
        return self

    def max_size(self, max_size: str | tuple):
        self.element["max_size"] = max_size
        return self

    def min_size(self, min_size: str | tuple):
        self.element["min_size"] = min_size
        return self

    def clip_ratio(self, clip_ratio: float | str):
        self.element["clip_ratio"] = clip_ratio
        return self

    def clip_direction(self, clip_direction: float | str):
        self.element["clip_direction"] = clip_direction
        return self

    def clip_pixelperfect(self, clip_pixelperfect: bool):
        self.element["clip_pixelperfect"] = clip_pixelperfect
        return self

    def maximum_grid_items(self, maximum_grid_items: int):
        self.element["maximum_grid_items"] = maximum_grid_items
        return self

    def line_padding(self, line_padding: int):
        self.element["line_padding"] = line_padding
        return self

    def uv(self, uv: tuple | str):
        self.element["uv"] = uv
        return self

    def uv_size(self, uv_size: tuple):
        self.element["uv_size"] = uv_size
        return self

    def alpha(self, alpha: str | tuple):
        self.element["alpha"] = alpha
        return self

    def offset(self, offset: str | tuple):
        self.element["offset"] = offset
        return self

    def clip_offset(self, clip_offset: tuple):
        self.element["clip_offset"] = clip_offset
        return self

    def keep_ratio(self, keep_ratio: bool):
        self.element["keep_ratio"] = keep_ratio
        return self

    def allow_clipping(self, allow_clipping: bool):
        self.element["allow_clipping"] = allow_clipping
        return self

    def grid_item_template(self, grid_item_template: bool):
        self.element["grid_item_template"] = grid_item_template
        return self

    def grid_dimension_binding(self, grid_dimension_binding: bool):
        self.element["grid_dimension_binding"] = grid_dimension_binding
        return self

    def grid_dimensions(self, grid_dimensions: tuple):
        self.element["grid_dimensions"] = grid_dimensions
        return self

    def grid_position(self, grid_position: tuple):
        self.element["grid_position"] = grid_position
        return self

    def grid_rescaling_type(self, grid_rescaling_type: str):
        self.element["grid_rescaling_type"] = grid_rescaling_type
        return self

    def grid_fill_direction(self, grid_fill_direction: str):
        self.element["grid_fill_direction"] = grid_fill_direction
        return self

    def collection_index(self, collection_index: int):
        self.element["collection_index"] = collection_index
        return self

    def collection_name(self, collection_name: bool):
        self.element["collection_name"] = collection_name
        return self

    def shadow(self, shadow: bool = False):
        self.element["shadow"] = shadow
        return self

    def use_anchored_offset(self, use_anchored_offset: bool = False):
        self.element["use_anchored_offset"] = use_anchored_offset
        return self

    def clips_children(self, clips_children: bool):
        self.element["clips_children"] = clips_children
        return self

    @property
    def enable_scissor_test(self):
        self.element["enable_scissor_test"] = True
        return self

    @property
    def focus_enabled(self):
        self.element["focus_enabled"] = True
        return self

    @property
    def propagate_alpha(self):
        self.element["propagate_alpha"] = True
        return self

    def variables(self, requires: str, **kwargs):
        if "variables" not in self.element:
            self.element["variables"] = []
        vars = {"requires": requires}
        for k, v in kwargs.items():
            vars.update({f"${k}": v})
        self.element["variables"].append(vars)
        return self

    @property
    def queue(self):
        for texture in self._textures:
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(
                    "resource_packs",
                    f"RP_{CONFIG._PASCAL_PROJECT_NAME}",
                    "textures",
                    "ui",
                ),
                f"{texture}.png",
            )
        for bind in self._bindings:
            self.element["bindings"].append(bind._content)
        for button in self._buttons:
            self.element["button_mappings"].append(button._content)
        for mod in self._modifications:
            if "value" in mod._content:
                mod._content["value"] = mod._content["value"].queue

            self.element["modifications"].append(mod._content)
        for ctrl in self._controls:
            self.element["controls"].append(ctrl.queue)
        return {self._element_name: self.element}


class _UIAnimationElement:
    def __init__(self, animation_name: str) -> None:
        self._animation_name = animation_name
        self.animation = {}

    def anim_type(self, anim_type: UIAnimType):
        self.animation["anim_type"] = anim_type.value
        return self

    def duration(self, duration: int | str):
        self.animation["duration"] = duration
        return self

    def next(self, next: str):
        self.animation["next"] = next
        return self

    def destroy_at_end(self, destroy_at_end: str):
        self.animation["destroy_at_end"] = destroy_at_end
        return self

    def play_event(self, play_event: str):
        self.animation["play_event"] = play_event
        return self

    def end_event(self, end_event: str):
        self.animation["end_event"] = end_event
        return self

    def start_event(self, start_event: str):
        self.animation["start_event"] = start_event
        return self

    def reset_event(self, reset_event: str):
        self.animation["reset_event"] = reset_event
        return self

    def easing(self, easing: UIEasing):
        self.animation["easing"] = easing.value
        return self

    def from_(self, from_: str | tuple):
        self.animation["from"] = from_
        return self

    def to(self, to: str | tuple):
        self.animation["to"] = to
        return self

    def initial_uv(self, initial_uv: tuple = (0, 0)):
        self.animation["initial_uv"] = initial_uv
        return self

    def fps(self, fps: int):
        self.animation["fps"] = fps
        return self

    def frame_count(self, frame_count: int):
        self.animation["frame_count"] = frame_count
        return self

    def frame_step(self, frame_step: int):
        self.animation["frame_step"] = frame_step
        return self

    @property
    def reversible(self):
        self.animation["reversible"] = True
        return self

    @property
    def resettable(self):
        self.animation["resettable"] = True
        return self

    @property
    def scale_from_starting_alpha(self):
        self.animation["scale_from_starting_alpha"] = True
        return self

    @property
    def activated(self):
        self.animation["activated"] = True
        return self

    @property
    def queue(self):
        return {self._animation_name: self.animation}

    def __str__(self) -> str:
        return self._animation_name


class _UICreditsConstructor:
    def __init__(self, hud_screen: "_UIScreen", credits_panel: _UIElement, credits_duration: int = 30) -> None:
        self._hud_screen = hud_screen

        anim = self._hud_screen._anvil_animation.add_animation("credits_scroll")
        anim.anim_type(UIAnimType.Offset)
        anim.duration(credits_duration)
        anim.from_((0, "160%")).to((0, "-160%"))
        anim.destroy_at_end("hud_title_text")

        self._credits_panel = credits_panel.controls("credits_text@anvil_common.stack_panel")
        self._credits_panel.offset("@anvil_animations.credits_scroll")

        self._element_count = 0

    def add_image(self, texture_name: str, scale_factor: int = 1, anchor = UIAnchor.Center, *nineslice_size: int):
        """Adds an image to the credits panel.

        Args:
            texture_name (str): The name of the texture.
            scale_factor (int, optional): The scale factor of the texture. Defaults to 1.
            anchor (UIAnchor, optional): The anchor of the image. Defaults to UIAnchor.Center.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        image = self._credits_panel.controls(f"panel_{self._element_count}@anvil_common.panel").size(("100%", "100%c")).controls(
            f"image_{self._element_count}@anvil_common.image"
        )
        image.texture(texture_name, scale_factor, *nineslice_size)
        image.size((50, 50))
        if anchor != UIAnchor.Center:
            image.anchor(anchor, anchor)

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
        title = self._credits_panel.controls(f"panel_{self._element_count}@anvil_common.panel").size(("100%", "100%c")).controls(
            f"title_{self._element_count}@anvil_common.label"
        )
        title.text(text)
        if font_size != UIFontSize.Normal:
            title.font_size(font_size)
        if color != (1, 1, 1):
            title.color(color)
        if text_alignment != UITextAlignment.Center:
            title.text_alignment(text_alignment)
            title.size(("100%", "default"))
            
        self._element_count += 1
        return self

    def add_space(self, size: int | str):
        """Adds a space to the credits panel.

        Args:
            size (int | str): The size of the space.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        space = self._credits_panel.controls(f"space_{self._element_count}@anvil_common.panel")
        space.size((0, size))
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
        # Section Setup
        section = self._credits_panel.controls(f"credits_section_{self._element_count}@anvil_common.stack_panel")
        section.orientation("horizontal")
        section.size(("100%", "100%c"))

        # Section title
        title = section.controls(f"panel_title_{self._element_count}@anvil_common.panel").size(("45%", "100%c")).controls(f"title_{self._element_count}@anvil_common.label")
        title.text(section_title)
        title.size(("100%", "default"))
        title.text_alignment(UITextAlignment.Right)
        if title_font_size != UIFontSize.Normal:
            title.font_size(title_font_size)
        if title_color != (1, 1, 1):
            title.color(title_color)

        # Section separator
        section.controls(f"section_sep_{self._element_count}@anvil_common.panel").size(("10%", 0))

        ## Section names
        names = section.controls(f"names_{self._element_count}@anvil_common.stack_panel")
        names.size(("45%", "100%c"))
        for i, n in enumerate(section_names):
            name = names.controls(f"name_{i}_{self._element_count}@anvil_common.label")
            name.text(n)
            name.text_alignment(UITextAlignment.Left)
            if names_font_size != UIFontSize.Normal:
                name.font_size(names_font_size)
            if names_color != (1, 1, 1):
                name.color(names_color)

        self._element_count += 1

# UI files ============================================================
class _UIVariables(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")

    def __init__(self) -> None:
        super().__init__("_global_variables")

    def add_variable(self, variable, value):
        self._content.update({variable: value})


class _UIDefs(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH)
    
    def __init__(self) -> None:
        super().__init__("_ui_defs")
        self.do_not_shorten
        self._files = []

    def add_file(self, path: str):
        self._files.append(path.replace("\\", "/"))

    @property
    def queue(self):
        self.content({"ui_defs": self._files})
        return super().queue("ui")


class _UIAnimation(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")

    def __init__(self, name: str, namespace: str, defs: _UIDefs) -> None:
        super().__init__(name)
        self.name = name
        self._defs = defs
        self.namespace = namespace
        self._animations: list[_UIAnimationElement] = []
        self._content = {
            "namespace": namespace,
        }

    def add_animation(self, animation_name: str):
        self._animations.append(_UIAnimationElement(animation_name))
        return self._animations[-1]

    def queue(self, directory: str = ""):
        for anim in self._animations:
            self._content.update(anim.queue)

        self._defs.add_file(os.path.join("ui", directory, f"{self.name}{_UIScreen._extension}"))
        return super().queue(directory)


class _UIScreen(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")

    def __init__(self, name: str, namespace: str, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__(name)
        self._content = {
            "namespace": namespace,
        }
        self.name = name
        self.namespace = namespace
        self._elements: list[_UIElement] = []
        self._anvil_animation = anvil_animation
        self._variables = variables
        self._defs = defs
        self._ignored_title_texts = []
        self._ignored_actionbar_texts = []
        self._hides_hud = []
        self.do_not_shorten

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
        hides_hud: bool = False,
    ):
        # Element name
        new_element = _UIElement(element_name)

        match trigger:
            case UIElementTrigger.Title:
                if not keyword is None:
                    self._variables.add_variable(f"$anvil.{element_name}.text", f"{CONFIG.NAMESPACE}:{keyword}")
                    self._variables.add_variable(f"$anvil.{element_name}.bool", f"(not ((#title_text - $anvil.{element_name}.text) = #title_text))")
                    self._ignored_title_texts.append(f"$anvil.{element_name}.text")
                    if hides_hud:
                        self._hides_hud.append(f"$anvil.{element_name}.text")

                    new_element = _UIElement(f"{element_name}@anvil_common.title_binding")
                    new_element.keys("binding_text", f"$anvil.{element_name}.bool")

                factory = self.add_element(f"{element_name}_factory")
                factory.type(UIElementType.Panel)
                factory.factory("hud_title_text_factory", "hud_title_text", f"{element_name}_element@{self.namespace}.{element_name}")
                self._elements.append(factory)

            case UIElementTrigger.Actionbar:
                if not keyword is None:
                    self._variables.add_variable(f"$anvil.{element_name}.text", f"{CONFIG.NAMESPACE}:{keyword}")
                    self._variables.add_variable(f"$anvil.{element_name}.bool", f"(not(($text - $anvil.{element_name}.text) = $text))")
                    self._ignored_actionbar_texts.append(f"$anvil.{element_name}.text")

                    new_element = _UIElement(f"{element_name}@anvil_common.actionbar_binding")
                    new_element.keys("binding_text", f"$anvil.{element_name}.bool")

                factory: _UIElement = self.add_element(f"{element_name}_factory")
                factory.type(UIElementType.Panel)
                factory.factory(
                    "hud_actionbar_text_factory",
                    "hud_actionbar_text",
                    f"{element_name}_element@anvil_hud.{element_name}",
                )

        self._elements.append(new_element)
        return new_element

    def queue(self, directory: str = ""):
        for element in self._elements:
            self._content.update(element.queue)

        if self._content != {"namespace": self.namespace}:
            self._defs.add_file(os.path.join("ui", directory, f"{self.name}{_UIScreen._extension}"))
            return super().queue(directory)

# UI Screens ==========================================================
# Vanilla
class _HUDScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__("hud_screen", "hud", anvil_animation, variables, defs)
        # Disable HUD
        self.root_panel = self.add_element("root_panel")
        self.anvil_element = self.root_panel.modification.insert_front("anvil@anvil_hud.anvil_hud")

        self.hud_title_text = self.add_element("hud_title_text")
        self.hud_title_text.binding.binding_name("#hud_title_text_string").binding_name_override("#text")
        self.hud_title_text.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#subtext")

        self.hud_actionbar_text = self.add_element("hud_actionbar_text")
        self.hud_actionbar_text.keys("text", "$actionbar_text")

        variables.add_variable("$anvil.show.text", f"{CONFIG.NAMESPACE}:show")
        variables.add_variable("$anvil.hide.text", f"{CONFIG.NAMESPACE}:hide")
        self._ignored_title_texts = ["$anvil.show.text"]
        self._ignored_actionbar_texts = ["$anvil.hide.text"]
        self._hides_hud = ["$anvil.hide.text"]

    def disable_mouse(self):
        self.add_element("hud_screen@common.base_screen").should_steal_mouse.absorbs_input
        self.root_panel.modification.remove("curor_rend")
        return self

    def disable_mob_effect(self):
        self.root_panel.modification.remove("mob_effects_renderer")
        return self

    def disable_helpers(self):
        self.root_panel.modification.remove("left_helpers")
        self.root_panel.modification.remove("right_helpers")
        self.root_panel.modification.remove("emote_expediate_helpers")
        return self

    def disable_hotbar(self):
        self.root_panel.modification.remove("centered_gui_elements")
        self.root_panel.modification.remove("centered_gui_elements_at_bottom_middle")
        self.root_panel.modification.remove("centered_ridingvr_gui_elements")
        self.root_panel.modification.remove("not_centered_gui_elements")
        self.root_panel.modification.remove("exp_rend")
        self.root_panel.modification.remove("exp_rend_resizable")
        return self

    def disable_sidebar(self):
        self.root_panel.modification.remove("sidebar")
        return self

    def queue(self, directory: str = ""):
        return super().queue()


class _NPCScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__("npc_interact_screen", "npc_interact", anvil_animation, variables, defs)
        self._npc_screen = self.add_element("npc_screen@common.base_screen").keys("screen_content", "anvil_npc.npc_screen_chooser")

    def add_element(self, element_name: str, trigger: UIElementTrigger = UIElementTrigger.NONE, keyword: str = None):
        return super().add_element(element_name, trigger, keyword, False)
    
    def queue(self, directory: str = ""):
        return super().queue()


# Anvil
class _AnvilHUDScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__("hud", "anvil_hud", anvil_animation, variables, defs)
        self.anvil_hud: _UIElement = super().add_element("anvil_hud")
        self.anvil_hud.type(UIElementType.Panel)

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
        hides_hud: bool = False,
    ):
        if trigger is not UIElementTrigger.NONE:
            self.anvil_hud.controls(f"{element_name}_instance@anvil_hud.{element_name}_factory")

        return super().add_element(element_name, trigger, keyword, hides_hud)

    def add_image_panel(
        self,
        name: str,
        background: str = "transparent",
        direction_out: bool = True,
        zoom_in: float = 1,
        zoom_wait: float = 6,
        zoom_out: float = 1,
    ):
        # element
        image_element = self.add_element(name, UIElementTrigger.Title, name)
        image_element.type(UIElementType.Panel)
        image_element.size(("100%", "100%"))
        image_element.layer(100)
        image_element.anchor(UIAnchor.Center, UIAnchor.Center)

        if not background == "transparent":
            background_image = image_element.controls(f"{name}_background")
            background_image.type(UIElementType.Image)
            background_image.texture(background)
            background_image.size(("100%", "100%"))
            background_image.keep_ratio(False)

        image = image_element.controls(f"{name}_image")
        image.type(UIElementType.Image)
        image.texture(name)
        image.anchor(UIAnchor.Center, UIAnchor.Center)
        image.offset((0, "-20px"))

        tip = image_element.controls(f"{name}_tip")
        tip.type(UIElementType.Label)
        tip.text_alignment(UITextAlignment.Center)
        tip.size(("80%", "default"))
        tip.offset((0, "100px"))
        tip.text("#text").shadow(True).font_size(UIFontSize.Large)
        tip.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#text")

        zoom_steps = []
        if direction_out:
            zoom_steps = ["30%", "40%", "50%"]
        else:
            zoom_steps = ["400%", "70%", "60%"]

        # animations
        self._variables.add_variable(f"$anvil.image.{name}_in", zoom_in)
        self._variables.add_variable(f"$anvil.image.{name}_wait", zoom_wait)
        self._variables.add_variable(f"$anvil.image.{name}_out", zoom_out)

        image_zoom_in = self._anvil_animation.add_animation(f"{name}_zoom_in")
        image_zoom_in.anim_type(UIAnimType.Size)
        image_zoom_in.easing(UIEasing.Linear)
        image_zoom_in.from_((zoom_steps[0], zoom_steps[0])).to((zoom_steps[1], zoom_steps[1]))
        image_zoom_in.duration(f"$anvil.image.{name}_in")
        image_zoom_in.next(f"@anvil_animations.{name}_zoom_wait")

        image_zoom_wait = self._anvil_animation.add_animation(f"{name}_zoom_wait")
        image_zoom_wait.anim_type(UIAnimType.Wait)
        image_zoom_wait.duration(f"$anvil.image.{name}_wait")
        image_zoom_wait.next(f"@anvil_animations.{name}_zoom_out")
        image_zoom_out = self._anvil_animation.add_animation(f"{name}_zoom_out")

        image_zoom_out.anim_type(UIAnimType.Size)
        image_zoom_out.easing(UIEasing.Linear)
        image_zoom_out.from_((zoom_steps[1], zoom_steps[1])).to((zoom_steps[2], zoom_steps[2]))
        image_zoom_out.duration(f"$anvil.image.{name}_out")

        image_alpha_in = self._anvil_animation.add_animation(f"{name}_alpha_in")
        image_alpha_in.anim_type(UIAnimType.Alpha)
        image_alpha_in.easing(UIEasing.OutQuad)
        image_alpha_in.from_(0)
        image_alpha_in.to(1)
        image_alpha_in.duration(f"$anvil.image.{name}_in")
        image_alpha_in.next(f"@anvil_animations.{name}_alpha_wait")
        image_alpha_wait = self._anvil_animation.add_animation(f"{name}_alpha_wait")
        image_alpha_wait.anim_type(UIAnimType.Wait)
        image_alpha_wait.duration(f"$anvil.image.{name}_wait")
        image_alpha_wait.next(f"@anvil_animations.{name}_alpha_out")
        image_alpha_out = self._anvil_animation.add_animation(f"{name}_alpha_out")
        image_alpha_out.anim_type(UIAnimType.Alpha)
        image_alpha_out.easing(UIEasing.InOutSine)
        image_alpha_out.from_(1)
        image_alpha_out.to(0)
        image_alpha_out.duration(f"$anvil.image.{name}_out")
        image_alpha_out.destroy_at_end("hud_title_text")

        image.size(f"@anvil_animations.{name}_zoom_in" if zoom_in > 0 else ("50%", "50%"))
        image.alpha(f"@anvil_animations.{name}_alpha_in" if zoom_in > 0 else 1)

        return image_element

    # Layer 100
    def add_logo(self):
        self.add_image_panel("logo")

    # Layer 101
    def add_blinking_screen(self):
        # animation
        blink_fade_in = self._anvil_animation.add_animation("blink_fade_in")
        blink_fade_in.anim_type(UIAnimType.Alpha)
        blink_fade_in.easing(UIEasing.InOutSine)
        blink_fade_in.from_(0).to(1)
        self._variables.add_variable("$anvil.blink.fade_in", 1)
        blink_fade_in.duration("$anvil.blink.fade_in")
        blink_fade_in.next("@anvil_animations.blink_fade_stay")

        blink_fade_stay = self._anvil_animation.add_animation("blink_fade_stay")
        blink_fade_stay.anim_type(UIAnimType.Wait)
        self._variables.add_variable("$anvil.blink.fade_stay", 1)
        blink_fade_stay.duration("$anvil.blink.fade_stay")
        blink_fade_stay.next("@anvil_animations.blink_fade_out")

        blink_fade_out = self._anvil_animation.add_animation("blink_fade_out")
        blink_fade_out.anim_type(UIAnimType.Alpha)
        blink_fade_out.easing(UIEasing.InOutSine)
        blink_fade_out.from_(1).to(0)
        self._variables.add_variable("$anvil.blink.fade_out", 1)
        blink_fade_out.duration("$anvil.blink.fade_out")
        # blink_fade_out.destroy_at_end('hud_title_text')
        # element
        blink_element = self.add_element("blink_element", UIElementTrigger.Title, "blink")
        blink_element.type(UIElementType.Image)
        blink_element.layer(101)
        blink_element.texture("black_element")
        blink_element.anchor(UIAnchor.Center, UIAnchor.Center)
        blink_element.size(("300%", "300%"))
        blink_element.alpha("@anvil_animations.blink_fade_in")

    # Layer 101
    def add_black_bars(self):
        black_bars_in = self._anvil_animation.add_animation("black_bars_in")
        black_bars_in.anim_type(UIAnimType.Size)
        black_bars_in.easing(UIEasing.InOutSine)
        black_bars_in.from_(("300%", "300%")).to(("300%", "100%"))
        self._variables.add_variable("$anvil.black_bars.in", 1.6)
        black_bars_in.duration("$anvil.black_bars.in")
        black_bars_in.next("@anvil_animations.black_bars_wait")

        black_bars_wait = self._anvil_animation.add_animation("black_bars_wait")
        black_bars_wait.anim_type(UIAnimType.Wait)
        self._variables.add_variable("$anvil.black_bars.stay", 1)
        black_bars_wait.duration("$anvil.black_bars.stay")

        black_bars_out = self._anvil_animation.add_animation("black_bars_out")
        black_bars_out.anim_type(UIAnimType.Size)
        black_bars_out.easing(UIEasing.InOutSine)
        black_bars_out.from_(("300%", "100%")).to(("300%", "300%"))
        self._variables.add_variable("$anvil.black_bars.out", 1.6)
        black_bars_out.duration("$anvil.black_bars.out")
        # black_bars_out.destroy_at_end('hud_title_text')

        # element
        black_bars = self.add_element("black_bars_element", UIElementTrigger.Actionbar)
        black_bars.type(UIElementType.Image)
        black_bars.texture("black_bars")
        black_bars.keep_ratio(False)
        black_bars.anchor(UIAnchor.Center, UIAnchor.Center)
        black_bars.layer(101)
        black_bars.keys("anim_size", ("300%", "300%"))
        black_bars.keys("text", "$actionbar_text")
        black_bars.variables(
            "$anvil.black_bars_in.bool",
            anim_size="@anvil_animations.black_bars_in",
        )
        black_bars.variables(
            "$anvil.black_bars_out.bool",
            anim_size="@anvil_animations.black_bars_out",
        )
        black_bars.size("$anim_size")

        self._variables.add_variable(f"$anvil.black_bars_in.text", f"{CONFIG.NAMESPACE}:bars_in")
        self._variables.add_variable(f"$anvil.black_bars_in.bool", f"($text = $anvil.black_bars_in.text)")
        self._variables.add_variable(f"$anvil.black_bars_out.text", f"{CONFIG.NAMESPACE}:bars_out")
        self._variables.add_variable(f"$anvil.black_bars_out.bool", f"($text = $anvil.black_bars_out.text)")

        self._ignored_actionbar_texts.extend(
            [
                "($text = $anvil.black_bars_in.text)",
                "($text = $anvil.black_bars_out.text)",
            ]
        )


    def credits_screen_constructor(self, credits_duration: int = 30):
        credits = self.add_element("credits", UIElementTrigger.Title, "credits")
        credits.type(UIElementType.Panel)
        credits.layer(100)

        background_image = credits.controls("credits_background@anvil_common.image")
        background_image.texture("black_element")
        background_image.size(("100%", "100%"))
        background_image.keep_ratio(False)
        background_image.layer(-1)

        return _UICreditsConstructor(self, credits, credits_duration)


    def queue(self, directory: str = ""):
        return super().queue("anvil")


class _AnvilNPCScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__("npc", "anvil_npc", anvil_animation, variables, defs)
        self._ignored_panel_texts = []

        self._npc_screen_chooser = self.add_element("npc_screen_chooser").type(UIElementType.Panel)
        vanilla = self._npc_screen_chooser.controls("vanilla@npc_interact.npc_screen_contents").layer(500)
        vanilla.binding.binding_type(UIBindingType.Global).binding_name("#title_text").binding_name_override("#title_text")
        vanilla.binding.binding_type(UIBindingType.View).source_property_name("$anvil.npc_screen.vanilla").target_property_name("#visible")

    def add_element(self, element_name: str, trigger: UIElementTrigger = UIElementTrigger.NONE, keyword: str = None):
        return super().add_element(element_name, trigger, keyword, False)
    
    def queue(self, directory: str = ""):
        self._variables.add_variable("$anvil.npc_screen.vanilla", f'({" and ".join(self._ignored_panel_texts)})')
        return super().queue("anvil")


class _AnvilCommon(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs) -> None:
        super().__init__("common", "anvil_common", anvil_animation, variables, defs)
        self.basic_components()
        self.image_label()
        self.title_actionbar()
        self.scoreboard_retrieve()
        self.complex_components()

    def add_element(self, element_name: str, trigger: UIElementTrigger = UIElementTrigger.NONE, keyword: str = None):
        return super().add_element(element_name, trigger, keyword, False)
    
    def basic_components(self):
        # ---------------------------
        # Label
        # Must supply your own text
        # ---------------------------
        label = self.add_element("label")
        label.type(UIElementType.Label)
        label.text_alignment(UITextAlignment.Center)

        # ---------------------------
        # Image
        # Must supply your own texture
        # ---------------------------
        image = self.add_element("image")
        image.type(UIElementType.Image)

        # ---------------------------
        # Stack Panel
        # ---------------------------
        stack_panel = self.add_element("stack_panel")
        stack_panel.type(UIElementType.StackPanel)

        # ---------------------------
        # Stack Panel
        # ---------------------------
        panel = self.add_element("panel")
        panel.type(UIElementType.Panel)

    def complex_components(self):
        # npc model renderer (for npc screen)
        npc_renderer = self.add_element("npc_renderer")
        npc_renderer.type(UIElementType.Panel)
        npc_renderer.size(("100%", "100%"))
        npc_renderer.clips_children(True)
        npc_model = npc_renderer.controls("npc_model")
        npc_model.type(UIElementType.Custom)
        npc_model.layer(5)
        npc_model.renderer("actor_portrait_renderer")
        npc_model.size(("120%", "120%"))
        npc_model.enable_scissor_test
        npc_model.binding.binding_type(UIBindingType.Collection).binding_collection_name("skins_collection").binding_name("#skin_index")

        # player model renderer
        player_renderer = self.add_element("player_renderer")
        player_renderer.type(UIElementType.Panel)
        player_renderer.size(("80%", "80%"))
        player_renderer.clips_children(True)
        player_model = player_renderer.controls("player_model")
        player_model.type(UIElementType.Custom)
        player_model.renderer("live_player_renderer")
        player_model.size(("80%", "80%"))
        player_model.enable_scissor_test
        player_model.offset((0, "50%y"))

    def image_label(self):
        # ---------------------------
        # Image Label
        # Must supply your own text key
        # Must supply your own texture
        # ---------------------------
        image_label = self.add_element("image_label@anvil_common.image")
        image_label.size(("100%c + 8px", "100%c + 4px"))
        image_label.keys("text", "PLACEHOLDER TEXT")
        image_label.keys("localize", False)
        label = image_label.controls("label@anvil_common.label")
        label.text("$text")
        label.localize("$localize")

        # ---------------------------
        # Image Label Binding
        # Must supply your own control name key that has a text binding
        # Must supply your own texture
        # ---------------------------
        image_label_binding = self.add_element("image_label_binding@anvil_common.image")
        image_label_binding.size(("100%c + 8px", "100%c + 4px"))
        label_binding = image_label_binding.controls("text@anvil_common.label")
        label_binding.text("#text")
        label_binding.layer(1)
        label_binding.binding.binding_type(UIBindingType.View).source_control_name("$control_name").source_property_name("#text").target_property_name("#text")

    def title_actionbar(self):
        title_binding = self.add_element("title_binding")
        title_binding.property_bag(title_text="", subtitle_text="")
        title_binding.binding.binding_name("#hud_title_text_string").binding_name_override("#title_text")
        title_binding.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#subtitle_text")
        title_binding.binding.binding_type(UIBindingType.View).source_property_name("$binding_text").target_property_name("#visible")

        actionbar_binding = self.add_element("actionbar_binding")
        actionbar_binding.keys("text", "$actionbar_text")
        actionbar_binding.visible("$binding_text")

    def scoreboard_retrieve(self):
        """Use ``retrieve_score`` as the element. A few variables must be passed.
        To retrieve the score value, you must call the source_control_name using the element based on``retrieve_score``, then call the property ``score`` for the int value, or ``text`` for the string value.

        - index: this is the index of the score in the sidebar scoreboard.
        - score_offset: the number to subtract from the score.
        - color [optional]: The RGB tuple color of the text.
        """
        scoreboard_score = self.add_element("scoreboard_score_element@anvil_common.label")
        scoreboard_score.text("#text")
        scoreboard_score.color("$color")
        scoreboard_score.shadow("$shadow")
        scoreboard_score.layer(1)
        scoreboard_score.binding.binding_name("#player_score_sidebar").binding_type(UIBindingType.Collection).binding_collection_name("scoreboard_scores")
        scoreboard_score.binding.binding_type(UIBindingType.View).source_property_name("('§z' + ((#player_score_sidebar * 1) - $score_offset))").target_property_name("#text")
        scoreboard_score.binding.binding_type(UIBindingType.View).source_property_name("((#player_score_sidebar * 1) - $score_offset)").target_property_name("#score")

        retrieve_score = self.add_element("retrieve_score@anvil_common.stack_panel")
        retrieve_score.size(("100%c", "100%c"))
        retrieve_score.keys("index", 0)
        retrieve_score.keys("shadow", False)
        retrieve_score.keys("score_offset", 0)
        retrieve_score.keys("color", (1, 1, 1))
        retrieve_score.keys("name", "('score_text_' + $index)")
        retrieve_score.collection_name("scoreboard_scores")
        retrieve_score.controls("$name@scoreboard_score_element").collection_index("$index")
        retrieve_score.visible(False)
        retrieve_score.binding.binding_type(UIBindingType.View).source_control_name("$name").source_property_name("#text").target_property_name("#text")
        retrieve_score.binding.binding_type(UIBindingType.View).source_control_name("$name").source_property_name("#score").target_property_name("#score")

    def queue(self, directory: str = ""):
        return super().queue("anvil")


class _AnvilAnimations(_UIAnimation):
    def __init__(self, defs: _UIDefs) -> None:
        super().__init__("animations", "anvil_animations", defs)

    @property
    def queue(self):
        return super().queue("anvil")


class UI:
    _extension = {0: ".json", 1: ".json"}

    def __init__(self) -> None:
        self._defs = _UIDefs()
        self.variables = _UIVariables()

        self.animations_screen = _AnvilAnimations(self._defs)

        self.hud_screen = _HUDScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_hud_screen = _AnvilHUDScreen(self.animations_screen, self.variables, self._defs)

        self.npc_screen = _NPCScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_npc_screen = _AnvilNPCScreen(self.animations_screen, self.variables, self._defs)

        self.anvil_common = _AnvilCommon(self.animations_screen, self.variables, self._defs)

        self._screens: list[_UIScreen] = [
            self.hud_screen,
            self.anvil_hud_screen,
            self.npc_screen,
            self.anvil_npc_screen,
            self.anvil_common
        ]

    def add_ui_screen(self, filename, namespace):
        self._screens.append(_UIScreen(filename, namespace, self.animations_screen, self.variables, self._defs))
        return self._screens[-1]

    def queue(self):
        self.anvil_hud_screen._variables.add_variable("$anvil.empty.text", "")
        self.anvil_hud_screen._ignored_title_texts.append("$anvil.empty.text")
        self.anvil_hud_screen._ignored_actionbar_texts.append("$anvil.empty.text")
        # Manage Titles, Subtitles and actionbars
        ignored_title_texts = self.hud_screen._ignored_title_texts
        ignored_title_texts.extend(self.anvil_hud_screen._ignored_title_texts)

        ignored_actionbar_texts = self.hud_screen._ignored_actionbar_texts
        ignored_actionbar_texts.extend(self.anvil_hud_screen._ignored_actionbar_texts)
        
        hides_hud = self.hud_screen._hides_hud

        # Add to ANVIL queue
        for screen in self._screens:
            ignored_actionbar_texts.extend(screen._ignored_actionbar_texts)
            ignored_title_texts.extend(screen._ignored_title_texts)
            hides_hud.extend(screen._hides_hud)

        self.anvil_hud_screen._variables.add_variable(
            f"$anvil.title_visible.bool",
            f"({'(' * len(ignored_title_texts)}#text - " + " - ".join(f"{var})" for var in ignored_title_texts) + " = #text)",
        )
        self.anvil_hud_screen._variables.add_variable(
            f"$anvil.actionbar_visible.bool",
            f"({'(' * len(ignored_actionbar_texts)}$text - " + " - ".join(f"{var})" for var in ignored_actionbar_texts) + " = $text)",
        )

        self.hud_screen.hud_title_text.binding.binding_type(UIBindingType.View).source_property_name(
            f"$anvil.title_visible.bool"
        ).target_property_name("#visible")
        self.hud_screen.hud_actionbar_text.visible(f"$anvil.actionbar_visible.bool")

        source_prop = f"(#hud_visible and ({'(' * len(hides_hud)}#text - " + " - ".join(f"{var})" for var in hides_hud) + " = #text))"

        self.hud_screen.root_panel.binding.binding_name("#hud_visible")
        self.hud_screen.root_panel.binding.binding_name("#hud_title_text_string").binding_name_override("#text")
        self.hud_screen.root_panel.binding.binding_type(UIBindingType.View).source_property_name(source_prop).target_property_name("#visible")

        for screen in self._screens:
            screen.queue("anvil")

        self.animations_screen.queue
        self.variables.queue()

        self._defs.queue
