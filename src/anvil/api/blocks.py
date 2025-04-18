import os
from enum import StrEnum

from anvil import ANVIL, CONFIG
from anvil.api.actors import _Components
from anvil.api.blockbench import _Blockbench
from anvil.api.components import _component
from anvil.api.enums import (BlockFaces, BlockLiquidDetectionTouching,
                             BlockMaterial, BlockVanillaTags, ItemCategory,
                             ItemGroups, PlacementDirectionTrait,
                             PlacementPositionTrait, TintMethod)
from anvil.api.types import Molang, coordinates, position
from anvil.lib.format_versions import (BLOCK_JSON_FORMAT_VERSION,
                                       BLOCK_SERVER_VERSION,
                                       ITEM_SERVER_VERSION)
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription

__all__ = [
    "Block",
    "VanillaBlockTexture",
    "BlockDestructibleByExplosion",
    "BlockDestructibleByMining",
    "BlockFlammable",
    "BlockFriction",
    "BlockLightDampening",
    "BlockLightEmission",
    "BlockLootTable",
    "BlockMapColor",
    "BlockMaterialInstance",
    "BlockGeometry",
    "BlockCollisionBox",
    "BlockSelectionBox",
    "BlockPlacementFilter",
    "BlockTransformation",
    "BlockDisplayName",
    "BlockCraftingTable",
    "PlacementDirectionTrait",
    "PlacementPositionTrait",
    "CardinalDirectionsTrait",
    "FacingDirectionsTrait",
    "BlockFacesTrait",
    "VerticalHalfTrait",
]


class BlockDescriptor(dict):
    """
    A class that inherits from Python's built-in dict class. It is used to create a descriptor for a block in Minecraft
    with its name, tags, and states.
    """

    def __init__(self, name: str, tags: Molang, **states):
        """
        Initializes a BlockDescriptor object.

        Args:
            name (str): The name of the block.
            tags (Molang): The tags of the block.
            **states: The states of the block.
        """
        super().__init__(name=name, tags=tags, states=states)


# Components
class BlockRedstoneConductivity(_component):
    component_namespace = "minecraft:redstone_conductivity"

    def __init__(self, allows_wire_to_step_down: bool = True, redstone_conductor: bool = False) -> None:
        """Specifies whether a block has redstone properties. If the component is not provided, the default values are used.

        Args:
            allows_wire_to_step_down (bool, optional): Specifies if redstone wire can stair-step downward on the block, Defaults to True.
            redstone_conductor (bool, optional): Specifies if the block can be powered by redstone, Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_redstone_conductivity
        """
        super().__init__("redstone_conductivity")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.30")
        self._component_add_field("allows_wire_to_step_down", allows_wire_to_step_down)
        self._component_add_field("redstone_conductor", redstone_conductor)


class BlockCustomComponents(_component):
    component_namespace = "minecraft:custom_components"

    def __init__(self, *components: str) -> None:
        """Sets the color of the block when rendered to a map.

        Args:
            components (str): The components to register, if the namespace is not provided, the project namespace will be used.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_custom_components
        """
        super().__init__("custom_components")
        self._component_set_value(components)


class BlockDefault(_component):
    component_namespace = "minecraft:block_default"

    def __init__(self) -> None:
        """The default block component."""
        super().__init__("block_default")

    def ambient_occlusion_exponent(self, exponent: int):
        """The exponent for ambient occlusion of the block."""
        self._component_add_field("ambient_occlusion_exponent", max(0, exponent))
        return self

    def sound(self, sound: str):
        """The sound of the block."""
        self._component_add_field("sound", sound)
        return self

    def isotropic(self, **kwargs: dict[str, BlockFaces]):
        """The isotropic of the block."""
        if BlockFaces.All in kwargs.values():
            self._component_set_value("isotropic", True)
        else:
            self._component_add_field("isotropic", {v: k for k, v in kwargs.items()})
        return self

    def textures(self, **kwargs: dict[str, BlockFaces]):
        """The textures of the block."""
        for k in kwargs.keys():
            if not FileExists(os.path.join("assets", "textures", "blocks", f"{k}.png")):
                CONFIG.Logger.file_exist_error(f"{k}.png", os.path.join("assets", "textures", "blocks"))

            CopyFiles(
                os.path.join("assets", "textures", "blocks"),
                os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "blocks").replace("\\", "/"),
                f"{k}.png",
            )
            ANVIL.definitions.register_terrain_texture(k, "", k)

        if BlockFaces.All in kwargs.values():
            self._component_add_field(
                "textures", [f"{CONFIG.NAMESPACE}:{k}" for k, v in kwargs.items() if v == BlockFaces.All][0]
            )
        else:
            self._component_add_field("textures", {v: f"{CONFIG.NAMESPACE}:{k}" for k, v in kwargs.items()})

        return self

    def carried_textures(self, **kwargs: dict[str, BlockFaces]):
        """The carried textures of the block."""
        if BlockFaces.All in kwargs.values():
            self._component_set_value(
                "carried_textures", [f"{CONFIG.NAMESPACE}:{k}" for k, v in kwargs.items() if v == BlockFaces.All][0]
            )
        else:
            self._component_add_field("carried_textures", {v: f"{CONFIG.NAMESPACE}:{k}" for k, v in kwargs.items()})
        return self


