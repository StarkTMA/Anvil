from .lib import *
from .lib import _Config, _Logger, _JsonSchemes


class AddonObject():
    _extensions = {
        0: ".json", 
        1: ".json"
    }

    def __init__(self, name: str, path: str) -> None:
        self._shorten = True

        self._name = name
        self._path = path

        self._content = {}
        self._directory = ''

        _logger.object_initiated(self._name)

    @classmethod
    @property
    def _extension(self):
        return self._extensions[ANVIL.NAMESPACE_FORMAT_BIT]

    @property
    def do_not_shorten(self):
        self._shorten = False

    def content(self, content):
        self._content = content
        return self

    def queue(self, directory: str = ''):
        self._directory = directory if not directory is None else ''
        self._path = os.path.join(self._path, self._directory)
        ANVIL._queue(self)
        _logger.object_queued(self._name)
        return self

    def _export(self):
        def _shorten_dict(d):
            if isinstance(d, dict):
                return {
                    k: v
                    for k, v in ((k, _shorten_dict(v)) for k, v in d.items())
                    if v != {} and v != [] or str(k).startswith("minecraft:")
                }

            elif isinstance(d, list):
                return [v for v in map(_shorten_dict, d) if v != []]

            return d
        
        path = self._path.removeprefix('resource_packs/').removeprefix('behavior_packs/').removeprefix(f'RP_{ANVIL.PASCAL_PROJECT_NAME}/').removeprefix(f'BP_{ANVIL.PASCAL_PROJECT_NAME}/')
        path = os.path.join(path, self._name + self._extension)
        if len(path) > 80:
            ANVIL.Logger.path_length_error(path)

        if self._shorten and type(self._content) is dict:
            self._content = _shorten_dict(self._content)
        
        _logger.object_exported(self._name)
        File(f'{self._name}{self._extension}', self._content, self._path, 'w')


class RawTextConstructor():
    def __init__(self):
        self._raw_text = []

    def style(self, *styles: Style):
        self._raw_text.append({'text': ''.join(styles)})
        return self

    def text(self, text):
        self._raw_text.append({'text': str(text)})
        return self

    def translate(self, text):
        self.id = f'raw_text_{ANVIL._tellraw_index}'
        ANVIL.localize(self.id, text)
        ANVIL._tellraw_index += 1
        self._raw_text.append({'translate': self.id, 'with': ['\n']})
        return self

    def score(self, objective, target):
        self._raw_text.append(
            {'score': {'name': target, 'objective': objective}})
        return self

    def selector(self, target):
        self._raw_text.append({'selector': target})
        return self

    def __str__(self) -> str:
        return f'{{"rawtext":{json.dumps(self._raw_text, ensure_ascii=False)}}}'

# ---------------------------------------------------------------
# Internal Only
# ---------------------------------------------------------------
class _MinecraftDescription():
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._identifier = identifier
        self._namespace_format = ANVIL.NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._description: dict = _JsonSchemes.description(self._namespace_format, self._identifier)

    @property
    def _export(self):
        return self._description


