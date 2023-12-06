from typing import Dict

from anvil.api.actors import _Components
from anvil.api.components import _component
from anvil.core import ANVIL, AddonObject, _MinecraftDescription
from anvil.lib import *
from anvil.lib import _JsonSchemes

__all__ = ['Block', 'VanillaBlockTexture',
           'BlockDestructibleByExplosion', 'BlockDestructibleByMining', 
           'BlockFlammable', 'BlockFriction', 'BlockLightDampening', 'BlockLightEmission',
           'BlockLootTable', 'BlockMapColor', 'BlockMaterialInstance', 'BlockGeometry', 'BlockCollisionBox',
           'BlockSelectionBox', 'BlockPlacementFilter', 'BlockTransformation', 'BlockDisplayName', 'BlockCraftingTable',
           'PlacementDirectionTrait', 'PlacementPositionTrait', 'CardinalDirectionsTrait', 'FacingDirectionsTrait', 'BlockFacesTrait', 'VerticalHalfTrait',
           ]

# Block Traits
class PlacementDirectionTrait(Arguments):
    CardinalDirection = "minecraft:cardinal_direction" # North, South, East, West
    FacingDirection = "minecraft:facing_direction" # Up, Down, North, South, East, West


class PlacementPositionTrait(Arguments):
    BlockFace = "minecraft:block_face" # Up, Down, North, South, East, West
    VerticalHalf = "minecraft:vertical_half" # Top, Bottom


class CardinalDirectionsTrait(Arguments):
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class FacingDirectionsTrait(Arguments):
    Up = "up"
    Down = "down"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class BlockFacesTrait(Arguments):
    Up = "up"
    Down = "down"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class VerticalHalfTrait(Arguments):
    TOP = "top"
    BOTTOM = "bottom"


# Components
class BlockDestructibleByExplosion(_component):
    component_namespace = 'minecraft:destructible_by_explosion'
    def __init__(self, explosion_resistance: int) -> None:
        """Describes the destructible by explosion properties for this block.

        Args:
            explosion_resistance (int): The amount of resistance to explosions in a range of 0 to 100.
        """
        super().__init__('destructible_by_explosion')
        self._component_add_field('explosion_resistance', explosion_resistance)


class BlockDestructibleByMining(_component):
    component_namespace = 'minecraft:destructible_by_mining'
    def __init__(self, seconds_to_destroy: int) -> None:
        """Describes the destructible by mining properties for this block.

        Args:
            seconds_to_destroy (int): The amount of time it takes to destroy the block in seconds.
        """
        super().__init__('destructible_by_mining')
        self._component_add_field('seconds_to_destroy', seconds_to_destroy)


class BlockFlammable(_component):
    component_namespace = 'minecraft:flammable'
    def __init__(self, catch_chance_modifier: int, destroy_chance_modifier: int) -> None:
        """Describes the flammable properties for this block.

        Args:
            catch_chance_modifier (int): The chance that this block will catch fire in a range of 0 to 100.
            destroy_chance_modifier (int): The chance that this block will be destroyed when on fire in a range of 0 to 100.
        """
        super().__init__('flammable')
        self._component_add_field('catch_chance_modifier', catch_chance_modifier)
        self._component_add_field('destroy_chance_modifier', destroy_chance_modifier)


class BlockFriction(_component):
    component_namespace = 'minecraft:friction'
    def __init__(self, friction: float = 0.4) -> None:
        """Describes the friction for this block in a range of 0.0 to 0.9.

        Args:
            friction (float, optional): The friction of the block. Defaults to 0.4.
        """
        super().__init__('flammable')
        self._component_set_value(clamp(friction, 0, 0.9))


class BlockLightDampening(_component):
    component_namespace = 'minecraft:light_dampening'
    def __init__(self, light_dampening: int = 15) -> None:
        """The amount that light will be dampened when it passes through the block in a range of 0 to 15.

        Args:
            light_dampening (int, optional): The amount of light dampening. Defaults to 15.
        """
        super().__init__('light_dampening')
        self._component_set_value(clamp(light_dampening, 0, 15))


class BlockLightEmission(_component):
    component_namespace = 'minecraft:light_emission'
    def __init__(self, light_emission: int = 0) -> None:
        """The amount of light this block will emit in a range of 0 to 15.

        Args:
            light_emission (int, optional): The amount of light emission. Defaults to 0.
        """
        super().__init__('light_emission')
        self._component_set_value(clamp(light_emission, 0, 15))


