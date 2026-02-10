from dataclasses import dataclass
from typing import Dict, Optional, Union

from anvil import CONFIG
from anvil.api.actors.actors import Entity
from anvil.api.actors.components import (
    EntityBodyRotationBlocked,
    EntityCollisionBox,
    EntityConditionalBandwidthOptimization,
    EntityPhysics,
    EntityProjectile,
    EntityPushable,
)
from anvil.api.blocks.blocks import Block
from anvil.api.core.enums import ItemCategory
from anvil.api.core.types import RGBA, Vector3D
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemCustomComponents,
    ItemDisplayName,
    ItemFood,
    ItemIcon,
    ItemMaxStackSize,
    ItemProjectile,
    ItemStackedByData,
    ItemUseAnimation,
    ItemUseModifiers,
)
from anvil.api.items.crafting import PotionMixingRecipe
from anvil.api.items.items import Item
from anvil.api.logic.molang import Query
from anvil.api.pbr.pbr import TextureComponents
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.kit.actors.components import ItemCustomProjectile
from anvil.lib.lib import Color, clamp, convert_color

# ========================== Utility Functions ===============================

# Cache for formatted durations to avoid repeated calculations
_duration_cache: Dict[int, str] = {}


def _format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds not in _duration_cache:
        minutes, remainder = divmod(int(seconds), 60)
        _duration_cache[seconds] = f"{minutes:02d}:{remainder:02d}"
    return _duration_cache[seconds]


def create_universal_potion_projectile() -> Entity:
    """Create a single universal projectile entity for all potion types"""
    entity = Entity("potion_projectile")
    entity.server.description.Summonable

    # Properties for potion configuration
    entity.server.description.add_property.int("amplifier", [1, 255], default=1)
    entity.server.description.add_property.int("duration", [1, 2**31 - 1], default=1)
    entity.server.description.add_property.int(
        "type", [0, 2**31 - 1], default=0, client_sync=True
    )
    entity.server.description.add_property.int(
        "effect_id", [0, 2**31 - 1], default=0, client_sync=True
    )

    # Color properties for different potion effects
    for color in ["r", "g", "b", "a"]:
        default_val = 1.0 if color == "a" else 0.8
        entity.server.description.add_property.float(
            f"color_{color}", [0, 1], default=default_val
        )

    # Client description
    entity.client.description.animation("potion_model", "face_camera", True)
    entity.client.description.geometry("potion_model")

    # Components - optimized grouping
    entity.server.components.add(
        EntityCollisionBox(0.25, 0.25),
        EntityPhysics(has_gravity=False),
        EntityPushable(),
        EntityProjectile(
            angle_offset=-18, gravity=0.02, hit_sound="glass", power=0.35, inertia=0.96
        ).on_hit(douse_fire=True),
        EntityConditionalBandwidthOptimization(
            max_optimized_distance=80,
            max_dropped_ticks=10,
            use_motion_prediction_hints=True,
        ),
        EntityBodyRotationBlocked(),
    )

    entity.queue()
    return entity


def create_universal_tick_potion_block() -> Block:
    """Create a single universal potion block for lingering potions"""
    block = Block("potion_tick")

    block.queue()
    return block


# ========================== Potion Variant Classes ===============================


@dataclass
class PotionVariant:
    """Base class for all potion variants with common functionality."""

    strength: str = "I"
    amplifier: int = 1
    duration: int = 180
    icon_suffix: str = ""
    potion_type: str = "base"
    potion_display: str = "Potion"

    def _create_item(
        self, config: "PotionConfig", index: int, effect_component, projectile: Entity
    ) -> Item:
        """Create the item for this variant."""

        duration_display = _format_duration(self.duration)

        title = f"{self.potion_display} of {config.effect_title}"
        subtitle = f"§9{config.effect_title} {self.strength} ({duration_display})"
        display_name = f"{title}\\n{subtitle}"
        icon_name = f"{config.effect_key}_{self.potion_type}_potion"

        # Create item
        item = Item(f"{self.potion_type}_{config.effect_key}_potion_{index}")
        item.server.description.menu_category(
            ItemCategory.Equipment, is_hidden_in_commands=True
        )

        components = [
            ItemDisplayName(
                display_name,
                localized_key=f"item.{CONFIG.NAMESPACE}:{self.potion_type}_{config.effect_key}_potion_{index}.name",
            ),
            ItemIcon("potion_model", TextureComponents(color=icon_name)),
            ItemMaxStackSize(1),
            ItemStackedByData(False),
        ]

        item.server.components.add(*components)
        item.queue()
        return item

    def _setup_projectile(
        self, config: "PotionConfig", index: int, projectile: Entity
    ) -> None:
        """Setup projectile configuration for this variant - override in subclasses."""
        pass


