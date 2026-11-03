import dataclasses
from dataclasses import InitVar
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Literal, get_args

from anvil.api.core.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
)
from anvil.api.textures import FlipBookTexturesObject, TerrainTexturesObject
from anvil.api.core.types import (
    RGB,
    RGB255,
    RGBA,
    RGBA255,
    BlockChestObstructionRule,
    BlockConnectionSource,
    BlockCullingLayer,
    BlockDefaultGeometry,
    BlockLavaFlammable,
    BlockMovementType,
    BlockPrecipitationBehavior,
    BlockSticky,
    BlockSupportShape,
    HexRGB,
    HexRGBA,
    InstrumentSound,
    TintMethod,
)
from anvil.api.logic.molang import Molang
from anvil.api.models.geometry import (
    Geometry,
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
    ItemDisplayTransforms,
)
from anvil.api.models.voxel_shape import VoxelShape
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.world.loot_tables import LootTable
from anvil.lib.blockbench import (
    _Blockbench,
    _blockbench_geometry_name,
    _BlockBenchSource,
    _geometry_block_culling,
)
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    ComponentPlacement,
    ExpandFaces,
    Hex,
    InRange,
    JsonComponent,
    JsonCustomComponent,
    JsonObject,
    JsonValue,
    JsonValueComponent,
    Keyed,
    Length,
    MinMax,
    NonNegative,
    Ordered,
    RedstoneSignal,
    ShortTag,
    Unique,
    json_field,
)
from anvil.lib.jsonmodel.identifier import Identifier
from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor
from anvil.lib.translator import AnvilTranslator

if TYPE_CHECKING:
    from anvil.api.blocks.server import BlockServer


# region Parts: objects nested inside components


@dataclasses.dataclass(frozen=True, kw_only=True)
class FlipbookParams:
    """A flipbook animation of a material instance's texture, added to `flipbook_textures.json`.

    Args:
        frames (list[int]): The atlas frames to play, in order.
        ticks_per_frame (int, optional): How long each frame shows. Defaults to 20.
        atlas_index (int, optional): The atlas index. Defaults to 0.
        atlas_tile_variant (int, optional): The variation the animation uses. Defaults to 0.
        replicate (int, optional): A power of two. Defaults to 1.
        blend_frames (bool, optional): Whether frames blend into each other. Defaults to True.
    """

    frames: list[int]
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
            raise ValueError(
                "FlipbookParams.replicate must be a power of two (1,2,4,8,...)"
            )
        if not 0 <= self.atlas_tile_variant < variant_count:
            raise ValueError(
                "FlipbookParams.atlas_tile_variant out of range for variations."
            )


@dataclasses.dataclass(frozen=True)
class InstanceVariant(TextureComponents):
    """One texture of a material instance, with its PBR maps, and its weight when the
    instance picks one of several textures at random."""

    weight: int = 1

    def has_aux(self) -> bool:
        return bool(self.normal or self.height or self.mer or self.mers)


class MaterialParams(JsonObject):
    """How a material instance renders. Unset options are left out, so the game defaults apply.

    Args:
        render_method (BlockMaterial, optional): The render method. Game default opaque.
        ambient_occlusion (float, optional): Exponent applied to ambient occlusion after lighting, from 0 to 10. Game default 1.
        face_dimming (bool, optional): Whether faces are dimmed by their direction. Game default true.
        isotropic (bool, optional): Whether the texture is randomly rotated per face.
        tint_method (TintMethod, optional): Tint multiplied to the texture by the biome.
        alpha_masked_tint (bool, optional): Tints only where the texture's alpha is not 0. Needs a `tint_method` and an opaque render method.
        emissive (bool, optional): Whether the texture glows.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_material_instances)
    """

    render_method: BlockMaterial | None = json_field(default=None)
    ambient_occlusion: Annotated[float, InRange(0.0, 10.0)] | None = json_field(
        default=None
    )
    face_dimming: bool | None = json_field(default=None)
    isotropic: bool | None = json_field(default=None)
    tint_method: TintMethod | None = json_field(default=None)
    alpha_masked_tint: bool | None = json_field(default=None)
    emissive: bool | None = json_field(default=None)

    def __validate__(self) -> None:
        if self.alpha_masked_tint:
            if self.tint_method in (None, "none"):
                raise ValueError(
                    f"{type(self).__name__}.alpha_masked_tint needs a tint_method."
                )
            if self.render_method not in (None, BlockMaterial.Opaque):
                raise ValueError(
                    f"{type(self).__name__}.alpha_masked_tint needs the opaque render method."
                )


class MaterialInstance(MaterialParams):
    """A material instance: a texture and how it renders. It also takes every option of
    `MaterialParams`.

    Args:
        face (BlockFaceValues | str, optional): The face, or the name of a material instance in the geometry. Written as the instance's key. Defaults to every face.
        texture (str): The texture's short name in `terrain_texture.json`.
    """

    face: BlockFaceValues | str = json_field(default=BlockFaceValues.All, exclude=True)
    texture: str = json_field()

    @property
    def key(self) -> str:
        """The instance's key in `material_instances`: `*` for every face."""
        return "*" if self.face == BlockFaceValues.All else str(self.face)


@dataclasses.dataclass(kw_only=True)
class InstanceSpec:
    """A material instance to add with `BlockMaterialInstance.add_instance`, and the textures
    to take from a Blockbench model for it.

    Args:
        blockbench (str): The Blockbench model the textures come from.
        face (BlockFaceValues | str, optional): The face, or the name of a material instance in the geometry. Defaults to every face.
        variations (list[InstanceVariant]): The textures. With more than one, the game picks one at random, by weight.
        params (MaterialParams, optional): How the material renders.
        flipbooks (list[FlipbookParams], optional): Flipbook animations of the texture.
    """

    blockbench: str
    face: BlockFaceValues | str = BlockFaceValues.All
    variations: list[InstanceVariant] = dataclasses.field(default_factory=list)
    params: MaterialParams = dataclasses.field(default_factory=MaterialParams)
    flipbooks: list[FlipbookParams] = dataclasses.field(default_factory=list)

    def validate(self) -> None:
        if self.face == BlockFaceValues.Side:
            raise ValueError(
                "BlockFaceValues.Side is not supported; use All or explicit faces."
            )
        if not self.variations:
            raise ValueError("InstanceSpec needs at least one variation.")
        if any(v.weight <= 0 for v in self.variations):
            raise ValueError("InstanceVariant.weight must be positive.")

        def maps(v: InstanceVariant) -> tuple[bool, bool, bool, bool]:
            return (
                v.normal is not None,
                v.height is not None,
                v.mer is not None,
                v.mers is not None,
            )

        if any(maps(v) != maps(self.variations[0]) for v in self.variations[1:]):
            raise ValueError(
                "All variations must provide the same set of PBR maps (present/absent)."
            )
        for flipbook in self.flipbooks:
            flipbook.validate(len(self.variations))

    def any_aux(self) -> bool:
        return any(vp.has_aux() for vp in self.variations)

    def color_texture(self, index: int = 0) -> str:
        return self.variations[index].color