class BlockDestructibleByExplosion(_component):
    component_namespace = "minecraft:destructible_by_explosion"

    def __init__(self, explosion_resistance: int) -> None:
        """Describes the destructible by explosion properties for this block.

        Args:
            explosion_resistance (int): The amount of resistance to explosions in a range of 0 to 100.
        """
        super().__init__("destructible_by_explosion")
        self._component_add_field("explosion_resistance", explosion_resistance)


class BlockDestructibleByMining(_component):
    component_namespace = "minecraft:destructible_by_mining"

    def __init__(self, seconds_to_destroy: int) -> None:
        """Describes the destructible by mining properties for this block.

        Args:
            seconds_to_destroy (int): The amount of time it takes to destroy the block in seconds.
        """
        super().__init__("destructible_by_mining")
        self._enforce_version(ITEM_SERVER_VERSION, "1.21.50")
        self._component_add_field("seconds_to_destroy", seconds_to_destroy)
        self._component_add_field("item_specific_speeds", [])

    def item_specific_speeds_name(self, destroy_speed: float, item_name: str):
        self[self.component_namespace]["item_specific_speeds"].append({"item": item_name, "destroy_speed": destroy_speed})

    def item_specific_speeds_tag(self, destroy_speed: float, item_tag: str | Molang):
        self[self.component_namespace]["item_specific_speeds"].append(
            {"item": {"tags": item_tag}, "destroy_speed": destroy_speed}
        )


class BlockFlammable(_component):
    component_namespace = "minecraft:flammable"

    def __init__(self, catch_chance_modifier: int, destroy_chance_modifier: int) -> None:
        """Describes the flammable properties for this block.

        Args:
            catch_chance_modifier (int): The chance that this block will catch fire in a range of 0 to 100.
            destroy_chance_modifier (int): The chance that this block will be destroyed when on fire in a range of 0 to 100.
        """
        super().__init__("flammable")
        self._component_add_field("catch_chance_modifier", catch_chance_modifier)
        self._component_add_field("destroy_chance_modifier", destroy_chance_modifier)


class BlockFriction(_component):
    component_namespace = "minecraft:friction"

    def __init__(self, friction: float = 0.4) -> None:
        """Describes the friction for this block in a range of 0.0 to 0.9.

        Args:
            friction (float, optional): The friction of the block. Defaults to 0.4.
        """
        super().__init__("flammable")
        self._component_set_value(clamp(friction, 0, 0.9))


class BlockLightDampening(_component):
    component_namespace = "minecraft:light_dampening"

    def __init__(self, light_dampening: int = 15) -> None:
        """The amount that light will be dampened when it passes through the block in a range of 0 to 15.

        Args:
            light_dampening (int, optional): The amount of light dampening. Defaults to 15.
        """
        super().__init__("light_dampening")
        self._component_set_value(clamp(light_dampening, 0, 15))


class BlockLightEmission(_component):
    component_namespace = "minecraft:light_emission"

    def __init__(self, light_emission: int = 0) -> None:
        """The amount of light this block will emit in a range of 0 to 15.

        Args:
            light_emission (int, optional): The amount of light emission. Defaults to 0.
        """
        super().__init__("light_emission")
        self._component_set_value(clamp(light_emission, 0, 15))


class BlockLootTable(_component):
    component_namespace = "minecraft:loot"

    def __init__(self, loot: str) -> None:
        """Specifies the path to the loot table.

        Args:
            loot (str): The path to the loot table.
        """
        super().__init__("loot")
        self._component_set_value(loot)