class BlockLootTable(_component):
    component_namespace = 'minecraft:loot'
    def __init__(self, loot: str) -> None:
        """Specifies the path to the loot table.

        Args:
            loot (str): The path to the loot table.
        """
        super().__init__('loot')
        self._component_set_value(loot)


class BlockMapColor(_component):
    component_namespace = 'minecraft:map_color'
    def __init__(self, map_color: str) -> None:
        """Sets the color of the block when rendered to a map.

        Args:
            map_color (str): The color of the block when rendered to a map, must be a hexadecimal color value.
        """
        super().__init__('map_color')
        self._component_set_value(map_color)


class BlockMaterialInstance(_component):
    component_namespace = 'minecraft:material_instances'
    def __init__(self) -> None:
        """Maps face or material_instance names in a geometry file to an actual material instance."""
        super().__init__('material_instances')

    def add_instance(self, texture_name: str, block_face: BlockFaces = BlockFaces.All, render_method: BlockMaterial = BlockMaterial.Opaque, ambient_occlusion: bool = True, face_dimming: bool = True):
        """Maps face or material_instance names in a geometry file to an actual material instance.

        Args:
            texture_name (str): The name of the texture to use for this block.
            block_face (BlockFaces, optional): The face of the block to apply the texture to. Defaults to BlockFaces.All.
            render_method (BlockMaterial, optional): The render method to use for this block. Defaults to BlockMaterial.Opaque.
            ambient_occlusion (bool, optional): Whether or not to use ambient occlusion for this block. Defaults to True.
            face_dimming (bool, optional): Whether or not to use face dimming for this block. Defaults to True.

        """
        if FileExists(os.path.join('assets', 'textures', 'blocks', f'{texture_name}.png')):
            self[self.component_namespace].update({
                "*" if block_face == BlockFaces.All else block_face: {
                    'texture': f"{ANVIL.NAMESPACE}:{texture_name}",
                    'render_method': render_method.value if not render_method == BlockMaterial.Opaque else {},
                    'ambient_occlusion': ambient_occlusion if ambient_occlusion is False else {},
                    'face_dimming': face_dimming if face_dimming is False else {},
                }
            })
        else:
            ANVIL.Logger.file_exist_error(f'{texture_name}.png', os.path.join('assets', 'textures', 'blocks'))
        return self


class BlockGeometry(_component):
    component_namespace = 'minecraft:geometry'
    def __init__(self, geometry_name: str) -> None:
        """The description identifier of the geometry file to use to render this block.

        Args:
            geometry_name (str): The name of the geometry to use to render this block.
        """
        super().__init__('geometry')
        self._component_set_value(f'geometry.{ANVIL.NAMESPACE_FORMAT}.{geometry_name}')

    def bone_visibility(self, **bone: Dict[str, bool | str | Molang]):
        """Specifies the visibility of bones in the geometry file.

        Example:
            >>> BlockGeometry('block').bone_visibility(bone0=True, bone1=False)

        """
        self._component_add_field('bone_visibility', [
            {b:v for b, v in bone.items()}
        ])
        return self


class BlockCollisionBox(_component): 
    component_namespace = 'minecraft:collision_box'
    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that collides with entities.

        Args:
            size (coordinates): The size of the collision box.
            origin (coordinates): The origin of the collision box.
        """
        super().__init__('collision_box')
        if size == (0, 0, 0):
            self._component_set_value(False)
        else:
            self._component_add_field('size', size)
            self._component_add_field('origin', origin)


class BlockSelectionBox(_component): 
    component_namespace = 'minecraft:selection_box'
    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that is selected by the player's cursor.

        Args:
            size (coordinates): The size of the selection box.
            origin (coordinates): The origin of the selection box.
        """
        super().__init__('selection_box')
        if size == (0, 0, 0):
            self._component_set_value(False)
        else:
            self._component_add_field('size', size)
            self._component_add_field('origin', origin)


class BlockPlacementFilter(_component):
    component_namespace = 'minecraft:placement_filter'
    def __init__(self) -> None:
        """By default, custom blocks can be placed anywhere and do not have placement restrictions unless you specify them in this component."""
        super().__init__('placement_filter')
        self._component_add_field('conditions', [])

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
        self[self.component_namespace]['conditions'].append({
            "allowed_faces": allowed_faces,
            "block_filter": block_filter,
        })
        return self


