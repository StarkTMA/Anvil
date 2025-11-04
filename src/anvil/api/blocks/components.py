from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, overload

from anvil.api.core.components import List, _BaseComponent
from anvil.api.core.core import TerrainTexturesObject
from anvil.api.core.textures import FlipBookTexturesObject
from anvil.api.logic.molang import Molang
from anvil.api.pbr.pbr import TextureSet
from anvil.api.world.loot_tables import LootTable
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG
from anvil.lib.enums import (
    BlockFaces,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockMovementType,
    TintMethod,
)
from anvil.lib.format_versions import (
    BLOCK_JSON_FORMAT_VERSION,
    BLOCK_SERVER_VERSION,
    ITEM_SERVER_VERSION,
)
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.schemas import BlockDescriptor
from anvil.lib.translator import AnvilTranslator
from anvil.lib.types import Identifier


@dataclass(frozen=True, kw_only=True)
class FlipbookParams:
    frames: List[int]
    ticks_per_frame: int = 20
    atlas_index: int = 0
    atlas_tile_variant: int = 0
    replicate: int = 1
    blend_frames: bool = True

    def validate(self, variant_count: int) -> None:
        if not self.frames:
            raise ValueError("FlipbookParams.frames cannot be empty.")
        if self.ticks_per_frame <= 0:
            raise ValueError("FlipbookParams.ticks_per_frame must be positive.")
        if self.replicate <= 0 or (self.replicate & (self.replicate - 1)) != 0:
            # power-of-two check; matches Bedrock expectations for replicate granularity
            raise ValueError(
                "FlipbookParams.replicate must be a power of two (1,2,4,8,...)"
            )
        if self.atlas_tile_variant is not None:
            if self.atlas_tile_variant < 0 or self.atlas_tile_variant >= variant_count:
                raise ValueError(
                    "FlipbookParams.atlas_tile_variant out of range for variations."
                )


@dataclass(frozen=True)
class InstanceVariant:
    color: str
    normal: str | None = None
    height: str | None = None
    mer: str | None = None
    mers: str | None = None
    weight: int = 1

    def queue(self, bb: "_Blockbench") -> None:
        bb.textures.queue_texture(self.color)
        if self.normal:
            bb.textures.queue_texture(self.normal)
        if self.height:
            bb.textures.queue_texture(self.height)
        if self.mer:
            bb.textures.queue_texture(self.mer)
        if self.mers:
            bb.textures.queue_texture(self.mers)

    def has_aux(self) -> bool:
        return bool(self.normal or self.height or self.mer or self.mers)


@dataclass(kw_only=True)
class MaterialParams:
    render_method: BlockMaterial = BlockMaterial.Opaque
    ambient_occlusion: Optional[float] = None
    face_dimming: Optional[bool] = None
    isotropic: bool = False
    tint_method: TintMethod = TintMethod.None_
    alpha_masked_tint: bool = False
    emissive: bool = False

    def validate(self, enforce_version) -> None:
        if self.alpha_masked_tint:
            enforce_version(BLOCK_SERVER_VERSION, "1.21.120")
            if self.tint_method is TintMethod.None_:
                raise ValueError("alpha_masked_tint requires a non-None tint_method")
            if self.render_method is not BlockMaterial.Opaque:
                raise ValueError("alpha_masked_tint requires render_method = Opaque")
        if self.emissive:
            enforce_version(BLOCK_SERVER_VERSION, "1.21.120")