class BlockMapColor(_component):
    component_namespace = "minecraft:map_color"

    def __init__(self, color: str, tint_method: TintMethod = TintMethod.None_) -> None:
        """Sets the color of the block when rendered to a map. If this component is omitted, the block will not show up on the map.

        Args:
            color (str): The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255.
            tint_method (str, optional): Optional, tint multiplied to the color. Tint method logic varies, but often refers to the "rain" and "temperature" of the biome the block is placed in to compute the tint. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color
        """
        self._enforce_version(BLOCK_JSON_FORMAT_VERSION, "1.21.70")
        super().__init__("map_color")
        self._component_add_field("color", color)
        if tint_method is not TintMethod.None_:
            self._component_add_field("tint_method", tint_method)


class BlockMaterialInstance(_component):
    component_namespace = "minecraft:material_instances"

    def __init__(self) -> None:
        """Maps face or material_instance names in a geometry file to an actual material instance."""
        super().__init__("material_instances")

    def add_instance(
        self,
        blockbench_name: str,
        texture_name: str,
        block_face: BlockFaces = BlockFaces.All,
        render_method: BlockMaterial = BlockMaterial.Opaque,
        ambient_occlusion: float = 0,
        face_dimming: bool = True,
        tint_method: TintMethod = TintMethod.None_,
    ):
        """Maps face or material_instance names in a geometry file to an actual material instance.

        Args:
            texture_name (str): The name of the texture to use for this block.
            block_face (BlockFaces, optional): The face of the block to apply the texture to. Defaults to BlockFaces.All.
            render_method (BlockMaterial, optional): The render method to use for this block. Defaults to BlockMaterial.Opaque.
            ambient_occlusion (float, optional): The amount of ambient occlusion for this block. Defaults to 0.
            face_dimming (bool, optional): Whether or not to use face dimming for this block. Defaults to True.
            tint_method (TintMethod, optional): The tint method to use for this block. Defaults to TintMethod.None_.

        """
        bb = _Blockbench(blockbench_name, "blocks")
        bb.textures.queue_texture(texture_name)

        ANVIL.definitions.register_terrain_texture(texture_name, blockbench_name, texture_name)

        self[self.component_namespace].update(
            {
                "*" if block_face == BlockFaces.All else block_face: {
                    "texture": f"{CONFIG.NAMESPACE}:{texture_name}",
                    "render_method": render_method if not render_method == BlockMaterial.Opaque else {},
                    "ambient_occlusion": ambient_occlusion if ambient_occlusion is False else {},
                    "face_dimming": face_dimming if face_dimming is False else {},
                    "tint_method": tint_method if not tint_method == TintMethod.None_ else {},
                }
            }
        )

        return self


class BlockGeometry(_component):
    component_namespace = "minecraft:geometry"

    def __init__(self, geometry_name: str) -> None:
        """The description identifier of the geometry file to use to render this block.

        Args:
            geometry_name (str): The name of the geometry to use to render this block.
        """
        super().__init__("geometry")
        self._component_add_field("identifier", f"geometry.{CONFIG.NAMESPACE}.{geometry_name}")

        bb = _Blockbench(geometry_name, "blocks")
        bb.model.queue_model()

    def bone_visibility(self, **bone: dict[str, bool | str | Molang]):
        """Specifies the visibility of bones in the geometry file.

        Example:
            >>> BlockGeometry('block').bone_visibility(bone0=True, bone1=False)

        """
        self._component_add_field("bone_visibility", {b: v for b, v in bone.items()})
        return self


class BlockCollisionBox(_component):
    component_namespace = "minecraft:collision_box"

    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that collides with entities.

        Args:
            size (coordinates): The size of the collision box.
            origin (coordinates): The origin of the collision box.
        """
        super().__init__("collision_box")
        if size == (0, 0, 0):
            self._component_set_value(False)
        else:
            self._component_add_field("size", size)
            self._component_add_field("origin", origin)


class BlockSelectionBox(_component):
    component_namespace = "minecraft:selection_box"

    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that is selected by the player's cursor.

        Args:
            size (coordinates): The size of the selection box.
            origin (coordinates): The origin of the selection box.
        """
        super().__init__("selection_box")
        if size == (0, 0, 0):
            self._component_set_value(False)
        else:
            self._component_add_field("size", size)
            self._component_add_field("origin", origin)


