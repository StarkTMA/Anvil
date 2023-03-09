from ..core import (ANVIL, NAMESPACE, NAMESPACE_FORMAT, PASCAL_PROJECT_NAME,
                    Exporter, _MinecraftDescription)
from ..packages import *
from .actors import _Components
from .components import _component

__all__ = ['Block', 'VanillaBlockTexture',
           'BlockDestructibleByExplosion', 'BlockDestructibleByMining', 
           'BlockFlammable', 'BlockFriction', 'BlockLightDampening', 'BlockLightEmission',
           'BlockLootTable', 'BlockMapColor', 'BlockMaterialInstance', 'BlockGeometry', 'BlockCollisionBox',
           'BlockCraftingTable', 'BlockPlacementFilter'
           ]

# Experimental
class _BlockRotation(_component):
    def __init__(self, rotation: rotation) -> None:
        super().__init__('rotation')
        self.SetValue(rotation)


class _BlockDisplayName(_component):
    def __init__(self, display_name: str) -> None:
        """Describes the destructible by mining properties for this block."""
        super().__init__('display_name')
        self.SetValue(display_name)

class _BlockTransformation(_component):
    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """The block's transfomration."""
        super().__init__('transformation')
    
    def translation(self, translation: position):
        self.AddField('translation', translation)
        return self
    
    def scale(self, scale: position):
        self.AddField('scale', scale)
        return self
    
    def rotation(self, rotation: rotation):
        self.AddField('rotation', rotation)
        return self

# Released

class BlockDestructibleByExplosion(_component):
    def __init__(self, explosion_resistance: int) -> None:
        """Describes the destructible by explosion properties for this block."""
        super().__init__('destructible_by_explosion')
        self.AddField('explosion_resistance', explosion_resistance)


class BlockDestructibleByMining(_component):
    def __init__(self, seconds_to_destroy: int) -> None:
        """Describes the destructible by mining properties for this block."""
        super().__init__('destructible_by_mining')
        self.AddField('seconds_to_destroy', seconds_to_destroy)


class BlockFlammable(_component):
    def __init__(self, catch_chance_modifier: int, destroy_chance_modifier: int) -> None:
        """Describes the flammable properties for this block."""
        super().__init__('flammable')
        self.AddField('catch_chance_modifier', catch_chance_modifier)
        self.AddField('destroy_chance_modifier', destroy_chance_modifier)


class BlockFriction(_component):
    def __init__(self, friction: float = 0.4) -> None:
        """Describes the friction for this block in a range of 0.0 to 0.9."""
        super().__init__('flammable')
        self.SetValue(clamp(friction, 0, 0.9))


class BlockLightDampening(_component):
    def __init__(self, light_dampening: int = 15) -> None:
        """The amount that light will be dampened when it passes through the block in a range (0-15)."""
        super().__init__('light_dampening')
        self.SetValue(clamp(light_dampening, 0, 15))


class BlockLightEmission(_component):
    def __init__(self, light_emission: int = 0) -> None:
        """The amount of light this block will emit in a range (0-15)."""
        super().__init__('light_emission')
        self.SetValue(clamp(light_emission, 0, 15))


class BlockLootTable(_component):
    def __init__(self, loot: str) -> None:
        """Specifies the path to the loot table."""
        super().__init__('loot')
        self.SetValue(loot)


class BlockMapColor(_component):
    def __init__(self, map_color: str) -> None:
        """Sets the color of the block when rendered to a map."""
        super().__init__('map_color')
        self.SetValue(map_color)


class BlockMaterialInstance(_component):
    """Maps face or material_instance names in a geometry file to an actual material instance."""

    def __init__(self) -> None:
        super().__init__('material_instances')

    def add_instance(self, texture_name: str, block_face: str = '*', render_method: BlockMaterial = BlockMaterial.Opaque, ambient_occlusion: bool = True, face_dimming: bool = True):
        CheckAvailability(f'{texture_name}.png', 'texture',
                          MakePath('assets', 'textures', 'blocks'))
        self[self._component_namespace].update({
            block_face: {
                'texture': texture_name,
                'render_method': render_method if not render_method == BlockMaterial.Opaque else {},
                'ambient_occlusion': ambient_occlusion if ambient_occlusion is False else {},
                'face_dimming': face_dimming if face_dimming is False else {},
            }
        })
        return self


class BlockGeometry(_component):
    def __init__(self, geometry_name) -> None:
        """The description identifier of the geometry file to use to render this block."""
        super().__init__('geometry')
        self.SetValue(f'geometry.{NAMESPACE_FORMAT}.{geometry_name}')


class BlockCollisionBox(_component): 
    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that collides with entities."""
        super().__init__('collision_box')
        if size == (0, 0, 0):
            self.SetValue(False)
        else:
            self.AddField('size', size)
            self.AddField('origin', origin)


class BlockSelectionBox(_component): 
    def __init__(self, size: coordinates, origin: coordinates) -> None:
        """Defines the area of the block that is selected by the player's cursor."""
        super().__init__('selection_box')
        if size == (0, 0, 0):
            self.SetValue(False)
        else:
            self.AddField('size', size)
            self.AddField('origin', origin)


class BlockCraftingTable(_component):
    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """Makes your block into a custom crafting table."""
        super().__init__('transformation')
        self.AddField('table_name', table_name)
        self.AddField('crafting_tags', crafting_tags)


