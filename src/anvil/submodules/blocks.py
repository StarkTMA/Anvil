from ..packages import *
from ..core import NAMESPACE, NAMESPACE_FORMAT, PASCAL_PROJECT_NAME, ANVIL, Exporter, _MinecraftDescription
from .actors import _Properties, _Components
from .components import _component

# Experimental 
class _BlockCollisionBox(_component):
    def __init__(self, size: coordinates, origin : coordinates) -> None:
        """Sets the size of the Block's collision box."""
        super().__init__('collision_box')
        self.AddField('size', size)
        self.AddField('origin', origin)

class _BlockSelectionBox(_component):
    def __init__(self, size: coordinates, origin : coordinates) -> None:
        """Defines the area of the block that is selected by the player's cursor."""
        super().__init__('selection_box')
        self.AddField('size', size)
        self.AddField('origin', origin)

class _BlockRotation(_component):
    def __init__(self, rotation: rotation) -> None:
        """The block's rotation around the center of the cube in degrees."""
        super().__init__('rotation')
        self.SetValue(rotation)

class _BlockDisplayName(_component):
    def __init__(self, display_name: str) -> None:
        """Describes the destructible by mining properties for this block."""
        super().__init__('display_name')
        self.SetValue(display_name)

class _BlockCraftingTable(_component):
    def __init__(self, table_name: str, *crafting_tags: str) -> None:
        """Makes your block into a custom crafting table."""
        super().__init__('collision_box')
        self.AddField('table_name', table_name)
        self.AddField('crafting_tags', crafting_tags)

# Probably removed
class _BlockPartVisibility(_component):
    def __init__(self) -> None:
        """Sets conditions for when the block's different parts are visible."""
        super().__init__('part_visibility')

    def add_condition(self, bone_name: str, condition: Molang | bool):
        self[self._component_namespace].update({
            bone_name: condition
        })
        return self

class _BlockUnitCube(_component):
    def __init__(self) -> None:
        """Specifies that a unit cube is to be used with tessellation."""
        super().__init__('unit_cube')
        self.SetValue(True)

class _BlockDummyGeo(_component):
    def __init__(self) -> None:
        """The description identifier of the geometry file to use to render this block."""
        super().__init__('geometry')
        File('dummy.geo.json', Schemes('geometry', NAMESPACE_FORMAT, 'dummy_block', {"name": "dummy","pivot": [0, 0, 0],"cubes": [{"origin": [-8, 0, -8], "size": [16, 16, 16], "uv": [0, 0]}]}), MakePath('assets', 'models', 'blocks'), 'w')
        CreateImage('dummy', 8, 8, (0, 0, 0, 0), MakePath('assets', 'textures', 'blocks'))
        self.SetValue(f'geometry.{NAMESPACE_FORMAT}.dummy_block')

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

class BlockLighEmission(_component):
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
        CheckAvailability(f'{texture_name}.png', 'texture', MakePath('assets', 'textures', 'blocks'))
        self[self._component_namespace].update({
            block_face: {
                'texture': texture_name,
                'render_method': render_method if not render_method == BlockMaterial.Opaque else {},
                'ambient_occlusion': ambient_occlusion if ambient_occlusion is False else {},
                'face_dimming': face_dimming if face_dimming is False else {},
            }
        })
        return self

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
            'category' : category if not category is None else {},
            'group': group if not group is None else {},
        }
        return self

    @property
    def _export(self):
        return super()._export

class _BlockServer(Exporter):
    def _check_model(self, block_name):
        CheckAvailability(f'{block_name}.geo.json', 'geometry', MakePath('assets','models','blocks'))
        geo_namespace = f'geometry.{NAMESPACE_FORMAT}.{block_name}'
        with open(MakePath('assets','models','blocks', f'{block_name}.geo.json')) as file:
            data = file.read()
            if geo_namespace not in data:
                RaiseError(f'The geometry file {block_name}.geo.json doesn\'t contain a geometry called {geo_namespace}')

    def __init__(self, identifier: str, is_vanilla: bool) -> None:
        super().__init__(identifier, 'server_block')
        self._identifier = identifier
        self._server_block = Schemes('server_block')
        self._description = _BlockServerDescription(identifier, is_vanilla)
        self._components = _Components()

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    @property
    def queue(self):
        self._server_block['minecraft:block'].update(self.description._export)
        self._server_block['minecraft:block']['components'].update(self._components._export()['components'])
        comps = self._server_block['minecraft:block']['components']

        if not any(['minecraft:unit_cube', 'minecraft:geometry']) in comps:
            self._check_model(self._identifier)
            self._server_block['minecraft:block']['components'].update({'minecraft:geometry': f'geometry.{NAMESPACE}.{self._identifier}'})
            CopyFiles(
                MakePath('assets', 'models', 'blocks'), 
                MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'models', 'blocks'), 
                f'{self._identifier}.geo.json'
            )

        if not 'minecraft:material_instances' in comps:
            RaiseError(MISSING_TEXTURE(f"{NAMESPACE}:{self._identifier}"))
        
        textures = []
        for m in comps['minecraft:material_instances'].values():
            try:
                CopyFiles(MakePath('assets','textures', 'blocks'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures', 'blocks'), f'{m["texture"]}.png')
            except:
                CopyFiles(MakePath('assets','textures', 'blocks'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures', 'blocks'), f'{m["texture"]}.tga')
            textures.append(m['texture'])

        ANVIL._terrain_texture.add_block(self._identifier, '', *textures)
        
        self.content(self._server_block)                              
        super().queue()

class _BlockClient():
    def __init__(self, identifier, is_vanilla) -> None:
        pass
    
    def add_sound(self):
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
        ANVIL.localize(f'tile.{self._namespace_format}:{self._identifier}.name={display_name}')
        ANVIL._blocks.update({f'{self._namespace_format}:{self._identifier}': {"Display Name": display_name}})
        self.Server.queue