class BlockBox(JsonObject):
    """A box inside the block, in pixels, measured from the bottom centre of the block.

    Args:
        origin (tuple[float, float, float]): The minimal corner, x and z from -8 to 8, y from 0.
        size (tuple[float, float, float]): The size along each axis.
    """

    origin: tuple[float, float, float] = json_field()
    size: tuple[float, float, float] = json_field()


class ItemTagFilter(JsonObject):
    """Items matched by their tags, for `BlockDestructibleByMining`.

    Args:
        tags (Molang | str): A tag query, for example `Query.AnyTag(["minecraft:is_pickaxe"])`.
    """

    tags: Molang | str = json_field()


class ItemSpecificSpeed(JsonObject):
    """How long the block takes to mine with specific items.

    Args:
        item (str | MinecraftItemDescriptor | ItemTagFilter): The item, or the tags of the items.
        destroy_speed (float): The seconds to destroy the block with those items.
    """

    item: str | MinecraftItemDescriptor | ItemTagFilter = json_field()
    destroy_speed: float = json_field()


class PlacementCondition(JsonObject):
    """Where the block can be placed and stay, for `BlockPlacementFilter`.

    Args:
        allowed_faces (list[BlockFaceValues], optional): The faces of the block below or beside it the block can be placed on. Game default every face.
        block_filter (list[str | MinecraftBlockDescriptor], optional): The blocks it can be placed on, at most 64. Game default any block.
    """

    allowed_faces: Annotated[list[BlockFaceValues], ExpandFaces] | None = json_field(
        default=None
    )
    block_filter: (
        Annotated[list[str | MinecraftBlockDescriptor], Length(maximum=64)] | None
    ) = json_field(default=None)


class LiquidDetectionRule(JsonObject):
    """How the block reacts to a liquid, for `BlockLiquidDetection`.

    Args:
        liquid_type (Literal["water"], optional): The liquid. Only water is supported. Game default water.
        on_liquid_touches (BlockLiquidDetectionTouching, optional): What happens when the liquid flows into the block. Game default blocking.
        can_contain_liquid (bool, optional): Whether the block can be waterlogged. Game default false.
        stops_liquid_flowing_from_direction (list[BlockFaceValues], optional): The faces liquid can't flow out of the block through.
        use_liquid_clipping (bool, optional): Whether the liquid is visually clipped by the block's collision. Game default false.
    """

    liquid_type: Literal["water"] | None = json_field(default=None)
    on_liquid_touches: BlockLiquidDetectionTouching | None = json_field(default=None)
    can_contain_liquid: bool | None = json_field(default=None)
    stops_liquid_flowing_from_direction: (
        Annotated[list[BlockFaceValues], ExpandFaces] | None
    ) = json_field(default=None)
    use_liquid_clipping: bool | None = json_field(default=None)


class NWayVisualRotation(JsonObject):
    """The block states that turn a visual's geometry around each axis.

    Args:
        x (str, optional): The state for the x axis.
        y (str, optional): The state for the y axis, for example "minecraft:cardinal_direction".
        z (str, optional): The state for the z axis.
    """

    x: str | None = json_field(default=None)
    y: str | None = json_field(default=None)
    z: str | None = json_field(default=None)


class BoneVisibility(JsonValue):
    """Whether one bone of a custom geometry is visible. Added with `add_bone_visibility`.

    Args:
        bone (str): The bone name. Written as the key.
        visible (bool | Molang): True, False, or a Molang expression evaluated against the block states.
    """

    bone: str = json_field(exclude=True)
    visible: bool | Molang | str = json_field()


class VisualGeometry(JsonObject):
    """The geometry of an item or embedded visual.

    Args:
        identifier (str): The geometry identifier.
        n_way_visual_rotation (NWayVisualRotation, optional): The states that turn it.

    Its `bone_visibility` is filled by the visual's `add_bone_visibility`.
    """

    identifier: str = json_field()
    bone_visibility: Annotated[list[BoneVisibility], Unique("bone"), Keyed("bone")] = (
        json_field(default_factory=list, init=False, omit_default=True)
    )
    n_way_visual_rotation: NWayVisualRotation | None = json_field(default=None)


class BlockEntityContainer(JsonObject):
    """The inventory of a block entity.

    Args:
        slot_count (int): The number of slots, from 1 to 54.
    """

    slot_count: Annotated[int, InRange(1, 54)] = json_field()


class OffsetRange(JsonObject):
    """The random offset along one axis, for `BlockRandomOffset`.

    Args:
        range (tuple[float, float], optional): The `(min, max)` offset, in pixels. Game default (0, 0).
        steps (int, optional): How many positions the range is split into. 0 allows any value between. Game default 0.
    """

    range: Annotated[tuple[float, float], MinMax] | None = json_field(default=None)
    steps: Annotated[int, NonNegative] | None = json_field(default=None)


def _geometry_source(
    blockbench: str | Geometry | None, collection: str | None
) -> tuple[str, "_Blockbench | Geometry | None", str | None]:
    """Queues the model a geometry comes from, and returns the geometry identifier, the model
    (`None` for a vanilla geometry) and the geometry name."""
    if blockbench is None or blockbench in get_args(BlockDefaultGeometry):
        if collection is not None:
            raise ValueError(
                "Collection selection is only supported for custom Blockbench geometries."
            )
        return blockbench or "minecraft:geometry.full_block", None, None
    if isinstance(blockbench, Geometry):
        if collection is not None:
            raise ValueError(
                "Collection selection only applies to Blockbench models. Pass the collection's Geometry instead."
            )
        blockbench.queue(_BlockBenchSource.BLOCK)
        return blockbench.geometry_identifier, blockbench, blockbench.name
    name = _blockbench_geometry_name(blockbench, collection)
    model = _Blockbench(blockbench, _BlockBenchSource.BLOCK)
    model.model.queue_model(collection)
    return f"geometry.{CONFIG.NAMESPACE}.{name}", model, name


