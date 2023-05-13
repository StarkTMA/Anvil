from ..core import ANVIL, NAMESPACE, PASCAL_PROJECT_NAME, AddonObject
from ..packages import *

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


class UIBindingType:
    View = "view"
    Global = "global"
    Collection = "collection"
    CollectionDetails = "collection_details"
    NONE = "none"


class UIElementType:
    Image = "image"
    Panel = "panel"
    Label = "label"
    Screen = "screen"
    Factory = "factory"
    StackPanel = "stack_panel"
    Grid = 'grid'
    Custom = 'custom'
    Button = 'button'


class UIAnchor:
    Center = "center"
    TopLeft = "top_left"
    TopMiddle = "top_middle"
    TopRight = "top_right"
    LeftMiddle = "left_middle"
    RightMiddle = "right_middle"
    BottomLeft = "bottom_left"
    BottomMiddle = "bottom_middle"
    BottomRight = "bottom_right"


class UITextAlignment:
    Center = "center"
    Left = "left"
    Right = "right"


class UIAnimType:
    Alpha = "alpha"
    Clip = "clip"
    Color = "color"
    Flip_book = "flip_book"
    Offset = "offset"
    Size = "size"
    UV = "uv"
    Wait = "wait"
    Aseprite_flip_book = "aseprite_flip_book"


class UIEasing:
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


class UIElementTrigger:
    Title = "title"
    Actionbar = "actionbar"
    NONE = None


class UIFontSize:
    Normal = "normal"
    Small = "small"
    Large = "large"
    ExtraLarge = "extra_large"