class BlockPlacementFilter(_component):
    component_namespace = "minecraft:placement_filter"

    def __init__(self) -> None:
        """By default, custom blocks can be placed anywhere and do not have placement restrictions unless you specify them in this component."""
        super().__init__("placement_filter")
        self._component_add_field("conditions", [])

    def add_condition(self, allowed_faces: list[BlockFaces], block_filter: list[BlockDescriptor | str]):
        """Adds a condition to the placement filter.

        Args:
            allowed_faces (list[BlockFaces]): The faces of the block that are allowed to be placed on.
            block_filter (list[BlockDescriptor | str]): The blocks that are allowed to be placed on.
        """
        if BlockFaces.Side in allowed_faces:
            allowed_faces.remove(BlockFaces.North)
            allowed_faces.remove(BlockFaces.South)
            allowed_faces.remove(BlockFaces.East)
            allowed_faces.remove(BlockFaces.West)
        if BlockFaces.All in allowed_faces:
            allowed_faces = [BlockFaces.All]
        self[self.component_namespace]["conditions"].append(
            {
                "allowed_faces": allowed_faces,
                "block_filter": block_filter,
            }
        )
        return self


class BlockTransformation(_component):
    component_namespace = "minecraft:transformation"

    def __init__(self) -> None:
        """The block's transfomration."""
        super().__init__("transformation")

    def translation(self, translation: tuple[float, float, float]):
        """The block's translation.

        Args:
            translation (position): The block's translation.
        """
        self._component_add_field("translation", translation)
        return self

    def scale(self, scale: tuple[float, float, float], scale_pivot: tuple[float, float, float] = (0, 0, 0)):
        """The block's scale.

        Args:
            scale (position): The block's scale.
        """
        self._component_add_field("scale", scale)

        if scale_pivot != (0, 0, 0):
            self._component_add_field("scale_pivot", scale_pivot)

        return self

    def rotation(self, rotation: tuple[float, float, float], rotation_pivot: tuple[float, float, float] = (0, 0, 0)):
        """The block's rotation.

        Args:
            rotation (position): The block's rotation.

        """
        self._component_add_field("rotation", rotation)

        if rotation_pivot != (0, 0, 0):
            self._component_add_field("rotation_pivot", rotation_pivot)
        return self


class BlockDisplayName(_component):
    component_namespace = "minecraft:display_name"

    def __init__(self, display_name: str, localize: bool = True) -> None:
        """Sets the block display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Args:
            display_name (str): Set the display name for an block.
            localize (bool, optional): Whether to use the name with a localization file or not. Defaults to True.

        """
        super().__init__("display_name")
        if localize:
            key = f'tile.{CONFIG.NAMESPACE}:{display_name.lower().replace(" ", "_")}.name'
            ANVIL.definitions.register_lang(key, display_name)
            self._component_set_value(key)
        else:
            self._component_set_value(display_name)


class BlockCraftingTable(_component):
    component_namespace = "minecraft:crafting_table"

    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes.

        Args:
            table_name (str): The name of the crafting table.

        Raises:
            IndexError: The crafting table tags cannot exceed 64 tags.
            ValueError: The crafting table tags are limited to 64 characters.
        """
        super().__init__("crafting_table")
        self._component_add_field("table_name", table_name)

        if len(crafting_tags) > 64:
            raise IndexError("Crafting Table tags cannot exceed 64 tags.")

        for tag in crafting_tags:
            if len(tag) > 64:
                raise ValueError("Crafting Table tags are limited to 64 characters.")

        self._component_add_field("crafting_tags", crafting_tags)


class BlockItemVisual(_component):
    component_namespace = "minecraft:item_visual"

    def __init__(self, geometry_name: str, texture: str, render_method: BlockMaterial = BlockMaterial.Opaque) -> None:
        """The description identifier of the geometry and material used to render the item of this block.

        Args:
            geometry (str): The geometry of the item.
            texture (str): The texture of the item.
            render_method (BlockMaterial): The method used to render the item.

        """
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.60")
        super().__init__("item_visual")

        bb = _Blockbench(geometry_name, "blocks")
        bb.model.queue_model()

        self._component_add_field("geometry", {"identifier": geometry_name})
        self._component_add_field("material_instances", {"*": {"texture": texture, "render_method": render_method}})


class BlockLiquidDetection(_component):
    component_namespace = "minecraft:liquid_detection"

    def __init__(self) -> None:
        """The block's liquid detection."""
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.60")
        super().__init__("liquid_detection")
        self._component_add_field("detection_rules", [])

    def add_rule(
        self,
        liquid_type: str = "minecraft:water",
        on_liquid_touches: BlockLiquidDetectionTouching = BlockLiquidDetectionTouching.Blocking,
        can_contain_liquid: bool = False,
        stops_liquid_flowing_from_direction: list[BlockFaces] = [],
    ):
        """Adds a rule to the liquid detection.

        Args:
            liquid_type (str): The type of liquid, defaults to "minecraft:water".
            on_liquid_touches (BlockLiquidDetectionTouching): The action to take when the liquid touches the block.
            can_contain_liquid (bool, optional): Whether the block can contain the liquid. Defaults to False.

        """
        self[self.component_namespace]["detection_rules"].append(
            {
                "liquid_type": "minecraft:water",
                "on_liquid_touches": on_liquid_touches.value,
                "can_contain_liquid": can_contain_liquid,
                "stops_liquid_flowing_from_direction": (
                    [BlockFaces.North, BlockFaces.South, BlockFaces.East, BlockFaces.West]
                    if BlockFaces.Side in stops_liquid_flowing_from_direction
                    else (
                        [BlockFaces.North, BlockFaces.South, BlockFaces.East, BlockFaces.West, BlockFaces.Up, BlockFaces.Down]
                        if BlockFaces.All in stops_liquid_flowing_from_direction
                        else stops_liquid_flowing_from_direction
                    )
                ),
            }
        )
        return self


