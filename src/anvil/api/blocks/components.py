import os

from anvil import ANVIL, CONFIG
from anvil.api.logic.molang import Molang
from anvil.api.pbr.pbr import __TextureSet
from anvil.lib.blockbench import _Blockbench
from anvil.lib.enums import (BlockFaces, BlockLiquidDetectionTouching,
                             BlockMaterial, TintMethod)
from anvil.lib.format_versions import (BLOCK_JSON_FORMAT_VERSION,
                                       BLOCK_SERVER_VERSION,
                                       ITEM_SERVER_VERSION)
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.schemas import _BaseComponent
from anvil.lib.types import RGB, RGBA


class BlockRedstoneConductivity(_BaseComponent):
    _identifier = "minecraft:redstone_conductivity"

    def __init__(self, allows_wire_to_step_down: bool = True, redstone_conductor: bool = False) -> None:
        """Specifies whether a block has redstone properties. If the component is not provided, the default values are used.

        Parameters:
            allows_wire_to_step_down (bool, optional): Specifies if redstone wire can stair-step downward on the block, Defaults to True.
            redstone_conductor (bool, optional): Specifies if the block can be powered by redstone, Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_redstone_conductivity
        """
        super().__init__("redstone_conductivity")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.30")
        self._add_field("allows_wire_to_step_down", allows_wire_to_step_down)
        self._add_field("redstone_conductor", redstone_conductor)


class BlockCustomComponents(_BaseComponent):
    _identifier = "minecraft:custom_components"

    def __init__(self, *components: str) -> None:
        """Sets the color of the block when rendered to a map.

        Parameters:
            components (str): The components to register, if the namespace is not provided, the project namespace will be used.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_custom_components
        """
        super().__init__("custom_components")
        self._set_value(components)


class BlockDefault(_BaseComponent):
    _identifier = "minecraft:block_default"

    def __init__(self) -> None:
        """The default block component."""
        super().__init__("block_default")

    def ambient_occlusion_exponent(self, exponent: int):
        """The exponent for ambient occlusion of the block."""
        self._add_field("ambient_occlusion_exponent", max(0, exponent))
        return self

    def sound(self, sound: str):
        """The sound of the block."""
        self._add_field("sound", sound)
        return self

    def isotropic(self, **kwParameters: dict[str, BlockFaces]):
        """The isotropic of the block."""
        if BlockFaces.All in kwParameters.values():
            self._set_value("isotropic", True)
        else:
            self._add_field("isotropic", {v: k for k, v in kwParameters.items()})
        return self

    def textures(self, **kwParameters: dict[str, BlockFaces]):
        """The textures of the block."""
        for k in kwParameters.keys():
            if not FileExists(os.path.join("assets", "textures", "blocks", f"{k}.png")):
                raise FileNotFoundError(
                    f"{k}.png not found in {os.path.join("assets", "textures", "blocks")}. Please ensure the file exists."
                )

            CopyFiles(
                os.path.join("assets", "textures", "blocks"),
                os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "blocks").replace("\\", "/"),
                f"{k}.png",
            )
            ANVIL.definitions.register_terrain_texture(k, "", k)

        if BlockFaces.All in kwParameters.values():
            self._add_field("textures", [f"{CONFIG.NAMESPACE}:{k}" for k, v in kwParameters.items() if v == BlockFaces.All][0])
        else:
            self._add_field("textures", {v: f"{CONFIG.NAMESPACE}:{k}" for k, v in kwParameters.items()})

        return self

    def carried_textures(self, **kwParameters: dict[str, BlockFaces]):
        """The carried textures of the block."""
        if BlockFaces.All in kwParameters.values():
            self._set_value(
                "carried_textures", [f"{CONFIG.NAMESPACE}:{k}" for k, v in kwParameters.items() if v == BlockFaces.All][0]
            )
        else:
            self._add_field("carried_textures", {v: f"{CONFIG.NAMESPACE}:{k}" for k, v in kwParameters.items()})
        return self


class BlockDestructibleByExplosion(_BaseComponent):
    _identifier = "minecraft:destructible_by_explosion"

    def __init__(self, explosion_resistance: int) -> None:
        """Describes the destructible by explosion properties for this block.

        Parameters:
            explosion_resistance (int): The amount of resistance to explosions in a range of 0 to 100.
        """
        super().__init__("destructible_by_explosion")
        self._add_field("explosion_resistance", explosion_resistance)


