"""
Anvil UI Framework for Minecraft Bedrock Edition.

This module provides a comprehensive framework for creating custom user interfaces
in Minecraft Bedrock Edition resource packs. It includes enums for UI properties,
classes for managing UI elements, animations, and screens, and utilities for
building complex interactive interfaces.

The framework supports:
- Custom UI elements (panels, labels, images, buttons, etc.)
- Animation systems with easing functions
- Data binding and property management
- Screen composition and layout
- Integration with Minecraft's built-in UI systems
- Asset management for textures and resources

Classes:
    UI: Main entry point for creating UI systems
    UIBindingType: Enumeration of binding types for data connections
    UIElementType: Enumeration of UI element types
    UIAnchor: Enumeration of anchor positions for layout
    UITextAlignment: Enumeration of text alignment options
    UIAnimType: Enumeration of animation types
    UIEasing: Enumeration of easing functions for animations
    UIElementTrigger: Enumeration of trigger types for UI activation
    UIFontSize: Enumeration of font size options

Example:
    ```python
    # Create a new UI system
    ui = UI()

    # Add a custom screen
    my_screen = ui.add_ui_screen("my_screen", "my_namespace")

    # Add elements to the screen
    panel = my_screen.add_element("my_panel")
    panel.type(UIElementType.Panel).size(("100%", "50px"))

    # Queue the UI for generation
    ui.queue()
    ```
"""

from enum import StrEnum

import click
from PIL import Image

from anvil.lib.config import ConfigPackageTarget
from anvil.lib.lib import *
from anvil.lib.schemas import AddonObject

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
    """Enumeration of UI binding types for data connections.

    Binding types determine how UI elements connect to data sources
    and how they respond to data changes.

    Attributes:
        View: Binds to view-level data (element properties)
        Global: Binds to global game data
        Collection: Binds to collection data (arrays, lists)
        CollectionDetails: Binds to specific collection item details
        NONE: No binding applied
    """

    View = "view"
    Global = "global"
    Collection = "collection"
    CollectionDetails = "collection_details"
    NONE = "none"


class UIElementType(StrEnum):
    """Enumeration of UI element types.

    Defines the different types of UI elements that can be created
    within the framework.

    Attributes:
        Image: Image element for displaying textures
        Panel: Container element for grouping other elements
        Label: Text display element
        Screen: Top-level screen container
        Factory: Dynamic element generator
        StackPanel: Container that arranges children in a stack
        Grid: Container that arranges children in a grid layout
        Custom: Custom renderer element
        Button: Interactive button element
    """

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
    """Enumeration of anchor positions for UI element layout.

    Anchors determine how elements are positioned relative to their
    parent containers.

    Attributes:
        Center: Center position
        TopLeft: Top-left corner
        TopMiddle: Top center
        TopRight: Top-right corner
        LeftMiddle: Left center
        RightMiddle: Right center
        BottomLeft: Bottom-left corner
        BottomMiddle: Bottom center
        BottomRight: Bottom-right corner
    """

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
    """Enumeration of text alignment options.

    Defines how text content is aligned within text elements.

    Attributes:
        Center: Center-aligned text
        Left: Left-aligned text
        Right: Right-aligned text
    """

    Center = "center"
    Left = "left"
    Right = "right"


class UIAnimType(StrEnum):
    """Enumeration of animation types.

    Defines the different types of animations that can be applied
    to UI elements.

    Attributes:
        Alpha: Transparency/opacity animation
        Clip: Clipping animation
        Color: Color transition animation
        Flip_book: Frame-based flipbook animation
        Offset: Position offset animation
        Size: Size scaling animation
        UV: Texture coordinate animation
        Wait: Pause/delay animation
        Aseprite_flip_book: Aseprite-based flipbook animation
    """

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
    """Enumeration of easing functions for animations.

    Easing functions control the rate of change in animations,
    providing smooth transitions and natural motion effects.

    Attributes:
        Linear: Constant rate of change
        Spring: Spring-like motion
        InQuad, OutQuad, InOutQuad: Quadratic easing variations
        InCubic, OutCubic, InOutCubic: Cubic easing variations
        InQuart, OutQuart, InOutQuart: Quartic easing variations
        InQuint, OutQuint, InOutQuint: Quintic easing variations
        InSine, OutSine, InOutSine: Sinusoidal easing variations
        InExpo, OutExpo, InOutExpo: Exponential easing variations
        InCirc, OutCirc, InOutCirc: Circular easing variations
        InBounce, OutBounce, InOutBounce: Bouncing easing variations
        InBack, OutBack, InOutBack: Back easing variations
        InElastic, OutElastic, InOutElastic: Elastic easing variations
    """

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
    """Enumeration of trigger types for UI element activation.

    Defines when and how UI elements are triggered to appear or activate.

    Attributes:
        Title: Triggered by title/subtitle display
        Actionbar: Triggered by actionbar message display
        NONE: No trigger (always active or manually controlled)
    """

    Title = "title"
    Actionbar = "actionbar"
    NONE = "None"


class UIFontSize(StrEnum):
    """Enumeration of font size options.

    Defines the available font sizes for text elements.

    Attributes:
        Normal: Standard font size
        Small: Smaller font size
        Large: Larger font size
        ExtraLarge: Extra large font size
    """

    Normal = "normal"
    Small = "small"
    Large = "large"
    ExtraLarge = "extra_large"


# Subclasses ==========================================================