class BlockDestructionParticles(_component):
    component_namespace = "minecraft:destruction_particles"

    def __init__(self, blockbench_name: str, texture: str = None, tint_method: TintMethod = TintMethod.None_) -> None:
        """Sets the particles that will be used when the block is destroyed.

        Args:
            blockbench_name (str): The name of the blockbench model.
            texture (str, optional): The texture name used for the particle.
            tint_method (TintMethod, optional): Tint multiplied to the color. Defaults to TintMethod.None_.
        """
        super().__init__("destruction_particles")
        if texture is not None:
            bb = _Blockbench(blockbench_name, "blocks")
            bb.textures.queue_texture(texture)
            self._component_add_field("texture", texture)
        if tint_method is not TintMethod.None_:
            self._component_add_field("tint_method", tint_method)


# Core
class _PermutationComponents(_Components):
    _count = 0

    def __init__(self, condition: str | Molang = None):
        """The permutation components.

        Args:
            condition (str | Molang): The condition for the permutation.
        """
        super().__init__()
        _PermutationComponents._count += 1
        self._component_group_name = "components"
        self._condition = condition

    def tag(self, *tags: BlockVanillaTags):
        """The tags for the block.

        Args:
            tags (BlockVanillaTags): The tags for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktags
        """
        for tag in tags:
            self._set(f"tag:{tag}", {f"tag:{tag}": {"do_not_shorten": True}})

        return self

    def _export(self):
        cmp = super()._export()
        if self._condition:
            cmp["condition"] = self._condition
        return cmp


class _BlockTraits:
    def __init__(self) -> None:
        self._traits = {}

    def placement_direction(self, y_rotation_offset: float = 0, *traits: PlacementDirectionTrait):
        """can add states containing information about the player's rotation when the block is placed.

        Args:
            y_rotation_offset (float, optional): The y rotation offset. Defaults to 0.
            traits (PlacementDirectionTrait): The traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_direction-example
        """

        self._traits["minecraft:placement_direction"] = {
            "enabled_states": [t for t in traits if t],
            "y_rotation_offset": y_rotation_offset,
        }

    def placement_position(self, *traits: PlacementPositionTrait):
        """Can add states containing information about the position of the block when it is placed.

        Args:
            traits (PlacementPositionTrait): The traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example
        """
        self._traits["minecraft:placement_position"] = {"enabled_states": traits}

    @property
    def export(self):
        return self._traits