class BlockDestructibleByMining(_BaseComponent):
    _identifier = "minecraft:destructible_by_mining"

    def __init__(self, seconds_to_destroy: int) -> None:
        """Describes the destructible by mining properties for this block.

        Parameters:
            seconds_to_destroy (int): The amount of time it takes to destroy the block in seconds.
        """
        super().__init__("destructible_by_mining")
        self._enforce_version(ITEM_SERVER_VERSION, "1.21.50")
        self._add_field("seconds_to_destroy", seconds_to_destroy)
        self._add_field("item_specific_speeds", [])

    def item_specific_speeds_name(self, destroy_speed: float, item_name: str):
        self._component["item_specific_speeds"].append({"item": item_name, "destroy_speed": destroy_speed})

    def item_specific_speeds_tag(self, destroy_speed: float, item_tag: str | Molang):
        self._component["item_specific_speeds"].append({"item": {"tags": item_tag}, "destroy_speed": destroy_speed})


class BlockFlammable(_BaseComponent):
    _identifier = "minecraft:flammable"

    def __init__(self, catch_chance_modifier: int, destroy_chance_modifier: int) -> None:
        """Describes the flammable properties for this block.

        Parameters:
            catch_chance_modifier (int): The chance that this block will catch fire in a range of 0 to 100.
            destroy_chance_modifier (int): The chance that this block will be destroyed when on fire in a range of 0 to 100.
        """
        super().__init__("flammable")
        self._add_field("catch_chance_modifier", catch_chance_modifier)
        self._add_field("destroy_chance_modifier", destroy_chance_modifier)


class BlockFriction(_BaseComponent):
    _identifier = "minecraft:friction"

    def __init__(self, friction: float = 0.4) -> None:
        """Describes the friction for this block in a range of 0.0 to 0.9.

        Parameters:
            friction (float, optional): The friction of the block. Defaults to 0.4.
        """
        super().__init__("flammable")
        self._set_value(clamp(friction, 0, 0.9))


class BlockLightDampening(_BaseComponent):
    _identifier = "minecraft:light_dampening"

    def __init__(self, light_dampening: int = 15) -> None:
        """The amount that light will be dampened when it passes through the block in a range of 0 to 15.

        Parameters:
            light_dampening (int, optional): The amount of light dampening. Defaults to 15.
        """
        super().__init__("light_dampening")
        self._set_value(clamp(light_dampening, 0, 15))


class BlockLightEmission(_BaseComponent):
    _identifier = "minecraft:light_emission"

    def __init__(self, light_emission: int = 0) -> None:
        """The amount of light this block will emit in a range of 0 to 15.

        Parameters:
            light_emission (int, optional): The amount of light emission. Defaults to 0.
        """
        super().__init__("light_emission")
        self._set_value(clamp(light_emission, 0, 15))


class BlockLootTable(_BaseComponent):
    _identifier = "minecraft:loot"

    def __init__(self, loot: str) -> None:
        """Specifies the path to the loot table.

        Parameters:
            loot (str): The path to the loot table.
        """
        super().__init__("loot")
        self._set_value(loot)


class BlockMapColor(_BaseComponent):
    _identifier = "minecraft:map_color"

    def __init__(self, color: str, tint_method: TintMethod = TintMethod.None_) -> None:
        """Sets the color of the block when rendered to a map. If this component is omitted, the block will not show up on the map.

        Parameters:
            color (str): The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255.
            tint_method (str, optional): Optional, tint multiplied to the color. Tint method logic varies, but often refers to the "rain" and "temperature" of the biome the block is placed in to compute the tint. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color
        """
        self._enforce_version(BLOCK_JSON_FORMAT_VERSION, "1.21.70")
        super().__init__("map_color")
        self._add_field("color", color)
        if tint_method is not TintMethod.None_:
            self._add_field("tint_method", tint_method)