class _UIBinding:
    """Manages data binding configuration for UI elements.

    This class handles the configuration of data bindings that connect
    UI elements to data sources, allowing dynamic content updates.

    Attributes:
        _content (dict): Internal storage for binding configuration
    """

    def __init__(self) -> None:
        """Initialize a new UI binding configuration."""
        self._content = {}

    def binding_name(self, binding_name: str):
        """Set the binding name for the data source.

        Args:
            binding_name (str): Name of the binding property

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_name"] = binding_name
        return self

    def binding_name_override(self, binding_name_override: str):
        """Set an override for the binding name.

        Args:
            binding_name_override (str): Override name for the binding

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_name_override"] = binding_name_override
        return self

    def binding_type(self, binding_type: UIBindingType = UIBindingType.View):
        """Set the type of binding.

        Args:
            binding_type (UIBindingType): Type of binding to use

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_type"] = binding_type.value
        return self

    def binding_collection_name(self, binding_collection_name: str):
        """Set the collection name for collection bindings.

        Args:
            binding_collection_name (str): Name of the collection

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_collection_name"] = binding_collection_name
        return self

    def binding_collection_prefix(self, binding_collection_prefix: str):
        """Set the collection prefix for collection bindings.

        Args:
            binding_collection_prefix (str): Prefix for collection items

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_collection_prefix"] = binding_collection_prefix
        return self

    def source_control_name(self, source_control_name: str):
        """Set the source control name for the binding.

        Args:
            source_control_name (str): Name of the source control

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["source_control_name"] = source_control_name
        return self

    def source_property_name(self, source_property_name: str):
        """Set the source property name for the binding.

        Args:
            source_property_name (str): Name of the source property

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["source_property_name"] = source_property_name
        return self

    def target_property_name(self, target_property_name: str):
        """Set the target property name for the binding.

        Args:
            target_property_name (str): Name of the target property

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["target_property_name"] = target_property_name
        return self

    @property
    def resolve_sibling_scope(self):
        """Enable sibling scope resolution for the binding.

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["resolve_sibling_scope"] = True
        return self

    def binding_condition(self, binding_condition: str):
        """Set a condition for the binding activation.

        Args:
            binding_condition (str): Condition expression

        Returns:
            _UIBinding: Self for method chaining
        """
        self._content["binding_condition"] = binding_condition
        return self


class _UIButtonMapping:
    """Manages button mapping configuration for UI elements.

    This class handles the configuration of button mappings that
    define how controller/keyboard inputs are handled by UI elements.

    Attributes:
        _content (dict): Internal storage for button mapping configuration
    """

    def __init__(self) -> None:
        """Initialize a new button mapping configuration."""
        self._content = {}

    def from_button_id(self, from_button_id: str):
        """Set the source button ID for the mapping.

        Args:
            from_button_id (str): ID of the source button

        Returns:
            _UIButtonMapping: Self for method chaining
        """
        self._content["from_button_id"] = from_button_id
        return self

    def to_button_id(self, to_button_id: str):
        """Set the target button ID for the mapping.

        Args:
            to_button_id (str): ID of the target button

        Returns:
            _UIButtonMapping: Self for method chaining
        """
        self._content["to_button_id"] = to_button_id
        return self

    def mapping_type(self, mapping_type: str):
        """Set the type of button mapping.

        Args:
            mapping_type (str): Type of the mapping

        Returns:
            _UIButtonMapping: Self for method chaining
        """
        self._content["mapping_type"] = mapping_type
        return self

    def ignored(self, ignored: bool):
        """Set whether the button mapping should be ignored.

        Args:
            ignored (bool): Whether to ignore this mapping

        Returns:
            _UIButtonMapping: Self for method chaining
        """
        self._content["ignored"] = ignored
        return self

    @property
    def button_up_right_of_first_refusal(self):
        """Enable button up right of first refusal.

        Returns:
            _UIButtonMapping: Self for method chaining
        """
        self._content["button_up_right_of_first_refusal"] = True
        return self


class _UIModifications:
    """Manages UI element modifications for existing elements.

    This class handles modifications to existing UI elements,
    such as removing or inserting new elements.

    Attributes:
        _content (dict): Internal storage for modification configuration
    """

    def __init__(self) -> None:
        """Initialize a new UI modification configuration."""
        self._content = {}

    def remove(self, control_name: str):
        """Remove a control from the UI.

        Args:
            control_name (str): Name of the control to remove

        Returns:
            _UIModifications: Self for method chaining
        """
        self._content["control_name"] = control_name
        self._content["operation"] = "remove"
        return self

    def insert_front(self, control_name: str):
        """Insert a new control at the front of the controls list.

        Args:
            control_name (str): Name of the control to insert

        Returns:
            _UIElement: New UI element for further configuration
        """
        element = _UIElement(control_name)
        self._content["array_name"] = "controls"
        self._content["operation"] = "insert_front"
        self._content["value"] = element
        return element


class _UIElement:
    """Represents a UI element with properties, bindings, and child elements.

    This is the core class for building UI elements. It provides a fluent
    interface for configuring element properties, managing child elements,
    setting up data bindings, and handling animations.

    Attributes:
        _element_name (str): Name identifier for the element
        _textures (list): List of textures used by this element
        element (dict): Dictionary containing element properties
        _buttons (list[_UIButtonMapping]): List of button mappings
        _bindings (list[_UIBinding]): List of data bindings
        _controls (list[_UIElement]): List of child elements
        _modifications (list[_UIModifications]): List of modifications

    Example:
        ```python
        element = _UIElement("my_panel")
        element.type(UIElementType.Panel)
        element.size(("100%", "50px"))
        element.anchor(UIAnchor.Center, UIAnchor.Center)

        # Add child element
        child = element.controls("my_label")
        child.type(UIElementType.Label).text("Hello World")
        ```
    """

    def __init__(self, element_name: str) -> None:
        """Initialize a new UI element.

        Args:
            element_name (str): Unique name for the element
        """
        self._element_name = element_name
        self._textures = []
        self.element = {}
        self._buttons: list[_UIButtonMapping] = []
        self._bindings: list[_UIBinding] = []
        self._controls: list[_UIElement] = []
        self._modifications: list[_UIModifications] = []

    def inherit(self, element_name: str):
        """Inherit properties from an existing element.

        Args:
            element_name (str): Name of the element to inherit from
        Returns:
            _UIElement: Self for method chaining
        """
        self._element_name = f"{self._element_name}@{element_name}"
        return self

    @property
    def should_steal_mouse(self):
        """Enable mouse stealing for this element.

        When enabled, this element will capture mouse events
        and prevent them from reaching elements behind it.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["should_steal_mouse"] = True
        return self

    @property
    def absorbs_input(self):
        """Enable input absorption for this element.

        When enabled, this element will absorb input events
        and prevent them from propagating to other elements.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["absorbs_input"] = True
        return self

    def visible(self, visible: bool | str):
        """Set the visibility of the element.

        Args:
            visible (bool | str): Visibility state or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["visible"] = visible
        return self

    def fill(self, fill: bool | str):
        """Set whether the element should fill available space.

        Args:
            fill (bool | str): Fill state or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["fill"] = fill
        return self

    def ignored(self, ignored: bool | str):
        """Set whether the element should be ignored for input.

        Args:
            ignored (bool | str): Ignored state or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["ignored"] = ignored
        return self

    def enabled(self, enabled: bool | str):
        """Set the enabled state of the element.

        Args:
            enabled (bool | str): Enabled state or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["enabled"] = enabled
        return self

    def text(self, text: str):
        """Set the text content of the element.

        Args:
            text (str): Text content or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["text"] = text
        return self

    def localize(self, localize: bool):
        """Set whether the text should be localized.

        Args:
            localize (bool): Whether to apply localization

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["localize"] = localize
        return self

    def renderer(self, renderer: str):
        """Set the custom renderer for the element.

        Args:
            renderer (str): Name of the custom renderer

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["renderer"] = renderer
        return self

    def type(self, type: UIElementType):
        """Set the type of the UI element.

        Args:
            type (UIElementType): Type of the element

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["type"] = type.value
        return self

    def orientation(self, orientation: str):
        """Set the orientation for container elements.

        Args:
            orientation (str): Orientation ("horizontal" or "vertical")

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["orientation"] = orientation
        return self

    def anchor(self, anchor_from: UIAnchor, anchor_to: UIAnchor):
        """Set the anchor points for element positioning.

        Args:
            anchor_from (UIAnchor): Source anchor point on the element
            anchor_to (UIAnchor): Target anchor point on the parent

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["anchor_from"] = (
            anchor_from.value if isinstance(anchor_from, UIAnchor) else anchor_from
        )
        self.element["anchor_to"] = (
            anchor_to.value if isinstance(anchor_to, UIAnchor) else anchor_to
        )
        return self

    def text_alignment(self, text_alignment: UITextAlignment):
        """Set the text alignment for text elements.

        Args:
            text_alignment (UITextAlignment): Text alignment option

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["text_alignment"] = text_alignment.value
        return self

    def color(self, color: tuple[float, float, float]):
        """Set the color of the element.

        Args:
            color (tuple[float, float, float]): RGB color values (0.0-1.0)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["color"] = color
        return self

    def font_size(self, font_size: UIFontSize):
        """Set the font size for text elements.

        Args:
            font_size (UIFontSize): Font size option

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["font_size"] = font_size.value
        return self

    def layer(self, layer: int):
        """Set the rendering layer for the element.

        Higher layer numbers render on top of lower numbers.

        Args:
            layer (int): Layer number for rendering order

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["layer"] = layer
        return self

    def locked_control(self, locked_control: str):
        """Set a locked control reference.

        Args:
            locked_control (str): Name of the locked control

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["locked_control"] = locked_control
        return self

    def font_scale_factor(self, font_scale_factor: int):
        """Set the font scaling factor.

        Args:
            font_scale_factor (int): Scale factor for font size

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["font_scale_factor"] = font_scale_factor
        return self

    def texture(self, texture: str, scale_factor: int = 1, *nineslice_size: int):
        """Set the texture for image elements with optional scaling and nineslice.

        Args:
            texture (str): Name of the texture file (without .png extension)
                         or binding expression starting with $
            scale_factor (int, optional): Scale factor for texture. Defaults to 1.
            *nineslice_size (int): Nineslice border sizes for scalable textures

        Returns:
            _UIElement: Self for method chaining

        Raises:
            FileNotFoundError: If texture file doesn't exist in assets/textures/ui/
        """
        if not "$" in texture:
            if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
                self.element["texture"] = os.path.join("textures", "ui", texture)
                self._textures.append(texture)
            else:
                raise FileNotFoundError(
                    f"{texture}.png not found in {os.path.join('assets', 'textures', 'ui')}. Please ensure the file exists."
                )
        else:
            self.element["texture"] = texture

        if len(nineslice_size) > 0 or scale_factor != 1:
            File(
                f"{texture}.json",
                {
                    "nineslice_size": (
                        nineslice_size[0] * scale_factor
                        if len(nineslice_size) == 1
                        else [i * scale_factor for i in nineslice_size]
                    ),
                    "base_size": [
                        i * scale_factor
                        for i in Image.open(
                            os.path.join("assets", "textures", "ui", f"{texture}.png")
                        ).size
                    ],
                },
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                "w",
            )
        return self

    def texture_key(
        self, key: str, texture: str, scale_factor: int = 1, *nineslice_size: int
    ):
        """Set a texture using a custom key for variable substitution.

        Args:
            key (str): Variable key name for the texture
            texture (str): Name of the texture file (without .png extension)
            scale_factor (int, optional): Scale factor for texture. Defaults to 1.
            *nineslice_size (int): Nineslice border sizes for scalable textures

        Returns:
            _UIElement: Self for method chaining

        Raises:
            FileNotFoundError: If texture file doesn't exist in assets/textures/ui/
        """
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.element[f"${key}"] = os.path.join("textures", "ui", texture)
            self._textures.append(texture)
            if len(nineslice_size) > 0 or scale_factor != 1:
                File(
                    f"{texture}.json",
                    {
                        "nineslice_size": nineslice_size,
                        "base_size": [
                            i * scale_factor
                            for i in Image.open(
                                os.path.join(
                                    "assets", "textures", "ui", f"{texture}.png"
                                )
                            ).size
                        ],
                    },
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "w",
                )
        else:
            raise FileNotFoundError(
                f"{texture}.png not found in {os.path.join('assets', 'textures', 'ui')}. Please ensure the file exists."
            )
        return self

    def aseprite_texture(self, texture: str):
        """Set an Aseprite texture with animation data.

        This method sets up a texture that includes Aseprite animation
        metadata from a corresponding .json file.

        Args:
            texture (str): Name of the Aseprite texture file (without .png extension)

        Returns:
            _UIElement: Self for method chaining

        Raises:
            FileNotFoundError: If texture file doesn't exist in assets/textures/ui/
        """
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.texture(texture)
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                f"{texture}.json",
            )
        else:
            raise FileNotFoundError(
                f"{texture}.png not found in {os.path.join('assets', 'textures', 'ui')}. Please ensure the file exists."
            )
        return self

    def aseprite_key(self, key: str, texture: str):
        """Set an Aseprite texture using a custom key.

        Args:
            key (str): Variable key name for the texture
            texture (str): Name of the Aseprite texture file (without .png extension)

        Returns:
            _UIElement: Self for method chaining

        Raises:
            FileNotFoundError: If texture file doesn't exist in assets/textures/ui/
        """
        if FileExists(os.path.join("assets", "textures", "ui", f"{texture}.png")):
            self.element[f"${key}"] = os.path.join("textures", "ui", texture)
            self._textures.append(texture)
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                f"{texture}.json",
            )
        else:
            raise FileNotFoundError(
                f"{texture}.png not found in {os.path.join('assets', 'textures', 'ui')}. Please ensure the file exists."
            )
        return self

    def keys(self, key, value):
        """Set a custom key-value pair for the element.

        Args:
            key (str): Key name (will be prefixed with $)
            value: Value to assign (StrEnum values will be converted)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element[f"${key}".replace("$$", "$")] = (
            value.value if isinstance(value, StrEnum) else value
        )
        return self

    def property_bag(self, **properties):
        """Set multiple properties in the element's property bag.

        Args:
            **properties: Key-value pairs to add to the property bag

        Returns:
            _UIElement: Self for method chaining
        """
        if "property_bag" not in self.element:
            self.element["property_bag"] = {}
        self.element["property_bag"].update({f"#{k}": v for k, v in properties.items()})
        return self

    @property
    def binding(self):
        """Create and return a new data binding for this element.

        Returns:
            _UIBinding: New binding configuration object
        """
        if "bindings" not in self.element:
            self.element["bindings"] = []
        bind = _UIBinding()
        self._bindings.append(bind)
        return bind

    @property
    def button_mapping(self):
        """Create and return a new button mapping for this element.

        Returns:
            _UIButtonMapping: New button mapping configuration object
        """
        if "button_mappings" not in self.element:
            self.element["button_mappings"] = []
        bind = _UIButtonMapping()
        self._buttons.append(bind)
        return bind

    @property
    def modification(self):
        """Create and return a new modification for this element.

        Returns:
            _UIModifications: New modification configuration object
        """
        if "modifications" not in self.element:
            self.element["modifications"] = []
        mod = _UIModifications()
        self._modifications.append(mod)
        return mod

    def control_ids(self, id: str, element: str):
        """Set control IDs for factory elements.

        Args:
            id (str): Control ID key
            element (str): Element name

        Returns:
            _UIElement: Self for method chaining
        """
        if "control_ids" not in self.element:
            self.element["control_ids"] = {}
        self.element["control_ids"][id] = element
        return self

    def controls(self, element_name: str):
        """Add a child control element.

        Args:
            element_name (str): Name of the child element

        Returns:
            _UIElement: New child element for further configuration
        """
        if "controls" not in self.element:
            self.element["controls"] = []

        ctrl = _UIElement(element_name)
        self._controls.append(ctrl)
        return ctrl

    def factory(self, name, id, element):
        """Configure this element as a factory.

        Args:
            name (str): Factory name
            id (str): Control ID or "control_name"
            element (str): Element reference

        Returns:
            _UIElement: Self for method chaining
        """
        if not id == "control_name":
            self.element["factory"] = {"name": name, "control_ids": {id: element}}
        else:
            self.element["factory"] = {"name": name, id: element}
        return self

    def size(self, size: str | tuple):
        """Set the size of the element.

        Args:
            size (str | tuple): Size specification as string (e.g., "100%", "50px")
                               or tuple (width, height)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["size"] = size
        return self

    def tiled(self, bool: bool | str):
        """Set whether the texture should be tiled.

        Args:
            bool (bool | str): Tiling state or binding expression

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["tiled"] = bool
        return self

    def max_size(self, max_size: str | tuple):
        """Set the maximum size constraint for the element.

        Args:
            max_size (str | tuple): Maximum size specification

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["max_size"] = max_size
        return self

    def min_size(self, min_size: str | tuple):
        """Set the minimum size constraint for the element.

        Args:
            min_size (str | tuple): Minimum size specification

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["min_size"] = min_size
        return self

    def clip_ratio(self, clip_ratio: float | str):
        """Set the clipping ratio for the element.

        Args:
            clip_ratio (float | str): Ratio for clipping (0.0-1.0) or binding

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["clip_ratio"] = clip_ratio
        return self

    def clip_direction(self, clip_direction: float | str):
        """Set the clipping direction for the element.

        Args:
            clip_direction (float | str): Direction for clipping or binding

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["clip_direction"] = clip_direction
        return self

    def clip_pixelperfect(self, clip_pixelperfect: bool):
        """Set whether clipping should be pixel-perfect.

        Args:
            clip_pixelperfect (bool): Whether to use pixel-perfect clipping

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["clip_pixelperfect"] = clip_pixelperfect
        return self

    def maximum_grid_items(self, maximum_grid_items: int):
        """Set the maximum number of items in a grid.

        Args:
            maximum_grid_items (int): Maximum number of grid items

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["maximum_grid_items"] = maximum_grid_items
        return self

    def line_padding(self, line_padding: int):
        """Set the padding between lines for text elements.

        Args:
            line_padding (int): Padding between lines in pixels

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["line_padding"] = line_padding
        return self

    def uv(self, uv: tuple | str):
        """Set the UV coordinates for texture mapping.

        Args:
            uv (tuple | str): UV coordinates as tuple (u, v) or binding

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["uv"] = uv
        return self

    def uv_size(self, uv_size: tuple):
        """Set the UV size for texture mapping.

        Args:
            uv_size (tuple): UV size as tuple (width, height)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["uv_size"] = uv_size
        return self

    def alpha(self, alpha: str | tuple):
        """Set the alpha (transparency) of the element.

        Args:
            alpha (str | tuple): Alpha value (0.0-1.0), binding, or animation reference

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["alpha"] = alpha
        return self

    def offset(self, offset: str | tuple):
        """Set the positional offset of the element.

        Args:
            offset (str | tuple): Offset as string, tuple (x, y), or animation reference

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["offset"] = offset
        return self

    def clip_offset(self, clip_offset: tuple):
        """Set the clipping offset for the element.

        Args:
            clip_offset (tuple): Clip offset as tuple (x, y)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["clip_offset"] = clip_offset
        return self

    def keep_ratio(self, keep_ratio: bool):
        """Set whether to maintain aspect ratio when scaling.

        Args:
            keep_ratio (bool): Whether to maintain aspect ratio

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["keep_ratio"] = keep_ratio
        return self

    def allow_clipping(self, allow_clipping: bool):
        """Set whether the element allows clipping.

        Args:
            allow_clipping (bool): Whether clipping is allowed

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["allow_clipping"] = allow_clipping
        return self

    def grid_item_template(self, grid_item_template: bool):
        """Set whether this element is a grid item template.

        Args:
            grid_item_template (bool): Whether this is a grid item template

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_item_template"] = grid_item_template
        return self

    def grid_dimension_binding(self, grid_dimension_binding: bool):
        """Set grid dimension binding.

        Args:
            grid_dimension_binding (bool): Whether to use grid dimension binding

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_dimension_binding"] = grid_dimension_binding
        return self

    def grid_dimensions(self, grid_dimensions: tuple):
        """Set the grid dimensions.

        Args:
            grid_dimensions (tuple): Grid dimensions as tuple (columns, rows)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_dimensions"] = grid_dimensions
        return self

    def grid_position(self, grid_position: tuple):
        """Set the position within a grid.

        Args:
            grid_position (tuple): Grid position as tuple (column, row)

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_position"] = grid_position
        return self

    def grid_rescaling_type(self, grid_rescaling_type: str):
        """Set the grid rescaling type.

        Args:
            grid_rescaling_type (str): Type of grid rescaling

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_rescaling_type"] = grid_rescaling_type
        return self

    def grid_fill_direction(self, grid_fill_direction: str):
        """Set the grid fill direction.

        Args:
            grid_fill_direction (str): Direction to fill grid items

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["grid_fill_direction"] = grid_fill_direction
        return self

    def collection_index(self, collection_index: int):
        """Set the collection index for collection bindings.

        Args:
            collection_index (int): Index within the collection

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["collection_index"] = collection_index
        return self

    def collection_name(self, collection_name: bool):
        """Set the collection name binding.

        Args:
            collection_name (bool): Collection name binding state

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["collection_name"] = collection_name
        return self

    def shadow(self, shadow: bool = False):
        """Set whether text should have a shadow effect.

        Args:
            shadow (bool, optional): Whether to enable text shadow. Defaults to False.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["shadow"] = shadow
        return self

    def use_anchored_offset(self, use_anchored_offset: bool = False):
        """Set whether to use anchored offset positioning.

        Args:
            use_anchored_offset (bool, optional): Whether to use anchored offset. Defaults to False.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["use_anchored_offset"] = use_anchored_offset
        return self

    def clips_children(self, clips_children: bool):
        """Set whether this element clips its children.

        Args:
            clips_children (bool): Whether to clip child elements

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["clips_children"] = clips_children
        return self

    @property
    def enable_scissor_test(self):
        """Enable scissor testing for clipping.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["enable_scissor_test"] = True
        return self

    @property
    def focus_enabled(self):
        """Enable focus capability for this element.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["focus_enabled"] = True
        return self

    @property
    def propagate_alpha(self):
        """Enable alpha propagation to child elements.

        Returns:
            _UIElement: Self for method chaining
        """
        self.element["propagate_alpha"] = True
        return self

    def variables(self, requires: str, **kwParameters):
        """Add conditional variables to the element.

        Args:
            requires (str): Condition expression for variable activation
            **kwParameters: Variable key-value pairs

        Returns:
            _UIElement: Self for method chaining
        """
        if "variables" not in self.element:
            self.element["variables"] = []
        vars = {"requires": requires}
        for k, v in kwParameters.items():
            vars.update({f"${k}": v})
        self.element["variables"].append(vars)
        return self

    @property
    def queue(self):
        """Process and queue the element for generation.

        This method processes all textures, bindings, button mappings,
        modifications, and child controls, preparing the element
        for final UI generation.

        Returns:
            dict: Processed element data ready for JSON serialization
        """
        for texture in self._textures:
            CopyFiles(
                os.path.join("assets", "textures", "ui"),
                os.path.join(
                    CONFIG.RP_PATH,
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
    """Represents a UI animation with timing, easing, and property changes.

    This class configures individual animations that can be applied to UI elements.
    It supports various animation types like alpha fading, size scaling, position
    offset, and timing controls.

    Attributes:
        _animation_name (str): Name identifier for the animation
        animation (dict): Dictionary containing animation properties

    Example:
        ```python
        anim = _UIAnimationElement("fade_in")
        anim.anim_type(UIAnimType.Alpha)
        anim.duration(2.0)
        anim.from_(0).to(1)
        anim.easing(UIEasing.InOutSine)
        ```
    """

    def __init__(self, animation_name: str) -> None:
        """Initialize a new animation element.

        Args:
            animation_name (str): Unique name for the animation
        """
        self._animation_name = animation_name
        self.animation = {}

    def anim_type(self, anim_type: UIAnimType):
        """Set the type of animation.

        Args:
            anim_type (UIAnimType): Type of animation to perform

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["anim_type"] = anim_type.value
        return self

    def duration(self, duration: int | str):
        """Set the duration of the animation.

        Args:
            duration (int | str): Duration in seconds or variable reference

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["duration"] = duration
        return self

    def next(self, next: str):
        """Set the next animation to play after this one completes.

        Args:
            next (str): Reference to the next animation

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["next"] = next
        return self

    def destroy_at_end(self, destroy_at_end: str):
        """Set an element to destroy when the animation ends.

        Args:
            destroy_at_end (str): Element name to destroy

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["destroy_at_end"] = destroy_at_end
        return self

    def play_event(self, play_event: str):
        """Set an event to trigger when the animation starts playing.

        Args:
            play_event (str): Event name to trigger

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["play_event"] = play_event
        return self

    def end_event(self, end_event: str):
        """Set an event to trigger when the animation ends.

        Args:
            end_event (str): Event name to trigger

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["end_event"] = end_event
        return self

    def start_event(self, start_event: str):
        """Set an event to trigger when the animation starts.

        Args:
            start_event (str): Event name to trigger

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["start_event"] = start_event
        return self

    def reset_event(self, reset_event: str):
        """Set an event to trigger when the animation resets.

        Args:
            reset_event (str): Event name to trigger

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["reset_event"] = reset_event
        return self

    def easing(self, easing: UIEasing):
        """Set the easing function for the animation.

        Args:
            easing (UIEasing): Easing function to use

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["easing"] = easing.value
        return self

    def from_(self, from_: str | tuple):
        """Set the starting value for the animation.

        Args:
            from_ (str | tuple): Starting value or coordinate

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["from"] = from_
        return self

    def to(self, to: str | tuple):
        """Set the ending value for the animation.

        Args:
            to (str | tuple): Ending value or coordinate

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["to"] = to
        return self

    def initial_uv(self, initial_uv: tuple = (0, 0)):
        """Set the initial UV coordinates for texture animations.

        Args:
            initial_uv (tuple, optional): Starting UV coordinates. Defaults to (0, 0).

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["initial_uv"] = initial_uv
        return self

    def fps(self, fps: int):
        """Set the frames per second for flipbook animations.

        Args:
            fps (int): Frames per second

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["fps"] = fps
        return self

    def frame_count(self, frame_count: int):
        """Set the number of frames in a flipbook animation.

        Args:
            frame_count (int): Total number of frames

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["frame_count"] = frame_count
        return self

    def frame_step(self, frame_step: int):
        """Set the frame step size for flipbook animations.

        Args:
            frame_step (int): Number of frames to step per update

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["frame_step"] = frame_step
        return self

    @property
    def reversible(self):
        """Make the animation reversible.

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["reversible"] = True
        return self

    @property
    def resettable(self):
        """Make the animation resettable.

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["resettable"] = True
        return self

    @property
    def scale_from_starting_alpha(self):
        """Scale animation values from the starting alpha value.

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["scale_from_starting_alpha"] = True
        return self

    @property
    def activated(self):
        """Mark the animation as activated.

        Returns:
            _UIAnimationElement: Self for method chaining
        """
        self.animation["activated"] = True
        return self

    @property
    def queue(self):
        """Get the processed animation data.

        Returns:
            dict: Animation data ready for JSON serialization
        """
        return {self._animation_name: self.animation}

    def __str__(self) -> str:
        """Get the animation name as string.

        Returns:
            str: Animation name
        """
        return self._animation_name


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
        anim.anim_type(UIAnimType.Offset)
        anim.duration(credits_duration)
        anim.from_((0, "160%")).to((0, "-160%"))
        anim.destroy_at_end("hud_title_text")

        self._credits_panel = credits_panel.controls(
            "credits_text@anvil_common.stack_panel"
        )
        self._credits_panel.offset("@anvil_animations.credits_scroll")

        self._element_count = 0

    def add_image(
        self,
        texture_name: str,
        scale_factor: int = 1,
        anchor=UIAnchor.Center,
        *nineslice_size: int,
    ):
        """Adds an image to the credits panel.

        Parameters:
            texture_name (str): The name of the texture.
            scale_factor (int, optional): The scale factor of the texture. Defaults to 1.
            anchor (UIAnchor, optional): The anchor of the image. Defaults to UIAnchor.Center.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        image = (
            self._credits_panel.controls(
                f"panel_{self._element_count}@anvil_common.panel"
            )
            .size(("100%", "100%c"))
            .controls(f"image_{self._element_count}@anvil_common.image")
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

        Parameters:
            text (str): The text of the title.
            font_size (UIFontSize, optional): The font size of the title. Defaults to UIFontSize.Normal.
            color (tuple[float], optional): The color of the title. Defaults to (1, 1, 1).
            text_alignment (UITextAlignment, optional): The text alignment of the title. Defaults to UITextAlignment.Center.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        title = (
            self._credits_panel.controls(
                f"panel_{self._element_count}@anvil_common.panel"
            )
            .size(("100%", "100%c"))
            .controls(f"title_{self._element_count}@anvil_common.label")
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

        Parameters:
            size (int | str): The size of the space.

        Returns:
            _UICreditsConstructor: The credits constructor.
        """
        space = self._credits_panel.controls(
            f"space_{self._element_count}@anvil_common.panel"
        )
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
        # Section Setup
        section = self._credits_panel.controls(
            f"credits_section_{self._element_count}@anvil_common.stack_panel"
        )
        section.orientation("horizontal")
        section.size(("100%", "100%c"))

        # Section title
        title = (
            section.controls(f"panel_title_{self._element_count}@anvil_common.panel")
            .size(("45%", "100%c"))
            .controls(f"title_{self._element_count}@anvil_common.label")
        )
        title.text(section_title)
        title.size(("100%", "default"))
        title.text_alignment(UITextAlignment.Right)
        if title_font_size != UIFontSize.Normal:
            title.font_size(title_font_size)
        if title_color != (1, 1, 1):
            title.color(title_color)

        # Section separator
        section.controls(f"section_sep_{self._element_count}@anvil_common.panel").size(
            ("10%", 0)
        )

        ## Section names
        names = section.controls(
            f"names_{self._element_count}@anvil_common.stack_panel"
        )
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
    """Manages global UI variables for the resource pack.

    This class handles the creation and management of global variables
    that can be used throughout the UI system for dynamic content and
    conditional logic.

    Inherits from AddonObject to provide file generation capabilities.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")
    _object_type = "UI Variables"

    def __init__(self) -> None:
        """Initialize the global variables container."""
        super().__init__("_global_variables")
        self.do_not_shorten()

    def add_variable(self, variable, value):
        """Add a global variable.

        Args:
            variable (str): Variable name (should start with $)
            value: Variable value (string, number, boolean, or expression)
        """
        self._content.update({variable: value})


class _UIDefs(AddonObject):
    """Manages UI definition files list for the resource pack.

    This class maintains a list of UI files that should be loaded
    by the game's UI system.

    Inherits from AddonObject to provide file generation capabilities.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH)
    _object_type = "UI Definitions"

    def __init__(self) -> None:
        """Initialize the UI definitions container."""
        super().__init__("_ui_defs")
        self.do_not_shorten()
        self._files = []

    def add_file(self, path: str):
        """Add a UI file to the definitions list.

        Args:
            path (str): Relative path to the UI file
        """
        self._files.append(path)

    @property
    def queue(self):
        """Process and generate the UI definitions file.

        Returns:
            Generated file content
        """
        self.content({"ui_defs": self._files})
        return super().queue("ui")


class _UIAnimation(AddonObject):
    """Manages UI animations for a specific namespace.

    This class handles the creation and management of animations
    that can be applied to UI elements. It maintains a collection
    of animation elements and generates the final animation file.

    Inherits from AddonObject to provide file generation capabilities.

    Attributes:
        _defs (_UIDefs): Reference to UI definitions manager
        _animations (list[_UIAnimationElement]): List of animation elements
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")
    _object_type = "UI Animation"

    def __init__(self, name: str, namespace: str, defs: _UIDefs) -> None:
        """Initialize the animation manager.

        Args:
            name (str): Name of the animation file
            namespace (str): Namespace for the animations
            defs (_UIDefs): UI definitions manager to register with
        """
        super().__init__(name)
        self._defs = defs
        self._animations: list[_UIAnimationElement] = []
        self._content = {
            "namespace": namespace,
        }
        self.do_not_shorten()

    def add_animation(self, animation_name: str):
        """Add a new animation to the collection.

        Args:
            animation_name (str): Name of the animation

        Returns:
            _UIAnimationElement: New animation element for configuration
        """
        self._animations.append(_UIAnimationElement(animation_name))
        return self._animations[-1]

    def queue(self, directory: str = ""):
        """Process and generate the animation file.

        Args:
            directory (str, optional): Subdirectory for the file. Defaults to "".

        Returns:
            Generated file content
        """
        for anim in self._animations:
            self._content.update(anim.queue)

        self._defs.add_file(
            os.path.join("ui", directory, f"{self.name}{_UIScreen._extension}")
        )
        return super().queue(directory)


class _UIScreen(AddonObject):
    """Manages a UI screen with elements, animations, and bindings.

    This is the base class for creating UI screens. It handles element
    management, trigger systems, and integration with the broader UI
    framework.

    Inherits from AddonObject to provide file generation capabilities.

    Attributes:
        _namespace (str): Namespace for the screen
        _elements (list[_UIElement]): List of UI elements in the screen
        _anvil_animation (_UIAnimation): Reference to animation manager
        _variables (_UIVariables): Reference to variables manager
        _defs (_UIDefs): Reference to UI definitions manager
        _ignored_title_texts (list): List of title texts to ignore
        _ignored_actionbar_texts (list): List of actionbar texts to ignore
        _hides_hud (list): List of conditions that hide the HUD
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "ui")
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
        self._content = {
            "namespace": namespace,
        }
        self._namespace = namespace
        self._elements: list[_UIElement] = []
        self._anvil_animation = anvil_animation
        self._variables = variables
        self._defs = defs
        self._ignored_title_texts = []
        self._ignored_actionbar_texts = []
        self._hides_hud = []
        self.do_not_shorten()

    def add_element(
        self,
        element_name: str,
        trigger: UIElementTrigger = UIElementTrigger.NONE,
        keyword: str = None,
        hides_hud: bool = False,
    ):
        """Add a new UI element to the screen.

        This method creates a new UI element and configures it based on the
        trigger type. It can set up elements that respond to title/subtitle
        displays or actionbar messages.

        Args:
            element_name (str): Name of the element
            trigger (UIElementTrigger, optional): Trigger type for activation.
                                                Defaults to UIElementTrigger.NONE.
            keyword (str, optional): Keyword for trigger matching. Defaults to None.
            hides_hud (bool, optional): Whether this element hides the HUD.
                                      Defaults to False.

        Returns:
            _UIElement: New UI element for further configuration
        """
        # Element name
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
                factory.type(UIElementType.Panel)
                factory.factory(
                    "hud_title_text_factory",
                    "hud_title_text",
                    f"{element_name}_element@{self._namespace}.{element_name}",
                )
                self._elements.append(factory)

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
        """Process and generate the screen file.

        Args:
            directory (str, optional): Subdirectory for the file. Defaults to "".

        Returns:
            Generated file content or None if screen is empty
        """
        for element in self._elements:
            self._content.update(element.queue)

        if self._content != {"namespace": self._namespace}:
            self._defs.add_file(
                os.path.join("ui", directory, f"{self.name}{_UIScreen._extension}")
            )
            return super().queue(directory)


# UI Screens ==========================================================
# Vanilla
class _HUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("hud_screen", "hud", anvil_animation, variables, defs)
        # Disable HUD
        self.root_panel = self.add_element("root_panel")
        self.anvil_element = self.root_panel.modification.insert_front(
            "anvil@anvil_hud.anvil_hud"
        )

        self.hud_title_text = self.add_element("hud_title_text")
        self.hud_title_text.binding.binding_name(
            "#hud_title_text_string"
        ).binding_name_override("#text")
        self.hud_title_text.binding.binding_name(
            "#hud_subtitle_text_string"
        ).binding_name_override("#subtext")

        self.hud_actionbar_text = self.add_element("hud_actionbar_text")
        self.hud_actionbar_text.keys("text", "$actionbar_text")

        variables.add_variable("$anvil.show.text", f"{CONFIG.NAMESPACE}:show")
        variables.add_variable("$anvil.hide.text", f"{CONFIG.NAMESPACE}:hide")
        self._ignored_title_texts = ["$anvil.show.text"]
        self._ignored_actionbar_texts = ["$anvil.hide.text"]
        self._hides_hud = ["$anvil.hide.text"]

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
    ):
        return super().add_element(element_name, trigger, keyword, False)

    def queue(self, directory: str = ""):
        return super().queue()


# Anvil
class _AnvilHUDScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
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
        if not trigger is UIElementTrigger.NONE:
            self.anvil_hud.controls(
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
        tip.binding.binding_name("#hud_subtitle_text_string").binding_name_override(
            "#text"
        )

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
        image_zoom_in.from_((zoom_steps[0], zoom_steps[0])).to(
            (zoom_steps[1], zoom_steps[1])
        )
        image_zoom_in.duration(f"$anvil.image.{name}_in")
        image_zoom_in.next(f"@anvil_animations.{name}_zoom_wait")

        image_zoom_wait = self._anvil_animation.add_animation(f"{name}_zoom_wait")
        image_zoom_wait.anim_type(UIAnimType.Wait)
        image_zoom_wait.duration(f"$anvil.image.{name}_wait")
        image_zoom_wait.next(f"@anvil_animations.{name}_zoom_out")
        image_zoom_out = self._anvil_animation.add_animation(f"{name}_zoom_out")

        image_zoom_out.anim_type(UIAnimType.Size)
        image_zoom_out.easing(UIEasing.Linear)
        image_zoom_out.from_((zoom_steps[1], zoom_steps[1])).to(
            (zoom_steps[2], zoom_steps[2])
        )
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

        image.size(
            f"@anvil_animations.{name}_zoom_in" if zoom_in > 0 else ("50%", "50%")
        )
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

        self._variables.add_variable(
            f"$anvil.black_bars_in.text", f"{CONFIG.NAMESPACE}:bars_in"
        )
        self._variables.add_variable(
            f"$anvil.black_bars_in.bool", f"($text = $anvil.black_bars_in.text)"
        )
        self._variables.add_variable(
            f"$anvil.black_bars_out.text", f"{CONFIG.NAMESPACE}:bars_out"
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
        return super().queue(directory)


class _AnvilNPCScreen(_UIScreen):
    def __init__(
        self, anvil_animation: _UIAnimation, variables: _UIVariables, defs: _UIDefs
    ) -> None:
        super().__init__("npc", "anvil_npc", anvil_animation, variables, defs)
        self._ignored_panel_texts = []

        self._npc_screen_chooser = (
            super().add_element("npc_screen_chooser", True).type(UIElementType.Panel)
        )
        vanilla = self._npc_screen_chooser.controls(
            "vanilla@npc_interact.npc_screen_contents"
        )
        vanilla.binding.binding_type(UIBindingType.Global).binding_name(
            "#title_text"
        ).binding_name_override("#title_text")
        vanilla.binding.binding_type(UIBindingType.Global).binding_name(
            "#dialogtext"
        ).binding_name_override("#dialogtext")
        vanilla.binding.binding_type(UIBindingType.View).source_property_name(
            "$anvil.npc_screen.vanilla"
        ).target_property_name("#visible")

    def add_element(
        self,
        element_name: str,
        keyword: str = None,
    ):
        if keyword:
            self._ignored_panel_texts.append(f"$anvil.npc_screen.{element_name}.text")
            self._variables.add_variable(
                f"$anvil.npc_screen.{element_name}.text", keyword
            )
            self._variables.add_variable(
                f"$anvil.npc_screen.{element_name}.bool",
                f"(#dialogtext = $anvil.npc_screen.{element_name}.text)",
            )
            custom_panel = self._npc_screen_chooser.controls(
                f"{element_name}_instance@anvil_npc.{element_name}"
            )
            custom_panel.binding.binding_type(UIBindingType.Global).binding_name(
                "#dialogtext"
            ).binding_name_override("#dialogtext")
            custom_panel.binding.binding_type(UIBindingType.View).source_property_name(
                f"$anvil.npc_screen.{element_name}.bool"
            ).target_property_name("#visible")

        return super().add_element(element_name, UIElementTrigger.NONE, keyword, False)

    def queue(self, directory: str = ""):
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
    ):
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
        npc_model.binding.binding_type(
            UIBindingType.Collection
        ).binding_collection_name("skins_collection").binding_name("#skin_index")

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
        label_binding.binding.binding_type(UIBindingType.View).source_control_name(
            "$control_name"
        ).source_property_name("#text").target_property_name("#text")

    def title_actionbar(self):
        title_binding = self.add_element("title_binding")
        title_binding.property_bag(title_text="", subtitle_text="")
        title_binding.binding.binding_name(
            "#hud_title_text_string"
        ).binding_name_override("#title_text")
        title_binding.binding.binding_name(
            "#hud_subtitle_text_string"
        ).binding_name_override("#subtitle_text")
        title_binding.binding.binding_type(UIBindingType.View).source_property_name(
            "$binding_text"
        ).target_property_name("#visible")

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
        scoreboard_score = self.add_element(
            "scoreboard_score_element@anvil_common.label"
        )
        scoreboard_score.text("#text")
        scoreboard_score.color("$color")
        scoreboard_score.shadow("$shadow")
        scoreboard_score.layer(1)
        scoreboard_score.binding.binding_name("#player_score_sidebar").binding_type(
            UIBindingType.Collection
        ).binding_collection_name("scoreboard_scores")
        scoreboard_score.binding.binding_type(UIBindingType.View).source_property_name(
            "('§z' + ((#player_score_sidebar * 1) - $score_offset))"
        ).target_property_name("#text")
        scoreboard_score.binding.binding_type(UIBindingType.View).source_property_name(
            "((#player_score_sidebar * 1) - $score_offset)"
        ).target_property_name("#score")

        retrieve_score = self.add_element("retrieve_score@anvil_common.stack_panel")
        retrieve_score.size(("100%c", "100%c"))
        retrieve_score.keys("index", 0)
        retrieve_score.keys("shadow", False)
        retrieve_score.keys("score_offset", 0)
        retrieve_score.keys("color", (1, 1, 1))
        retrieve_score.keys("name", "('score_text_' + $index)")
        retrieve_score.collection_name("scoreboard_scores")
        retrieve_score.controls("$name@scoreboard_score_element").collection_index(
            "$index"
        )
        retrieve_score.visible(False)
        retrieve_score.binding.binding_type(UIBindingType.View).source_control_name(
            "$name"
        ).source_property_name("#text").target_property_name("#text")
        retrieve_score.binding.binding_type(UIBindingType.View).source_control_name(
            "$name"
        ).source_property_name("#score").target_property_name("#score")

    def queue(self, directory: str = ""):
        return super().queue("anvil")


class _AnvilAnimations(_UIAnimation):
    def __init__(self, defs: _UIDefs) -> None:
        super().__init__("animations", "anvil_animations", defs)

    @property
    def queue(self):
        return super().queue("anvil")


class UI:
    """Main UI framework class for creating Minecraft Bedrock Edition interfaces.

    This is the primary entry point for the Anvil UI framework. It manages
    all UI screens, animations, variables, and provides a high-level interface
    for creating complex user interfaces.

    The UI class automatically sets up core screens like HUD, NPC interactions,
    and common components. It handles the integration between different UI
    systems and manages the final generation of UI files.

    Attributes:
        _defs (_UIDefs): UI definitions manager
        variables (_UIVariables): Global variables manager
        animations_screen (_AnvilAnimations): Animation manager
        hud_screen (_HUDScreen): Main HUD screen
        anvil_hud_screen (_AnvilHUDScreen): Custom Anvil HUD screen
        npc_screen (_NPCScreen): NPC interaction screen
        anvil_npc_screen (_AnvilNPCScreen): Custom Anvil NPC screen
        anvil_common (_AnvilCommon): Common UI components
        _screens (list[_UIScreen]): List of all UI screens

    Example:
        ```python
        # Create UI system
        ui = UI()

        # Configure HUD
        ui.hud_screen.disable_hotbar()
        ui.anvil_hud_screen.add_logo()

        # Add custom screen
        custom_screen = ui.add_ui_screen("my_screen", "my_namespace")
        panel = custom_screen.add_element("main_panel")
        panel.type(UIElementType.Panel).size(("100%", "100%"))

        # Generate all UI files
        ui.queue()
        ```
    """

    def __init__(self) -> None:
        """Initialize the UI framework with core screens and managers."""
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise RuntimeError(
                f"UI is not allowed for packages of type '{CONFIG._TARGET}'."
            )

        click.echo(
            "\r[Info]: UI is supported by Anvil but is not officially supported by Mojang. Code will very likely break in future versions of Minecraft Bedrock Edition.",
        )

        self._defs = _UIDefs()
        self.variables = _UIVariables()

        self.animations_screen = _AnvilAnimations(self._defs)

        self.hud_screen = _HUDScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_hud_screen = _AnvilHUDScreen(
            self.animations_screen, self.variables, self._defs
        )

        self.npc_screen = _NPCScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_npc_screen = _AnvilNPCScreen(
            self.animations_screen, self.variables, self._defs
        )

        self.anvil_common = _AnvilCommon(
            self.animations_screen, self.variables, self._defs
        )

        self._screens: list[_UIScreen] = [
            self.hud_screen,
            self.anvil_hud_screen,
            self.npc_screen,
            self.anvil_npc_screen,
            self.anvil_common,
        ]

    def add_ui_screen(self, filename, namespace):
        """Add a new custom UI screen to the framework.

        Args:
            filename (str): Name of the screen file
            namespace (str): Namespace for the screen

        Returns:
            _UIScreen: New screen instance for configuration
        """
        self._screens.append(
            _UIScreen(
                filename, namespace, self.animations_screen, self.variables, self._defs
            )
        )
        return self._screens[-1]

    def queue(self):
        """Process and generate all UI files.

        This method orchestrates the final generation of all UI components,
        manages text filtering for titles and actionbars, sets up HUD visibility
        logic, and outputs all necessary files to the resource pack.

        The method handles:
        - Title and actionbar text filtering
        - HUD visibility management
        - Animation processing
        - Variable generation
        - File output coordination
        """
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
            f"({'(' * len(ignored_title_texts)}#text - "
            + " - ".join(f"{var})" for var in ignored_title_texts)
            + " = #text)",
        )
        self.anvil_hud_screen._variables.add_variable(
            f"$anvil.actionbar_visible.bool",
            f"({'(' * len(ignored_actionbar_texts)}$text - "
            + " - ".join(f"{var})" for var in ignored_actionbar_texts)
            + " = $text)",
        )

        self.hud_screen.hud_title_text.binding.binding_type(
            UIBindingType.View
        ).source_property_name(f"$anvil.title_visible.bool").target_property_name(
            "#visible"
        )
        self.hud_screen.hud_actionbar_text.visible(f"$anvil.actionbar_visible.bool")

        source_prop = (
            f"(#hud_visible and ({'(' * len(hides_hud)}#text - "
            + " - ".join(f"{var})" for var in hides_hud)
            + " = #text))"
        )

        self.hud_screen.root_panel.binding.binding_name("#hud_visible")
        self.hud_screen.root_panel.binding.binding_name(
            "#hud_title_text_string"
        ).binding_name_override("#text")
        self.hud_screen.root_panel.binding.binding_type(
            UIBindingType.View
        ).source_property_name(source_prop).target_property_name("#visible")

        for screen in self._screens:
            screen.queue("anvil")

        self.animations_screen.queue
        self.variables.queue()

        self._defs.queue
