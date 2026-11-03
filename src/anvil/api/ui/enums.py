"""The enums of Anvil's JSON UI: element types, anchors, bindings, animations and fonts."""

from enum import StrEnum


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
        CollectionPanel: A stack panel for collections that does not stack its children
        InputPanel: A panel that accepts input
        Toggle: A toggle with a checked and an unchecked state
        Dropdown: A toggle that opens a dropdown
        Slider: A range input
        SliderBox: The handle of a slider
        EditBox: A text field
        ScrollView: A scrolling panel
        ScrollbarTrack: The track of a scrollbar
        ScrollbarBox: The handle of a scrollbar
        SelectionWheel: A selection wheel
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
    CollectionPanel = "collection_panel"
    InputPanel = "input_panel"
    Toggle = "toggle"
    Dropdown = "dropdown"
    Slider = "slider"
    SliderBox = "slider_box"
    EditBox = "edit_box"
    ScrollView = "scroll_view"
    ScrollbarTrack = "scrollbar_track"
    ScrollbarBox = "scrollbar_box"
    SelectionWheel = "selection_wheel"


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