class BlockMaterialInstance(_BaseComponent):
    _identifier = "minecraft:material_instances"

    def __init__(self) -> None:
        """Maps face or material_instance names in a geometry file to an actual material instance."""
        super().__init__("material_instances")
        self._texture_set: __TextureSet = None

    def add_instance(
        self,
        blockbench_name: str,
        color_texture: str,
        block_face: BlockFaces = BlockFaces.All,
        render_method: BlockMaterial = BlockMaterial.Opaque,
        ambient_occlusion: float = 0,
        face_dimming: bool = True,
        isotropic: bool = False,
        tint_method: TintMethod = TintMethod.None_,
        normal_texture: str | RGB | RGBA = None,
        heightmap_texture: str | RGB | RGBA = None,
        metalness_emissive_roughness_texture: str | RGB | RGBA = None,
        metalness_emissive_roughness_subsurface_texture: str | RGB | RGBA = None,
    ):
        """Maps face or material_instance names in a geometry file to an actual material instance.

        Parameters:
            color_texture (str): The name of the texture to use for this block.
            block_face (BlockFaces, optional): The face of the block to apply the texture to. Defaults to BlockFaces.All.
            render_method (BlockMaterial, optional): The render method to use for this block. Defaults to BlockMaterial.Opaque.
            ambient_occlusion (float, optional): The amount of ambient occlusion for this block. Defaults to 0.
            face_dimming (bool, optional): Whether or not to use face dimming for this block. Defaults to True.
            tint_method (TintMethod, optional): The tint method to use for this block. Defaults to TintMethod.None_.


        """
        bb = _Blockbench(blockbench_name, "blocks")
        bb.textures.queue_texture(color_texture)

        ANVIL.definitions.register_terrain_texture(color_texture, blockbench_name, color_texture)

        self._add_dict(
            {
                "*" if block_face == BlockFaces.All else block_face: {
                    "texture": f"{CONFIG.NAMESPACE}:{color_texture}",
                    "render_method": render_method if not render_method == BlockMaterial.Opaque else {},
                    "ambient_occlusion": ambient_occlusion if ambient_occlusion is False else {},
                    "face_dimming": face_dimming if face_dimming is False else {},
                    "tint_method": tint_method if not tint_method == TintMethod.None_ else {},
                    "isotropic": isotropic if isotropic is True else {},
                }
            }
        )

        if any(
            [
                normal_texture,
                heightmap_texture,
                metalness_emissive_roughness_texture,
                metalness_emissive_roughness_subsurface_texture,
            ]
        ):
            self._texture_set = __TextureSet(self.identifier, "blocks")
            self._texture_set.set_textures(
                blockbench_name,
                color_texture,
                normal_texture,
                heightmap_texture,
                metalness_emissive_roughness_texture,
                metalness_emissive_roughness_subsurface_texture,
            )

        return self

    def __getitem__(self, key):
        if self._texture_set:
            self._texture_set.queue()
        return super().__getitem__(key)


class BlockGeometry(_BaseComponent):
    _identifier = "minecraft:geometry"

    def __init__(self, geometry_name: str) -> None:
        """The description identifier of the geometry file to use to render this block.

        Parameters:
            geometry_name (str): The name of the geometry to use to render this block.
        """
        super().__init__("geometry")
        self._add_field("identifier", f"geometry.{CONFIG.NAMESPACE}.{geometry_name}")

        bb = _Blockbench(geometry_name, "blocks")
        bb.model.queue_model()

    def bone_visibility(self, **bone: dict[str, bool | str | Molang]):
        """Specifies the visibility of bones in the geometry file.

        Example:
            >>> BlockGeometry('block').bone_visibility(bone0=True, bone1=False)

        """
        self._add_field("bone_visibility", {b: v for b, v in bone.items()})
        return self


class BlockCollisionBox(_BaseComponent):
    _identifier = "minecraft:collision_box"

    def __init__(self, size: list[float], origin: list[float]) -> None:
        """Defines the area of the block that collides with entities.

        Parameters:
            size (list[float]): The size of the collision box.
            origin (list[float]): The origin of the collision box.
        """
        super().__init__("collision_box")
        if size == (0, 0, 0):
            self._set_value(False)
        else:
            self._add_field("size", size)
            self._add_field("origin", origin)


class BlockSelectionBox(_BaseComponent):
    _identifier = "minecraft:selection_box"

    def __init__(self, size: list[float], origin: list[float]) -> None:
        """Defines the area of the block that is selected by the player's cursor.

        Parameters:
            size (list[float]): The size of the selection box.
            origin (list[float]): The origin of the selection box.
        """
        super().__init__("selection_box")
        if size == (0, 0, 0):
            self._set_value(False)
        else:
            self._add_field("size", size)
            self._add_field("origin", origin)


class BlockPlacementFilter(_BaseComponent):
    _identifier = "minecraft:placement_filter"

    def __init__(self) -> None:
        """By default, custom blocks can be placed anywhere and do not have placement restrictions unless you specify them in this component."""
        super().__init__("placement_filter")
        self._add_field("conditions", [])

    def add_condition(self, allowed_faces: list[BlockFaces], block_filter: list[str]):
        """Adds a condition to the placement filter.

        Parameters:
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
        self._component["conditions"].append(
            {
                "allowed_faces": allowed_faces,
                "block_filter": block_filter,
            }
        )
        return self


class BlockTransformation(_BaseComponent):
    _identifier = "minecraft:transformation"

    def __init__(self) -> None:
        """The block's transfomration."""
        super().__init__("transformation")

    def translation(self, translation: tuple[float, float, float]):
        """The block's translation.

        Parameters:
            translation (position): The block's translation.
        """
        self._add_field("translation", translation)
        return self

    def scale(self, scale: tuple[float, float, float], scale_pivot: tuple[float, float, float] = (0, 0, 0)):
        """The block's scale.

        Parameters:
            scale (position): The block's scale.
        """
        self._add_field("scale", scale)

        if scale_pivot != (0, 0, 0):
            self._add_field("scale_pivot", scale_pivot)

        return self

    def rotation(self, rotation: tuple[float, float, float], rotation_pivot: tuple[float, float, float] = (0, 0, 0)):
        """The block's rotation.

        Parameters:
            rotation (position): The block's rotation.

        """
        self._add_field("rotation", rotation)

        if rotation_pivot != (0, 0, 0):
            self._add_field("rotation_pivot", rotation_pivot)
        return self