class BlockTransformation(_component):
    component_namespace = 'minecraft:transformation'
    def __init__(self) -> None:
        """The block's transfomration.
        """
        super().__init__('transformation')
    
    def translation(self, translation: position):
        """The block's translation.

        Args:
            translation (position): The block's translation.
        """
        self._component_add_field('translation', translation)
        return self
    
    def scale(self, scale: position):
        """The block's scale.

        Args:
            scale (position): The block's scale.
        """
        self._component_add_field('scale', scale)
        return self
    
    def rotation(self, rotation: position):
        """The block's rotation.

        Args:
            rotation (position): The block's rotation.

        """
        self._component_add_field('rotation', rotation)
        return self


class BlockDisplayName(_component):
    component_namespace = 'minecraft:display_name'
    def __init__(self, display_name: str) -> None:
        """This component is specified as a Localization String. If this component is omitted, the default value for this component is the name of the block.

        Args:
            display_name (str): The display name of the block.
        """
        super().__init__('display_name')
        self._component_set_value(display_name)


class BlockCraftingTable(_component):
    component_namespace = 'minecraft:crafting_table'
    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes.

        Args:
            table_name (str): The name of the crafting table.

        Raises:
            IndexError: The crafting table tags cannot exceed 64 tags.
            ValueError: The crafting table tags are limited to 64 characters.
        """ 
        super().__init__('crafting_table')
        self._component_add_field('table_name', table_name)

        if len(crafting_tags) > 64:
            raise IndexError('Crafting Table tags cannot exceed 64 tags.')
        
        for tag in crafting_tags:
            if len(tag) > 64:
                raise ValueError('Crafting Table tags are limited to 64 characters.')

        self._component_add_field('crafting_tags', crafting_tags)

# Core
class _PermutationComponents(_Components):
    def __init__(self, condition: str | Molang):
        """The permutation components.

        Args:
            condition (str | Molang): The condition for the permutation.
        """
        super().__init__()
        self._component_group_name = 'components'
        self._components = {
            'condition': condition,
            self._component_group_name: {}
        }


class _BlockTraits():
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
            "enabled_states": [str(t) for t in traits],
            "y_rotation_offset": y_rotation_offset
        }

    def placement_position(self, *traits: PlacementPositionTrait):
        """Can add states containing information about the position of the block when it is placed.

        Args:
            traits (PlacementPositionTrait): The traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example
        """
        self._traits["minecraft:placement_position"] = {
            "enabled_states": traits
        }

    @property
    def export(self):
        return self._traits


class _BlockServerDescription(_MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block description.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._traits = _BlockTraits()
        self._description['description'].update({
            'states': {},
            "traits":{},
        })

    def add_state(self, name: str, *range: float | str |bool):
        """Adds a state to the block.

        Args:
            name (str): The name of the state.
            range (float | str |bool): Values this state can have.

        """
        self._description['description']['states'][f'{ANVIL.NAMESPACE}:{name}'] = range
        return self

    def menu_category(self, category: BlockCategory = BlockCategory.none, group: str = None):
        """Sets the menu category for the block.

        Args:
            category (BlockCategory, optional): The category of the block. Defaults to BlockCategory.none.
            group (str, optional): The group of the block. Defaults to None.

        """
        self._description['description']['menu_category'] = {
            'category': category.value if not category == BlockCategory.none else {},
            'group': group if not group is None else {},
        }
        return self

    @property
    def traits(self):
        """Sets the traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits
        """
        return self._traits
    
    @property
    def _export(self):
        self._description['description']['traits'] = self._traits.export
        return super()._export


class _BlockServer(AddonObject):
    """The block server object."""
    
    _extensions = {
        0: ".block.json", 
        1: ".block.json"
    }
    
    def _check_model(self, block_name):
        if FileExists(os.path.join('assets', 'models', 'blocks', f'{block_name}.geo.json')):
            geo_namespace = f'geometry.{ANVIL.NAMESPACE_FORMAT}.{block_name}'
            with open(os.path.join('assets', 'models', 'blocks', f'{block_name}.geo.json')) as file:
                data = file.read()
                if geo_namespace not in data:
                    ANVIL.Logger.namespace_not_in_geo(block_name, geo_namespace)

        else:
            ANVIL.Logger.file_exist_error(f'{block_name}.geo.json', os.path.join('assets', 'models', 'blocks'))
    
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block server object.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name, os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "blocks"))
        self._server_block = _JsonSchemes.server_block()
        self._description = _BlockServerDescription(name, is_vanilla)
        self._components = _Components()
        self._permutations : list[_PermutationComponents] = []

    @property
    def description(self):
        """The block description."""
        return self._description

    @property
    def components(self):
        """The block components.
        """
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
        """Queues the block to be exported.
        """
        self._server_block['minecraft:block'].update(self.description._export)
        self._server_block['minecraft:block']['components'].update(self._components._export()['components'])
        comps = self._server_block['minecraft:block']['components']
        self._server_block['minecraft:block']['permutations'] = [permutation._export() for permutation in self._permutations]

        target_models = []
        target_textures = []

        if not BlockMaterialInstance.component_namespace in comps:
            ANVIL.Logger.block_missing_texture(self._name)
        else:
            for i, m in comps[BlockMaterialInstance.component_namespace].items():
                target_textures.append(m['texture'].removeprefix(f"{ANVIL.NAMESPACE}:"))

        if not BlockGeometry.component_namespace in comps:
            ANVIL.Logger.block_missing_geometry(self._name)
        else:
            target_models.append(self._server_block['minecraft:block']['components'][BlockGeometry.component_namespace].split('.')[-1])

        for p in self._server_block['minecraft:block']['permutations']:
            if BlockGeometry.component_namespace in p['components']:
                target_models.append(p['components'][BlockGeometry.component_namespace].split('.')[-1])
            if BlockMaterialInstance.component_namespace in p['components']:
                for i, m in p['components'][BlockMaterialInstance.component_namespace].items():
                    target_textures.append(m['texture'])
        
        for model in target_models:
            self._check_model(model)
            CopyFiles(
                os.path.join('assets', 'models', 'blocks'),
                os.path.join('resource_packs',f'RP_{ANVIL.PASCAL_PROJECT_NAME}', 'models', 'blocks'),
                f'{model}.geo.json'
            ) 
        
        for texture in target_textures:
            ANVIL._terrain_texture.add_block(texture, '', texture)


        self.content(self._server_block)
        super().queue()


class Block():
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block object.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        self._name = name
        self._is_vanilla = is_vanilla
        self._server = _BlockServer(name, is_vanilla)

        self._namespace_format = ANVIL.NAMESPACE_FORMAT
        if self._is_vanilla:
            self._namespace_format = 'minecraft'

    @property
    def Server(self):
        """The block server object.
        """
        return self._server

    @property
    def identifier(self):
        """The block identifier.
        """
        return f'{self._namespace_format}:{self._name}'

    @property
    def name(self):
        return self._name
    
    @property
    def queue(self):
        """Queues the block to be exported."""

        if not "minecraft:display_name" in self.Server._server_block["minecraft:block"]["components"]:
            display_name = self._name.replace("_", " ").title()
        elif self.Server._server_block["minecraft:block"]["components"]["minecraft:display_name"].startswith("tile."):
            display_name = ANVIL._langs[self.Server._server_block["minecraft:block"]["components"]["minecraft:display_name"]]
        else:
            display_name = self.Server._server_block["minecraft:block"]["components"]["minecraft:display_name"]

        ANVIL._report.add_report(
            ReportType.BLOCK, 
            vanilla = self._is_vanilla, 
            col0 = display_name, 
            col1 = self.identifier,
            col2 = [
                f"{key}: {[', '.join(value)]}"
                for key, value in self.Server.description._description["description"]["states"].items()
            ]
        )

        self.Server.queue

#  TODO: Integrate with the Block class

class VanillaBlockTexture(_MinecraftDescription):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, True)
        self._identifier = identifier

    @property
    def update_texture(self):
        self._ext = ''
        if FileExists(os.path.join('assets', 'textures', 'blocks', f'{self._identifier}.png')):
            self._ext = 'png'
        if FileExists(os.path.join('assets', 'textures', 'blocks', f'{self._identifier}.tga')):
            self._ext = 'tga'

        return self

    def queue(self, directory: str = ""):
        CopyFiles(
            os.path.join('assets', 'textures', 'blocks'),
            os.path.join('resource_packs', f'RP_{ANVIL.PASCAL_PROJECT_NAME}', 'textures', 'blocks', directory),
            f'{self._identifier}.{self._ext}'
        )