@dataclass
class Drinkable(PotionVariant):
    """Drinkable potion variant."""

    use_duration: float = 1.5
    potion_type: str = "base"
    potion_display: str = "Potion"

    def _create_item(
        self, config: "PotionConfig", index: int, effect_component, projectile: Entity
    ) -> Item:
        """Create base drinkable potion item."""
        item = super()._create_item(config, index, effect_component, projectile)

        components = [
            effect_component(
                amplifier=self.amplifier,
                duration=self.duration,
                potion_color=config.color_hex,
            ),
            ItemUseModifiers(use_duration=self.use_duration),
            ItemFood(True, 0, 0, MinecraftItemTypes.GlassBottle()),
            ItemUseAnimation("drink"),
        ]

        item.server.components.add(*components)
        return item


@dataclass
class Splash(PotionVariant):
    """Splash potion variant."""

    duration: int = 135  # Default 75% of base duration
    projectile_offset: Vector3D = (0, 0, 0.3)
    projectile_angle: float = -20
    potion_type: str = "splash"
    potion_display: str = "Splash Potion"

    def _create_item(
        self, config: "PotionConfig", index: int, effect_component, projectile: Entity
    ) -> Item:
        """Create base drinkable potion item."""
        item = super()._create_item(config, index, effect_component, projectile)
        event_name = f"{config.effect_key}_splash_{index}"

        components = [
            ItemCustomProjectile(
                projectile=projectile,
                spawn_event=event_name,
                offset=self.projectile_offset,
                angle_offset=self.projectile_angle,
            ),
            ItemProjectile(f"{projectile}<{event_name}>", 1),
        ]

        item.server.components.add(*components)
        return item

    def _setup_projectile(
        self, config: "PotionConfig", index: int, projectile: Entity
    ) -> None:
        """Setup splash projectile event."""
        event_name = f"{config.effect_key}_splash_{index}"
        red, green, blue, alpha = convert_color(config.color_hex, RGBA)
        event = projectile.server.event(event_name)

        properties = {
            "duration": self.duration,
            "amplifier": self.amplifier,
            "type": 1,
            "effect_id": config.effect_id,
            "color_r": red,
            "color_g": green,
            "color_b": blue,
            "color_a": alpha,
        }

        for prop, value in properties.items():
            event.set_property(prop, value)


@dataclass
class Lingering(PotionVariant):
    """Lingering potion variant."""

    duration: int = int(180 * 0.25)
    projectile_offset: Vector3D = (0, 0, 0.3)
    projectile_angle: float = -20
    potion_type: str = "lingering"
    potion_display: str = "Lingering Potion"

    def _create_item(
        self, config: "PotionConfig", index: int, effect_component, projectile: Entity
    ) -> Item:
        item = super()._create_item(config, index, effect_component, projectile)
        event_name = f"{config.effect_key}_lingering_{index}"

        components = [
            ItemCustomProjectile(
                projectile=projectile,
                spawn_event=event_name,
                offset=self.projectile_offset,
                angle_offset=self.projectile_angle,
            ),
            ItemProjectile(f"{projectile}<{event_name}>", 1),
        ]

        item.server.components.add(*components)
        item.queue()
        return item

    def _setup_projectile(
        self, config: "PotionConfig", index: int, projectile: Entity
    ) -> None:
        """Setup lingering projectile event."""
        event_name = f"{config.effect_key}_lingering_{index}"
        cloud_duration = int(self.duration)
        red, green, blue, alpha = convert_color(config.color_hex, RGBA)
        event = projectile.server.event(event_name)

        properties = {
            "duration": cloud_duration,
            "amplifier": self.amplifier,
            "type": 2,
            "effect_id": config.effect_id,
            "color_r": red,
            "color_g": green,
            "color_b": blue,
            "color_a": alpha,
        }

        for prop, value in properties.items():
            event.set_property(prop, value)


@dataclass
class Tick(PotionVariant):
    """Tick potion variant."""

    duration: int = 135
    projectile_offset: Vector3D = (0, 0, 0.3)
    projectile_angle: float = -20
    potion_type: str = "splash"
    potion_display: str = "Splash Potion"

    def _create_item(
        self, config: "PotionConfig", index: int, effect_component, projectile: Entity
    ) -> Item:
        """Create base drinkable potion item."""
        item = super()._create_item(config, index, effect_component, projectile)
        event_name = f"{config.effect_key}_tick_{index}"

        components = [ItemBlockPlacer()]

        item.server.components.add(*components)
        return item


