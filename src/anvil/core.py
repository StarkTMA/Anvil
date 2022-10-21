from .packages import *
from .submodules import components

# Rework
# File System Exporter for the rework
class Exporter():
    def __init__(self, name: str, type: str) -> None:
        self._valids = {
            'function': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'functions', 'NAMESPACE'),
                'extension':{
                    0: '.mcfunction',
                    1: '.mcfunction',
                }
            },
            'server_entity': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'entities'),
                'extension':{
                    0: '.behavior.json',
                    1: '.behavior.json'
                }
            },
            'client_entity': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'entity'),
                'extension':{
                    0: '.entity.json',
                    1: '.entity.json'
                }
            },
            'dialogue': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'dialogue'),
                'extension':{
                    0: '.dialogue.json',
                    1: '.dialogue.json'
                }
            },
            'bp_item_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'items'),
                'extension':{
                    0: '.bp_item.json',
                    1: '.bp_item.json'
                }
            },
            'bp_block_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'blocks'),
                'extension':{
                    0: '.block.json',
                    1: '.block.json'
                }
            },
            'loot_table': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'loot_tables'),
                'extension':{
                    0: '.loot_table.json',
                    1: '.loot_table.json'
                }
            },
            'bp_animation_controllers': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animation_controllers'),
                'extension':{
                    0: '.bp_ac.json',
                    1: '.animation_controller.json'
                }
            },
            'bp_animations': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animations'),
                'extension':{
                    0: '.bp_anim.json',
                    1: '.animation.json'
                }
            },
            'spawn_rules': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'spawn_rules'),
                'extension':{
                    0: '.spawn_rule.json',
                    1: '.spawn_rules.json'
                }
            },
            'recipe': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'recipe'),
                'extension':{
                    0: '.recipe.json',
                    1: '.recipe.json'
                }
            },
            'language': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'texts'),
                'extension':{
                    0: '.lang',
                    1: '.lang'
                }
            },
            'rp_item_v1': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'items'),
                'extension':{
                    0: '.rp_item.json',
                    1: '.rp_item.json'
                }
            },
            'rp_animation_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animation_controllers'),
                'extension':{
                    0: '.rp_ac.json',
                    1: '.animation_controller.json'
                }
            },
            'render_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'render_controllers'),
                'extension':{
                    0: '.render.json',
                    1: '.render_controller.json'
                }
            },
            'rp_animation': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animations'),
                'extension':{
                    0: '.rp_anim.json',
                    1: '.animation.json'
                }
            },
            'attachable': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'attachables'),
                'extension':{
                    0: '.attachable.json',
                    1: '.attachable.json'
                }
            },
            'particle': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'particles'),
                'extension':{
                    0: '.particle.json',
                    1: '.particle.json'
                }
            },
            'assets': {
                'path': MakePath('assets'),
            },
            'ui': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'ui'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'uivars': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'ui'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'item_texture': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'terrain_textures': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'flipbook_textures': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'sound_definitions': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'music_definitions': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            },
            'blocks': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}'),
                'extension':{
                    0: '.json',
                    1: '.json'
                }
            }
        }
        self._name = name
        self._type = type
        self._shorten = True
        self._content = {}
        self._directory = ''
        if self._type not in self._valids:
            raise TypeError(ANVIL_TYPE_ERROR(self._type))

    @property
    def do_not_shorten(self):
        self._shorten = False

    def content(self, content):
        self._content = content
        return self

    def queue(self, directory: str = None):
        # Console Output
        self._directory = directory
        self._path = MakePath(self._valids[self._type]['path'], self._directory)
        ANVIL._queue(self)
        return self

    def _export(self):
        if self._shorten and type(self._content) is dict:
            self._content = ShortenDict(self._content)
        File(f'{self._name}{self._valids[self._type]["extension"][NAMESPACE_FORMAT_BIT]}', self._content, self._path, 'w')

# General
class _MinecraftDescription():
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._identifier = identifier
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._description : dict = Schemes('description', self._namespace_format, self._identifier)

    @property
    def _export(self):
        return self._description

class _ItemTextures(Exporter):
    def __init__(self) -> None:
        super().__init__('item_texture', 'item_texture')
        self.content(Schemes('item_texture', PROJECT_NAME))

    def add_item(self, item_name: str, directory, *item_sprites: str):
        for item in item_sprites:
            CheckAvailability(f'{item}.png', 'sprite', MakePath('assets', 'textures', 'items'))
        self._content['texture_data'][item_name]=[
            *[
                MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'items', directory, f'{sprite}.png') 
                for sprite in item_sprites
            ]
        ]

    @property
    def queue(self):
        return super().queue('')
    
    def _export(self):
        if len(self._content['texture_data']) > 0:
            for items in self._content['texture_data'].values():
                for sprite in items:
                    CopyFiles(MakePath('assets', 'textures', 'items'), sprite.rstrip(sprite.split('/')[-1]), sprite.split('/')[-1])
        return super()._export()

class _TerrainTextures(Exporter):
    def __init__(self) -> None:
        super().__init__('terrain_textures', 'terrain_textures')
        self.content(Schemes('terrain_textures', PROJECT_NAME))

    def add_block(self, block_name: str, directory, *block_textures: str):
        for block in block_textures:
            CheckAvailability(f'{block}.png', 'sprite', MakePath('assets', 'textures', 'blocks'))
        self._content['texture_data'][block_name]=[
            *[
                MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'blocks', directory, f'{face}.png') 
                for face in block_textures
            ]
        ]

    @property
    def queue(self):
        return super().queue('')
    
    def _export(self):
        if len(self._content['texture_data']) > 0:
            for blocks in self._content['texture_data'].values():
                for block in blocks:
                    CopyFiles(MakePath('assets', 'textures', 'blocks'), block.rstrip(block.split('/')[-1]), block.split('/')[-1])
        return super()._export()

class _Blocks(Exporter):
    def __init__(self) -> None:
        super().__init__('blocks', 'blocks')
        self.content(Schemes('blocks', PROJECT_NAME))

    def add_block(self, block_name: str, *block_textures: str):
        for block in block_textures:
            CheckAvailability(f'{block}.png', 'sprite', MakePath('assets', 'textures', 'blocks'))
        self._content['texture_data'][block_name]={
            "sound": "",
            "textures":{},
            "carried_textures":{},
            "brightness_gamma": 0,
            "isotropic":True
        }