class _BlockServerDescription(MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block description.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._traits = _BlockTraits()
        self._description["description"].update(
            {
                "states": {},
                "traits": {},
            }
        )

    def add_state(self, name: str, *range: float | str | bool):
        """Adds a state to the block.

        Args:
            name (str): The name of the state.
            range (float | str |bool): Values this state can have.

        """
        if len(range) > 16:
            CONFIG.Logger.block_state_values_out_of_range(self._name, name, len(range))
        self._description["description"]["states"][f"{CONFIG.NAMESPACE}:{name}"] = range
        return self

    def menu_category(
        self,
        category: ItemCategory = ItemCategory.none,
        group: ItemGroups | str = ItemGroups.none,
    ):
        """Sets the menu category for the block.

        Args:
            category (ItemCategory, optional): The category of the block. Defaults to ItemCategory.none.
            group (str, optional): The group of the block. Defaults to None.

        """
        self._description["description"]["menu_category"] = {
            "category": category.value if not category == ItemCategory.none else {},
            "group": f"{CONFIG.NAMESPACE}:{group}" if not group == ItemGroups.none else {},
        }
        return self

    @property
    def is_hidden_in_commands(self):
        self._description["description"]["is_hidden_in_commands"] = True
        return self

    @property
    def traits(self):
        """Sets the traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits
        """
        return self._traits

    @property
    def to_dict(self):
        self._description["description"]["traits"] = self._traits.export
        return super().to_dict


class _BlockServer(AddonObject):
    """The block server object."""

    _extension = ".block.json"
    _path = os.path.join(CONFIG.BP_PATH, "blocks")

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block server object.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name)
        self._server_block = JsonSchemes.server_block()
        self._description = _BlockServerDescription(name, is_vanilla)
        self._components = _PermutationComponents(None)
        self._permutations: list[_PermutationComponents] = []

    @property
    def description(self):
        """The block description."""
        return self._description

    @property
    def components(self):
        """The block components."""
        return self._components

    def permutation(self, condition: str | Molang):
        """Adds a permutation to the block.

        Args:
            condition (str | Molang): The condition for the permutation.
        """
        self._permutation = _PermutationComponents(condition)
        self._permutations.append(self._permutation)
        return self._permutation

    @property
    def queue(self):
        """Queues the block to be exported."""
        self._server_block["minecraft:block"].update(self.description.to_dict)
        self._server_block["minecraft:block"].update(self._components._export())
        comps: dict = self._server_block["minecraft:block"]["components"]
        self._server_block["minecraft:block"]["permutations"] = [permutation._export() for permutation in self._permutations]

        if not BlockDefault.component_namespace in comps:
            if not BlockMaterialInstance.component_namespace in comps:
                CONFIG.Logger.block_missing_texture(self._name)
            if not BlockGeometry.component_namespace in comps:
                CONFIG.Logger.block_missing_geometry(self._name)
        else:
            ANVIL.definitions.register_block(self.description.identifier, comps[BlockDefault.component_namespace])
            comps.pop(BlockDefault.component_namespace)

        if not BlockDisplayName.component_namespace in self._server_block["minecraft:block"]["components"]:
            display_name = self._name.replace("_", " ").title()
            self._server_block["minecraft:block"]["components"][BlockDisplayName.component_namespace] = display_name

        self.content(self._server_block)
        super().queue()


class Block:
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block object.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        self._name = name
        self._is_vanilla = is_vanilla
        self._server = _BlockServer(name, is_vanilla)
        self._item = None

        self._namespace_format = CONFIG.NAMESPACE
        if self._is_vanilla:
            self._namespace_format = "minecraft"

    @property
    def Server(self):
        """The block server object."""
        return self._server

    @property
    def identifier(self):
        """The block identifier."""
        return f"{self._namespace_format}:{self._name}"

    @property
    def name(self):
        return self._name

    @property
    def item(self):
        if not self._item:
            from anvil.api.items import Item

            self._item = Item(self.name)

        return self._item

    def queue(self):
        """Queues the block to be exported."""
        self.Server.queue

        if self._item:
            self._item.queue()

        if self.Server._server_block["minecraft:block"]["components"][BlockDisplayName.component_namespace].startswith("tile."):
            display_name = ANVIL.definitions._language[
                self.Server._server_block["minecraft:block"]["components"][BlockDisplayName.component_namespace]
            ]
        else:
            display_name = self.Server._server_block["minecraft:block"]["components"][BlockDisplayName.component_namespace]

        CONFIG.Report.add_report(
            ReportType.BLOCK,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
            col2=[
                f"{key}: {[', '.join(str(v) for v in value)]}"
                for key, value in self.Server.description._description["description"]["states"].items()
            ],
        )


#  TODO: Integrate with the Block class


class VanillaBlockTexture(MinecraftDescription):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, True)
        self._identifier = identifier

    @property
    def update_texture(self):
        self._ext = ""
        if FileExists(os.path.join("assets", "textures", "blocks", f"{self._identifier}.png")):
            self._ext = "png"
        if FileExists(os.path.join("assets", "textures", "blocks", f"{self._identifier}.tga")):
            self._ext = "tga"

        return self

    def queue(self, directory: str = ""):
        CopyFiles(
            os.path.join("assets", "textures", "blocks"),
            os.path.join(CONFIG.RP_PATH, "textures", "blocks", directory),
            f"{self._identifier}.{self._ext}",
        )