# endregion

# region Shared bases


class _Switchable(JsonComponent, abstract=True):
    """A component that can be written as `false` to turn its behaviour off, and is written as
    `true` when none of its options are set."""

    enabled: bool = json_field(default=True, exclude=True)

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        if not self.enabled:
            if payload:
                raise ValueError(
                    f"{type(self).__name__} sets options while enabled is False."
                )
            return {self.identifier: False}
        return {self.identifier: payload or True}


class _BlockBoxComponent(_Switchable, abstract=True):
    """A box the block occupies, checked against the space a block may use."""

    _max_height: ClassVar[int] = 16

    origin: tuple[float, float, float] | None = json_field(default=None)
    size: tuple[float, float, float] | None = json_field(default=None)

    def _check_box(
        self, origin: tuple[float, float, float], size: tuple[float, float, float]
    ) -> None:
        low = (-8, 0, -8)
        high = (8, self._max_height, 8)
        end = [o + s for o, s in zip(origin, size)]
        if any(not lo <= v <= hi for v, lo, hi in zip(origin, low, high)) or any(
            not lo <= v <= hi for v, lo, hi in zip(end, low, high)
        ):
            raise ValueError(
                f"{type(self).__name__}: the box at {tuple(origin)} of size {tuple(size)} "
                f"must stay within {low} and {high}."
            )

    def __validate__(self) -> None:
        if (self.origin is None) != (self.size is None):
            raise ValueError(f"{type(self).__name__} needs both origin and size.")
        if self.origin is not None:
            self._check_box(self.origin, self.size)


class _BlockVisual(JsonComponent, abstract=True):
    """The geometry and material instances of an item or embedded visual."""

    blockbench: InitVar[str | Geometry | None] = None
    collection: InitVar[str | None] = None
    n_way_visual_rotation: InitVar[NWayVisualRotation | None] = None
    geometry: VisualGeometry = json_field(default=None, init=False)
    material_instances: Annotated[
        list[MaterialInstance], Unique("key"), Keyed("key")
    ] = json_field(default_factory=list, omit_default=True)
    _model: Any = json_field(default=None, init=False, exclude=True)
    _collection: str | None = json_field(default=None, init=False, exclude=True)

    def __post_init__(
        self,
        blockbench: str | Geometry | None,
        collection: str | None,
        n_way_visual_rotation: NWayVisualRotation | None,
    ) -> None:
        identifier, self._model, _ = _geometry_source(blockbench, collection)
        self._collection = collection
        self.geometry = VisualGeometry(
            identifier=identifier,
            n_way_visual_rotation=n_way_visual_rotation,
        )

    def __validate__(self) -> None:
        if self._model is None and self.geometry.bone_visibility:
            raise ValueError(
                f"{type(self).__name__}: bone_visibility needs a custom geometry."
            )

    def add_bone_visibility(self, **bones: bool | Molang | str):
        """Sets which bones are visible. Custom geometries only.

        Example:
            >>> BlockItemVisual(blockbench="door").add_bone_visibility(door_open=False)

        Args:
            **bones (bool | Molang): Each bone name, and True, False or a Molang expression.
        """
        self.geometry.bone_visibility.extend(
            BoneVisibility(bone=bone, visible=visible)
            for bone, visible in bones.items()
        )
        return self

    def add_material_instance(
        self,
        *,
        blockbench: str,
        texture: str,
        face: BlockFaceValues | str = BlockFaceValues.All,
        render_method: BlockMaterial | None = None,
    ):
        """Adds a material instance, and its texture to the resource pack.

        Args:
            blockbench (str): The Blockbench model the texture comes from.
            texture (str): The texture.
            face (BlockFaceValues | str, optional): The face, or a material instance name. Defaults to every face.
            render_method (BlockMaterial, optional): The render method. Game default opaque.
        """
        _Blockbench(blockbench, _BlockBenchSource.BLOCK).textures.queue_texture(texture)
        TerrainTexturesObject().add_block(
            block_name=texture, directory=blockbench, block_textures=[texture]
        )
        self.material_instances.append(
            MaterialInstance(
                face=face,
                texture=f"{CONFIG.NAMESPACE}:{texture}",
                render_method=render_method,
            )
        )
        return self


# endregion

# region Components


class BlockCustomComponent(JsonCustomComponent, abstract=True):
    """Base of block custom components: components registered by a script, with parameters.

    Subclass it with an `identifier` and the parameters as fields. The identifier is in the project
    namespace: a name without one gets it, any other namespace is refused.

        class Explosive(BlockCustomComponent):
            identifier = "explosive"

            power: float = json_field()

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/scripting/custom-components)
    """


class BlockChestObstruction(JsonComponent):
    """Defines how this block obstructs a chest directly below it from opening.

    Args:
        obstruction_rule (BlockChestObstructionRule, optional): "always", "never", or "shape" to use the block's shape. Game default "shape".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_chest_obstruction)
    """

    identifier = "minecraft:chest_obstruction"

    obstruction_rule: BlockChestObstructionRule | None = json_field(default=None)


class BlockCollisionBox(_BlockBoxComponent):
    """The area of the block that collides with entities. With no box, the full block collides.

    Args:
        origin (tuple[float, float, float], optional): The minimal corner of the box, in pixels from the bottom centre of the block.
        size (tuple[float, float, float], optional): The size of the box. The box must stay within (-8, 0, -8) and (8, 24, 8).
        enabled (bool, optional): False makes the block collide with nothing, written as `false`. Defaults to True.

    Add more boxes with `add_box`. Boxes are always written as a list, even when there is only one.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_collision_box)
    """

    identifier = "minecraft:collision_box"
    _max_height = 24

    _boxes: list[BlockBox] = json_field(default_factory=list, init=False, exclude=True)

    def add_box(
        self, *, origin: tuple[float, float, float], size: tuple[float, float, float]
    ) -> "BlockCollisionBox":
        """Adds another collision box, for more complex shapes.

        Args:
            origin (tuple[float, float, float]): The minimal corner of the box.
            size (tuple[float, float, float]): The size of the box.
        """
        self._boxes.append(BlockBox(origin=origin, size=size))
        return self

    def __validate__(self) -> None:
        _BlockBoxComponent.__validate__(self)
        if self._boxes and self.origin is None:
            raise ValueError("BlockCollisionBox needs origin and size to add boxes.")
        for box in self._boxes:
            self._check_box(box.origin, box.size)

    def __json__(self) -> Any:
        payload = _Switchable.__json__(self)
        box = payload[self.identifier]
        if not isinstance(box, dict):
            return payload
        return {self.identifier: [box, *(extra.__json__() for extra in self._boxes)]}