@dataclass(kw_only=True)
class InstanceSpec:
    blockbench_name: str
    face: Union[BlockFaces, str] = BlockFaces.All
    variations: List[InstanceVariant] = field(default_factory=list)
    params: MaterialParams = field(default_factory=MaterialParams)
    flipbooks: list[FlipbookParams] = field(default_factory=list)

    def validate(self) -> None:
        if self.face == BlockFaces.Side:
            raise ValueError(
                "BlockFaces.Side is not supported; use All or explicit faces."
            )
        if not self.variations:
            raise ValueError("At least one VariantPackage is required.")
        if any(v.weight <= 0 for v in self.variations):
            raise ValueError("VariantPackage.weight must be positive.")

        def sig(v: InstanceVariant) -> tuple[bool, bool, bool, bool]:
            return (
                v.normal is not None,
                v.height is not None,
                v.mer is not None,
                v.mers is not None,
            )

        base_sig = sig(self.variations[0])
        for v in self.variations[1:]:
            if sig(v) != base_sig:
                raise ValueError(
                    "All variants must provide the same set of PBR maps (present/absent)."
                )

        if self.flipbooks:
            for fb in self.flipbooks:
                fb.validate(len(self.variations))

    def queue_all(self) -> "_Blockbench":
        bb = _Blockbench(self.blockbench_name, "blocks")
        for vp in self.variations:
            vp.queue(bb)
        return bb

    def any_aux(self) -> bool:
        return any(vp.has_aux() for vp in self.variations)

    def color_texture(self, index: int = 0) -> str:
        return self.variations[index].color


class BlockMaterialInstance(_BaseComponent):
    _identifier = "minecraft:material_instances"

    def __init__(self) -> None:
        super().__init__("material_instances")
        self._require_components(BlockGeometry)
        self._parsed_textures: Dict[str, List[str]] = {}

    def add_instance(self, spec: InstanceSpec) -> "BlockMaterialInstance":
        spec.validate()
        spec.params.validate(self._enforce_version)
        bb = spec.queue_all()

        if len(spec.variations) > 1:
            variations_payload = [
                {"weight": vp.weight, "texture": vp.color} for vp in spec.variations
            ]
            TerrainTexturesObject().add_block_variations(
                block_name=spec.color_texture(),
                directory=spec.blockbench_name,
                block_variant=variations_payload,
            )
        else:
            only = spec.variations[0]
            TerrainTexturesObject().add_block(
                spec.color_texture(),
                spec.blockbench_name,
                [only.color],
            )

        self._add_dict(
            {
                (
                    "*" if spec.face == BlockFaces.All else spec.face
                ): self._material_payload(spec)
            }
        )

        if spec.any_aux():
            for vp in spec.variations:
                self._texture_set = TextureSet(vp.color, "blocks")
                self._texture_set.set_textures(
                    spec.blockbench_name,
                    vp.color,
                    vp.normal,
                    vp.height,
                    vp.mer,
                    vp.mers,
                )
                self._texture_set.queue()

        if spec.flipbooks:
            for fb in spec.flipbooks:

                FlipBookTexturesObject().add_block(
                    spec.color_texture(),
                    spec.blockbench_name,
                    spec.color_texture(fb.atlas_tile_variant),
                    fb.frames,
                    fb.ticks_per_frame,
                    fb.atlas_index,
                    fb.atlas_tile_variant,
                    fb.replicate,
                    fb.blend_frames,
                )

        return self

    def _material_payload(self, spec: InstanceSpec) -> dict:
        p = spec.params
        return {
            "texture": f"{CONFIG.NAMESPACE}:{spec.color_texture()}",
            "render_method": (
                p.render_method if p.render_method != BlockMaterial.Opaque else {}
            ),
            "ambient_occlusion": (
                p.ambient_occlusion if p.ambient_occlusion is not None else {}
            ),
            "face_dimming": p.face_dimming if p.face_dimming is not None else {},
            "tint_method": p.tint_method if p.tint_method != TintMethod.None_ else {},
            "isotropic": p.isotropic if p.isotropic else {},
            "alpha_masked_tint": p.alpha_masked_tint if p.alpha_masked_tint else {},
            "emissive": p.emissive if p.emissive else {},
        }

    def _export(self):
        return super()._export()