class BlockPlacementFilter(_component):
    """By default, custom blocks can be placed anywhere and do not have placement restrictions unless you specify them in this component."""

    def __init__(self) -> None:
        super().__init__('placement_filter')
        self.AddField('conditions', [])

    def add_condition(self, allowed_faces: list[BlockFaces], block_filter: list[Union[BlockDescriptor, str]]):
        if BlockFaces.Side in allowed_faces:
            allowed_faces.remove(BlockFaces.North)
            allowed_faces.remove(BlockFaces.South)
            allowed_faces.remove(BlockFaces.East)
            allowed_faces.remove(BlockFaces.West)
        if BlockFaces.All in allowed_faces:
            allowed_faces = [BlockFaces.All]
        self[self._component_namespace]['conditions'].append({
            "allowed_faces": allowed_faces,
            "block_filter": block_filter,
        })
        return self

#Blocks
class _PermutationComponents(_Components):
    def __init__(self, condition):
        super().__init__()
        self._component_group_name = 'components'
        self._components = {
            'condition': condition,
            self._component_group_name: {}
        }


class _BlockServerDescription(_MinecraftDescription):
    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier, is_vanilla)
        self._description['description'].update({
            'properties': {},
        })

    def add_property(self, name, range: tuple[float, float]):
        self._description['description']['properties'][f'{NAMESPACE}:{name}'] = range
        return self

    def menu_category(self, category: BlockCategory = BlockCategory.none, group: str = None):
        self._description['description']['menu_category'] = {
            'category': category if not category is None else {},
            'group': group if not group is None else {},
        }
        return self

    @property
    def _export(self):
        return super()._export


class _BlockServer(Exporter):
    def _check_model(self, block_name):
        CheckAvailability(f'{block_name}.geo.json', 'geometry',
                          MakePath('assets', 'models', 'blocks'))
        geo_namespace = f'geometry.{NAMESPACE_FORMAT}.{block_name}'
        with open(MakePath('assets', 'models', 'blocks', f'{block_name}.geo.json')) as file:
            data = file.read()
            if geo_namespace not in data:
                RaiseError(
                    f'The geometry file {block_name}.geo.json doesn\'t contain a geometry called {geo_namespace}')

    def __init__(self, identifier: str, is_vanilla: bool) -> None:
        super().__init__(identifier, 'server_block')
        self._identifier = identifier
        self._server_block = Schemes('server_block')
        self._description = _BlockServerDescription(identifier, is_vanilla)
        self._components = _Components()
        self._permutations : list[_PermutationComponents] = []

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    def permutation(self, condition: str):
        self._permutation = _PermutationComponents(condition)
        self._permutations.append(self._permutation)
        return self._permutation

    @property
    def queue(self):
        self._server_block['minecraft:block'].update(self.description._export)
        self._server_block['minecraft:block']['components'].update(self._components._export()['components'])
        comps = self._server_block['minecraft:block']['components']
        self._server_block['minecraft:block']['permutations'] = [permutation._export() for permutation in self._permutations]

            

        if 'minecraft:geometry' in comps:
            target_model = self._server_block['minecraft:block']['components']['minecraft:geometry'].split('.')[-1]
            self._check_model(target_model)
            CopyFiles(
                MakePath('assets', 'models', 'blocks'),
                MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}', 'models', 'blocks'),
                f'{target_model}.geo.json'
            )
        
        for p in self._server_block['minecraft:block']['permutations']:
            if 'minecraft:geometry' in p['components']:
                target_model = p['components']['minecraft:geometry'].split('.')[-1]
                self._check_model(target_model)
                CopyFiles(
                    MakePath('assets', 'models', 'blocks'),
                    MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}', 'models', 'blocks'),
                    f'{target_model}.geo.json'
                )
        
        if not 'minecraft:material_instances' in comps:
            RaiseError(MISSING_TEXTURE(f"{NAMESPACE}:{self._identifier}"))


        for i, m in comps['minecraft:material_instances'].items():
            try:
                CopyFiles(MakePath('assets', 'textures', 'blocks'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'blocks'), f'{m["texture"]}.png')
            except:
                CopyFiles(MakePath('assets', 'textures', 'blocks'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'blocks'), f'{m["texture"]}.tga')
            ANVIL._terrain_texture.add_block(m['texture'], '', m['texture'])

        self.content(self._server_block)
        super().queue()


class _BlockClient():
    def __init__(self, identifier, is_vanilla) -> None:
        pass


class Block():
    def _validate_name(self, identifier):
        if ':' in identifier:
            raise ValueError(NAMESPACES_NOT_ALLOWED(identifier))

    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._validate_name(identifier)

        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._server = _BlockServer(identifier, is_vanilla)
        self._client = _BlockClient(identifier, is_vanilla)

        self._namespace_format = NAMESPACE_FORMAT
        if self._is_vanilla:
            self._namespace_format = 'minecraft'

    @property
    def Server(self):
        return self._server

    @property
    def Client(self):
        return self._client

    @property
    def identifier(self):
        return f'{self._namespace_format}:{self._identifier}'

    @property
    def queue(self):
        display_name = RawText(self._identifier)[1]
        ANVIL.localize(
            f'tile.{self._namespace_format}:{self._identifier}.name={display_name}')
        ANVIL._blocks.update({f'{self._namespace_format}:{self._identifier}': {
                             "Display Name": display_name}})
        self.Server.queue

#  TODO: Integrate with the Block class

class VanillaBlockTexture(_MinecraftDescription):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, True)
        self._identifier = identifier

    @property
    def update_texture(self):
        self._ext = ''
        try:
            CheckAvailability(f'{self._identifier}.png', 'texture', MakePath(
                'assets', 'textures', 'blocks'))
            self._ext = 'png'
        except:
            CheckAvailability(f'{self._identifier}.tga', 'texture', MakePath(
                'assets', 'textures', 'blocks'))
            self._ext = 'tga'

        return self

    def queue(self, directory: str = None):
        CopyFiles(
            MakePath('assets', 'textures', 'blocks'),
            MakePath(
                'resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'blocks', directory),
            f'{self._identifier}.{self._ext}'
        )