class BlockConnectionRule(JsonComponent):
    """Defines whether fences, walls, bars and glass panes can connect to this block.

    Args:
        accepts_connections_from (BlockConnectionSource, optional): "all", "only_fences" or "none". Game default "all".
        enabled_directions (list[BlockFaceValues], optional): The sides that can connect. Game default every side.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_connection_rule)
    """

    identifier = "minecraft:connection_rule"

    accepts_connections_from: BlockConnectionSource | None = json_field(default=None)
    enabled_directions: (
        Annotated[
            list[
                Literal[
                    BlockFaceValues.North,
                    BlockFaceValues.South,
                    BlockFaceValues.East,
                    BlockFaceValues.West,
                    BlockFaceValues.Side,
                ]
            ],
            ExpandFaces,
        ]
        | None
    ) = json_field(default=None)


class BlockCraftingTable(JsonComponent):
    """Makes the block a crafting table: it opens the crafting table UI and crafts the recipes with its tags.

    Args:
        crafting_tags (list[str]): The tags of the recipes it crafts, at most 64, each at most 64 characters.
        table_name (str, optional): The name shown on the UI. Anvil adds it to the language file under a key made from the block identifier.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_crafting_table)
    """

    identifier = "minecraft:crafting_table"

    crafting_tags: Annotated[list[Annotated[str, ShortTag]], Length(maximum=64)] = (
        json_field()
    )
    table_name: str | None = json_field(default=None)

    def __prepare_export__(self, owner: "BlockServer", *, root: bool = True) -> None:
        """Adds the name to the language file under `tile.<identifier>.table_name` for the root,
        and `tile.<identifier>.<name>.table_name` for a permutation, then writes the key.
        """
        prefix = f"tile.{owner.identifier}"
        if self.table_name is None or self.table_name.startswith(f"{prefix}."):
            return
        if root:
            key = f"{prefix}.table_name"
            AnvilTranslator().add_localization_entry(key, self.table_name)
        else:
            key = AnvilTranslator().localize(
                self.table_name, prefix=prefix, suffix="table_name"
            )
        self.table_name = key


class BlockDestructibleByExplosion(_Switchable):
    """Describes how the block resists explosions.

    Args:
        explosion_resistance (float, optional): The resistance to explosions. Game default 0.
        enabled (bool, optional): False makes the block indestructible by explosions, written as `false`. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_explosion)
    """

    identifier = "minecraft:destructible_by_explosion"

    explosion_resistance: Annotated[float, NonNegative] | None = json_field(
        default=None
    )


class BlockDestructibleByMining(_Switchable):
    """Describes how long the block takes to mine.

    Args:
        seconds_to_destroy (float, optional): The seconds to mine the block with base equipment. Game default 0.
        item_specific_speeds (list[ItemSpecificSpeed], optional): The seconds to mine it with specific items. Set them directly or add them with `add_item_specific_speed`.
        enabled (bool, optional): False makes the block indestructible by mining, written as `false`. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_mining)
    """

    identifier = "minecraft:destructible_by_mining"

    seconds_to_destroy: Annotated[float, NonNegative] | None = json_field(default=None)
    item_specific_speeds: list[ItemSpecificSpeed] = json_field(
        default_factory=list, omit_default=True
    )

    def add_item_specific_speed(
        self,
        *,
        item: str | MinecraftItemDescriptor | ItemTagFilter,
        destroy_speed: float,
    ) -> "BlockDestructibleByMining":
        """Adds the seconds to mine the block with an item, or items with tags.

        Example:
            >>> mining.add_item_specific_speed(
            ...     item=ItemTagFilter(tags=Query.AllTags(["minecraft:is_axe"])), destroy_speed=1.5
            ... )
        """
        self.item_specific_speeds.append(
            ItemSpecificSpeed(item=item, destroy_speed=destroy_speed)
        )
        return self


class BlockDestructionParticles(JsonComponent):
    """Sets the particles shown when the block is destroyed.

    Args:
        texture (str, optional): The texture of the particles.
        particle_count (int, optional): How many particles, at most 255. Game default 100.
        tint_method (TintMethod, optional): Tint multiplied to the texture.
        blockbench (str, optional): The Blockbench model to take the texture from. Not written to the JSON.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destruction_particles)
    """

    identifier = "minecraft:destruction_particles"

    texture: str | None = json_field(default=None)
    particle_count: Annotated[int, InRange(0, 255)] | None = json_field(default=None)
    tint_method: TintMethod | None = json_field(default=None)
    blockbench: InitVar[str | None] = None

    def __post_init__(self, blockbench: str | None) -> None:
        if blockbench and self.texture:
            _Blockbench(blockbench, _BlockBenchSource.BLOCK).textures.queue_texture(
                self.texture
            )


class BlockDisplayName(JsonValueComponent):
    """Sets the name of the block. Anvil adds it to the language file under a key made from the
    block identifier, and writes the key.

    Args:
        value (str): The name.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_display_name)
    """

    identifier = "minecraft:display_name"

    value: str = json_field()

    def __prepare_export__(self, owner: "BlockServer", *, root: bool = True) -> None:
        """Adds the name to the language file under `tile.<identifier>.name` for the root, and
        `tile.<identifier>.<name>.name` for a permutation, then writes the key in its place.
        """
        prefix = f"tile.{owner.identifier}"
        if self.value.startswith(f"{prefix}."):
            return
        if root:
            key = f"{prefix}.name"
            AnvilTranslator().add_localization_entry(key, self.value)
        else:
            key = AnvilTranslator().localize(self.value, prefix=prefix, suffix="name")
        self.value = key


class BlockEmbeddedVisual(_BlockVisual):
    """The geometry and material instances used to render the block when it is embedded in
    another block, such as a flower in a flower pot.

    Args:
        blockbench (str | Geometry, optional): The Blockbench model, or a Geometry built in code. Defaults to the full block.
        collection (str, optional): The exported Blockbench collection to use.
        n_way_visual_rotation (NWayVisualRotation, optional): The states that turn the geometry.

    Add material instances with `add_material_instance`, and bone visibility with
    `add_bone_visibility`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_embedded_visual)
    """

    identifier = "minecraft:embedded_visual"