class BlockFlowerPottable(_BaseComponent):
    _identifier = "minecraft:flower_pottable"

    def __init__(self) -> None:
        """Indicates that this block can be placed in a flower pot.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flower_pottable
        """
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.120")
        super().__init__("flower_pottable")
        self._set_value({"do_not_shorten": True})


class BlockEmbeddedVisual(_BaseComponent):
    _identifier = "minecraft:embedded_visual"

    @overload
    def __init__(self) -> None:
        """Uses the default full block geometry for the item visual."""
        pass

    @overload
    def __init__(
        self,
        blockbench_name: str,
    ) -> None:
        """The description identifier of the geometry and material used to render this block when it it is embedded inside of another block (for example, a flower inside of a flower pot).

        Parameters:
            blockbench_name (str): The geometry of the item.
        """
        pass

    def __init__(
        self,
        blockbench_name: str = None,
    ) -> None:
        """The description identifier of the geometry and material used to render this block when it it is embedded inside of another block (for example, a flower inside of a flower pot).

        Parameters:
            blockbench_name (str, optional): The geometry of the item. Defaults to None for default full block geometry.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_embedded_visual
        """
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.120")
        super().__init__("item_visual")
        self._is_default = blockbench_name is None

        if blockbench_name is None:
            self._add_field("geometry", {"identifier": "minecraft:geometry.full_block"})
        else:
            bb = _Blockbench(blockbench_name, "blocks")
            bb.model.queue_model()

            self._add_field(
                "geometry",
                {"identifier": f"geometry.{CONFIG.NAMESPACE}.{blockbench_name}"},
            )

    def material_instance(
        self,
        blockbench_name: str,
        texture: str,
        block_face: BlockFaces | str = BlockFaces.All,
        render_method: BlockMaterial = BlockMaterial.Opaque,
    ):
        """Adds a material instance to the embedded visual.

        Parameters:
            blockbench_name (str): The blockbench reference name.
            texture (str): The texture of the block.
            block_face (BlockFaces): The face of the block to apply the texture to.

        """
        if block_face == BlockFaces.All:
            face_key = "*"
        else:
            face_key = block_face

        bb = _Blockbench(blockbench_name, "blocks")
        bb.textures.queue_texture(texture)

        TerrainTexturesObject().add_block(texture, blockbench_name, [texture])

        self._get_field("material_instances", {})[face_key] = {
            "texture": f"{CONFIG.NAMESPACE}:{texture}",
            "render_method": (
                render_method if not render_method == BlockMaterial.Opaque else {}
            ),
        }
        return self


class BlockRedstoneProducer(_BaseComponent):
    _identifier = "minecraft:redstone_producer"

    def __init__(
        self,
        power: int = 0,
        connected_faces: list[BlockFaces] = [BlockFaces.All],
        strongly_powered_face: BlockFaces = None,
        transform_relative: bool = False,
    ) -> None:
        """Indicates that this block produces a redstone signal.

        Parameters:
            power (int, optional): Signal strength produced by the block (0-15). Defaults to 0.
            connected_faces (list[BlockFaces], optional): Faces considered connected to the circuit. If omitted, all faces are connected.
            strongly_powered_face (BlockFaces | str, optional): The face that will be strongly powered by this block.
            transform_relative (bool, optional): If true, connected_faces and strongly_powered_face are transformed relative to the block's transformation. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_producer
        """
        super().__init__("redstone_producer")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.120")

        if not 0 <= power <= 15:
            raise ValueError("Power must be between 0 and 15.")
        self._add_field("power", int(power))

        if connected_faces is not None:
            # Expand shorthand faces if provided (Side -> N,S,E,W). If All present, keep as [All].
            faces = list(connected_faces)
            if BlockFaces.Side in faces:
                # replace Side with cardinal faces
                faces = [f for f in faces if f is not BlockFaces.Side]
                faces.extend(
                    [
                        BlockFaces.North,
                        BlockFaces.South,
                        BlockFaces.East,
                        BlockFaces.West,
                    ]
                )
            if BlockFaces.All in faces:
                faces.remove(BlockFaces.All)

            self._add_field("connected_faces", faces)

        if strongly_powered_face is not None:
            # allow callers to pass either a BlockFaces enum or a raw string
            self._add_field("strongly_powered_face", strongly_powered_face)

        if transform_relative:
            self._add_field("transform_relative", True)