class BlockDisplayName(_BaseComponent):
    _identifier = "minecraft:display_name"

    def __init__(self, display_name: str, localize: bool = True) -> None:
        """Sets the block display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Parameters:
            display_name (str): Set the display name for an block.
            localize (bool, optional): Whether to use the name with a localization file or not. Defaults to True.

        """
        super().__init__("display_name")
        if localize:
            key = f'tile.{CONFIG.NAMESPACE}:{display_name.lower().replace(" ", "_")}.name'
            ANVIL.definitions.register_lang(key, display_name)
            self._set_value(key)
        else:
            self._set_value(display_name)


class BlockCraftingTable(_BaseComponent):
    _identifier = "minecraft:crafting_table"

    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes.

        Parameters:
            table_name (str): The name of the crafting table.

        Raises:
            IndexError: The crafting table tags cannot exceed 64 tags.
            ValueError: The crafting table tags are limited to 64 characters.
        """
        super().__init__("crafting_table")
        self._add_field("table_name", table_name)

        if len(crafting_tags) > 64:
            raise IndexError("Crafting Table tags cannot exceed 64 tags.")

        for tag in crafting_tags:
            if len(tag) > 64:
                raise ValueError("Crafting Table tags are limited to 64 characters.")

        self._add_field("crafting_tags", crafting_tags)


class BlockItemVisual(_BaseComponent):
    _identifier = "minecraft:item_visual"

    def __init__(self, geometry_name: str, texture: str, render_method: BlockMaterial = BlockMaterial.Opaque) -> None:
        """The description identifier of the geometry and material used to render the item of this block.

        Parameters:
            geometry (str): The geometry of the item.
            texture (str): The texture of the item.
            render_method (BlockMaterial): The method used to render the item.

        """
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.60")
        super().__init__("item_visual")

        bb = _Blockbench(geometry_name, "blocks")
        bb.model.queue_model()

        self._add_field("geometry", {"identifier": geometry_name})
        self._add_field("material_instances", {"*": {"texture": texture, "render_method": render_method}})


class BlockLiquidDetection(_BaseComponent):
    _identifier = "minecraft:liquid_detection"

    def __init__(self) -> None:
        """The block's liquid detection."""
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.60")
        super().__init__("liquid_detection")
        self._add_field("detection_rules", [])

    def add_rule(
        self,
        liquid_type: str = "minecraft:water",
        on_liquid_touches: BlockLiquidDetectionTouching = BlockLiquidDetectionTouching.Blocking,
        can_contain_liquid: bool = False,
        stops_liquid_flowing_from_direction: list[BlockFaces] = [],
    ):
        """Adds a rule to the liquid detection.

        Parameters:
            liquid_type (str): The type of liquid, defaults to "minecraft:water".
            on_liquid_touches (BlockLiquidDetectionTouching): The action to take when the liquid touches the block.
            can_contain_liquid (bool, optional): Whether the block can contain the liquid. Defaults to False.

        """
        self._component["detection_rules"].append(
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


class BlockDestructionParticles(_BaseComponent):
    _identifier = "minecraft:destruction_particles"

    def __init__(self, blockbench_name: str, texture: str = None, tint_method: TintMethod = TintMethod.None_) -> None:
        """Sets the particles that will be used when the block is destroyed.

        Parameters:
            blockbench_name (str): The name of the blockbench model.
            texture (str, optional): The texture name used for the particle.
            tint_method (TintMethod, optional): Tint multiplied to the color. Defaults to TintMethod.None_.
        """
        super().__init__("destruction_particles")
        if texture is not None:
            bb = _Blockbench(blockbench_name, "blocks")
            bb.textures.queue_texture(texture)
            self._add_field("texture", texture)
        if tint_method is not TintMethod.None_:
            self._add_field("tint_method", tint_method)


class BlockTick(_BaseComponent):
    _identifier = "minecraft:tick"

    def __init__(
        self,
        interval_range: tuple[int, int] = (0, 0),
        looping: bool = True,
    ) -> None:
        """Causes the block to tick at intervals randomly chosen from interval_range.

        Parameters:
            interval_range (tuple[int, int], optional): [min, max] ticks before next tick. Defaults to (0, 0).
            looping (bool, optional): If True, block will continue ticking; otherwise it ticks only once. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_tick
        """
        super().__init__("tick")
        # ensure first value <= second value
        low, high = interval_range
        if low > high:
            low, high = high, low
        self._add_field("interval_range", [low, high])
        self._add_field("looping", looping)