class BlockEntity(JsonComponent):
    """Gives each placed block its own data.

    Args:
        container (BlockEntityContainer, optional): An inventory. Set it with `set_container`.
        dynamic_properties (bool, optional): Whether scripts can store dynamic properties on the block. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_entity)
    """

    identifier = "minecraft:block_entity"

    container: BlockEntityContainer | None = json_field(default=None)
    dynamic_properties: bool | None = json_field(default=None)

    def set_container(
        self,
        *,
        slot_count: int,
    ) -> "BlockEntity":
        """Gives the block an inventory. See `BlockEntityContainer` for the parameters."""
        self.container = BlockEntityContainer(
            slot_count=slot_count,
        )
        return self


class BlockEntityFallOn(JsonComponent):
    """Sets how far an entity must fall onto the block to trigger the `onEntityFallOn` event of its custom components.

    Args:
        minimum_fall_distance (float, optional): The distance, in blocks. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_entity_fall_on)
    """

    identifier = "minecraft:entity_fall_on"

    minimum_fall_distance: Annotated[float, NonNegative] | None = json_field(
        default=None
    )


class BlockFlammable(_Switchable):
    """Describes how the block catches fire from its neighbours.

    Args:
        catch_chance_modifier (int, optional): The chance the block catches fire. Game default 5.
        destroy_chance_modifier (int, optional): The chance the fire destroys the block. Game default 20.
        lava_flammable (BlockLavaFlammable, optional): Whether lava next to the block sets it on fire: "always" or "never".
        enabled (bool, optional): False keeps fire from spreading to the block, written as `false`. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flammable)
    """

    identifier = "minecraft:flammable"

    catch_chance_modifier: Annotated[int, NonNegative] | None = json_field(default=None)
    destroy_chance_modifier: Annotated[int, NonNegative] | None = json_field(
        default=None
    )
    lava_flammable: BlockLavaFlammable | None = json_field(default=None)


class BlockFlowerPottable(JsonComponent):
    """The block can be placed in a flower pot. Root components only.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_flower_pottable)
    """

    identifier = "minecraft:flower_pottable"
    _placement = ComponentPlacement.ROOT


class BlockFriction(JsonValueComponent):
    """How slippery the block is, from 0.0 to 0.9. Higher is less slippery.

    Args:
        value (float, optional): The friction. Defaults to 0.4, ice uses 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_friction)
    """

    identifier = "minecraft:friction"

    value: Annotated[float, InRange(0.0, 0.9)] = json_field(default=0.4)


class BlockGeometry(JsonComponent):
    """The geometry used to render the block. The block also needs `BlockMaterialInstance`.

    Args:
        blockbench (str | Geometry | BlockDefaultGeometry, optional): The Blockbench model of the block, a Geometry built in code, or a vanilla geometry. Defaults to "minecraft:geometry.full_block". Written as `"identifier"`, a name the base class reserves.
        collection (str, optional): The exported Blockbench collection to use. The geometry identifier becomes `geometry.<namespace>.<model>.<collection>`.
        culling_layer (BlockCullingLayer, optional): The culling layer. Game default "minecraft:culling_layer.undefined".
        culling_shape (str, optional): The shape used to cull neighbouring faces, such as "minecraft:unit_cube". Set by `block_culling`.
        n_way_visual_rotation (NWayVisualRotation, optional): The block states that turn the geometry around each axis, for example `NWayVisualRotation(y="minecraft:cardinal_direction")`. Set it with `set_n_way_visual_rotation`.
        uv_lock (bool | list[str], optional): Locks the UV orientation of every bone, or of the bones named.

    Set which bones are visible with `add_bone_visibility`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_geometry)
    """

    identifier = "minecraft:geometry"

    # public init
    # init only
    blockbench: InitVar[str | Geometry] = "minecraft:geometry.full_block"
    collection: InitVar[str | None] = None
    # fields
    culling_layer: BlockCullingLayer | None = json_field(default=None)
    n_way_visual_rotation: NWayVisualRotation | None = json_field(default=None)
    uv_lock: bool | list[str] | None = json_field(default=None)
    # private from init
    geometry: str = json_field(default=None, init=False, key="identifier")
    bone_visibility: Annotated[list[BoneVisibility], Unique("bone"), Keyed("bone")] = (
        json_field(default_factory=list, init=False, omit_default=True)
    )
    culling_shape: str | None = json_field(default=None, init=False)
    culling: str | None = json_field(default=None, init=False)

    _model: _Blockbench | None = json_field(default=None, init=False, exclude=True)
    _collection: str | None = json_field(default=None, init=False, exclude=True)
    _name: str | None = json_field(default=None, init=False, exclude=True)

    def __post_init__(self, blockbench: str | Geometry, collection: str | None) -> None:
        self.geometry, self._model, self._name = _geometry_source(
            blockbench, collection
        )
        self._collection = collection

    def __validate__(self) -> None:
        if self._model is None and (self.bone_visibility or self.uv_lock):
            raise ValueError(
                "BlockGeometry: bone_visibility and uv_lock need a custom geometry."
            )

    def add_bone_visibility(self, **bones: bool | Molang | str) -> "BlockGeometry":
        """Sets which bones are visible. Custom geometries only.

        Example:
            >>> BlockGeometry(blockbench="door").add_bone_visibility(
            ...     door_open=Query.BlockState("open"), door_closed=~Query.BlockState("open")
            ... )

        Args:
            **bones (bool | Molang): Each bone name, and True, False or a Molang expression.
        """
        self.bone_visibility.extend(
            BoneVisibility(bone=bone, visible=visible)
            for bone, visible in bones.items()
        )
        return self

    def block_culling(
        self, *, culling_shape: Literal["empty", "custom"] | VoxelShape = "empty"
    ):
        """Gives the geometry culling rules, and returns them to add rules to.

        Args:
            culling_shape ("empty" | "custom" | VoxelShape, optional): "custom" uses the bounding boxes of the Blockbench model; a VoxelShape is used as is. Defaults to "empty".
        """
        if self._model is None:
            raise ValueError("Cannot set block culling on a vanilla geometry.")

        if isinstance(culling_shape, VoxelShape):
            culling_shape.queue()
            self.culling_shape = culling_shape.shape_identifier
        elif culling_shape == "custom":
            if isinstance(self._model, Geometry):
                raise ValueError(
                    "'custom' uses the bounding boxes of a Blockbench model, and this geometry was built in code. "
                    "Pass a VoxelShape instead."
                )
            self._model.model.queue_voxel_shape(self._collection)
            self.culling_shape = f"{CONFIG.NAMESPACE}:{self._name}_culling_shape"

        self.culling = f"{CONFIG.NAMESPACE}:{self._name}"
        if isinstance(self._model, Geometry):
            return _geometry_block_culling(self._model)
        return self._model.model.block_culling(self._collection)

    def set_n_way_visual_rotation(
        self,
        *,
        x: str | None = None,
        y: str | None = None,
        z: str | None = None,
    ) -> "BlockGeometry":
        """Sets the block states that turn the geometry around each axis. See `NWayVisualRotation` for the parameters."""
        self.n_way_visual_rotation = NWayVisualRotation(
            x=x,
            y=y,
            z=z,
        )
        return self