class BlockDestructionParticles(_BaseComponent):
    _identifier = "minecraft:destruction_particles"

    def __init__(
        self,
        blockbench_name: str,
        texture: str,
        particle_count: int,
        tint_method: TintMethod = TintMethod.None_,
    ) -> None:
        """Sets the particles that will be used when the block is destroyed.

        Parameters:
            blockbench_name (str): The name of the blockbench model.
            texture (str): The texture name used for the particle.
            particle_count (int): The number of particles to spawn on destruction.
            tint_method (TintMethod, optional): Tint multiplied to the color. Defaults to TintMethod.None_.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_destruction_particles
        """
        super().__init__("destruction_particles")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.100")
        bb = _Blockbench(blockbench_name, "blocks")
        bb.textures.queue_texture(texture)
        self._add_field("texture", texture)

        self._add_field("particle_count", particle_count)

        if tint_method is not TintMethod.None_:
            self._add_field("tint_method", tint_method)


class BlockMovable(_BaseComponent):
    _identifier = "minecraft:movable"

    def __init__(
        self,
        movement_type: BlockMovementType = BlockMovementType.PushPull,
        sticky: str = "none",
    ) -> None:
        """The description identifier of the movable component.

        Parameters:
            movement_type (BlockMovementType, optional): How the block reacts to being pushed by another block like a piston. Defaults to BlockMovementType.PushPull.
            sticky (str, optional): How the block should handle adjacent blocks around it when being pushed by another block like a piston. Defaults to "none".

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_movable
        """
        super().__init__("movable")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.100")
        self._add_field("movement_type", movement_type)
        self._add_field("sticky", sticky)


class BlockRedstoneConductivity(_BaseComponent):
    _identifier = "minecraft:redstone_conductivity"

    def __init__(
        self, allows_wire_to_step_down: bool = True, redstone_conductor: bool = False
    ) -> None:
        """Specifies whether a block has redstone properties. If the component is not provided, the default values are used.

        Parameters:
            allows_wire_to_step_down (bool, optional): Specifies if redstone wire can stair-step downward on the block, Defaults to True.
            redstone_conductor (bool, optional): Specifies if the block can be powered by redstone, Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraft_redstone_conductivity
        """
        super().__init__("redstone_conductivity")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.30")
        self._add_field("allows_wire_to_step_down", allows_wire_to_step_down)
        self._add_field("redstone_conductor", redstone_conductor)


class BlockCustomComponents(_BaseComponent):
    _identifier = "minecraft:custom_components"

    def __init__(self, component_name: str) -> None:
        """Allows you to add custom components to a block.

        Parameters:
            component_name (str): The components name to register, if the namespace is not provided, the project namespace will be used.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/documents/scripting/custom-components
        """
        super().__init__(component_name, False)
        self._set_value({"do_not_shorten": True})


class BlockDestructibleByExplosion(_BaseComponent):
    _identifier = "minecraft:destructible_by_explosion"

    def __init__(self, explosion_resistance: int = None) -> None:
        """Describes the destructible by explosion properties for this block.

        Parameters:
            explosion_resistance (int): The amount of resistance to explosions in a range of 0 to 100.
        """
        super().__init__("destructible_by_explosion")

        if explosion_resistance is None:
            self._set_value(False)
        else:
            self._add_field("explosion_resistance", explosion_resistance)


