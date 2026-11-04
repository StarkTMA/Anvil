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
    panel.set_type(UIElementType.Panel).set_size(("100%", "50px"))

    # Queue the UI for generation
    ui.queue()
    ```
"""

import click

from anvil.api.ui.animations import _AnvilAnimations
from anvil.api.ui.files import _UIDefs, _UIVariables
from anvil.api.ui.screens import (
    _AnvilCommon,
    _AnvilHUDScreen,
    _AnvilNPCScreen,
    _HUDScreen,
    _NPCScreen,
    _UIScreen,
)
from anvil.lib.config import CONFIG, ConfigPackageTarget
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
        panel.set_type(UIElementType.Panel).set_size(("100%", "100%"))

        # Generate all UI files
        ui.queue()
        ```
    """

    def __init__(self) -> None:
        """Initialize the UI framework with core screens and managers."""
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError(
                f"UI is not allowed for packages of type '{CONFIG._TARGET}'."
            )

        click.echo(
            click.style(
                "\r[INFO]: UI is supported by Anvil but is not officially supported by Mojang. Code will very likely break in future versions of Minecraft Bedrock Edition.",
                fg="yellow",
            ),
        )

        self._defs = _UIDefs()
        self.variables = _UIVariables()

        self.animations_screen = _AnvilAnimations(self._defs)

        self.anvil_common = _AnvilCommon(
            self.animations_screen, self.variables, self._defs
        )

        self.hud_screen = _HUDScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_hud_screen = _AnvilHUDScreen(
            self.animations_screen, self.variables, self._defs
        )

        self.npc_screen = _NPCScreen(self.animations_screen, self.variables, self._defs)
        self.anvil_npc_screen = _AnvilNPCScreen(
            self.animations_screen, self.variables, self._defs
        )

        self._screens: list[_UIScreen] = [
            self.anvil_common,
            self.hud_screen,
            self.anvil_hud_screen,
            self.npc_screen,
            self.anvil_npc_screen,
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
        ignored_title_texts = self.hud_screen._ignored_title_texts
        ignored_title_texts.extend(self.anvil_hud_screen._ignored_title_texts)

        ignored_actionbar_texts = self.hud_screen._ignored_actionbar_texts
        ignored_actionbar_texts.extend(self.anvil_hud_screen._ignored_actionbar_texts)

        hides_hud = self.hud_screen._hides_hud

        for screen in self._screens:
            ignored_actionbar_texts.extend(screen._ignored_actionbar_texts)
            ignored_title_texts.extend(screen._ignored_title_texts)
            hides_hud.extend(screen._hides_hud)

        self.anvil_hud_screen._variables.add_variable(
            "$anvil.title_visible.bool",
            f"({'(' * len(ignored_title_texts)}#text - "
            + " - ".join(f"{var})" for var in ignored_title_texts)
            + " = #text)",
        )
        self.anvil_hud_screen._variables.add_variable(
            "$anvil.actionbar_visible.bool",
            f"({'(' * len(ignored_actionbar_texts)}$text - "
            + " - ".join(f"{var})" for var in ignored_actionbar_texts)
            + " = $text)",
        )

        self.hud_screen.hud_title_text.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_property_name(
            "$anvil.title_visible.bool"
        ).set_target_property_name(
            "#visible"
        )
        self.hud_screen.hud_actionbar_text.set_visible("$anvil.actionbar_visible.bool")

        source_prop = (
            f"(#hud_visible and ({'(' * len(hides_hud)}#text - "
            + " - ".join(f"{var})" for var in hides_hud)
            + " = #text))"
        )

        self.hud_screen.root_panel.add_binding().set_binding_name("#hud_visible")
        self.hud_screen.root_panel.add_binding().set_binding_name(
            "#hud_title_text_string"
        ).set_binding_name_override("#text")
        self.hud_screen.root_panel.add_binding().set_binding_type(
            UIBindingType.View
        ).set_source_property_name(source_prop).set_target_property_name("#visible")

        for screen in self._screens:
            screen.queue("anvil")

        self.animations_screen.queue()
        self.variables.queue()

        self._defs.queue()