class BlockInstrumentSound(JsonComponent):
    """Sets the sound a note block plays when it is above or below this block. At least one face is needed.

    Args:
        up (InstrumentSound, optional): The sound when the note block is above. Game default "note.harp".
        down (InstrumentSound, optional): The sound when the note block is below. Game default "note.none".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_instrument_sound)
    """

    identifier = "minecraft:instrument_sound"

    up: InstrumentSound | None = json_field(default=None)
    down: InstrumentSound | None = json_field(default=None)

    def __validate__(self) -> None:
        if self.up is None and self.down is None:
            raise ValueError(
                "At least one of 'up' or 'down' must be defined for BlockInstrumentSound."
            )


class BlockItemVisual(_BlockVisual):
    """The geometry and material instances used to render the block's item.

    Args:
        blockbench (str | Geometry, optional): The Blockbench model, or a Geometry built in code. Defaults to the full block.
        collection (str, optional): The exported Blockbench collection to use.
        n_way_visual_rotation (NWayVisualRotation, optional): The states that turn the geometry.

    Add material instances with `add_material_instance`, and bone visibility with
    `add_bone_visibility`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_item_visual)
    """

    identifier = "minecraft:item_visual"

    def item_display_transforms(
        self,
        *,
        merge: bool = False,
        thirdperson_righthand: ItemDisplayTransform | None = None,
        thirdperson_lefthand: ItemDisplayTransform | None = None,
        firstperson_righthand: ItemDisplayTransform | None = None,
        firstperson_lefthand: ItemDisplayTransform | None = None,
        gui: ItemDisplayGuiTransform | None = None,
        head: ItemDisplayTransform | None = None,
        ground: ItemDisplayTransform | None = None,
        fixed: ItemDisplayTransform | None = None,
    ) -> "BlockItemVisual":
        """Overrides the `item_display_transforms` the Blockbench model brings with it.

        Only works on a visual made from a Blockbench collection, e.g.
        ``BlockItemVisual(blockbench="oak_planks", collection="stairs")``: the transforms live
        in that collection's geometry file, so every block that uses the same collection
        shares them.

        Example:
            >>> BlockItemVisual(blockbench="planks", collection="stairs").item_display_transforms(
            ...     gui=ItemDisplayGuiTransform(rotation=(30, 225, 0), scale=(0.6, 0.6, 0.6)),
            ...     ground=ItemDisplayTransform(translation=(0, 3, 0), scale=(0.5, 0.5, 0.5)),
            ... )

        Args:
            merge (bool): Keep the model's transforms for the slots not given. By default
                the model's transforms are dropped and only the ones given are used.
            thirdperson_righthand (ItemDisplayTransform, optional): The transform of the `thirdperson_righthand` slot.
            thirdperson_lefthand (ItemDisplayTransform, optional): The transform of the `thirdperson_lefthand` slot.
            firstperson_righthand (ItemDisplayTransform, optional): The transform of the `firstperson_righthand` slot.
            firstperson_lefthand (ItemDisplayTransform, optional): The transform of the `firstperson_lefthand` slot.
            head (ItemDisplayTransform, optional): The transform of the `head` slot.
            ground (ItemDisplayTransform, optional): The transform of the `ground` slot.
            fixed (ItemDisplayTransform, optional): The transform of the `fixed` slot.
            gui (ItemDisplayGuiTransform, optional): The transform of the `gui` slot, the only
                one that accepts `fit_to_frame`.
        """
        if not isinstance(self._model, _Blockbench) or self._collection is None:
            raise ValueError(
                "item_display_transforms only supports a visual made from a Blockbench "
                "collection: pass `collection` to BlockItemVisual."
            )
        slots = {
            "thirdperson_righthand": thirdperson_righthand,
            "thirdperson_lefthand": thirdperson_lefthand,
            "firstperson_righthand": firstperson_righthand,
            "firstperson_lefthand": firstperson_lefthand,
            "gui": gui,
            "head": head,
            "ground": ground,
            "fixed": fixed,
        }
        if all(transform is None for transform in slots.values()):
            raise ValueError(
                "Pass at least one display slot, e.g. gui=ItemDisplayGuiTransform(...)."
            )

        geometry = self._model.model.geometry(self._collection)
        kept = geometry.item_display_transforms if merge else None
        geometry.set_item_display_transforms(
            ItemDisplayTransforms(
                **{
                    slot: (
                        transform
                        if transform is not None
                        else getattr(kept, slot, None)
                    )
                    for slot, transform in slots.items()
                }
            )
        )
        return self


class BlockLeashable(JsonComponent):
    """The block can be leashed to by a lead.

    Args:
        offset (tuple[float, float, float], optional): Where the lead attaches, in pixels. Game default (0, 8, 0).

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_leashable)
    """

    identifier = "minecraft:leashable"

    offset: tuple[float, float, float] | None = json_field(default=None)


class BlockLightDampening(JsonValueComponent):
    """How much light is dampened as it passes through the block, from 0 to 15.

    Args:
        value (int, optional): 15 is fully opaque, like stone; 0 is fully transparent, like glass. Defaults to 15.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_dampening)
    """

    identifier = "minecraft:light_dampening"

    value: Annotated[int, RedstoneSignal] = json_field(default=15)


class BlockLightEmission(JsonValueComponent):
    """How much light the block emits, from 0 to 15.

    Args:
        value (int, optional): The light level. Defaults to 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_light_emission)
    """

    identifier = "minecraft:light_emission"

    value: Annotated[int, RedstoneSignal] = json_field(default=0)