class _SoundDefinition():
    def __init__(self, sound_definition: str, category, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999) -> None:
        self._category = category
        if category not in SoundCategory.list:
            RaiseError(SOUND_CATEGORY_ERROR)
        self._sound_definition = sound_definition
        self._sound = Schemes('sound', self._sound_definition, category)
        
        if use_legacy_max_distance != False:
            self._sound[self._sound_definition].update({'__use_legacy_max_distance': use_legacy_max_distance})
        if max_distance != 0:
            self._sound[self._sound_definition].update({'max_distance': max_distance})
        if min_distance != 9999:
            self._sound[self._sound_definition].update({'min_distance': min_distance})
        self._sounds = []

    def add_sound(self, sound_name, volume: int = 1, weight: int = 1, pitch: int = [1, 1], is_3d: bool = False, stream: bool = False, load_on_low_memory: bool = False):
        CheckAvailability(f'{sound_name}.ogg', 'audio', 'assets/sounds')
        self._sound_name = sound_name
        splits = self._sound_definition.split(".")
        self._path = ''
        for i in range(len(splits)-1):
            self._path += f'{splits[i]}/'
        sound = {
            "name": MakePath('sounds', self._path, self._sound_name),
            "weight": weight
        }
        if pitch != [1, 1]:
            sound.update({"pitch": pitch})
        if is_3d != False:
            sound.update({"is3D": is_3d})
        if stream != False:
            sound.update({"stream": stream})
        if load_on_low_memory != False:
            sound.update({"load_on_low_memory": load_on_low_memory})
        if volume != 1:
            sound.update({"volume": volume})
        self._sounds.append(sound)
        ANVIL._sounds.update({ self._sound_name: self._sound_definition})
        return self

    @property
    def _export(self):
        for sound in self._sounds:
            CopyFiles('assets/sounds', MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds', self._path), f'{sound["name"].split("/")[-1]}.ogg')
        self._sound[self._sound_definition]['sounds'] = self._sounds
        return self._sound

class _Sound(Exporter):
    def __init__(self) -> None:
        super().__init__('sound_definitions', 'sound_definitions')
        self.content(Schemes('sound_definitions'))
        self._sounds : list[_SoundDefinition] = []
    
    def sound_definition(self, sound_definition: str, category: SoundCategory(), use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
        sound = _SoundDefinition(sound_definition,category,use_legacy_max_distance,max_distance,min_distance)
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        return super().queue('')
    
    def _export(self):
        for sound in self._sounds:
            self._content['sound_definitions'].update(sound._export)
        return super()._export()

class _Music(Exporter):
    def __init__(self) -> None:
        super().__init__('music_definitions', 'music_definitions')
        self.content(Schemes('music_definitions'))
        self._sounds : list[_SoundDefinition] = []
    
    def music_definition(self, music_category: MusicCategory(), min_delay: int = 60, max_delay: int = 180):
        if music_category not in MusicCategory.list:
            RaiseError(MUSIC_CATEGORY_ERROR)
            
        self._content.update({
            music_category : {
               "event_name" : f"music.{music_category}",
               "max_delay" : max_delay,
               "min_delay" : min_delay
            }
        })
        sound = ANVIL.sound(f"music.{music_category}", 'music')
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        return super().queue('')
    
    def _export(self):
        return super()._export()

class NewBlock(_MinecraftDescription):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, is_vanilla)
        self._identifier = identifier
    
    @property
    def update_texture(self):
        self._ext = ''
        try:
            CheckAvailability(f'{self._identifier}.png', 'texture', MakePath('assets', 'textures', 'blocks'))
            self._ext = 'png'
        except:
            CheckAvailability(f'{self._identifier}.tga', 'texture', MakePath('assets', 'textures', 'blocks'))
            self._ext = 'tga'

        return self
    
    @property
    def queue(self):
        CopyFiles(
            MakePath('assets', 'textures', 'blocks'),
            MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'blocks'),
            f'{self._identifier}.{self._ext}'
        )

class SkinPack():
    def __init__(self) -> None:
        self._skins = []

    def add_skin(self, filename:str, display_name: str, is_slim:bool = False, free: bool = False):
        self._skins.append({
            "localization_name": filename,
            "geometry": f"geometry.humanoid.{ 'customSlim' if is_slim else 'custom'}",
            "texture": f"{filename}.png",
            "type": "free" if free else "paid"
        })
        ANVIL._skins_langs.append(f'skin.{PROJECT_NAME}.{filename}={display_name}\n')

    def queue(self):
        ANVIL._queue(self)
    
    def _export(self):
        CreateDirectory('assets/skin_pack/texts')
        File('languages.json', Defaults('languages'), 'assets/skin_pack/texts', 'w')
        if FileExists('assets/skin_pack/manifest.json') is False:
            File("manifest.json", Schemes('manifest_skins', PROJECT_NAME),"assets/skin_pack", "w")
        File('en_US.lang', Schemes('skin_language', PROJECT_NAME, DISPLAY_NAME+ ' Skin Pack') + ''.join(ANVIL._skins_langs),'assets/skin_pack/texts', 'w')
        File('skins.json', Schemes('skins', PROJECT_NAME, self._skins), 'assets/skin_pack', 'w')




# Core Functionalities
class EngineComponent():
    def __init__(self, name: str, engine_component: str, file_type: str):
        self._valid_bp = [
            'function',
            'behavior',
            'dialogue',
            'bp_item_v1',
            'bp_block_v1',
            'loot_table',
            'bp_animation_controller',
            'bp_animation',
            'spawn_rule',
            'recipe'
        ]
        self._valid_rp = [
            'language',
            'client_entity',
            'rp_item_v1',
            'rp_animation_controller',
            'render_controller',
            'rp_animation',
            'attachable',
            'particle'
        ]
        if engine_component in self._valid_bp:
            self._path = f'behavior_packs/BP_{PASCAL_PROJECT_NAME}'
        elif engine_component in self._valid_rp:
            self._path = f'resource_packs/RP_{PASCAL_PROJECT_NAME}'
        elif engine_component == 'asset':
            self._path = f'assets'
        else:
            RaiseError('Component type must be one of %r.' %[self._valid_bp+self._valid_rp])
        self._name = name
        self._engine_component = engine_component
        self._file_type = file_type
        self._directory = ''
        self._export_mode = 'w'

    def content(self, content):
        self._content = content
        return self

    def queue(self, directory: str = ''):
        # Console Output
        self._directory = directory
        match self._engine_component:
            case 'recipe':
                self._path += f'/recipes'
            case 'function':
                self._path += MakePath('/functions',PROJECT_NAME,self._directory)
            case 'behavior':
                self._path += f'/entities/{self._directory}'
            case 'dialogue':
                self._path += f'/dialogue/{self._directory}'
            case 'bp_item_v1':
                self._path += f'/items/{self._directory}'
            case 'rp_item_v1':
                self._path += f'/items/{self._directory}'
            case 'bp_block_v1':
                self._path += f'/blocks/{self._directory}'
            case 'loot_table':
                self._path += f'/loot_tables/{self._directory}'
            case 'bp_animation_controller':
                self._path += f'/animation_controllers/{self._directory}'
            case 'bp_animation':
                self._path += f'/animations/{self._directory}'
            case 'rp_animation_controller':
                self._path += f'/animation_controllers/{self._directory}'
            case 'client_entity':
                self._path += f'/entity/{self._directory}'
            case 'render_controller':
                self._path += f'/render_controllers/{self._directory}'
            case 'spawn_rule':
                self._path += f'/spawn_rules/{self._directory}'
            case 'attachable':
                self._path += f'/attachables/{self._directory}'
            case 'asset':
                self._path += f'/{self._directory}'
            case 'particle':
                self._path += f'/particles'

        CreateDirectory(self._path)
        ANVIL._queue(self)
        return self

    def _export(self):
        File(f'{self._name}{self._file_type}', self._content, self._path, self._export_mode)