class BlockDestructibleByMining(_BaseComponent):
    _identifier = "minecraft:destructible_by_mining"

    def __init__(self, seconds_to_destroy: int = None) -> None:
        """Describes the destructible by mining properties for this block.

        Parameters:
            seconds_to_destroy (int, optional): The amount of time it takes to destroy the block in seconds. If None, disables mining destructibility.
        """
        super().__init__("destructible_by_mining")
        self._enforce_version(ITEM_SERVER_VERSION, "1.21.50")
        if seconds_to_destroy is None:
            self._set_value(False)
        else:
            self._add_field("seconds_to_destroy", seconds_to_destroy)
            self._add_field("item_specific_speeds", [])

    def item_specific_speeds_name(self, destroy_speed: float, item_name: str):
        if "item_specific_speeds" in self._component:
            self._component["item_specific_speeds"].append(
                {"item": item_name, "destroy_speed": destroy_speed}
            )

    def item_specific_speeds_tag(self, destroy_speed: float, item_tag: str | Molang):
        if "item_specific_speeds" in self._component:
            self._component["item_specific_speeds"].append(
                {"item": {"tags": item_tag}, "destroy_speed": destroy_speed}
            )


class BlockFlammable(_BaseComponent):
    _identifier = "minecraft:flammable"

    def __init__(
        self, catch_chance_modifier: int, destroy_chance_modifier: int
    ) -> None:
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

    def __init__(self, loot_table: LootTable | str) -> None:
        """SSets the loot table for what items this block drops upon being broken.

        Parameters:
            loot_table (LootTable | str): The loot table to use for this block.
        """
        super().__init__("loot")
        self._set_value(
            loot_table.table_path if isinstance(loot_table, LootTable) else loot_table
        )


class BlockMapColor(_BaseComponent):
    _identifier = "minecraft:map_color"

    def __init__(self, color: str, tint_method: TintMethod = TintMethod.None_) -> None:
        """Sets the color of the block when rendered to a map. If this component is omitted, the block will not show up on the map.

        Parameters:
            color (str): The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255.
            tint_method (str, optional): Optional, tint multiplied to the color. Tint method logic varies, but often refers to the "rain" and "temperature" of the biome the block is placed in to compute the tint. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color
        """
        self._enforce_version(BLOCK_JSON_FORMAT_VERSION, "1.21.70")
        super().__init__("map_color")
        self._add_field("color", color)
        if tint_method is not TintMethod.None_:
            self._add_field("tint_method", tint_method)


class BlockGeometry(_BaseComponent):
    _identifier = "minecraft:geometry"

    @overload
    def __init__(self, blockbench_name: str, uv_lock: bool = False) -> None:
        """The description identifier of the geometry file to use to render this block.

        Parameters:
            blockbench_name (str): The name of the Blockbench model to use to render this block.
            uv_lock (bool, optional): A Boolean locking UV orientation of all bones in the geometry, or an array of strings locking UV orientation of specific bones in the geometry. For performance reasons it is recommended to use the Boolean. Note that for cubes using Box UVs, rather than Per-face UVs, 'uv_lock' is only supported if the cube faces are square.
        """
        pass

    @overload
    def __init__(self) -> None:
        """Used 'minecraft:geometry.full_block' to specify the default full cube geometry for a block. Which comes with built-in culling and lighting optimizations."""
        pass

    def __init__(
        self,
        blockbench_name: str = None,
        uv_lock: bool = False,
    ) -> None:
        """The description identifier of the geometry file to use to render this block.
        Parameters:
            blockbench_name (str, optional): The name of the Blockbench model to use to render this block. Defaults to "minecraft:geometry.full_block".
            uv_lock (bool, optional): A Boolean locking UV orientation of all bones in the geometry, or an array of strings locking UV orientation of specific bones in the geometry. For performance reasons it is recommended to use the Boolean. Note that for cubes using Box UVs, rather than Per-face UVs, 'uv_lock' is only supported if the cube faces are square.
        """
        super().__init__("geometry")
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.80")
        self._is_default = blockbench_name is None

        if blockbench_name is None:
            self._add_field("identifier", "minecraft:geometry.full_block")

        else:
            self._require_components(BlockMaterialInstance)
            self._add_field(
                "identifier", f"geometry.{CONFIG.NAMESPACE}.{blockbench_name}"
            )

            self._geometry_name = blockbench_name
            if uv_lock:
                self._add_field("uv_lock", uv_lock)

            self._bb = _Blockbench(blockbench_name, "blocks")
            self._bb.model.queue_model()

    def bone_visibility(self, **bone: dict[str, bool | str | Molang]):
        """Specifies the visibility of bones in the geometry file.

        Example:
            >>> BlockGeometry('block').bone_visibility(bone0=True, bone1=False)

        """
        if self._is_default:
            raise ValueError("Cannot set bone visibility on default geometry.")

        self._add_field("bone_visibility", {b: v for b, v in bone.items()})
        return self

    def block_culling(self):
        """Specifies the block culling rules for the geometry file."""
        if self._is_default:
            raise ValueError("Cannot set block culling on default geometry.")

        self._add_field("culling", f"{CONFIG.NAMESPACE}:{self._geometry_name}")
        return self._bb.model.block_culling()