class BlockLiquidDetection(JsonComponent):
    """How the block reacts to liquids. Only one rule per liquid is used.

    Args:
        detection_rules (list[LiquidDetectionRule], optional): The rules, at least one. Set them directly or add them with `add_detection_rule`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_liquid_detection)
    """

    identifier = "minecraft:liquid_detection"

    detection_rules: Annotated[list[LiquidDetectionRule], Length(minimum=1)] = (
        json_field(default_factory=list)
    )

    def add_detection_rule(
        self,
        *,
        liquid_type: Literal["water"] | None = None,
        on_liquid_touches: BlockLiquidDetectionTouching | None = None,
        can_contain_liquid: bool | None = None,
        stops_liquid_flowing_from_direction: list[BlockFaceValues] | None = None,
        use_liquid_clipping: bool | None = None,
    ) -> "BlockLiquidDetection":
        """Adds a rule. See `LiquidDetectionRule` for the parameters."""
        self.detection_rules.append(
            LiquidDetectionRule(
                liquid_type=liquid_type,
                on_liquid_touches=on_liquid_touches,
                can_contain_liquid=can_contain_liquid,
                stops_liquid_flowing_from_direction=stops_liquid_flowing_from_direction,
                use_liquid_clipping=use_liquid_clipping,
            )
        )
        return self


class BlockLootTable(JsonValueComponent):
    """The loot table the block drops when broken. Without it, the block drops itself.

    Args:
        value (LootTable | str): The loot table, or its path from the behaviour pack root.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_loot)
    """

    identifier = "minecraft:loot"

    value: LootTable | str = json_field()

    def __post_init__(self) -> None:
        if isinstance(self.value, LootTable):
            self.value = self.value.table_path


class BlockMapColor(JsonComponent):
    """The color of the block on a map. Without it, the block doesn't show on maps.

    Args:
        color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The color, written as "#RRGGBB".
        tint_method (TintMethod, optional): Tint multiplied to the color by the biome.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_map_color)
    """

    identifier = "minecraft:map_color"

    color: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] = (
        json_field()
    )
    tint_method: TintMethod | None = json_field(default=None)


class BlockMaterialInstance(JsonValueComponent):
    """The material instances of the block: the texture and render options of each face, or
    of each material instance named in the geometry. The block also needs `BlockGeometry`.

    Args:
        instances (list[MaterialInstance], optional): The instances, one per face or name. Add them with `add_instance`, which also adds the textures to the resource pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_material_instances)
    """

    identifier = "minecraft:material_instances"

    instances: Annotated[list[MaterialInstance], Unique("key"), Keyed("key")] = (
        json_field(default_factory=list)
    )

    def add_instance(
        self, *, spec: InstanceSpec, force_vanilla: bool = False
    ) -> "BlockMaterialInstance":
        """Adds a material instance, and its textures to the resource pack.

        Args:
            spec (InstanceSpec): The instance and its textures.
            force_vanilla (bool, optional): Registers the textures as vanilla textures. Defaults to False.
        """
        spec.validate()

        if len(spec.variations) > 1:
            TerrainTexturesObject().add_block_variations(
                block_name=spec.color_texture(),
                directory=spec.blockbench,
                block_variant=[(vp.color, vp.weight) for vp in spec.variations],
                force_vanilla=force_vanilla,
            )
        else:
            TerrainTexturesObject().add_block(
                block_name=spec.color_texture(),
                directory=spec.blockbench,
                block_textures=[spec.color_texture()],
                force_vanilla=force_vanilla,
            )

        params = spec.params
        self.instances.append(
            MaterialInstance(
                face=spec.face,
                texture=f"{CONFIG.NAMESPACE}:{spec.color_texture()}",
                render_method=params.render_method,
                ambient_occlusion=params.ambient_occlusion,
                face_dimming=params.face_dimming,
                isotropic=params.isotropic,
                tint_method=params.tint_method,
                alpha_masked_tint=params.alpha_masked_tint,
                emissive=params.emissive,
            )
        )

        for vp in spec.variations:
            texture_set = TextureSet(vp.color, _BlockBenchSource.BLOCK)
            texture_set.set_blockbench_textures(spec.blockbench, vp)
            texture_set.queue()

        for fb in spec.flipbooks:
            FlipBookTexturesObject().add_block(
                block_name=spec.color_texture(),
                directory=spec.blockbench,
                block_texture=spec.color_texture(fb.atlas_tile_variant),
                frames=fb.frames,
                ticks_per_frame=fb.ticks_per_frame,
                atlas_index=fb.atlas_index,
                atlas_tile_variant=fb.atlas_tile_variant,
                replicate=fb.replicate,
                blend_frames=fb.blend_frames,
            )

        return self


class BlockMovable(JsonComponent):
    """How the block reacts to pistons.

    Args:
        movement_type (BlockMovementType, optional): Pushed and pulled, pushed only, popped or immovable. Game default push_pull.
        sticky (BlockSticky, optional): "same" also moves the neighbouring blocks with the same setting. Game default "none".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_movable)
    """

    identifier = "minecraft:movable"

    movement_type: BlockMovementType | None = json_field(default=None)
    sticky: BlockSticky | None = json_field(default=None)


class BlockPlacementFilter(JsonComponent):
    """Where the block can be placed and stay. When a condition stops being met, the block pops off.

    Args:
        conditions (list[PlacementCondition], optional): The conditions, at most 64. Set them directly or add them with `add_condition`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_placement_filter)
    """

    identifier = "minecraft:placement_filter"

    conditions: Annotated[list[PlacementCondition], Length(maximum=64)] = json_field(
        default_factory=list
    )

    def add_condition(
        self,
        *,
        allowed_faces: list[BlockFaceValues] | None = None,
        block_filter: list[str | MinecraftBlockDescriptor] | None = None,
    ) -> "BlockPlacementFilter":
        """Adds a condition. See `PlacementCondition` for the parameters."""
        self.conditions.append(
            PlacementCondition(allowed_faces=allowed_faces, block_filter=block_filter)
        )
        return self


class BlockPrecipitationInteractions(JsonComponent):
    """How the block interacts with rain and snow.

    Args:
        precipitation_behavior (BlockPrecipitationBehavior): "obstruct_rain", "obstruct_rain_accumulate_snow", "none" or "snowlogging".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_precipitation_interactions)
    """

    identifier = "minecraft:precipitation_interactions"

    precipitation_behavior: BlockPrecipitationBehavior = json_field()