class Recipe(EngineComponent):
    class _Crafting():
        class _Shapeless():
            def __init__(self, parent, identifier, output_item_id: str, data: int = 0, count: int = 1):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 9
                self._ingredients = []
                self._default = Defaults(
                    'recipe_shapeless', self._identifier, output_item_id, data, count)

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    RaiseError(
                        f'The recipe {self._parent._name} has more than 9 items')
                if item_id not in [item['item'] for item in self._ingredients]:
                    self._ingredients.append(
                        {'item': item_id, 'data': data, 'count': count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default['minecraft:recipe_shapeless']['ingredients'] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _Shaped():
            def __init__(self, parent, identifier, output_item_id, data, count, recipe_exactly):
                self._parent = parent
                self._identifier = identifier
                self._recipe_exactly = recipe_exactly
                self._keys = string.ascii_letters
                self._items = {}
                self._pattern = [
                    '   ',
                    '   ',
                    '   '
                ]
                self._key = {}
                self._default = Defaults(
                    'recipe_shaped', self._identifier, output_item_id, data, count)
                self._grid = [[' ' for i in range(3)] for j in range(3)]

            def item_0_0(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[0][0] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_0_1(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[0][1] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_0_2(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[0][2] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_1_0(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[1][0] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_1_1(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[1][1] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_1_2(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[1][2] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_2_0(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[2][0] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_2_1(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[2][1] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def item_2_2(self, item_identifier: str = ' ', data: int = 0, count: int = 1):
                self._grid[2][2] = {'item': item_identifier,
                                    'data': data, 'count': count}
                return self

            def queue(self):
                for i in range(0, 3):  # Row
                    for j in range(0, 3):  # Column
                        current_item = self._grid[i][j]['item'] if type(
                            self._grid[i][j]) is dict else ' '
                        current_data = self._grid[i][j]['data'] if type(
                            self._grid[i][j]) is dict else 0
                        current_count = self._grid[i][j]['count'] if type(
                            self._grid[i][j]) is dict else 0
                        current_key = self._keys[0]
                        if current_item != ' ':
                            if current_item not in self._items:
                                self._items.update({
                                    current_item: {
                                        'key': current_key,
                                        'data': current_data,
                                        'count': current_count
                                    }
                                })
                                self._pattern[i] = self._pattern[i][:j] + \
                                    current_key+self._pattern[i][j+1::]
                                self._keys = self._keys[1::]
                                self._key.update({
                                    current_key: {
                                        'item': current_item,
                                        'data': current_data,
                                        'count': current_count
                                    }
                                })
                            elif current_data != self._items[current_item]['data'] or current_count != self._items[current_item]['count']:
                                self._items.update({
                                    current_item: {
                                        'key': current_key,
                                        'data': current_data,
                                        'count': current_count
                                    }
                                })
                                self._pattern[i] = self._pattern[i][:j] + \
                                    current_key+self._pattern[i][j+1::]
                                self._keys = self._keys[1::]
                                self._key.update({
                                    current_key: {
                                        'item': current_item,
                                        'data': current_data,
                                        'count': current_count
                                    }
                                })
                            else:
                                self._pattern[i] = self._pattern[i][:j] + \
                                    self._items[current_item]['key'] + \
                                    self._pattern[i][j+1::]
                if not self._recipe_exactly:
                    for i in range(len(self._pattern[0])):
                        if self._pattern[0].endswith(' ') and self._pattern[1].endswith(' ') and self._pattern[2].endswith(' '):
                            for j in range(len(self._pattern)):
                                self._pattern[j] = self._pattern[j].removesuffix(
                                    ' ')

                        if self._pattern[0].startswith(' ') and self._pattern[1].startswith(' ') and self._pattern[2].startswith(' '):
                            for j in range(len(self._pattern)):
                                self._pattern[j] = self._pattern[j].removeprefix(
                                    ' ')

                    for i in range(len(self._pattern)):
                        if len(self._pattern) > 0:
                            if self._pattern[-1] == (' '*len(self._pattern[-1])):
                                self._pattern.pop(-1)
                        if len(self._pattern) > 0:
                            if self._pattern[0] == (' '*len(self._pattern[0])):
                                self._pattern.pop(0)

                self._default['minecraft:recipe_shaped']['pattern'] = self._pattern
                self._default['minecraft:recipe_shaped']['key'] = self._key
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _Stonecutter():
            def __init__(self, parent, identifier, output_item_id: str, data: int = 0, count: int = 1):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    'recipe_stonecutter', self._identifier, output_item_id, data, count)

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    RaiseError(
                        f'The recipe {self._parent._name} has more than 9 items')
                if item_id not in [item['item'] for item in self._ingredients]:
                    self._ingredients.append(
                        {'item': item_id, 'data': data, 'count': count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default['minecraft:recipe_shapeless']['ingredients'] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _Stonecutter():
            def __init__(self, parent, identifier, output_item_id: str, data: int = 0, count: int = 1):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    'recipe_stonecutter', self._identifier, output_item_id, data, count)

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    RaiseError(
                        f'The recipe {self._parent._name} can only take 1 item')
                self._ingredients.append(
                    {'item': item_id, 'data': data, 'count': count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default['minecraft:recipe_shapeless']['ingredients'] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _SmithingTable():
            def __init__(self, parent, identifier, output_item_id: str, data: int = 0, count: int = 1):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    'recipe_smithing_table', self._identifier, output_item_id, data, count)

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    RaiseError(
                        f'The recipe {self._parent._name} can only take 1 item')
                self._ingredients.append(
                    {'item': item_id, 'data': data, 'count': count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default['minecraft:recipe_shapeless']['ingredients'].extend(
                    self._ingredients)
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        def __init__(self, parent, identifier):
            self._parent = parent
            self._identifier = identifier

        def shapeless(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._Shapeless(self._parent, self._identifier, output_item_id, data, count)

        def shaped(self, output_item_id: str, data: int = 0, count: int = 1, recipe_exactly: bool = False):
            return self._Shaped(self._parent, self._identifier, output_item_id, data, count, recipe_exactly)

        def stonecutter(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._Stonecutter(self._parent, self._identifier, output_item_id, data, count)

        def smithing_table(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._SmithingTable(self._parent, self._identifier, output_item_id, data, count)

    class _Smelting():
        def __init__(self, parent, identifier):
            self._parent = parent
            self._identifier = identifier
            self._tags = []
            self._output = ' '
            self._input = ' '

        def output(self, output_item_id: str, data: int = 0, count: int = 1):
            self._output = f'{output_item_id}:{data}'
            return self

        def input(self, input_item_id: str, data: int = 0, count: int = 1):
            self._input = f'{input_item_id}:{data}'
            return self

        @property
        def furnace(self):
            self._tags.append('furnace')
            return self

        @property
        def blast_furnace(self):
            self._tags.append('blast_furnace')
            return self

        @property
        def smoker(self):
            self._tags.append('smoker')
            return self

        @property
        def campfire(self):
            self._tags.append('campfire')
            self._tags.append('soul_campfire')
            return self

        def queue(self):
            if self._output == ' ':
                RaiseError('Recipe missing output item')
            if self._input == ' ':
                RaiseError('Recipe missing input item')
            self._tags = list(set(self._tags))
            self._default = Defaults(
                'recipe_furnace', self._identifier, self._output, self._input, self._tags)
            self._parent.content(self._default)
            self._parent.queue()
            self._parent._export()

    def __init__(self, name: str):
        self._name = name
        self._content = ''
        super().__init__(name, 'recipe', '.json')

    def crafting(self, identifier: str):
        return self._Crafting(self, identifier)

    def smelting(self, identifier: str):
        return self._Smelting(self, identifier)
class Structure():
    def __init__(self, structure_name):
        self._structure_name = structure_name
        CheckAvailability(f'{self._structure_name}.mcstructure',
                          'structure', 'assets/structures')

    @property
    def queue(self):
        ANVIL._queue(self)

    @property
    def identifier(self):
        return f'{NAMESPACE_FORMAT}:{self._structure_name}'

    def _export(self):
        CopyFiles(f"assets/structures",
                  f"behavior_packs/BP_{PASCAL_PROJECT_NAME}/structures/{NAMESPACE_FORMAT}", f"{self._structure_name}.mcstructure")
class Particle(EngineComponent):
    def __init__(self, particle_name):
        super().__init__(particle_name, 'asset', '.particle.json')
        self._name = particle_name
        self._content = ''

    def queue(self):
        return super().queue('particles')

    def _export(self):
        if self._content != '':
            super()._export()
        CheckAvailability(f'{self._name}.png', 'texture', 'assets/particles')
        CopyFiles('assets/particles',
                  f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/particle', f'{self._name}.png')
        CheckAvailability(f'{self._name}.particle.json', 'particle', 'assets/particles')
        CopyFiles('assets/particles',
                  f'resource_packs/RP_{PASCAL_PROJECT_NAME}/particles', f'{self._name}.particle.json')
class Item():
    def __new__(self, identifier: str, is_vanilla: bool = False):
        self._identifier, self._display_name = RawText(identifier)
        ANVIL._items.update({self._display_name: f'{NAMESPACE_FORMAT}:{self._identifier}'})
        CheckAvailability(f'{self._identifier}.png', 'texture', 'assets/textures/items')
        if is_vanilla:
            ANVIL._items.update({self._display_name: f'minecraft:{self._identifier}'})
        self._item_rp = Item.__RP_Item(self._identifier, is_vanilla)
        self._item_bp = Item.__BP_Item(self._item_rp, self._identifier, is_vanilla)
        return self._item_bp

    class __RP_Item(EngineComponent):
        def __init__(self, identifier, is_vanilla):
            self._identifier, self._display_name = RawText(identifier)
            super().__init__(self._identifier, 'rp_item_v1', '.item.json')
            self.content(Defaults('rp_item_v1', NAMESPACE_FORMAT if not is_vanilla else 'minecraft', self._identifier))

        def queue(self, directory):
            ANVIL.localize(
                (f'item.{NAMESPACE_FORMAT}:{self._identifier}.name={self._display_name}'))
            super().queue(directory=directory)
            CopyFiles(
                'assets/textures/items', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/items/{directory}', f'{self._identifier}.png')
            if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json'):
                File('item_texture.json', Schemes('item_texture', PROJECT_NAME),f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
            with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json', 'r') as file:
                data = json.load(file)
                data['texture_data'][f'{self._identifier}'] = {'textures': []}
                data['texture_data'][f'{self._identifier}']['textures'].append(MakePath('textures/items',directory,self._identifier))
            File('item_texture.json', data,f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')

    class __BP_Item(EngineComponent):
        def __init__(self, parent, identifier, is_vanilla):
            self._identifier = identifier
            self._parent = parent
            super().__init__(self._identifier, 'bp_item_v1', '.item.json')
            self.content(Defaults('bp_item_v1', NAMESPACE_FORMAT if not is_vanilla else 'minecraft', self._identifier))

        def is_tool(self, max_damage: int = 0):
            max_damage = int(max_damage)
            if max_damage > 0:
                self._content['minecraft:item']['components']['minecraft:hand_equipped'] = True
                self._content['minecraft:item']['components']['minecraft:max_damage'] = max(
                    min(2031, max_damage), 1)
            return self
        
        @property
        def identifier(self):
            return f'{NAMESPACE_FORMAT}:{self._identifier}'
            
        @property
        def foil(self):
            self._content['minecraft:item']['components']['minecraft:foil'] = True
            return self

        def stack_size(self, max_stack_size: int = 64):
            max_stack_size = int(max_stack_size)
            if 1 <= max_stack_size < 65:
                self._content['minecraft:item']['components']['minecraft:stacked_by_data'] = True
                self._content['minecraft:item']['components']['minecraft:max_stack_size'] = max(
                    min(64, max_stack_size), 1)
            elif max_stack_size > 64:
                RaiseError(
                    f'Item Stack size should be between 1 and 64, Error at item {self._identifier}')
            return self

        def right_clickable(self, use_duration: int = 0):
            if 'minecraft:food' not in self._content['minecraft:item']['components']:
                self._content['minecraft:item']['components']['minecraft:food'] = {
                }
            self._content['minecraft:item']['components']['minecraft:food'].update(
                {"can_always_eat": True})
            use_duration = int(use_duration)
            if use_duration > 0:
                self._content['minecraft:item']['components']['minecraft:use_duration'] = max(
                    min(1000000, use_duration), 1)
            return self

        def cooldown_duration(self, cooldowns_duration: int = 0):
            cooldowns_duration = int(cooldowns_duration*20)
            if cooldowns_duration > 0:
                if 'minecraft:food' not in self._content['minecraft:item']['components']:
                    self._content['minecraft:item']['components']['minecraft:food'] = {
                    }
                self._content['minecraft:item']['components']['minecraft:food']['cooldown_time'] = max(
                    min(1000000, cooldowns_duration), 1)
                self._content['minecraft:item']['components']['minecraft:food']['cooldown_type'] = 'chorusfruit'
                if 'minecraft:hand_equipped' in self._content['minecraft:item']['components']:
                    self._content['minecraft:item']['components']['minecraft:food']['can_always_eat'] = True
            return self

        def effect(self, effect_name: str, amplifier: int = 1, duration: float or int = 120, chance: int = 1):
            if 'minecraft:food' not in self._content['minecraft:item']['components']:
                self._content['minecraft:item']['components']['minecraft:food'] = {
                    'nutrition': 4, 'saturation_modifier': 'normal', 'effects': []}
            self._content['minecraft:item']['components']['minecraft:food']['effects'].append(
                {'name': effect_name, 'chance': chance, 'duration': duration, 'amplifier': amplifier})
            self._content['minecraft:item']['components']['minecraft:food']['can_always_eat'] = True
            return self

        def queue(self, directory=''):
            self._directory = directory
            self.content(self._content)
            super().queue(self._directory)
            self._parent.queue(self._directory)
class Block():
    class __RP_Block():
        class _BlockTextures():
            def __init__(self, identifier: str, sound: str, **kwargs):
                if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/blocks.json'):
                    File('blocks.json', Defaults('blocks'),f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')
                with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/blocks.json', 'r') as file:
                    data = json.load(file)
                    if len(kwargs.keys()) == 0:
                        data[f'{NAMESPACE_FORMAT}:{identifier}'] = {'textures': identifier, 'sound': sound}
                    else:
                        data[f'{NAMESPACE_FORMAT}:{identifier}'] = {'textures': {}, 'sound': sound}
                        keys = ['side', 'up', 'down','east', 'north', 'south', 'west']
                        for key in kwargs:
                            if key in keys:data[f'{NAMESPACE_FORMAT}:{identifier}']['textures'][key] = kwargs[key]
                            else:
                                RaiseError('Texture keys type must be one of %r.' % keys)
                File('blocks.json', data,f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')

        class _TerrainTexture():
            def __init__(self, identifier: str, directory: str, **kwargs):
                if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/terrain_texture.json'):
                    File('terrain_texture.json', Defaults('terrain_texture', PROJECT_NAME),f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
                with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/terrain_texture.json', 'r') as file:
                    data = json.load(file)
                    if len(kwargs.keys()) == 0:
                        data['texture_data'][f'{identifier}'] = {'textures': []}
                        data['texture_data'][f'{identifier}']['textures'].append(os.path.join('textures/blocks',directory,identifier).replace('\\','/'))
                    else:
                        keys = ['side', 'up', 'down',
                                'east', 'north', 'south', 'west']
                        for key in kwargs:
                            if key in keys:
                                data['texture_data'][kwargs[key]] = {'textures': []}
                                data['texture_data'][kwargs[key]]['textures'].append(MakePath('textures','blocks',directory,kwargs[key]))
                                
                            else:
                                RaiseError(
                                    'Texture keys type must be one of %r.' % keys)
                File('terrain_texture.json', data,f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')

        def __init__(self, identifier, sound, **textures):
            self._identifier, self._display_name = RawText(identifier)
            self._sound = sound
            self._textures = textures

        def queue(self, directory):
            ANVIL.localize(
                f'tile.{NAMESPACE_FORMAT}:{self._identifier}.name={self._display_name}')
            self._BlockTextures(
                self._identifier, self._sound, **self._textures)
            self._TerrainTexture(self._identifier, directory, **self._textures)
            if len(self._textures) == 0:
                if FileExists(f'assets/textures/blocks/{self._identifier}.png'):
                    CopyFiles('assets/textures/blocks', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/blocks/{directory}', f'{self._identifier}.png')
            else:
                for texture in self._textures:
                    CopyFiles('assets/textures/blocks', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/blocks/{directory}',f'{self._textures[texture]}.png')

    class __BP_Block(EngineComponent):
        def __init__(self, parent, identifier):
            self._identifier = identifier
            self._parent = parent
            super().__init__(self._identifier, 'bp_block_v1', '.block.json')
            self._content = Defaults('bp_block_v1', NAMESPACE_FORMAT, self._identifier)
            if FileExists(f'assets/textures/blocks/{self._identifier}.png'):
                self._most_dominant_color, self._least_dominant_color = GetColors(
                    f'assets/textures/blocks/{self._identifier}.png')
            else:
                self._most_dominant_color = '#000000'
            self._content['minecraft:block']['components']['minecraft:map_color'] = self._most_dominant_color

        def destroy_time(self, destroy_time: int = 0):
            destroy_time = int(destroy_time)
            self._content['minecraft:block']['components']['minecraft:destroy_time'] = max(
                min(1000, destroy_time), 0)
            return self

        def explosion_resistance(self, explosion_resistance: int = 0):
            explosion_resistance = int(explosion_resistance)
            self._content['minecraft:block']['components']['minecraft:explosion_resistance'] = max(
                min(1000, explosion_resistance), 0)
            return self

        def friction(self, friction: float = 0.6):
            friction = float(friction)
            self._content['minecraft:block']['components']['minecraft:friction'] = max(
                min(1000, friction), 0)
            return self

        @property
        def flammable(self):
            self._content['minecraft:block']['components']['minecraft:flammable'] = {
                'flame_odds': 1,
                'burn_odds': 1
            }
            return self

        def light_emission(self, light_emission: int = 0):
            light_emission = int(light_emission)
            if light_emission not in range(0, 16, 1):
                RaiseError('Light Emission level must be in range 0 - 15')
            self._content['minecraft:block']['components']['minecraft:block_light_emission'] = max(
                min(15, light_emission), 0)/15
            return self

        def light_absorption(self, light_absorption: int = 0):
            light_absorption = int(light_absorption)
            if light_absorption not in range(0, 16, 1):
                RaiseError('Light Emission level must be in range 0 - 15')
            self._content['minecraft:block']['components']['minecraft:block_light_absorption'] = max(
                min(15, light_absorption), 0)
            return self

        def loot(self, drops: str = 'self'):
            self._content['minecraft:block']['components'][
                'minecraft:loot'] = f'loot_tables/blocks/{self._identifier}.loot_table.json'
            if drops == 'self':
                LootTable(self._identifier).entry(
                    f'{NAMESPACE_FORMAT}:{self._identifier}', 1, 1, 1).queue('blocks')
            else:
                LootTable(self._identifier).entry(
                    drops, 1, 1, 1).queue('blocks')
            return self

        def queue(self, directory=''):
            self._directory = directory
            self.content(self._content)
            super().queue(self._directory)
            self._parent.queue(self._directory)

    def get_name(self):
        return f'{NAMESPACE_FORMAT}:{self._identifier}'

    def __new__(self, identifier: str = '', sound: str = 'stone', **textures):
        self._identifier, self._display_name = RawText(identifier)
        ANVIL._blocks.update(
            {self._display_name: f'{NAMESPACE_FORMAT}:{self._identifier}'})
        self._sound = sound
        self._textures = textures

        if not FileExists(f'assets/textures/blocks/{self._identifier}.png'):
            if 'up' in textures:
                CheckAvailability(f'{textures["up"]}.png', 'texture', 'assets/textures/blocks')
            else:
                RaiseError(
                    f'A texture with the name {self._identifier} cannot be found in assets/textures/blocks')

        self._block_rp = self.__RP_Block(self._identifier, self._sound, **self._textures)
        self._block_bp = self.__BP_Block(self._block_rp, self._identifier)
        return self._block_bp
class LootTable(EngineComponent):
    class _LootPool():
        class _entry():
            class _Functions():
                def __init__(self) -> None:
                    pass

                def SetName(self, name: str):
                    self._func = {"function": "set_name", "name": name}
                    return self

                def SetLore(self, *lore: str):
                    self._func = {"function": "set_lore", "lore": [lore]}
                    return self

                def SpecificEnchants(self, *enchants: tuple[str, int]):
                    self._func = {"function": "specific_enchants", "enchants": [
                        {'id': enchant[0], 'level': enchant[1]}for enchant in enchants]}
                    return self

                def SetDamage(self, damage: float | tuple[float, float]):
                    if damage > 1:
                        RaiseError('SetDamage value cannot be above the maximum of 1.')
                    self._func = {"function": "set_damage", "damage": {
                        'min': damage[0], 'max': damage[1]}}
                    return self

                def SetCount(self, count: int | tuple[int, int]):
                    if type(count) is tuple:
                        self._func = {"function": "set_count",
                                      "count": {'min': count[0], 'max': count[1]}}
                    elif type(count) is int:
                        self._func = {"function": "set_count", "count": count}
                    return self

                def SetData(self, data: int | tuple[int, int]):
                    if type(data) is tuple:
                        self._func = {"function": "set_data",
                                      "data": {'min': data[0], 'max': data[1]}}
                    elif type(data) is int:
                        self._func = {"function": "set_data", "data": data}
                    return self

                def EnchantRandomly(self):
                    self._func = {"function": "enchant_randomly"}
                    return self

                def _export(self):
                    return self._func

            def __init__(self, name: str, count: int = 1, weight: int = 1, entry_type: LootPoolType = LootPoolType.Item) -> None:
                self._entry = {
                    "type": entry_type,
                    "name": name,
                    "count": count,
                    "weight": weight
                }
                self._functions = []

            def quality(self, quality: int):
                self._entry.update({"quality": quality})

            @property
            def functions(self):
                function = self._Functions()
                self._functions.append(function)
                return function

            def _export(self):
                for function in self._functions:
                    if 'functions' not in self._entry:
                        self._entry.update({'functions': []})
                    self._entry["functions"].append(function._export())
                return self._entry

        def __init__(self, rolls: int | Tuple[int, int] = 1, loot_type: LootPoolType = LootPoolType.Item):
            self._pool = {}
            self._entries = []
            if type(rolls) is int:
                self._pool.update({"rolls": rolls})
            elif type(rolls) is tuple:
                self._pool.update({"rolls": {rolls[0], rolls[1]}})
            self._pool.update({"type": loot_type})

        def tiers(self, bonus_chance: int = 0, bonus_rolls: int = 0, initial_range: int = 0):
            self._pool.update({"tiers": {}})
            if bonus_chance != 0:
                self._pool['tiers'].update({'bonus_chance': bonus_chance})
            if bonus_rolls != 0:
                self._pool['tiers'].update({'bonus_rolls': bonus_rolls})
            if initial_range != 0:
                self._pool['tiers'].update({'initial_range': initial_range})

        def entry(self, name: str, count: int = 1, weight: int = 1, entry_type: LootPoolType = LootPoolType.Item):
            entry = self._entry(name, count, weight, entry_type)
            self._entries.append(entry)
            return entry

        def _export(self):
            for entry in self._entries:
                if 'entries' not in self._pool:
                    self._pool.update({'entries': []})
                self._pool["entries"].append(entry._export())
            return self._pool

    def __init__(self, name: str):
        super().__init__(name, 'loot_table', '.loot_table.json')
        self._content = Defaults('loot_table')
        self._pools = []

    def pool(self, rolls: int | Tuple[int, int] = 1, loot_type: LootPoolType = LootPoolType.Item):
        pool = self._LootPool(rolls, loot_type)
        self._pools.append(pool)
        return pool

    def queue(self, directory: str = ''):
        for pool in self._pools:
            self._content["pools"].append(pool._export())
        self.content(self._content)
        return super().queue(directory=directory)
class Function(EngineComponent):
    def __init__(self, name: str):
        self._name = name
        self._content = ''
        self._length = 0
        self._id = 0
        self._sub_functions : list[Function]= []
        super().__init__(name, 'function', '.mcfunction')

    def add(self, *functions: str):
        for function in functions:
            if self._length < 9998-len(functions)-self._id:
                self._content += f'{function}\n'
                self._length += 1
            else:
                if len(self._sub_functions) == 0:
                    self._id += 1
                    self._sub_functions.append(Function(f'{self._name}_{self._id}'))
                else:
                    if self._sub_functions[-1]._length < 9998-len(functions)-self._id:
                        self._sub_functions[-1]._content += f'{function}\n'
                        self._sub_functions[-1]._length += 1
                    else:
                        self._id += 1
                        self._sub_functions.append(Function(f'{self._name}_{self._id}'))
                        self._sub_functions[-1]._content += f'{function}\n'
                        self._sub_functions[-1]._length += 1
        return self

    @property
    def execute(self):
        return f'function {MakePath(PROJECT_NAME,self._directory,self._name)}'

    @property
    def identifier(self):
        return self._name

    @property
    def tick(self):
        ANVIL._tick(self)
        return self

    def queue(self, directory: str = ''):
        if len(self._sub_functions) > 0:
            content = str(self._content)
            self._content = ''
            self._sub_functions.insert(0, Function(f'{self._name}_{0}').content(content))
            for function in self._sub_functions:
                function.queue(directory)
                self._content += f'{function.execute}\n'
        return super().queue(directory)
class Dialogue(EngineComponent):
    def __init__(self, name: str):
        self._scenes = []
        super().__init__(name, 'dialogue', '.dialogue.json')

    def scene(self, tag: str):
        scene = Dialogue._Scene(tag)
        self._scenes.append(scene)
        return scene

    def queue(self, directory=''):
        self._directory = directory
        dialogues = Defaults('dialogue')
        for scene in self._scenes:
            dialogues['minecraft:npc_dialogue']['scenes'].append(
                scene._export())
        self.content(dialogues)
        return super().queue(self._directory)

    class _Scene():
        def __init__(self, tag: str):
            self._buttons = []
            self._tag = tag

        def properties(self, npc_name: str, text: str):
            self._npc_name, self._npc_display_name = RawText(npc_name)
            self._display_text = text
            return self

        def button(self, button_name: str, *commands: str or object):
            button = self._Button(button_name, *commands)
            self._buttons.append(button)
            return self

        def _export(self):
            buttons = []
            if len(self._buttons) > 6:
                RaiseError(
                    f'Error: The dialogue scene with the name {self._tag} has {len(self._buttons)} buttons. Maximum is 6')
            for button in self._buttons:
                buttons.append(button._export())
            ANVIL.localize(f'npc_name.{self._npc_name}={self._npc_display_name}')
            ANVIL.localize(f'npc_text.{self._tag}={self._display_text}')
            return {
                'scene_tag': self._tag,
                'npc_name': {'rawtext': [{'translate': f'npc_name.{self._npc_name}'}]},
                'text': {'rawtext': [{'translate': f'npc_text.{self._tag}', 'with': ['\n']}]},
                'buttons': buttons
            }

        class _Button():
            def __init__(self, button_name: str, *commands: str or Function):
                self._button_name = button_name
                if isinstance(commands, Function):
                    self._commands = f'/{commands.execute}'
                else:
                    self._commands = commands

            def _export(self):
                ANVIL.localize(
                    f'button.{self._button_name.replace(" ", "_").lower()}={self._button_name}')
                return {
                    'name': self._button_name,
                    'commands': [
                        command for command in self._commands
                    ]
                }



class Anvil():
    def get_github_file(self, path: str):
        from github import Github
        if not self._github_init:
            self._github = Github().get_repo('Mojang/bedrock-samples')
        return json.loads(self._github.get_contents(path, BUILD.lower()).decoded_content.decode())

    def __init__(self):
        """
        Provides a way to control different aspects of the project, setting up project scores, tags, ticking functions, languages and so on...

        Methods:
        ---------
        >>> Anvil.score()
        >>> Anvil.tag()
        >>> Anvil.tick()
        >>> Anvil.localize()
        >>> Anvil.material()
        >>> Anvil.setup()
        >>> Anvil.translate()
        >>> Anvil.compile
        >>> Anvil.package()
        """
        header()
        self._start_timer = time.time()
        with open('./config.json', 'r') as config:
            data = json.load(config)
            global COMPANY
            global NAMESPACE
            global PROJECT_NAME
            global PASCAL_PROJECT_NAME
            global DISPLAY_NAME
            global PROJECT_DESCRIPTION
            global VANILLA_VERSION
            global NAMESPACE_FORMAT
            global NAMESPACE_FORMAT_BIT
            global BUILD

            COMPANY = data['COMPANY']
            NAMESPACE = data['NAMESPACE']
            PROJECT_NAME = data['PROJECT_NAME']
            PASCAL_PROJECT_NAME = ''.join(x for x in PROJECT_NAME.title().replace('_', '').replace('-', '') if x.isupper())
            DISPLAY_NAME = data['DISPLAY_NAME']
            PROJECT_DESCRIPTION = data['PROJECT_DESCRIPTION']
            VANILLA_VERSION = data['VANILLA_VERSION']
            LAST_CHECK = data['LAST_CHECK']
            NAMESPACE_FORMAT_BIT = data['NAMESPACE_FORMAT']
            BUILD = data['BUILD']

            if NAMESPACE_FORMAT_BIT == 0:
                NAMESPACE_FORMAT = f'{NAMESPACE}'
            elif NAMESPACE_FORMAT_BIT == 1:
                NAMESPACE_FORMAT = f'{NAMESPACE}.{PROJECT_NAME}'
        
        self._setup = Function('setup')
        self._setup_scores = Function('setup_scores')
        self._remove_scores = Function('remove_scores')
        self._remove_tags = Function('remove_tags')
        self._item_texture = _ItemTextures()
        self._sound_definition = _Sound()
        self._music_definition = _Music()

        self._functions = []
        self._scores = {}
        self._objects_list = []
        self._tick_functions = []
        self._langs = []
        self._skins_langs = []
        self._tags = []
        self._entities = {}
        self._items = {}
        self._blocks = {}
        self._sounds = {}
        self._tellraw_index = 0
        self._score_index = 0
        self._materials = Defaults('materials')
        self._setup_scores.content(f'scoreboard objectives add {PROJECT_NAME} dummy "{PROJECT_NAME.replace("_"," ").title()}"\n')
        self._remove_scores.content(f'scoreboard objectives remove {PROJECT_NAME}\n')
        self._deltatime = int((datetime.now() - datetime.strptime(LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds())
        self._github_init = False

        # 12 Hours
        if (self._deltatime > 12*3600):
            click.echo(CHECK_UPDATE)
            LATEST_BUILD = self.get_github_file('version.json')['latest']['version']

            if VANILLA_VERSION < LATEST_BUILD:
                click.echo(NEW_BUILD(VANILLA_VERSION, LATEST_BUILD))
            else:
                click.echo(UP_TO_DATE)
            File("config.json", Schemes('config', NAMESPACE, COMPANY, PROJECT_NAME, DISPLAY_NAME, PROJECT_DESCRIPTION, LATEST_BUILD, NAMESPACE_FORMAT_BIT, BUILD), ".", "w")
    
    def sound(self, sound_definition: str, category: SoundCategory(), use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
        return self._sound_definition.sound_definition(sound_definition,category,use_legacy_max_distance,max_distance,min_distance)

    def music(self, music_category: MusicCategory(), min_delay: int = 60, max_delay: int = 180):
        return self._music_definition.music_definition(music_category, min_delay, max_delay)

    def localize(self, *texts: str) -> None:
        """
        Adds a localized string to en_US. Translatable.

        Parameters:
        ---------
        `texts` : `str`
            Minecraft lang string.

        Examples:
        ---------
        >>> ANVIL.localize('raw_text_0=Created with Anvil')
        """

        for text in texts:
            if len(text.split('=')) != 2:
                RaiseError(LANG_ERROR(text))
            if f'{text}\n' not in self._langs:
                self._langs.append(f'{text}\n')

    def score(self, **score_id_value) -> None:
        """
        Adds the provided scores to the setup functions as well as setting the global score values.
        Score objective must be 16 characters or less.

        Parameters:
        ---------
        `score_id_value` : `kwargs`
            The score and it's initial value.

        Examples:
        ---------
        >>> ANVIL.score(player_id=0,test=4)
        >>> ANVIL.score(**{'level':5,'type':1})
        """

        for score_id, score_value in score_id_value.items():
            if len(score_id) > 16:
                RaiseError(click.style(SCORE_ERROR(score_id)))
            if score_id not in self._scores:
                self._scores.update({score_id: score_value})
                self._remove_scores.add(f'scoreboard objectives remove {score_id}')
                self._setup_scores.add(f'scoreboard objectives add {score_id} dummy "{score_id.replace("_"," ").title()}"')
                self._setup_scores.add(f'scoreboard players set {PROJECT_NAME} {score_id} {score_value}')

    def tag(self, *tags: str) -> None:
        """
        Adds the provided tags to the setup functions by clearing them from all entities on setup.

        Parameters:
        ---------
        `tags` : `str`
            String tags to be added.

        Examples:
        ---------
        >>> ANVIL.tag('is_alive')
        >>> ANVIL.tag('fly','interact')
        """

        for tag in tags:
            if tag not in self._tags:
                self._tags.append(tag)
                self._remove_tags.add(f'tag @a remove {tag}')

    def _tick(self, *functions: Function) -> None:
        """
        Adds the provided function to tick.json.

        Parameters:
        ---------
        `functions` : `Function`
            Function object.

        Examples:
        ---------
        >>> ANVIL.tick(Function)
        """

        for function in functions:
            if not type(function) is Function:
                RaiseError(FUNCTION_ERROR('tick', function))
            self._tick_functions.append(function.execute.split(' ')[-1].replace('\n', ''))

    def material(self, material: dict) -> None:
        self._materials['materials'].update(material)

    def setup(self, *functions: Function) -> None:
        """
        Adds the provided functions to run on project setup function.

        Parameters:
        ---------
        `functions` : `Function`
            Function object.

        Examples:
        ---------
        >>> ANVIL.tick(Function)
        """

        for function in functions:
            if not type(function) is Function:
                RaiseError(FUNCTION_ERROR('setup', function))
            self._setup.add(function.execute)

    @property
    def translate(self) -> None:
        """
        Translates en_US to all supported Minecraft languages.
        This is a time consuming function, it will be executed with anvil.package(), so it's better to avoid it unless you really want to use it.


        Usage:
        ---------
        >>> ANVIL.translate
        """

        from deep_translator import GoogleTranslator
        click.echo(f'Translating...')
        languages = Defaults('languages')
        self._langs.sort()
        for language in languages:
            destination_language = language.split('_')[0]
            if language == 'zh_CN':
                destination_language = 'zh-CN'
            if language == 'zh_TW':
                destination_language = 'zh-TW'
            if language == 'nb_NO':
                destination_language = 'no'
            new_data = ''
            # Translating Skin Packs
            if not FileExists(f'assets/skin_pack/texts/{language}.lang'):
                TRANSLATOR = GoogleTranslator(target=destination_language)
                for line in self._skins_langs:
                    if len(line) > 0:
                        if '=' in line:
                            id, text = line.split("=")
                            text=text.replace('\n','')

                            click.echo(f'{language}: {text} = ', nl=False)
                            translated = TRANSLATOR.translate(text)
                            click.echo(f'{translated}\r', nl=False)
                            
                            new_data += f'{id}={translated}\n'
                    else:
                        new_data += f'{line}\n'
                    time.sleep(0.3)
                click.echo(f'{language}: Done.\n')
                File(f'{language}.lang', Schemes('skin_language', PROJECT_NAME, DISPLAY_NAME+ ' Skin Pack') + new_data, f'assets/skin_pack/texts', 'w')

            if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts/{language}.lang'):
                TRANSLATOR = GoogleTranslator(target=destination_language)
                for line in self._langs:
                    if len(line) > 0:
                        if '=' in line:
                            id, text = line.split("=")
                            text=text.replace('\n','')

                            click.echo(f'{language}: {text} = ', nl=False)
                            translated = TRANSLATOR.translate(text)
                            click.echo(f'{translated}\r', nl=False)
                            
                            new_data += f'{id}={translated}\n'
                    else:
                        new_data += f'{line}\n'
                    time.sleep(0.3)
                click.echo(f'{language}: Done.\n')
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, TRANSLATOR.translate(PROJECT_DESCRIPTION)) + new_data, f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts', 'w')
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, TRANSLATOR.translate(PROJECT_DESCRIPTION)), f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts', 'w')
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, TRANSLATOR.translate(PROJECT_DESCRIPTION)), 'texts', 'w')
            
    @property
    def compile(self) -> None:
        """
        Compiles queued anvil objects.
        This function must be called last at the very end of your script.


        Usage:
        ---------
        >>> ANVIL.compile
        """
        click.echo(f'Executed at: {datetime.now()}')
        click.echo(f'Compiling...')
        self._langs.sort()
        CreateDirectory(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts')
        CreateDirectory(f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts')
        CreateDirectory('texts')

        File('languages.json', Defaults('languages'),f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('languages.json', Defaults('languages'),f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('languages.json', Defaults('languages'),'texts', 'w')

        File('en_US.lang', Defaults('language', DISPLAY_NAME, PROJECT_DESCRIPTION) + ''.join(self._langs), f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', Defaults('language', DISPLAY_NAME, PROJECT_DESCRIPTION),f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', Defaults('language', DISPLAY_NAME, PROJECT_DESCRIPTION),'texts', 'w')
        
        if FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/manifest.json') is False:
            File("manifest.json", Schemes('manifest_rp'),f"resource_packs/RP_{PASCAL_PROJECT_NAME}", "w")
            with open(f"resource_packs/RP_{PASCAL_PROJECT_NAME}/manifest.json",'r') as file:
                data = json.load(file)
                uuid = data["header"]["uuid"]
                version = data["header"]["version"]
                File("world_resource_packs.json", Schemes('world_packs', uuid, version), ".", "w")
        if FileExists(f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/manifest.json') is False:
            File("manifest.json", Schemes('manifest_bp'),f"behavior_packs/BP_{PASCAL_PROJECT_NAME}", "w")
            with open(f"./behavior_packs/BP_{PASCAL_PROJECT_NAME}/manifest.json",'r') as file:
                data = json.load(file)
                uuid = data["header"]["uuid"]
                version = data["header"]["version"]
                File("world_behavior_packs.json", Schemes('world_packs', uuid, version), ".", "w") 
        
        if len(self._materials['materials']) > 1:
            CreateDirectory(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/materials')
            File('entity.material', self._materials,
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/materials', 'w')
        if FileExists('assets/gui'):
            CopyFolder('assets/gui',f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/gui')
        if FileExists('assets/textures/glyph_E1.png'):
            CopyFiles('assets/textures',f'resource_packs/RP_{PASCAL_PROJECT_NAME}/font', 'glyph_E1.png')
        
            
        self._setup_scores.queue('StateManager/misc')
        self._remove_scores.queue('StateManager/misc')
        self._remove_tags.queue('StateManager/misc')
        for function in self._functions:
            self._setup.add(function.execute)
        File('tick.json', {'values': self._tick_functions},
             f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/functions', 'w')
        self._setup.add(self._remove_tags.execute).add(
            self._remove_scores.execute).add(self._setup_scores.execute)
        self._setup.queue()

        # Export only if contains data
        if len(self._item_texture._content['texture_data']) > 0:
            self._item_texture.queue
        if len(self._sound_definition._sounds) > 0:
            self._sound_definition.queue
        if len(self._music_definition._sounds) > 0:
            self._music_definition.queue

        for object in self._objects_list:
            object._export()
        click.echo(f'Compiling time: {round(time.time() - self._start_timer,2)} s')

    def package(self, clear_assets: bool = False, skip_translation : bool = False) -> None:
        """
        Compiles queued anvil objects, translates and packages the project.
        This function should be called at the end of development and playtesting, it packages the project and exports a submission ready .zip file.

        clear_assets is set to False by default, if you pass True as the argument, everything in the project folder will be deleted.

        Notes:
        ---------
        List of items that must exist under assets/marketing
        `0-4.png`: Marketing art, must all be `1920x1080`
        `keyart.png`: Marketing Keyart, must be `1920x1080`

        Parameters:
        ---------
        `clear_assets` : `bool`
            Removes all files.

        Usage:
        ---------
        >>> ANVIL.package()
        >>> ANVIL.package(True)
        """
        
        def validate(path:str):
            return FileExists(path)

        def art():
            CreateDirectory('assets/marketing/Store Art')
            CreateDirectory('assets/marketing/Marketing Art')

            if validate('assets/marketing/pack_icon.png'):
                CopyFiles('assets/marketing',f'behavior_packs/BP_{PASCAL_PROJECT_NAME}', 'pack_icon.png')
                CopyFiles('assets/marketing',f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'pack_icon.png')
                original = Image.open('assets/marketing/pack_icon.png')
                resized = original.resize(pack_icon_size)
                resized.convert("RGB").save(f'assets/marketing/Store Art/{PROJECT_NAME}_packicon_0.jpg',dpi=(72,72),quality=95)

            #Keyart
            if validate('assets/marketing/keyart.png'):
                original = Image.open('assets/marketing/keyart.png')
                resized = original.resize(store_screenshot_size)
                resized.save('world_icon.jpeg')
                resized.convert("RGB").save(f'assets/marketing/Store Art/{PROJECT_NAME}_Thumbnail_0.jpg',dpi=(72,72),quality=95)

                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(f'assets/marketing/Marketing Art/{PASCAL_PROJECT_NAME}_MarketingKeyArt.jpg',dpi=(300,300),quality=95)
            #Panorama
            if validate('assets/marketing/panorama.png'):
                original = Image.open('assets/marketing/panorama.png')
                new_width = original.size[1]//450
                resized = original.resize((original.size[0]*new_width, 450))
                resized.convert("RGB").save(f'assets/marketing/Store Art/{PROJECT_NAME}_panorama_0.jpg',dpi=(72,72),quality=95)
            #Marketing
            for i in range(5):
                if validate(f'assets/marketing/{i}.png'):
                    original = Image.open(f'assets/marketing/{i}.png')
                    resized = original.resize(store_screenshot_size)
                    resized.convert("RGB").save(f'assets/marketing/Store Art/{PROJECT_NAME}_screenshot_{i}.jpg',dpi=(72,72),quality=95)
                    resized = original.resize(marketing_screenshot_size)
                    resized.convert("RGB").save(f'assets/marketing/Marketing Art/{PASCAL_PROJECT_NAME}_MarketingScreenshot_{i}.jpg',dpi=(300,300),quality=100)
            #Partner Art
            if validate(f'assets/marketing/partner_art.png'):
                original = Image.open(f'assets/marketing/partner_art.png')
                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(f'assets/marketing/Marketing Art/{PASCAL_PROJECT_NAME}_PartnerArt.jpg',dpi=(300,300),quality=100)

        def generate_submission_notes():
            with open('assets/submission_notes.txt', "w", encoding='utf-8') as file:
                file.write('Entities:\n')
                for name, data in self._entities.items():
                    file.write(f'   {data["Display Name"]}: {name}\n')

                file.write('\nSounds:\n')
                for item, id in self._sounds.items():
                    file.write(f'   {item}: {id}\n')

                file.write('\nItems:\n')
                for item, id in self._items.items():
                    file.write(f'   {item}: {id}\n')

                file.write('\nBlocks:\n')
                for item, id in self._blocks.items():
                    file.write(f'   {item}: {id}\n')
        
        def zipit(zip_name, dir_list:dict):
            def zipdir(ziph:zipfile.ZipFile, source, target):
                if os.path.isdir(source):
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            ziph.write(
                                os.path.join(root, file),
                                os.path.join(target,os.path.relpath(os.path.join(root, file), os.path.join(source, '.')))
                            )
                else:
                    ziph.write(source,os.path.relpath(os.path.join(target,source), os.path.join(source, '..')))

            zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
            for source, target in dir_list.items():
                zipdir(zipf, source, target)
            zipf.close()

            RemoveDirectory('assets/marketing/Store Art')
            RemoveDirectory('assets/marketing/Marketing Art')
            RemoveFile('assets/submission_notes.txt')

        self.compile
        if not skip_translation:
            self.translate
        
        click.echo(f'Packaging...')
        pack_icon_size = (256, 256)
        marketing_screenshot_size = (1920, 1080)
        store_screenshot_size = (800, 450)

        content_structure = {
            'assets/marketing/Store Art': 'Store Art',
            'assets/marketing/Marketing Art': 'Marketing Art',
            'assets/skin_pack': 'Content/skin_pack',

            'resource_packs': 'Content/world_template/resource_packs',
            'behavior_packs': 'Content/world_template/behavior_packs',
            'db': 'Content/world_template/db',
            'texts': 'Content/world_template/texts',

            'level.dat': 'Content/world_template',
            'levelname.txt': 'Content/world_template',
            'manifest.json': 'Content/world_template',
            'world_behavior_packs.json': 'Content/world_template',
            'world_icon.jpeg': 'Content/world_template',
            'world_resource_packs.json': 'Content/world_template',

            'assets/submission_notes.txt': '',
        }
        File("manifest.json", Schemes('manifest_world', [COMPANY]),"", "w")
        generate_submission_notes()
        art()
        zipit(f"assets/{PROJECT_NAME.title().replace('_', '').replace('-', '')}.zip", content_structure)
    
    @property
    def mcaddon(self):
        def zipit(zip_name, dir_list:dict):
            def zipdir(ziph:zipfile.ZipFile, source, target):
                if os.path.isdir(source):
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            ziph.write(
                                os.path.join(root, file),
                                os.path.join(target,os.path.relpath(os.path.join(root, file), os.path.join(source, '.')))
                            )
                else:
                    ziph.write(source,os.path.relpath(os.path.join(target,source), os.path.join(source, '..')))

            zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
            for source, target in dir_list.items():
                zipdir(zipf, source, target)
            zipf.close()

        self.compile
        click.echo(f'Packaging...')
        project = PROJECT_NAME.title().replace('_', '').replace('-', '')

        if FileExists('assets/marketing/pack_icon.png'):
            CopyFiles('assets/marketing',f'behavior_packs/BP_{PASCAL_PROJECT_NAME}', 'pack_icon.png')
            CopyFiles('assets/marketing',f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'pack_icon.png')

        resource_packs_structure = {
            f'resource_packs/RP_{PASCAL_PROJECT_NAME}': '',
        }
        behavior_packs_structure = {
            f'behavior_packs/BP_{PASCAL_PROJECT_NAME}': '',
        }
        content_structure = {
            f'assets/{project}_RP.mcpack': '',
            f'assets/{project}_BP.mcpack': '',
        }
        zipit(f"assets/{project}_RP.mcpack", resource_packs_structure)
        zipit(f"assets/{project}_BP.mcpack", behavior_packs_structure)
        zipit(f"assets/{project}.mcaddon", content_structure)

        RemoveFile(f"assets/{project}_RP.mcpack")
        RemoveFile(f"assets/{project}_BP.mcpack")

    def _queue(self, object: object):
        self._objects_list.append(object)

ANVIL = Anvil()