class BlockCollisionBox(_BaseComponent):
    _identifier = "minecraft:collision_box"

    def __init__(self, size: list[float], origin: list[float]) -> None:
        """Defines the area of the block that collides with entities.

        Parameters:
            size (list[float]): The size of the collision box.
            origin (list[float]): The origin of the collision box.
        """
        super().__init__("collision_box")
        min_origin = (-8, 0, -8)
        max_origin = (8, 16, 8)
        if size == (0, 0, 0):
            self._set_value(False)
        else:
            if any(
                o < min_o or o > max_o
                for o, min_o, max_o in zip(origin, min_origin, max_origin)
            ):
                raise ValueError(
                    f"Origin {origin} must be within {min_origin} and {max_origin}."
                )
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

    def add_condition(
        self,
        allowed_faces: list[BlockFaces],
        block_filter: list[BlockDescriptor | Identifier],
    ):
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
                "block_filter": [str(f) for f in block_filter],
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

    def scale(
        self,
        scale: tuple[float, float, float],
        scale_pivot: tuple[float, float, float] = (0, 0, 0),
    ):
        """The block's scale.

        Parameters:
            scale (position): The block's scale.
        """
        self._add_field("scale", scale)

        if scale_pivot != (0, 0, 0):
            self._add_field("scale_pivot", scale_pivot)

        return self

    def rotation(
        self,
        rotation: tuple[float, float, float],
        rotation_pivot: tuple[float, float, float] = (0, 0, 0),
    ):
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

    def __init__(self, display_name: str, localized_key: str = None) -> None:
        """Sets the block display name within Minecraft: Bedrock Edition. This component may also be used to pull from the localization file by referencing a key from it.

        Parameters:
            display_name (str): Set the display name for an block.
            localized_key (str, optional): The localization key to use for the block's display name. If not provided, a key will be generated.

        """
        super().__init__("display_name")
        if not localized_key:
            localized_key = f'tile.{CONFIG.NAMESPACE}:{display_name.lower().replace(" ", "_").replace("\\n", "_")}.name'

        AnvilTranslator().add_localization_entry(localized_key, display_name)
        self._set_value(localized_key)


class BlockCraftingTable(_BaseComponent):
    _identifier = "minecraft:crafting_table"

    def __init__(self, table_name: str, crafting_tags: list[str]) -> None:
        """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes.

        Parameters:
            table_name (str): The display name of the crafting table.
            crafting_tags (list[str]): A list of tags that define which recipes can be crafted at this crafting table.

        Raises:
            IndexError: The crafting table tags cannot exceed 64 tags.
            ValueError: The crafting table tags are limited to 64 characters.
        """
        super().__init__("crafting_table")
        localized_key = (
            f'tile.{CONFIG.NAMESPACE}:{table_name.lower().replace(" ", "_")}.name'
        )
        AnvilTranslator().add_localization_entry(
            localized_key,
            table_name,
        )
        self._add_field("table_name", localized_key)

        if len(crafting_tags) > 64:
            raise IndexError("Crafting Table tags cannot exceed 64 tags.")

        for tag in crafting_tags:
            if len(tag) > 64:
                raise ValueError("Crafting Table tags are limited to 64 characters.")

        self._add_field("crafting_tags", crafting_tags)