# ========================== Configuration Classes ===============================

# Union of all variant types (now using the base class)
PotionVariantType = Union[Drinkable, Splash, Lingering]


@dataclass
class Brewing:
    """Brewing recipe configuration"""

    from_index: int  # Index of input potion (from variants list, -1 for awkward potion)
    to_index: int  # Index of output potion (from variants list)
    reagent: str  # Item ID or reagent name
    unlock_reagent: Optional[str] = None  # Optional different unlock item


@dataclass
class PotionConfig:
    """Complete potion configuration"""

    effect_key: str
    effect_title: str
    effect_id: int
    color_hex: str
    variants: list[PotionVariantType]
    brewing: Optional[list[Brewing]] = None


# ========================== Main API Class ===============================


class PotionAPI:
    """Optimized potion registration API"""

    _projectile: Optional[Entity] = None
    _component_cache: Dict[str, type] = {}
    _catalog: list = []

    @classmethod
    def _get_projectile(cls) -> Entity:
        """Get or create the universal projectile entity."""
        if cls._projectile is None:
            cls._projectile = create_universal_potion_projectile()
        return cls._projectile

    @classmethod
    def _create_custom_component(cls, effect_key: str) -> type:
        """Create or retrieve cached custom component class."""
        if effect_key in cls._component_cache:
            return cls._component_cache[effect_key]

        component_id = f"{CONFIG.NAMESPACE}:{effect_key}_potion_effect"

        class DynamicPotionEffect(ItemCustomComponents):
            _identifier = component_id

            def __init__(
                self, *, amplifier: float, duration: float, potion_color: Color
            ) -> None:
                super().__init__(self._identifier)
                self._add_field("amplifier", clamp(amplifier, 0.0, 255.0))
                self._add_field("duration", duration)
                self._add_field("potion_color", convert_color(potion_color, RGBA))

        cls._component_cache[effect_key] = DynamicPotionEffect
        return DynamicPotionEffect

    @classmethod
    def _setup_brewing_recipes(cls, config: PotionConfig, items: list[Item]) -> None:
        """Setup brewing recipes for the potion configuration."""
        if not config.brewing:
            return

        for recipe in config.brewing:
            input_item = (
                items[recipe.from_index]
                if recipe.from_index >= 0
                else MinecraftItemTypes.Potion("awkward")
            )
            output_item = items[recipe.to_index]

            brewing_recipe = PotionMixingRecipe(
                f"brew_{config.effect_key}_{recipe.to_index}"
            )
            brewing_recipe.unlock_items([recipe.reagent])
            brewing_recipe.recipe(input_item, recipe.reagent, output_item)
            brewing_recipe.queue()

    @classmethod
    def _setup_render_controller(
        cls, config: PotionConfig, textures: list[str]
    ) -> None:
        """Setup render controller for projectile textures."""
        projectile = cls._get_projectile()

        # Set up textures
        for texture in textures:
            projectile.client.description.texture(
                "potion_model", TextureComponents(color=texture)
            )

        # Create render controller
        rc = projectile.client.description.render_controller(
            config.effect_key, Query.Property("effect_id") == config.effect_id
        )
        rc.geometry("potion_model")
        rc.texture_array("potions", textures)
        rc.textures(f'Array.potions[{Query.Property("type")}]')

    @classmethod
    def register(cls, config: PotionConfig) -> list[Item]:
        """Register a complete potion configuration."""
        # Create effect component
        effect_component = cls._create_custom_component(config.effect_key)
        projectile = cls._get_projectile()

        # Create all variant items and collect textures
        items = []
        textures = []

        for i, variant in enumerate(config.variants):
            item = variant._create_item(config, i, effect_component, projectile)
            variant._setup_projectile(config, i, projectile)

            texture_name = f"{config.effect_key}_{variant.potion_type}_potion"
            if texture_name not in textures:
                textures.append(texture_name)
            items.append(item)

        # Setup render controller
        cls._setup_render_controller(config, textures)

        # Setup brewing recipes
        cls._setup_brewing_recipes(config, items)

        # Add to catalog
        cls._catalog.append({config.effect_key: items})

        return items


# ========================== API Exports ===================================
__all__ = [
    "PotionAPI",
    "PotionConfig",
    "PotionVariant",
    "Drinkable",
    "Splash",
    "Lingering",
    "Brewing",
]