class _ItemTextures(AddonObject):
    _extensions = {
        0: '.json',
        1: '.json'
    }

    def __init__(self) -> None:
        super().__init__('item_texture', os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'))


        self.content(_JsonSchemes.item_texture(PROJECT_NAME))

    def add_item(self, item_name: str, directory, *item_sprites: str):
        for item in item_sprites:
            if not FileExists(os.path.join('assets', 'textures', 'items', f'{item}.png')):
                ANVIL.Logger.file_exist_error(f'{item}.png',os.path.join('assets', 'textures', 'items'))

        self._content['texture_data'][item_name] = {
            'textures' : [
                *[
                    os.path.join('textures', 'items', directory, sprite)
                    for sprite in item_sprites
                ]
            ]
        }

    @property
    def queue(self):
        return super().queue('')

    def _export(self):
        if len(self._content['texture_data']) > 0:
            for items in self._content['texture_data'].values():
                for sprite in items['textures']:
                    CopyFiles(
                        os.path.join('assets', 'textures', 'items'), 
                        os.path.join('resource_packs', f'RP_{ANVIL.PASCAL_PROJECT_NAME}', sprite.rstrip(sprite.split('/')[-1])), 
                        sprite.split('/')[-1] + '.png'
                    )
        return super()._export()


class _TerrainTextures(AddonObject):
    _extensions = {
        0: '.json',
        1: '.json'
    }

    def __init__(self) -> None:
        super().__init__('terrain_texture', os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'))
        self.content(_JsonSchemes.terrain_texture(PROJECT_NAME))

    def add_block(self, block_name: str, directory: str, *block_textures: str):
        self._content['texture_data'][block_name] = {
            "textures": [
                *[
                    os.path.join('textures', 'blocks', directory, face)
                    for face in block_textures
                ]
            ]}

    @property
    def queue(self):
        return super().queue()


class _SoundDefinition():
    def __init__(self, sound_definition: str, category, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999) -> None:
        self._category = category
        self._sound_definition = sound_definition
        self._sound = _JsonSchemes.sound(self._sound_definition, category)

        if use_legacy_max_distance != False:
            self._sound[self._sound_definition].update(
                {'__use_legacy_max_distance': use_legacy_max_distance})
        if max_distance != 0:
            self._sound[self._sound_definition].update(
                {'max_distance': max_distance})
        if min_distance != 9999:
            self._sound[self._sound_definition].update(
                {'min_distance': min_distance})
        self._sounds = []

    def add_sound(
        self,
        sound_name,
        volume: int = 1,
        weight: int = 1,
        pitch: int = [1, 1],
        is_3d: bool = None,
        stream: bool = None,
        load_on_low_memory: bool = False
    ):
        if not FileExists(os.path.join('assets', 'sounds', f'{sound_name}.ogg')):
            ANVIL.Logger.file_exist_error(f'{sound_name}.ogg', os.path.join('assets', 'sounds'))

        self._sound_name = sound_name
        splits = self._sound_definition.split(".")
        self._path = ''
        for i in range(len(splits)-1):
            self._path += f'{splits[i]}/'
        sound = {
            "name": os.path.join('sounds', self._path, self._sound_name)
        }
        if pitch != [1, 1]:
            sound.update({"pitch": pitch})
        if not is_3d is None:
            sound.update({"is3D": is_3d})
        if not stream is None:
            sound.update({"stream": stream})
        if load_on_low_memory:
            sound.update({"load_on_low_memory": load_on_low_memory})
        if volume != 1:
            sound.update({"volume": volume})
        if weight != 1:
            sound.update({"weight": weight})
        self._sounds.append(sound)
        ANVIL._sounds.update({self._sound_name: self._sound_definition})
        return self

    @property
    def _export(self):
        for sound in self._sounds:
            CopyFiles('assets/sounds', os.path.join('resource_packs',
                      f'RP_{ANVIL.PASCAL_PROJECT_NAME}', 'sounds', self._path), f'{sound["name"].split("/")[-1]}.ogg')
        self._sound[self._sound_definition]['sounds'] = self._sounds
        return self._sound


class _Sound(AddonObject):
    _extensions = {
        0: '.json',
        1: '.json'
    }

    def __init__(self) -> None:
        super().__init__('sound_definitions', os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'))
        self.content(_JsonSchemes.sound_definitions())
        self._sounds: list[_SoundDefinition] = []

    def sound_definition(self, sound_definition: str, category: SoundCategory, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
        sound = _SoundDefinition(
            sound_definition, category, use_legacy_max_distance, max_distance, min_distance)
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        return super().queue('')

    def _export(self):
        for sound in self._sounds:
            self._content['sound_definitions'].update(sound._export)
        return super()._export()


class _Music(AddonObject):
    _extensions = {
        0: '.json',
        1: '.json'
    }

    def __init__(self) -> None:
        super().__init__('music_definitions', os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'))
        self.content(_JsonSchemes.music_definitions())
        self._sounds: list[_SoundDefinition] = []

    def music_definition(self, music_category: MusicCategory, min_delay: int = 60, max_delay: int = 180):
        self._content.update({
            music_category: {
                "event_name": f"music.{music_category}",
                "max_delay": max_delay,
                "min_delay": min_delay
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


class _Materials(AddonObject):
    _extensions = {
        0: '.material',
        1: '.material'
    }

    def __init__(self) -> None:
        super().__init__('entity', os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'materials'))
        self._materials: list[_Material] = []

    def add_material(self, material_name, base_material):
        material = _Material(material_name, base_material)
        self._materials.append(material)
        return material

    @property
    def queue(self):
        if len(self._materials) > 0:
            self._content = _JsonSchemes.materials()
            for m in self._materials:
                self._content['materials'].update(m._queue)
            super().queue('')


class _DialogueButton():
    def __init__(self, button_name: str, *commands: str):
        self._button_name = button_name
        self._commands = [
            f'/{command}' if not str(command).startswith('/') else command for command in commands
        ]

    def _export(self):
        return _JsonSchemes.dialogue_button(self._button_name, self._commands)


class _DialogueScene():
    def __init__(self, scene_tag: str):
        self._tag = scene_tag
        self._buttons: list[_DialogueButton] = []
        self._on_open_commands = []
        self._on_close_commands = []
        self._npc_name = None
        self._text = None

    def properties(self, npc_name: str, text: str = ''):
        self._npc_name: str = RawTextConstructor().text(npc_name)
        if not text is None:
            self._text: str = RawTextConstructor().translate(text)
        return self

    def button(self, button_name: str, *commands: str):
        if len(self._buttons) >= 6:
            RaiseError(DIALOGUE_MAX_BUTTONS(self._tag, len(self._buttons)))
        # Buttons cannot be translated
        button = _DialogueButton(button_name, *commands)
        self._buttons.append(button)
        return self

    def on_open_commands(self, *commands: str):
        self._on_open_commands = commands
        return self

    def on_close_commands(self, *commands: str):
        self._on_close_commands = commands
        return self

    def _export(self):
        return _JsonSchemes.dialogue_scene(
            self._tag,
            self._npc_name.__str__(),
            self._text.__str__(),
            ['/' + cmd.__str__() for cmd in self._on_open_commands],
            ['/' + cmd.__str__() for cmd in self._on_close_commands],
            [button._export() for button in self._buttons]
        )


class _FogDistance():
    def __init__(self, camera_location: FogCameraLocation = FogCameraLocation.Air) -> None:
        self._camera_location = camera_location
        self._distance = {
            self._camera_location: {}
        }

    def color(self, color: str):
        self._distance[self._camera_location]['fog_color'] = color
        return self

    def distance(self, fog_start: int, fog_end: int, render_distance_type: RenderDistanceType = RenderDistanceType.Render):
        if fog_start >= fog_end:
            RaiseError(f'{ERROR}: fog_end must be greater than fog_start.')
        self._distance[self._camera_location]['fog_start'] = fog_start
        self._distance[self._camera_location]['fog_end'] = fog_end
        self._distance[self._camera_location]['render_distance_type'] = render_distance_type
        return self

    def transition_fog(self, color: str, fog_start: int, fog_end: int, render_distance_type: RenderDistanceType = RenderDistanceType.Render):
        if fog_start >= fog_end:
            RaiseError(f'{ERROR}: fog_end must be greater than fog_start.')
        self._distance[self._camera_location]['color'] = color
        self._distance[self._camera_location]['fog_start'] = fog_start
        self._distance[self._camera_location]['fog_end'] = fog_end
        self._distance[self._camera_location]['render_distance_type'] = render_distance_type
        return self

    def _export(self):
        return self._distance


class _Material():
    def __init__(self, material_name, base_material) -> None:
        self._material_name = f'{material_name}' + \
            f':{base_material}' if not base_material is None else ''
        self._material = {
            self._material_name: {}
        }

    def states(self, *states: MaterialStates):
        self._material[self._material_name]['states'] = states
        return self

    def remove_states(self, *states: MaterialStates):
        self._material[self._material_name]['-states'] = states
        return self

    def add_states(self, *states: MaterialStates):
        self._material[self._material_name]['+states'] = states
        return self

    def frontFace(self, stencilFunc: MaterialFunc = None, stencilFailOp: MaterialOperation = None, stencilDepthFailOp: MaterialOperation = None, stencilPassOp: MaterialOperation = None, stencilPass: MaterialOperation = None):
        a = {
            'stencilFunc': stencilFunc,
            'stencilFailOp': stencilFailOp,
            'stencilDepthFailOp': stencilDepthFailOp,
            'stencilPassOp': stencilPassOp,
            'stencilPass': stencilPass
        }
        self._material[self._material_name]['frontFace'] = {
            key: value for key, value in a.items() if value != None}
        return self

    def backFace(self, stencilFunc: MaterialFunc = None, stencilFailOp: MaterialOperation = None, stencilDepthFailOp: MaterialOperation = None, stencilPassOp: MaterialOperation = None, stencilPass: MaterialOperation = None):
        a = {
            'stencilFunc': stencilFunc,
            'stencilFailOp': stencilFailOp,
            'stencilDepthFailOp': stencilDepthFailOp,
            'stencilPassOp': stencilPassOp,
            'stencilPass': stencilPass
        }
        self._material[self._material_name]['backFace'] = {
            key: value for key, value in a.items() if value != None}
        return self

    def stencilRef(self, stencilRef: int):
        self._material[self._material_name]['stencilRef'] = stencilRef
        return self

    def depthFunc(self, depthFunc: MaterialFunc):
        self._material[self._material_name]['depthFunc'] = depthFunc
        return self

    def defines(self, *defines: MaterialDefinitions):
        self._material[self._material_name]['defines'] = defines
        return self

    def remove_defines(self, *defines: MaterialDefinitions):
        self._material[self._material_name]['-defines'] = defines
        return self

    def add_defines(self, *defines: MaterialDefinitions):
        self._material[self._material_name]['+defines'] = defines
        return self

    @property
    def _queue(self):
        return self._material


class _Bone():
    def __init__(self, name, pivot, parent) -> None:
        self._bone = {
            "name": name,
            "pivot": pivot,
            'parent': parent if not parent is None else {},
            "cubes": []
        }

    def add_cube(self,
                 origin: list[float, float, float],
                 size: list[float, float, float],
                 uv: list[int, int],
                 pivot: list[float, float, float] = (0, 0, 0),
                 rotation: list[float, float, float] = (0, 0, 0),
                 inflate: float = 0,
                 mirror: bool = False,
                 reset: bool = False,
                 uv_face: list[str, list[int, int], list[int, int]] = None
                 ):
        self._bone['cubes'].append({
            'origin': origin,
            'size': size,
            'uv': uv if uv_face is None else {
                uv_face[0]: {
                    'uv': uv_face[1],
                    'uv_size': uv_face[2]
                }
            },
            'pivot': pivot if not pivot == (0, 0, 0) else {},
            'rotation': rotation if not rotation == (0, 0, 0) else {},
            'inflate': inflate if not inflate == 0 else {},
            'mirror': mirror if mirror else {},
            'reset': reset if reset else {},
        })
        return self

    @property
    def _queue(self):
        return self._bone


class _Geo():
    def __init__(self, geometry_name: str, texture_size: list[int, int] = (16, 16)) -> None:
        self._geo_name = geometry_name
        self._geo = {
            "description": {
                "identifier": f"geometry.{ANVIL.NAMESPACE}.{geometry_name}",
                "texture_width": texture_size[0],
                "texture_height": texture_size[1],
            },
            "bones": [],
        }
        self._bones: list[_Bone] = []

    def set_visible_bounds(self, visible_bounds_wh: list[float, float], visible_bounds_offset: list[float, float, float]):
        self._geo['description']['visible_bounds_width'] = visible_bounds_wh[0]
        self._geo['description']['visible_bounds_height'] = visible_bounds_wh[1]
        self._geo['description']['visible_bounds_offset'] = visible_bounds_offset
        return self

    def add_bone(self, name: str, pivot: list[int, int, int], parent: str = None):
        bone = _Bone(name, pivot, parent)
        self._bones.append(bone)
        return bone

    @property
    def _queue(self):
        for bone in self._bones:
            self._geo['bones'].append(bone._queue)
        return self._geo


class _Anim_Bone():
    def __init__(self, name) -> None:
        self._name = name
        self._bone = {
            self._name: {}
        }

    def rotation(self, rotation: list[float, float, float] = (0, 0, 0),):
        self._bone[self._name].update({
            'rotation': rotation
        })
        return self

    def position(self, position: list[float, float, float] = (0, 0, 0),):
        self._bone[self._name].update({
            'position': position
        })
        return self

    def scale(self, scale: Union[list[float, float, float], float, Molang] = 1):
        self._bone[self._name].update({
            'scale': scale if scale != 1 else {}
        })
        return self

    @property
    def _queue(self):
        return self._bone


class _Anims():
    def __init__(self, name, animation_name: str, loop: bool = False, override_previous_animation: bool = False) -> None:
        self._name = name
        self._anim_name = animation_name
        self._loop = loop
        self._override_previous_animation = override_previous_animation
        self._anim = {
            f"animation.{ANVIL.NAMESPACE}.{self._name}.{self._anim_name}": {
                "loop": self._loop,
                "override_previous_animation": self._override_previous_animation,
                "bones": {}
            }
        }
        self._bones: list[_Anim_Bone] = []

    def add_bone(self, name: str):
        bone = _Anim_Bone(name)
        self._bones.append(bone)
        return bone

    @property
    def _queue(self):
        for bone in self._bones:
            self._anim[f"animation.{ANVIL.NAMESPACE}.{self._name}.{self._anim_name}"]['bones'].update(
                bone._queue)
        return self._anim


class _BlocksJSON(AddonObject):
    _extensions = {
        0: '.json',
        1: '.json'
    }

    def __init__(self) -> None:
        super().__init__('blocks', os.path.join('resource_packs', f'RP_{ANVIL.PASCAL_PROJECT_NAME}'))
        self.content(_JsonSchemes.blocks(ANVIL.PROJECT_NAME))

    def add_block(self, block_name: str):
        self._content['texture_data'][block_name] = {
            "sound": "",
            # "textures":{},
            # "carried_textures":{},
            # "brightness_gamma": 0,
            # "isotropic":True
        }


class Geometry(AddonObject):
    _extensions = {
        0: '.geo.json',
        1: '.geo.json'
    }

    def __init__(self, name: str) -> None:
        super().__init__(name, os.path.join('assets', 'models'))
        self._geos: list[_Geo] = []

    def add_geo(self, geometry_name: str, texture_size: tuple[int, int] = (16, 16)):
        geo = _Geo(geometry_name, texture_size)
        self._geos.append(geo)
        return geo

    def queue(self, type: str):
        if not type in ['entity', 'attachables', 'blocks']:
            RaiseError('Unsupported model type')

        if len(self._geos) == 0:
            RaiseError(
                f'The Geometry file {self._name} does not have any geometry.')

        if FileExists(os.path.join('assets', 'models', type, f'{self._name}.geo.json')):
            with open(os.path.join('assets', 'models', type, f'{self._name}.geo.json'), 'r') as file:
                self.content(commentjson.load(file))
        else:
            self.content(_JsonSchemes.geometry())

        for g in self._geos:
            for geo in self._content['minecraft:geometry']:
                if f"geometry.{ANVIL.NAMESPACE}.{g._geo_name}" == geo['description']['identifier']:
                    self._content['minecraft:geometry'].remove(geo)

            self._content['minecraft:geometry'].append(g._queue)
        super().queue(type)
        super()._export()


class Animation(AddonObject):
    _extensions = {
        0: '.animation.json',
        1: '.animation.json'
    }

    def __init__(self, name: str) -> None:
        super().__init__(name, os.path.join('assets', 'animations'))

        self._name = name
        self._anims: list[_Anims] = []

    def add_animation(self, animation_name: str, loop: bool = False, override_previous_animation: bool = False):
        geo = _Anims(self._name, animation_name, loop, override_previous_animation)
        self._anims.append(geo)
        return geo

    @property
    def queue(self):
        if len(self._anims) == 0:
            RaiseError(f'The Animation file {self._name} does not have any animations.')
        path = os.path.join('assets', 'animations', f'{self._name}{self._extension}')
        if FileExists(path):
            with open(path, 'r') as file:
                self.content(commentjson.load(file))
        else:
            self.content(_JsonSchemes.rp_animations())

        for a in self._anims:
            self._content['animations'].update(a._queue)

        super().queue()
        self._export()


class LootTable(AddonObject):
    _extensions = {
        0: ".loot_table.json", 
        1: ".loot_table.json"
    }
    class _LootPool():
        class _entry():
            class _Functions():
                def __init__(self) -> None:
                    pass

                def SetBookContent(self, author: str, title: str, *pages: str):
                    self._func = {
                        "author": author,
                        "title": title,
                        "pages": [str(p) for p in pages],
                        "function": "set_book_contents",
                    }
                    return self

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
                        RaiseError(
                            'SetDamage value cannot be above the maximum of 1.')
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
            entry = self._entry(str(name), count, weight, entry_type)
            self._entries.append(entry)
            return entry

        def _export(self):
            for entry in self._entries:
                if 'entries' not in self._pool:
                    self._pool.update({'entries': []})
                self._pool["entries"].append(entry._export())
            return self._pool

    def __init__(self, name: str):
        super().__init__(name, os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "loot_tables"))
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


class Recipe(AddonObject):
    _extensions = {
        0: ".recipe.json", 
        1: ".recipe.json"
    }
    class _Crafting():
        class _Shapeless():
            def __init__(self, parent, identifier, output_item_id: str, data: int = 0, count: int = 1):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 9
                self._ingredients = []
                self._default = Defaults(
                    'recipe_shapeless', self._identifier, output_item_id, data, count, ANVIL.NAMESPACE)

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                item_id = str(item_id)
                if self._item_count == 0:
                    RaiseError(f'The recipe {self._parent._name} has more than 9 items')
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
                    'recipe_shaped', self._identifier, output_item_id, data, count, ANVIL.NAMESPACE)
                self._grid = [[' ' for i in range(3)] for j in range(3)]

            def item_0_0(self, item_identifier: str = ' ', data: int = 0):
                self._grid[0][0] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_0_1(self, item_identifier: str = ' ', data: int = 0):
                self._grid[0][1] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_0_2(self, item_identifier: str = ' ', data: int = 0):
                self._grid[0][2] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_1_0(self, item_identifier: str = ' ', data: int = 0):
                self._grid[1][0] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_1_1(self, item_identifier: str = ' ', data: int = 0):
                self._grid[1][1] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_1_2(self, item_identifier: str = ' ', data: int = 0):
                self._grid[1][2] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_2_0(self, item_identifier: str = ' ', data: int = 0):
                self._grid[2][0] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_2_1(self, item_identifier: str = ' ', data: int = 0):
                self._grid[2][1] = {'item': item_identifier,
                                    'data': data}
                return self

            def item_2_2(self, item_identifier: str = ' ', data: int = 0):
                self._grid[2][2] = {'item': item_identifier,
                                    'data': data}
                return self

            def queue(self):
                for i in range(0, 3):  # Row
                    for j in range(0, 3):  # Column
                        current_item = str(self._grid[i][j]['item']) if type(self._grid[i][j]) is dict else ' '
                        current_data = self._grid[i][j]['data'] if type(
                            self._grid[i][j]) is dict else 0
                        current_key = self._keys[0]
                        if current_item != ' ':
                            if current_item not in self._items:
                                self._items.update({
                                    current_item: {
                                        'key': current_key,
                                        'data': current_data
                                    }
                                })
                                self._pattern[i] = self._pattern[i][:j] + \
                                    current_key+self._pattern[i][j+1::]
                                self._keys = self._keys[1::]
                                self._key.update({
                                    current_key: {
                                        'item': current_item,
                                        'data': current_data
                                    }
                                })
                            elif current_data != self._items[current_item]['data']:
                                self._items.update({
                                    current_item: {
                                        'key': current_key,
                                        'data': current_data
                                    }
                                })
                                self._pattern[i] = self._pattern[i][:j] + \
                                    current_key+self._pattern[i][j+1::]
                                self._keys = self._keys[1::]
                                self._key.update({
                                    current_key: {
                                        'item': current_item,
                                        'data': current_data
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
                    'recipe_stonecutter', self._identifier, output_item_id, data, count, ANVIL.NAMESPACE)

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
                    'recipe_stonecutter', self._identifier, output_item_id, data, count, ANVIL.NAMESPACE)

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
                    'recipe_smithing_table', self._identifier, output_item_id, data, count, ANVIL.NAMESPACE)

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
        super().__init__(name, os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "recipe"))

    def crafting(self, identifier: str):
        return self._Crafting(self, identifier)

    def smelting(self, identifier: str):
        return self._Smelting(self, identifier)


class Particle(AddonObject):
    _extensions = {
        0: ".particle.json", 
        1: ".particle.json"
    }
    
    def __init__(self, particle_name, use_vanilla_texture: bool = False):
        super().__init__(particle_name, os.path.join("resource_packs", f"RP_{ANVIL.PASCAL_PROJECT_NAME}", "particles"))
        self._name = particle_name
        self._content = ''
        self._use_vanilla_texture = use_vanilla_texture

    def queue(self):
        return super().queue('particles')

    def _export(self):
        if self._content != '':
            super()._export()
        if not self._use_vanilla_texture:
            if FileExists(os.path.join('assets', 'particles', f'{self._name}.png')):
                CopyFiles('assets/particles',f'resource_packs/RP_{ANVIL.PASCAL_PROJECT_NAME}/textures/particle', f'{self._name}.png')
            else:
                ANVIL.Logger.file_exist_error(f'{self._name}.png', os.path.join('assets', 'particles'))
        
        if FileExists(os.path.join('assets', 'particles', f'{self._name}.particle.json')):
            CopyFiles('assets/particles',f'resource_packs/RP_{ANVIL.PASCAL_PROJECT_NAME}/particles', f'{self._name}.particle.json')
        else:
            ANVIL.Logger.file_exist_error(f'{self._name}.particle.json', os.path.join('assets', 'particles'))


class Dialogue(AddonObject):
    _extensions = {
        0: '.dialogue.json',
        1: '.dialogue.json'
    }

    def __init__(self, name: str) -> None:
        super().__init__(name, os.path.join("behavior_packs", f"BP_{ANVIL.PASCAL_PROJECT_NAME}", "dialogue"))
        self._dialogues = _JsonSchemes.dialogues()
        self._scenes = []

    def add_scene(self, scene_tag: str):
        scene = _DialogueScene(scene_tag)
        self._scenes.append(scene)
        return scene

    def queue(self, directory: str = None):
        for scene in self._scenes:
            self._dialogues['minecraft:npc_dialogue']['scenes'].append(
                scene._export())
        self.content(self._dialogues)
        return super().queue(directory)


class Function(AddonObject):
    _extensions = {
        0: '.mcfunction',
        1: '.mcfunction',
    }

    _ticking: list['Function'] = set()
    _setup: list['Function'] = set()

    def __init__(self, name: str) -> None:
        super().__init__(name, os.path.join('behavior_packs', f'BP_{ANVIL.PASCAL_PROJECT_NAME}', 'functions'))
        self._function: list[str] = []
        self._sub_functions: list[Function] = [self]

    def add(self, *functions: str):
        if len(self._sub_functions[-1]._function) >= 10000-len(functions)-1:
            self._sub_functions.append(
                Function(f'{self._name}_{len(self._sub_functions)}'))

        self._sub_functions[-1]._function.extend([str(func)
                                                 for func in functions])
        return self

    @property
    def path(self):
        return os.path.join(self._directory, self._name).replace('\\', '/')

    @property
    def execute(self):
        return f'function {self.path}'

    @property
    def tick(self):
        Function._ticking.add(self)
        return self
    
    @property
    def add_to_setup(self):
        Function._setup.add(self)
        return self

    def queue(self, directory: str = None):
        self._directory = directory
        return super().queue(self._directory)

    def __len__(self):
        return len(self._function)
    
    def _export(self):
        for function in self._sub_functions[1:]:
            function.content('\n'.join(function._function)
                             ).queue(self._directory)
        self.content('\n'.join(self._function))
        if len(self._function) > 0:
            return super()._export()


class Fog(AddonObject):
    _extensions = {
        0: '.fog.json',
        1: '.fog.json',
    }

    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, os.path.join('resource_packs', f'RP_{ANVIL.PASCAL_PROJECT_NAME}', 'fogs'))
        self._identifier = identifier
        self._description = _MinecraftDescription(self._identifier, is_vanilla)
        self._fog = _JsonSchemes.fog()
        self._locations: list[_FogDistance] = []
        self._volumes = []

    def add_distance_location(self, camera_location: FogCameraLocation = FogCameraLocation.Air):
        self._locations.append(_FogDistance(camera_location))
        return self._locations[-1]

    def add_volume(self):
        pass

    @property
    def queue(self):
        for location in self._locations:
            self._fog['minecraft:fog_settings']['distance'].update(
                location._export())
        self._fog['minecraft:fog_settings'].update(self._description._export)
        self.content(self._fog)
        return super().queue()

# Fully Implemented
class SkinPack(AddonObject):
    def __init__(self) -> None:
        super().__init__('skins', os.path.join('assets', 'skins'))
        self.content(_JsonSchemes.skins_json(ANVIL.PROJECT_NAME))

    def add_skin(self, filename: str, display_name: str, is_slim: bool = False, free: bool = False):
        if not FileExists(os.path.join(self._path, f'{filename}.png')):
            ANVIL.Logger.file_exist_error(f'{filename}.png', self._path)
        self._content['skins'].append({
            "localization_name": filename,
            "geometry": f"geometry.humanoid.{ 'customSlim' if is_slim else 'custom'}",
            "texture": f"{filename}.png",
            "type": "free" if free else "paid"
        })
        ANVIL._skins_langs[f'skin.{ANVIL.PROJECT_NAME}.{filename}'] = display_name

    def queue(self):
        ANVIL._queue(self)

    def _export(self):
        l = _JsonSchemes.skin_pack_name_lang(ANVIL.PROJECT_NAME, ANVIL.PROJECT_NAME + ' Skin Pack')
        l.extend([f'{k}={v}' for k,v in ANVIL._skins_langs.items()])

        File('languages.json', _JsonSchemes.languages(), self._path, 'w')
        File("manifest.json", _JsonSchemes.manifest_skins(ANVIL.RELEASE), self._path, "w")
        File('en_US.lang', '\n'.join(l), os.path.join(self._path, 'texts'), 'w')
        
        super()._export()

# ---------------------------------------------------------------

class Fonts():
    def __init__(self) -> None:
        self._image = None
        self._path = os.path.join('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'font')

    def generate_font(self, font_name: str, character_size: int = 32):
        if character_size % 16 != 0:
            RaiseError(UNSUPPORTED_FONT_SIZE)
        
        font_size = round(character_size*.8)
        image_size = character_size*16

        try:
            font = ImageFont.truetype(f'assets/textures/ui/{font_name}.ttf', font_size)
        except FileNotFoundError:
            font = ImageFont.truetype(f'assets/textures/ui/{font_name}.otf', font_size)
        except:
            font = ImageFont.truetype(f'{font_name}.ttf', font_size)


        self._image = Image.new("RGBA", (image_size, image_size))
        backup_font = ImageFont.truetype('arial.ttf', font_size)

        ascii = u'ÀÁÂÈÉÊÍÓÔÕÚßãõǧÎ¹ŒœŞşŴŵŽê§©      !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂'
        extended_ascii = u'ÇüéâäàåçêëèïîìÄÅÉ§ÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴├├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■	'
        default8 = ascii + extended_ascii

        offset = [0, 0]

        img_draw = ImageDraw.Draw(self._image)
        for i in default8:
            bbox = font.getbbox(i)
            img_draw.text(
                (offset[0]*character_size - bbox[0], offset[1]*character_size), i, 
                fill=(255, 255, 255), font=font if i in ascii else backup_font, align='cl')

            offset[0] += 1
            if offset[0] >= 16:
                offset[0] = 0
                offset[1] += 1

        return self

    @property
    def queue(self):
        if not self._image is None:
            self._image.save(
                os.path.join('assets', 'textures', 'ui', 'default8.png'))

        for file in ['glyph_E1.png', 'default8.png']:
            if FileExists(os.path.join('assets', 'textures', 'ui', file)):
                CopyFiles(os.path.join('assets', 'textures', 'ui'), self._path, file)


class Structure():
    def __init__(self, structure_name):
        self._structure_name = structure_name
        CheckAvailability(f'{self._structure_name}.mcstructure',
                          'structure', os.path.join('assets', 'structures'))

    @property
    def queue(self):
        ANVIL._queue(self)

    @property
    def identifier(self):
        return f'{ANVIL.NAMESPACE_FORMAT}:{self._structure_name}'

    def _export(self):
        CopyFiles(
            os.path.join('assets', 'structures'),
            os.path.join('behavior_packs', f"BP_{ANVIL.PASCAL_PROJECT_NAME}", 'structures',
                     ANVIL.NAMESPACE_FORMAT, f"{self._structure_name}.mcstructure")
        )


class _Anvil():
    def _check_vanilla(self):
        import requests
        build = self.Config.get('ANVIL', 'BUILD')
        try:
            response = requests.get(f'https://raw.githubusercontent.com/Mojang/bedrock-samples/{build.lower()}/version.json')
            return response.json()['latest']['version']
        except:
            print('Could not receive latest build number.')
            return self.VANILLA_VERSION

    def _clone_vanilla(self):
        import git
        build = self.Config.get('ANVIL', 'BUILD')
        repo = git.Repo.clone_from(
            'https://github.com/Mojang/bedrock-samples.git',
            os.path.join('assets', 'vanilla'),
            branch=build.lower()
        )
    
    def _pull_vanilla(self):
        import git
        git.Remote(git.Repo(os.path.join('assets', 'vanilla')), 'origin').pull()

    def get_github_file(self, path: str):
        if not FileExists(os.path.join('assets', 'vanilla', path)):
            self._clone_vanilla()

        with open(os.path.join('assets', 'vanilla', path), 'r') as file:
            r = json.load(file)
        return r

    def __init__(self, config: _Config, logger: _Logger):
        # ------------------------------------------------------------------------
        self.Logger = logger
        self.Logger.header()

        self.Config = config
        # ------------------------------------------------------------------------
        self.VANILLA_VERSION = self.Config.get('MINECRAFT', 'VANILLA_VERSION')
        self.COMPANY = self.Config.get('PACKAGE', 'COMPANY')
        self.NAMESPACE = self.Config.get('PACKAGE', 'NAMESPACE')
        self.PROJECT_NAME = self.Config.get('PACKAGE', 'PROJECT_NAME')
        self.DISPLAY_NAME = self.Config.get('PACKAGE', 'DISPLAY_NAME')
        self.PROJECT_DESCRIPTION = self.Config.get('PACKAGE', 'PROJECT_DESCRIPTION')
        self.RELEASE = self.Config.get('BUILD', 'RELEASE')
        self.DEBUG = int(self.Config.get('ANVIL', 'DEBUG'))
        self.NAMESPACE_FORMAT_BIT = int(self.Config.get('ANVIL', 'NAMESPACE_FORMAT'))
        self.NAMESPACE_FORMAT = self.NAMESPACE + f'.{self.PROJECT_NAME}' * self.NAMESPACE_FORMAT_BIT
        self.PASCAL_PROJECT_NAME = self.Config.get('ANVIL', 'PASCAL_PROJECT_NAME')
        self.LAST_CHECK = self.Config.get('ANVIL', 'LAST_CHECK')
        self.LATEST_BUILD = self.VANILLA_VERSION

        global PASCAL_PROJECT_NAME, PROJECT_NAME
        PASCAL_PROJECT_NAME = self.PASCAL_PROJECT_NAME
        PROJECT_NAME = self.PROJECT_NAME
        # ------------------------------------------------------------------------
        self._objects_list: list[AddonObject] = []
        self._item_texture = _ItemTextures()
        self._terrain_texture = _TerrainTextures()
        self._sound_definition = _Sound()
        self._music_definition = _Music()
        self._materials = _Materials()
        # ------------------------------------------------------------------------
        # Tracks scores
        self._scores = {self.PROJECT_NAME: 0}
        # Tracks key-value langs
        self._langs = {}
        # Tracks skins key-value langs
        self._skins_langs = {}
        self._tags = []
        # ----------------------------------
        self._sounds = {}
        self._tellraw_index = 0
        self._score_index = 0
        self._deltatime = int((datetime.now() - datetime.strptime(self.LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds())
        self._github = None
        self._compiled = False
        #click.echo(EXECUTION_TIME(datetime.now().strptime(LAST_CHECK, "%Y-%m-%d %H:%M:%S")))
        # 12 Hours
        if (self._deltatime < 12*3600):
            click.echo(self.CHECK_UPDATE)
            self.LATEST_BUILD = self._check_vanilla()
            if self.VANILLA_VERSION < self.LATEST_BUILD:
                self.Logger.new_minecraft_build(self.VANILLA_VERSION, self.LATEST_BUILD)
                self._pull_vanilla()
            else:
                click.echo(self.Logger.minecraft_build_up_to_date())

            self.Config.set('MINECRAFT', 'VANILLA_VERSION', self.LATEST_BUILD)
            self.Config.set('ANVIL', 'LAST_CHECK', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def sound(self, sound_definition: str, category: SoundCategory, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
        return self._sound_definition.sound_definition(sound_definition, category, use_legacy_max_distance, max_distance, min_distance)

    def music(self, music_category: MusicCategory, min_delay: int = 60, max_delay: int = 180):
        return self._music_definition.music_definition(music_category, min_delay, max_delay)

    def localize(self, key, text) -> None:
        """
        Adds a localized string to en_US. Translatable.

        Parameters:
        ---------
        `texts` : `kwargs`
            Minecraft lang key-value pair.

        Examples:
        ---------
        >>> ANVIL.localize(raw_text_0, "Created with Anvil")
        """
        if key not in self._langs:
            self._langs[key] = text

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
                RaiseError(self.Logger.score_error(score_id))
            if score_id not in self._scores:
                self._scores[score_id] = score_value

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

    def _tick(self, *functions) -> None:
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

        self._tick_functions.extend(functions)

    def add_material(self, material_name, base_material: str | None = None):
        return self._materials.add_material(material_name=material_name, base_material=base_material)

    def _setup(self, *functions) -> None:
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
        self._setup_functions.extend(functions)

    def _translate(self, include_skin_pack: bool = False) -> None:
        """
        Translates en_US to all supported Minecraft languages.
        This is a time consuming function, it will be executed with anvil.package(), so it's better to avoid it unless you really want to use it.


        Usage:
        ---------
        >>> ANVIL.translate
        """
        from deep_translator import GoogleTranslator
        def _to_lang(translator: GoogleTranslator, langs: dict, skins: bool = False):
            if skins: translated = _JsonSchemes.skin_pack_name_lang(self.PROJECT_NAME, self.PROJECT_NAME + ' Skin Pack')
            else: translated = _JsonSchemes.pack_name_lang(self.PROJECT_NAME, self.PROJECT_NAME)
            for k, v in langs.items():
                translated.append(f'{k}={translator.translate(v)}')
            return translated

        for language in _JsonSchemes.languages():
            destination_language = language.replace('zh_CN', 'zh-CN').replace('zh_TW', 'zh-TW').replace('nb_NO', 'no').split('_')[0]
            if not FileExists(os.path.join('resource_packs', f'RP_{self.PASCAL_PROJECT_NAME}', 'texts', f'{language}.lang')):
                self._langs = dict(sorted(self._langs.items()))
                Translator = GoogleTranslator(target=destination_language)
                File(f'{language}.lang', "\n".join(_to_lang(Translator, self._langs)), os.path.join('resource_packs', f'RP_{self.PASCAL_PROJECT_NAME}', 'texts'), 'w')
                File(f'{language}.lang', "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)), os.path.join('behavior_packs', f'BP_{self.PASCAL_PROJECT_NAME}', 'texts'), 'w')
                File(f'{language}.lang', "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)), os.path.join('texts'), 'w')
                if include_skin_pack:
                    self._skins_langs = dict(sorted(self._skins_langs.items())) 
                    File(f'{language}.lang', "\n".join(_to_lang(Translator, self._skins_langs, True)), os.path.join('assets', 'skins', 'texts'), 'w')
    
    @property
    def compile(self) -> None:
        """
        Compiles queued anvil objects.
        This function must be called last at the very end of your script.


        Usage:
        ---------
        >>> ANVIL.compile
        """
        l = _JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)
        l.extend([f'{k}={v}' for k,v in self._langs.items()])
        
        File('languages.json', _JsonSchemes.languages(), os.path.join('behavior_packs', f'BP_{self.PASCAL_PROJECT_NAME}', 'texts'), 'w')
        File('languages.json', _JsonSchemes.languages(), os.path.join('resource_packs', f'RP_{self.PASCAL_PROJECT_NAME}', 'texts'), 'w')
        File('languages.json', _JsonSchemes.languages(), 'texts', 'w')


        File('en_US.lang', "\n".join(l), f'resource_packs/RP_{self.PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)), f'behavior_packs/BP_{self.PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', "\n".join(_JsonSchemes.pack_name_lang(self.DISPLAY_NAME, self.PROJECT_DESCRIPTION)), 'texts', 'w')
        
        File("manifest.json", _JsonSchemes.manifest_rp(self.RELEASE, self.Config.get('BUILD', 'RP_UUID'), self.Config.get('ANVIL', 'PBR')), os.path.join('resource_packs',f'RP_{self.PASCAL_PROJECT_NAME}'), "w")
        File("manifest.json", _JsonSchemes.manifest_bp(self.RELEASE, self.Config.get('BUILD', 'BP_UUID'), self.Config.get('ANVIL', 'SCRIPTAPI')), os.path.join('behavior_packs',f'BP_{self.PASCAL_PROJECT_NAME}'), "w")
        File("manifest.json", _JsonSchemes.manifest_world(self.RELEASE, self.Config.get('BUILD', 'PACK_UUID'), self.COMPANY), "", "w")

        File("world_resource_packs.json", _JsonSchemes.world_packs(self.Config.get('BUILD', 'RP_UUID'), self.RELEASE), ".", "w")
        File("world_behavior_packs.json", _JsonSchemes.world_packs(self.Config.get('BUILD', 'BP_UUID'), self.RELEASE), ".", "w")
        
        if self.Config.get('ANVIL', 'SCRIPTAPI'):
            File("package.json", _JsonSchemes.packagejson(self.PROJECT_NAME, ".".join(str(i) for i in self.RELEASE), self.PROJECT_DESCRIPTION, self.COMPANY), "", "w", True)

        if FileExists('assets/textures/gui'):
            CopyFolder('assets/textures/gui',
                       f'resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/gui')
        if FileExists('assets/textures/environment'):
            CopyFolder('assets/textures/environment',
                       f'resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/environment')
        
        for ui in [
            'hotbar_start_cap.png',
            'hotbar_0.png',
            'hotbar_1.png',
            'hotbar_2.png',
            'hotbar_3.png',
            'hotbar_4.png',
            'hotbar_5.png',
            'hotbar_6.png',
            'hotbar_7.png',
            'hotbar_8.png',
            'hotbar_end_cap.png',
            'selected_hotbar_slot.png',
        ]:
            if FileExists(f'assets/textures/ui/{ui}'):
                CopyFiles('assets/textures/ui',
                           f'resource_packs/RP_{self.PASCAL_PROJECT_NAME}/textures/ui', ui)

        self._setup_function = Function('setup')
        for f in Function._setup:
            self._setup_function.add(f.execute)
        self._setup_function.queue()

        File('tick.json', 
             {'values': [f'{f.path}' for f in Function._ticking]}, 
             os.path.join('behavior_packs', f'BP_{self.PASCAL_PROJECT_NAME}', 'functions'), 
             'w')

        self._setup_scores = Function('setup_scores')
        self._remove_scores = Function('remove_scores')
        self._remove_tags = Function('remove_tags')
        self._setup_scores.add(f'scoreboard objectives add {self.PROJECT_NAME} dummy "{self.DISPLAY_NAME}"')
        self._remove_scores.add(f'scoreboard objectives remove {self.PROJECT_NAME}\n')

        self._setup_scores.queue(os.path.join('StateMachine', 'misc'))
        self._remove_scores.queue(os.path.join('StateMachine', 'misc'))
        self._remove_tags.queue(os.path.join('StateMachine', 'misc'))
        
        self._setup_function.add(self._remove_tags.execute).add(self._remove_scores.execute).add(self._setup_scores.execute)
        self._setup_function.queue()

        for object in self._objects_list:
            object._export()

        self._compiled = True

    def package(self, skip_translation: bool = False, include_skin_pack: bool = False, apply_overlay: bool = False) -> None:
        """
        Compiles queued anvil objects, translates and packages the project.
        This function should be called at the end of development and playtesting, it packages the project and exports a submission ready .zip file.

        Notes:
        ---------
        List of items that must exist under assets/marketing
        `0-4.png`: Marketing art, must all be `1920x1080`
        `keyart.png`: Marketing Keyart, must be `1920x1080`

        Usage:
        ---------
        >>> ANVIL.package()
        >>> ANVIL.package(True)
        """
        
        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_zip()
        
        content_structure = {}

        def art():
            pack_icon_size = (256, 256)
            marketing_screenshot_size = (1920, 1080)
            store_screenshot_size = (800, 450)

            source = os.path.join('assets', 'marketing')
            output_store = os.path.join('assets', 'output', 'Store Art')
            output_marketing = os.path.join('assets', 'output', 'Marketing Art')

            CreateDirectory(output_store)
            CreateDirectory(output_marketing)

            if FileExists(os.path.join(source, 'pack_icon.png')):
                CopyFiles(source, os.path.join('behavior_packs',
                          f'BP_{self.PASCAL_PROJECT_NAME}'), 'pack_icon.png')
                CopyFiles(source, os.path.join('resource_packs',
                          f'RP_{self.PASCAL_PROJECT_NAME}'), 'pack_icon.png')
                original = Image.open(os.path.join(source, 'pack_icon.png'))
                resized = original.resize(pack_icon_size)
                resized.convert("RGB").save(os.path.join(
                    output_store, f'{self.PROJECT_NAME}_packicon_0.jpg'), dpi=(72, 72), quality=95)
            else:
                self.Logger.file_exist_warning('pack_icon.png')
            if FileExists(os.path.join(source, 'keyart.png')):
                original = Image.open(os.path.join(source, 'keyart.png')).convert('RGB')
                if apply_overlay:
                    overlay = Image.open(os.path.join(source, 'keyart_overlay.png'))

                resized = original.resize(store_screenshot_size)
                if apply_overlay:
                    resize_overlay = overlay.resize(store_screenshot_size)
                    resized.paste(resize_overlay, mask=resize_overlay.split()[3])
                resized.save('world_icon.jpeg', dpi=(72, 72), quality=300)
                resized.save(os.path.join(output_store, f'{self.PROJECT_NAME}_Thumbnail_0.jpg'), dpi=(72, 72), quality=300)

                resized = original.resize(marketing_screenshot_size)
                if apply_overlay:
                    resize_overlay = overlay.resize(store_screenshot_size)
                    resized.paste(resize_overlay, mask=overlay.split()[3])
                resized.save(os.path.join(output_marketing, f'{self.PROJECT_NAME}_MarketingKeyArt.jpg'), dpi=(300, 300), quality=300)

            else:
                self.Logger.file_exist_warning('keyart.png')
            if FileExists(os.path.join(source, 'panorama.png')):
                original = Image.open(os.path.join(source, 'panorama.png'))
                scale_factor = 450/original.size[1]
                resized = original.resize(
                    (round(original.size[0]*scale_factor), 450))
                resized.convert("RGB").save(os.path.join(
                    output_store, f'{self.PROJECT_NAME}_panorama_0.jpg'), dpi=(72, 72), quality=95)
            else:
                self.Logger.file_exist_warning('panorama.png')
            for i in range(5):
                if FileExists(os.path.join(source, f'{i}.png')):
                    original = Image.open(os.path.join(source, f'{i}.png'))
                    resized = original.resize(store_screenshot_size)
                    resized.convert("RGB").save(os.path.join(
                        output_store, f'{self.PROJECT_NAME}_screenshot_{i}.jpg'), dpi=(72, 72), quality=95)
                    resized = original.resize(marketing_screenshot_size)
                    resized.convert("RGB").save(os.path.join(
                        output_marketing, f'{self.PROJECT_NAME}_MarketingScreenshot_{i}.jpg'), dpi=(300, 300), quality=100)
                else:
                    self.Logger.file_exist_warning(f'{i}.png')
            if FileExists(os.path.join(source, 'partner_art.png')):
                original = Image.open(os.path.join(source, 'partner_art.png'))
                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(os.path.join(
                    output_marketing, f'{self.PROJECT_NAME}_PartnerArt.jpg'), dpi=(300, 300), quality=100)
            else:
                self.Logger.file_exist_warning('partner_art.png')

        if not skip_translation:
            self._translate(include_skin_pack)
        if include_skin_pack:
            content_structure.update({
                os.path.join('assets', 'skins'): os.path.join('Content', 'skin_pack'),
            })

        art()
        content_structure.update({
            os.path.join('assets', 'output', 'Store Art'):              os.path.join('Store Art'),
            os.path.join('assets', 'output', 'Marketing Art'):          os.path.join('Marketing Art'),
            'resource_packs':                                           os.path.join('Content', 'world_template', 'resource_packs'),
            'behavior_packs':                                           os.path.join('Content', 'world_template', 'behavior_packs'),
            'texts':                                                    os.path.join('Content', 'world_template', 'texts'),
            'db':                                                       os.path.join('Content', 'world_template', 'db'),
            'level.dat':                                                os.path.join('Content', 'world_template'),
            'levelname.txt':                                            os.path.join('Content', 'world_template'),
            'manifest.json':                                            os.path.join('Content', 'world_template'),
            'world_icon.jpeg':                                          os.path.join('Content', 'world_template'),
            'world_behavior_packs.json':                                os.path.join('Content', 'world_template'),
            'world_resource_packs.json':                                os.path.join('Content', 'world_template'),
        })
        zipit(os.path.join('assets', 'output',f'{self.PROJECT_NAME}.zip'), content_structure)

        RemoveDirectory(os.path.join('assets', 'output', 'Store Art'))
        RemoveDirectory(os.path.join('assets', 'output', 'Marketing Art'))

    @property
    def mcaddon(self):
        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_mcaddon()

        source = os.path.join('assets', 'marketing')
        output = os.path.join('assets', 'output')
        if FileExists(os.path.join(source, 'pack_icon.png')):
            CopyFiles(source, os.path.join('behavior_packs',
                      f'BP_{self.PASCAL_PROJECT_NAME}'), 'pack_icon.png')
            CopyFiles(source, os.path.join('resource_packs',
                      f'RP_{self.PASCAL_PROJECT_NAME}'), 'pack_icon.png')

        resource_packs_structure = {os.path.join('resource_packs', f'RP_{self.PASCAL_PROJECT_NAME}'): '', }
        behavior_packs_structure = {os.path.join('behavior_packs', f'BP_{self.PASCAL_PROJECT_NAME}'): '', }
        content_structure = {
            os.path.join(output, f'{self.PROJECT_NAME}_RP.mcpack'): '',
            os.path.join(output, f'{self.PROJECT_NAME}_BP.mcpack'): '',
        }

        zipit(os.path.join(output, f'{self.PROJECT_NAME}_RP.mcpack'), resource_packs_structure)
        zipit(os.path.join(output, f'{self.PROJECT_NAME}_BP.mcpack'), behavior_packs_structure)
        zipit(os.path.join(output, f'{self.PROJECT_NAME}.mcaddon'), content_structure)
        RemoveFile(os.path.join(output, f'{self.PROJECT_NAME}_RP.mcpack'))
        RemoveFile(os.path.join(output, f'{self.PROJECT_NAME}_BP.mcpack'))

    @property
    def mcworld(self):
        if not self._compiled:
            self.Logger.not_compiled()
        self.Logger.packaging_mcworld()

        content_structure = {
            'resource_packs':                                       os.path.join('resource_packs'),
            'behavior_packs':                                       os.path.join('behavior_packs'),
            'texts':                                                os.path.join('texts'),
            'db':                                                   os.path.join('db'),
            'level.dat':                                            os.path.join(''),
            'levelname.txt':                                        os.path.join(''),
            'manifest.json':                                        os.path.join(''),
            'world_icon.jpeg':                                      os.path.join(''),
            'world_behavior_packs.json':                            os.path.join(''),
            'world_resource_packs.json':                            os.path.join(''),
        }

        zipit(os.path.join('assets', 'output',f'{self.PROJECT_NAME}.mcworld'), content_structure)

    def _queue(self, object: object):
        self._objects_list.append(object)

_logger = _Logger()
ANVIL = _Anvil(_Config(), _logger)