class BlockRandomOffset(JsonComponent):
    """Offsets the block by a random amount seeded from its position. It moves what is drawn, the outline and the collision.

    Args:
        x (OffsetRange, optional): The offset along x. Set it with `set_x`.
        y (OffsetRange, optional): The offset along y. Set it with `set_y`.
        z (OffsetRange, optional): The offset along z. Set it with `set_z`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_random_offset)
    """

    identifier = "minecraft:random_offset"

    x: OffsetRange | None = json_field(default=None)
    y: OffsetRange | None = json_field(default=None)
    z: OffsetRange | None = json_field(default=None)

    def set_z(
        self,
        *,
        range: tuple[float, float] | None = None,
        steps: int | None = None,
    ) -> "BlockRandomOffset":
        """Sets the random offset along z. See `OffsetRange` for the parameters."""
        self.z = OffsetRange(
            range=range,
            steps=steps,
        )
        return self

    def set_y(
        self,
        *,
        range: tuple[float, float] | None = None,
        steps: int | None = None,
    ) -> "BlockRandomOffset":
        """Sets the random offset along y. See `OffsetRange` for the parameters."""
        self.y = OffsetRange(
            range=range,
            steps=steps,
        )
        return self

    def set_x(
        self,
        *,
        range: tuple[float, float] | None = None,
        steps: int | None = None,
    ) -> "BlockRandomOffset":
        """Sets the random offset along x. See `OffsetRange` for the parameters."""
        self.x = OffsetRange(
            range=range,
            steps=steps,
        )
        return self


class BlockRedstoneConductivity(JsonComponent):
    """The redstone properties of the block.

    Args:
        allows_wire_to_step_down (bool, optional): Whether redstone wire can step down over the block. Game default true.
        redstone_conductor (bool, optional): Whether the block can be powered by redstone. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_conductivity)
    """

    identifier = "minecraft:redstone_conductivity"

    allows_wire_to_step_down: bool | None = json_field(default=None)
    redstone_conductor: bool | None = json_field(default=None)


class BlockRedstoneConsumer(JsonComponent):
    """The block consumes a redstone signal, and may pass it on. Root components only.

    Args:
        min_power (int, optional): The signal strength, from 0 to 15, at which the `onRedstoneUpdate` script event fires. Game default 0.
        propagates_power (bool, optional): Whether the block passes the signal on. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_consumer)
    """

    identifier = "minecraft:redstone_consumer"
    _placement = ComponentPlacement.ROOT

    min_power: Annotated[int, RedstoneSignal] | None = json_field(default=None)
    propagates_power: bool | None = json_field(default=None)


class BlockRedstoneProducer(JsonComponent):
    """The block produces a redstone signal.

    Args:
        power (int, optional): The signal strength, from 0 to 15.
        connected_faces (list[BlockFaceValues], optional): The faces connected to the circuit. Game default every face.
        strongly_powered_face (BlockFaceValues, optional): The face that is strongly powered.
        transform_relative (bool, optional): Whether the faces turn with `minecraft:transformation`. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_redstone_producer)
    """

    identifier = "minecraft:redstone_producer"

    power: Annotated[int, RedstoneSignal] | None = json_field(default=None)
    connected_faces: Annotated[list[BlockFaceValues], ExpandFaces] | None = json_field(
        default=None
    )
    strongly_powered_face: BlockFaceValues | None = json_field(default=None)
    transform_relative: bool | None = json_field(default=None)


class BlockReplaceable(JsonComponent):
    """The block is replaced when another block is placed in its position.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_replaceable)
    """

    identifier = "minecraft:replaceable"


class BlockSelectionBox(_BlockBoxComponent):
    """The area of the block the player's cursor selects. With no box, the full block is selected.

    Args:
        origin (tuple[float, float, float], optional): The minimal corner of the box, in pixels from the bottom centre of the block.
        size (tuple[float, float, float], optional): The size of the box. The box must stay within (-8, 0, -8) and (8, 16, 8).
        enabled (bool, optional): False makes the block unselectable, written as `false`. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_selection_box)
    """

    identifier = "minecraft:selection_box"


class BlockSupport(JsonComponent):
    """The support shape of the block. Without it, the block supports like a full cube.

    Args:
        shape (BlockSupportShape): "fence" or "stair". Stairs need the `minecraft:vertical_half` and a direction state.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_support)
    """

    identifier = "minecraft:support"

    shape: BlockSupportShape = json_field()


class BlockTagComponent(JsonValueComponent):
    """The tags of the block. Custom tags must be in the project namespace.

    Args:
        value (list[MinecraftBlockTags | str]): The tags.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocktags)
    """

    identifier = "minecraft:tags"

    value: list[MinecraftBlockTags | str] = json_field()

    def __validate__(self) -> None:
        for tag in self.value:
            if tag in MinecraftBlockTags:
                continue
            Identifier.parse(tag, vanilla=False, object_type="BlockTag")


class BlockTick(JsonComponent):
    """Makes the block tick at intervals chosen at random from `interval_range`, sending `onTick` to its custom components.

    Args:
        interval_range (tuple[int, int]): The `(min, max)` ticks between ticks. The game rejects the block without it.
        looping (bool, optional): Whether the block keeps ticking. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_tick)
    """

    identifier = "minecraft:tick"

    interval_range: Annotated[tuple[int, int], NonNegative, Ordered] = json_field()
    looping: bool | None = json_field(default=None)


class BlockTransformation(JsonComponent):
    """Translates, rotates and scales the block around its centre.

    Args:
        translation (tuple[float, float, float], optional): The offset, in blocks.
        rotation (tuple[float, float, float], optional): The rotation, in degrees, in steps of 90.
        rotation_pivot (tuple[float, float, float], optional): The point the rotation turns around.
        scale (tuple[float, float, float], optional): The scale. Game default (1, 1, 1).
        scale_pivot (tuple[float, float, float], optional): The point the scale grows from.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_transformation)
    """

    identifier = "minecraft:transformation"

    translation: tuple[float, float, float] | None = json_field(default=None)
    rotation: tuple[float, float, float] | None = json_field(default=None)
    rotation_pivot: tuple[float, float, float] | None = json_field(default=None)
    scale: tuple[float, float, float] | None = json_field(default=None)
    scale_pivot: tuple[float, float, float] | None = json_field(default=None)


# endregion
# endregion