class BlockItemVisual(_BaseComponent):
    _identifier = "minecraft:item_visual"

    @overload
    def __init__(self) -> None:
        """Uses the default full block geometry for the item visual."""
        pass

    @overload
    def __init__(
        self,
        blockbench_name: str,
    ) -> None:
        """The description identifier of the geometry and material used to render the item of this block.

        Parameters:
            blockbench_name (str): The geometry of the item.
        """
        pass

    def __init__(
        self,
        blockbench_name: str = None,
    ) -> None:
        """The description identifier of the geometry and material used to render the item of this block.

        Parameters:
            blockbench_name (str, optional): The geometry of the item. Defaults to None for default full block geometry.
        """
        self._enforce_version(BLOCK_SERVER_VERSION, "1.21.60")
        super().__init__("item_visual")
        self._is_default = blockbench_name is None

        if blockbench_name is None:
            self._add_field("geometry", {"identifier": "minecraft:geometry.full_block"})
        else:
            bb = _Blockbench(blockbench_name, "blocks")
            bb.model.queue_model()

            self._add_field(
                "geometry",
                {"identifier": f"geometry.{CONFIG.NAMESPACE}.{blockbench_name}"},
            )

        self._add_field("material_instances", {})

    def material_instance(
        self,
        blockbench_name: str,
        texture: str,
        block_face: BlockFaces | str = BlockFaces.All,
        render_method: BlockMaterial = BlockMaterial.Opaque,
    ):
        """Adds a material instance to the item visual.

        Parameters:
            blockbench_name (str): The blockbench reference name.
            texture (str): The texture of the item.
            block_face (BlockFaces): The face of the block to apply the texture to.

        """
        if block_face == BlockFaces.All:
            face_key = "*"
        else:
            face_key = block_face

        bb = _Blockbench(blockbench_name, "blocks")
        bb.textures.queue_texture(texture)

        TerrainTexturesObject().add_block(texture, blockbench_name, [texture])

        self._component["material_instances"][face_key] = {
            "texture": f"{CONFIG.NAMESPACE}:{texture}",
            "render_method": (
                render_method if not render_method == BlockMaterial.Opaque else {}
            ),
        }
        return self


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
                    [
                        BlockFaces.North,
                        BlockFaces.South,
                        BlockFaces.East,
                        BlockFaces.West,
                    ]
                    if BlockFaces.Side in stops_liquid_flowing_from_direction
                    else (
                        [
                            BlockFaces.North,
                            BlockFaces.South,
                            BlockFaces.East,
                            BlockFaces.West,
                            BlockFaces.Up,
                            BlockFaces.Down,
                        ]
                        if BlockFaces.All in stops_liquid_flowing_from_direction
                        else stops_liquid_flowing_from_direction
                    )
                ),
            }
        )
        return self


class BlockDestructionParticles(_BaseComponent):
    _identifier = "minecraft:destruction_particles"

    def __init__(
        self,
        blockbench_name: str,
        texture: str = None,
        tint_method: TintMethod = TintMethod.None_,
    ) -> None:
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

            TerrainTexturesObject().add_block(texture, blockbench_name, [texture])
            self._add_field("texture", f"{CONFIG.NAMESPACE}:{texture}")
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_tick
        """
        super().__init__("tick")
        # ensure first value <= second value
        low, high = interval_range
        if low > high:
            low, high = high, low
        self._add_field("interval_range", [low, high])
        self._add_field("looping", looping)