class _UIVariables(AddonObject):
    _extensions = {
        0: ".json", 
        1: ".json"
    }
    def __init__(self) -> None:
        super().__init__("_global_variables", MakePath("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "ui"))

    def add_variable(self, variable, value):
        self._content.update({variable: value})


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
        self._content["binding_type"] = binding_type
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
    def resolve_sibling_scope(self,):
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

    def enabled(self, enabled: bool | str):
        self.element["enabled"] = enabled
        return self

    def text(self, text: str):
        self.element["text"] = text
        return self

    def renderer(self, renderer: str):
        self.element["renderer"] = renderer
        return self

    def type(self, type: UIElementType):
        self.element["type"] = type
        return self

    def orientation(self, orientation: str):
        self.element["orientation"] = orientation
        return self

    def anchor(self, anchor_from: UIAnchor, anchor_to: UIAnchor):
        self.element["anchor_from"] = anchor_from
        self.element["anchor_to"] = anchor_to
        return self

    def text_alignment(self, text_alignment: UITextAlignment):
        self.element["text_alignment"] = text_alignment
        return self

    def font_size(self, font_size: UIFontSize):
        self.element["font_size"] = font_size
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

    def texture(self, texture: str, *nineslice_size: int):
        if not "$" in texture:
            CheckAvailability(
                f"{texture}.png", "sprite", MakePath("assets", "textures", "ui")
            )
            self.element["texture"] = MakePath("textures", "ui", texture)
            self._textures.append(texture)
        else:
            self.element["texture"] = texture

        if len(nineslice_size) > 0:
            File(
                f"{texture}.json",
                {
                    "nineslice_size": nineslice_size,
                    "base_size": Image.open(
                        MakePath("assets", "textures", "ui", f"{texture}.png")
                    ).size,
                },
                MakePath(
                    "resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "textures", "ui"
                ),
                "w",
            )
        return self

    def aseprite_texture(self, texture: str):
        CheckAvailability(
            f"{texture}.png", "sprite", MakePath("assets", "textures", "ui")
        )
        self.element["texture"] = MakePath("textures", "ui", texture)
        CopyFiles(
            MakePath("assets", "textures", "ui"),
            MakePath("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "textures", "ui"),
            f"{texture}.json",
        )
        return self

    def keys(self, key, value):
        self.element[f"${key}"] = value
        return self

    def property_bag(self, **properties):
        if "property_bag" not in self.element:
            self.element["property_bag"] = {}
        self.element["property_bag"].update({
            f'#{k}': v for k,v in properties.items()
        })
        return self

    def texture_key(self, key: str, texture: str, *nineslice_size: int):
        CheckAvailability(
            f"{texture}.png", "sprite", MakePath("assets", "textures", "ui")
        )
        self.element[f"${key}"] = MakePath("textures", "ui", texture)
        self._textures.append(texture)
        if len(nineslice_size) > 0:
            File(
                f"{texture}.json",
                {
                    "nineslice_size": nineslice_size,
                    "base_size": Image.open(
                        MakePath("assets", "textures", "ui", f"{texture}.png")
                    ).size,
                },
                MakePath(
                    "resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "textures", "ui"
                ),
                "w",
            )
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
        self.element["factory"] = {"name": name, "control_ids": {id: element}}
        return self

    def size(self, size: str | tuple):
        self.element["size"] = size
        return self

    def maximum_grid_items(self, maximum_grid_items: int):
        self.element["maximum_grid_items"] = maximum_grid_items
        return self

    def line_padding(self, line_padding: int):
        self.element["line_padding"] = line_padding
        return self

    def uv(self, uv: tuple):
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

    def keep_ratio(self, visible: bool):
        self.element["keep_ratio"] = visible
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
        self.element['grid_dimensions'] = grid_dimensions
        return self
    
    def grid_position(self, grid_position: tuple):
        self.element['grid_position'] = grid_position
        return self
    
    def grid_rescaling_type(self, grid_rescaling_type: str):
        self.element["grid_rescaling_type"] = grid_rescaling_type
        return self

    def grid_fill_direction(self, grid_fill_direction: str):
        self.element["grid_fill_direction"] = grid_fill_direction
        return self

    def collection_index(self, collection_index: int):
        self.element['collection_index'] = collection_index
        return self
    
    def collection_name(self, collection_name: bool):
        self.element["collection_name"] = collection_name
        return self

    @property
    def shadow(self):
        self.element["shadow"] = True
        return self

    @property
    def clips_children(self):
        self.element["clips_children"] = True
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
        for k,v in kwargs.items():
            vars.update({
                f"${k}": v
            })
        self.element["variables"].append(vars)
        return self

    @property
    def queue(self):
        for texture in self._textures:
            CopyFiles(
                MakePath("assets", "textures", "ui"),
                MakePath("resource_packs",f"RP_{PASCAL_PROJECT_NAME}","textures","ui",),
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
        self.animation["anim_type"] = anim_type
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
        self.animation["easing"] = easing
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


class _UIAnimation(AddonObject):
    _extensions = {
        0: ".json", 
        1: ".json"
    }
    def __init__(self, name: str, namespace: str) -> None:
        super().__init__(name, MakePath("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "ui"))
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
        return super().queue(directory)


class _UIScreen(AddonObject):
    _extensions = {
        0: ".json", 
        1: ".json"
    }
    def __init__(
        self,
        name: str,
        namespace: str,
        anvil_animation: _UIAnimation,
        variables: _UIVariables,
    ) -> None:
        super().__init__(name, MakePath("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "ui"))
        self._content = {
            "namespace": namespace,
        }
        self.namespace = namespace
        self._elements: list[_UIElement] = []
        self._anvil_animation = anvil_animation
        self._variables = variables
        self._ignored_title_texts = []
        self._ignored_actionbar_texts = []
        self.do_not_shorten
        
    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
    ):
        #Element name
        new_element = _UIElement(element_name)
        
        if not keyword is None:
            new_element.binding.binding_type(UIBindingType.View).source_property_name(f"$anvil.{element_name}.bool").target_property_name("#visible")

        match trigger:
            case "title":
                if not keyword is None:
                    self._variables.add_variable(
                        f"$anvil.{element_name}.text", f"{NAMESPACE}:{keyword}"
                    )
                    self._variables.add_variable(
                        f"$anvil.{element_name}.bool",
                        f"(#text = $anvil.{element_name}.text)",
                    )
                    self._ignored_title_texts.append(
                        f"(#text = $anvil.{element_name}.text)"
                    )

                new_element.binding.binding_name("#hud_title_text_string").binding_name_override("#text")
                new_element.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#subtext")

                factory = self.add_element(f"{element_name}_factory")
                factory.type(UIElementType.Panel)
                factory.factory("hud_title_text_factory", "hud_title_text", f"{element_name}@anvil_hud.{element_name}")
                self._elements.append(factory)

            case "actionbar":
                if not keyword is None:
                    self._variables.add_variable(
                        f"$anvil.{element_name}.text", f"{NAMESPACE}:{keyword}"
                    )
                    self._variables.add_variable(
                        f"$anvil.{element_name}.bool",
                        f"($text = $anvil.{element_name}.text)",
                    )
                    self._ignored_actionbar_texts.append(
                        f"($text = $anvil.{element_name}.text)"
                    )
                factory: _UIElement = self.add_element(f"{element_name}_factory")
                factory.type(UIElementType.Panel)
                factory.factory(
                    "hud_actionbar_text_factory",
                    "hud_actionbar_text",
                    f"{element_name}_element@anvil_hud.{element_name}_element",
                )

                new_element.keys("text", "$actionbar_text")

        self._elements.append(new_element)
        return new_element

    def queue(self, directory: str = ""):
        for element in self._elements:
            self._content.update(element.queue)
        
        if self._content != {"namespace": self.namespace,}:
            return super().queue(directory)


class _HUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables
    ) -> None:
        super().__init__("hud_screen", "hud", anvil_animation, variables)
        # Disable HUD
        self.root_panel = self.add_element("root_panel")
        self.root_panel.binding.binding_name("#hud_title_text_string").binding_name_override("#text")
        self.root_panel.binding.binding_type(UIBindingType.View).source_property_name("$anvil.hud_visible").target_property_name("#visible")

        self.hud_title_text = self.add_element("hud_title_text")
        self.hud_title_text.binding.binding_name("#hud_title_text_string").binding_name_override("#text")
        self.hud_title_text.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#subtext")
        self.hud_title_text.binding.binding_type(UIBindingType.View).source_property_name("$anvil.title.bool").target_property_name("#visible")

        self.hud_actionbar_text = self.add_element("hud_actionbar_text")
        self.hud_actionbar_text.visible("$anvil.actionbar.bool")
        self.hud_actionbar_text.keys("text", "$actionbar_text")

        anvil_element = self.add_element("hud_content")
        # TO DO:
        # Add a modifications controlling class
        anvil_element.binding.binding_name("#hud_visible").binding_name_override("#visible").binding_type(UIBindingType.Global)
        anvil_element.modification.insert_front("anvil@anvil_hud.anvil_hud")
        variables.add_variable("$anvil.show.text", f"{NAMESPACE}:show")
        variables.add_variable("$anvil.hide.text", f"{NAMESPACE}:hide")
        self._ignored_title_texts = ["(#text = $anvil.show.text)","(#text = $anvil.hide.text)",]
        self._ignored_actionbar_texts = []

    def disable_mouse(self):
        self.add_element(
            "hud_screen@common.base_screen"
        ).should_steal_mouse.absorbs_input
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


class _AnvilHUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables
    ) -> None:
        super().__init__("hud", "anvil_hud", anvil_animation, variables)
        self.test_hud : _UIElement = self.add_element("anvil_hud")
        self.test_hud.type(UIElementType.Panel)

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
    ):
        if trigger is not None:
            self.test_hud.controls(f"{element_name}@anvil_hud.{element_name}_factory")
            
        return super().add_element(element_name, trigger, keyword)

    def add_image_panel(
        self,
        name: str,
        background: bool = False,
        zoom: bool = True,
        duration: float = 8,
    ):
        # element
        image_element = self.add_element(name, UIElementTrigger.Title, name)
        image_element.type(UIElementType.Panel)
        image_element.size(("100%", "100%"))
        image_element.layer(100)
        image_element.anchor(UIAnchor.Center, UIAnchor.Center)

        if background:
            background_image = image_element.controls(f"{name}_background")
            background_image.type(UIElementType.Image)
            background_image.texture("black_element")
            background_image.size(("100%", "100%"))
            background_image.keep_ratio(False)
            
        image = image_element.controls(f"{name}_image")
        image.type(UIElementType.Image)
        image.texture(name)
        image.anchor(UIAnchor.Center, UIAnchor.Center)
        image.offset((0, "-50px"))

        tip = image_element.controls(f"{name}_tip")
        tip.type(UIElementType.Label)
        tip.text_alignment(UITextAlignment.Center)
        tip.size(("80%", 'default'))
        tip.offset((0, "50px"))
        tip.text("#text").shadow.font_size(UIFontSize.Large)
        tip.binding.binding_name("#hud_subtitle_text_string").binding_name_override("#text")

        if zoom:
            # animations
            self._variables.add_variable(f"$anvil.image.{name}_zoom", duration - 1)
            image_zoom_in = self._anvil_animation.add_animation(f"{name}_zoom_in")
            image_zoom_in.anim_type(UIAnimType.Size)
            image_zoom_in.easing(UIEasing.Linear)
            image_zoom_in.from_(("30%", "30%")).to(("40%", "40%"))
            image_zoom_in.duration("$title_fade_in_time")
            image_zoom_in.next(f"@anvil_animations.{name}_zoom_wait")
            image_zoom_wait = self._anvil_animation.add_animation(f"{name}_zoom_wait")
            image_zoom_wait.anim_type(UIAnimType.Wait)
            image_zoom_wait.duration(f"$anvil.image.{name}_zoom")
            image_zoom_wait.next(f"@anvil_animations.{name}_zoom_out")
            image_zoom_out = self._anvil_animation.add_animation(f"{name}_zoom_out")
            image_zoom_out.anim_type(UIAnimType.Size)
            image_zoom_out.easing(UIEasing.Linear)
            image_zoom_out.from_(("40%", "40%")).to(("30%", "30%"))
            image_zoom_out.duration("$title_fade_out_time")

            image_alpha_in = self._anvil_animation.add_animation(f"{name}_alpha_in")
            image_alpha_in.anim_type(UIAnimType.Alpha)
            image_alpha_in.easing(UIEasing.OutQuad)
            image_alpha_in.from_(0)
            image_alpha_in.to(1)
            image_alpha_in.duration("$title_fade_in_time")
            image_alpha_in.next(f"@anvil_animations.{name}_alpha_wait")
            image_alpha_wait = self._anvil_animation.add_animation(f"{name}_alpha_wait")
            image_alpha_wait.anim_type(UIAnimType.Wait)
            image_alpha_wait.duration(f"$anvil.image.{name}_zoom")
            image_alpha_wait.next(f"@anvil_animations.{name}_alpha_out")
            image_alpha_out = self._anvil_animation.add_animation(f"{name}_alpha_out")
            image_alpha_out.anim_type(UIAnimType.Alpha)
            image_alpha_out.easing(UIEasing.InOutSine)
            image_alpha_out.from_(1)
            image_alpha_out.to(0)
            image_alpha_out.duration("$title_fade_out_time")

            image.size(f"@anvil_animations.{name}_zoom_in")
            image.alpha(f"@anvil_animations.{name}_alpha_in")
        else:
            image_alpha_destroy = self._anvil_animation.add_animation(f"{name}_destroy")
            image_alpha_destroy.anim_type(UIAnimType.Alpha)
            image_alpha_destroy.easing(UIEasing.Linear)
            image_alpha_destroy.from_(1)
            image_alpha_destroy.to(0)
            image_alpha_destroy.duration("$title_fade_out_time")
            #image_alpha_destroy.destroy_at_end('hud_title_text')
            image.size(("40%", "40%"))
            image.alpha(f"@anvil_animations.{name}_destroy")

    # Layer 100
    def add_logo(self):
        self.add_image_zoom("logo", True)

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
        #blink_fade_out.destroy_at_end('hud_title_text')
        # element
        blink_element = self.add_element(
            "blink_element", UIElementTrigger.Title, "blink"
        )
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
        #black_bars_out.destroy_at_end('hud_title_text')

        # element
        black_bars = self.add_element(
            "black_bars_element", UIElementTrigger.Actionbar
        )
        black_bars.type(UIElementType.Image)
        black_bars.texture("black_bars")
        black_bars.keep_ratio(False)
        black_bars.anchor(UIAnchor.Center, UIAnchor.Center)
        black_bars.layer(101)
        black_bars.keys("anim_size", ("300%", "300%"))
        black_bars.keys("text", "$actionbar_text")
        black_bars.variables(
            "$anvil.black_bars_in.bool",
            anim_size = "@anvil_animations.black_bars_in",
        )
        black_bars.variables(
            "$anvil.black_bars_out.bool",
            anim_size = "@anvil_animations.black_bars_out",
        )
        black_bars.size("$anim_size")

        self._variables.add_variable(
            f"$anvil.black_bars_in.text", f"{NAMESPACE}:bars_in"
        )
        self._variables.add_variable(
            f"$anvil.black_bars_in.bool", f"($text = $anvil.black_bars_in.text)"
        )
        self._variables.add_variable(
            f"$anvil.black_bars_out.text", f"{NAMESPACE}:bars_out"
        )
        self._variables.add_variable(
            f"$anvil.black_bars_out.bool", f"($text = $anvil.black_bars_out.text)"
        )

        self._ignored_actionbar_texts.extend(
            [
                "($text = $anvil.black_bars_in.text)",
                "($text = $anvil.black_bars_out.text)",
            ]
        )

    def queue(self):
        return super().queue("anvil")


class _NPCScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables) -> None:
        super().__init__("npc_interact_screen", "npc_interact", anvil_animation, variables)
        self._npc_screen = self.add_element('npc_screen@common.base_screen').keys('screen_content', 'anvil_npc.npc_screen_chooser')


class _AnvilNPCScreen(_UIScreen):
    def __init__(self, anvil_animation: _UIAnimation, variables: _UIVariables) -> None:
        super().__init__("npc", "anvil_npc", anvil_animation, variables)
        self._ignored_panel_texts = []
        
        self._npc_screen_chooser = self.add_element('npc_screen_chooser').type(UIElementType.Panel)
        vanilla = self._npc_screen_chooser.controls('vanilla@npc_interact.npc_screen_contents').layer(500)
        vanilla.binding.binding_type(UIBindingType.Global).binding_name('#dialogtext').binding_name_override('#dialogtext')
        vanilla.binding.binding_type(UIBindingType.View).source_property_name('$anvil.npc_screen.vanilla').target_property_name('#visible')

    def queue(self):
        self._variables.add_variable("$anvil.npc_screen.vanilla", f'({" or ".join(self._ignored_panel_texts)})')
        return super().queue("anvil")


class _AnvilAnimations(_UIAnimation):
    def __init__(self) -> None:
        super().__init__("animations", "anvil_animations")


class UI:
    _extensions = {
        0: ".json", 
        1: ".json"
    }
    def __init__(self) -> None:
        self.variables = _UIVariables()

        self._defs = AddonObject("_ui_defs", MakePath("resource_packs", f"RP_{PASCAL_PROJECT_NAME}", "ui")).content({
            "ui_defs": [
                "ui/anvil/npc.json",
                "ui/anvil/hud.json",
                "ui/anvil/animations.json",
            ]
        })

        self.animations_screen = _AnvilAnimations()

        self.hud_screen = _HUDScreen(self.animations_screen, self.variables)
        self.anvil_hud_screen = _AnvilHUDScreen(self.animations_screen, self.variables)

        self.npc_screen = _NPCScreen(self.animations_screen, self.variables)
        self.anvil_npc_screen = _AnvilNPCScreen(self.animations_screen, self.variables)

        self._screens : list[_UIScreen] = []

    def add_ui_screen(self, filename, namespace):
        self._screens.append(_UIScreen(filename, namespace, self.animations_screen, self.variables))
        return self._screens[-1]

    def queue(self):
        self.anvil_hud_screen._variables.add_variable('$anvil.empty.text', '')
        self.anvil_hud_screen._ignored_actionbar_texts.append('(text = $anvil.empty.text)')
        # Manage Titles, Subtitles and actionbars
        ignored_title_texts = self.hud_screen._ignored_title_texts
        ignored_title_texts.extend(self.anvil_hud_screen._ignored_title_texts)

        ignored_actionbar_texts = self.hud_screen._ignored_actionbar_texts
        ignored_actionbar_texts.extend(self.anvil_hud_screen._ignored_actionbar_texts)

        # Manage Variables
        self.variables.add_variable("$anvil.title.bool", f'(not({" or ".join(ignored_title_texts)}))')
        self.variables.add_variable("$anvil.actionbar.bool", f'(not({" or ".join(ignored_actionbar_texts)}))')
        self.variables.add_variable("$anvil.hud_visible",f"({ignored_title_texts.pop(0)} or not ({ignored_title_texts.pop(0)}))",)

        # Add to ANVIL queue
        for screen in self._screens:
            screen.queue()
        self.hud_screen.queue()
        self.anvil_hud_screen.queue()
        self.anvil_npc_screen.queue()
        self.npc_screen.queue()
        self.animations_screen.queue("anvil")
        self.variables.queue()
        self._defs.queue()
