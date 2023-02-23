from .packages import *

#__all__ = [
#    'ANVIL', 'LootTable', 'Item', 'Particle', 
#    'Recipe', 'oldBlock', 'Structure', 'Fog',
#    'Fonts', 'Function', 'Dialogue', 'SkinPack',
#    'NAMESPACE', 'PROJECT_NAME', 'PASCAL_PROJECT_NAME', 'DEBUG',
#    'EngineComponent'
#]

class Exporter():
    def __init__(self, name: str, type: str) -> None:
        self._valids = {
            'function': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'functions'),
                'extension': {
                    0: '.mcfunction',
                    1: '.mcfunction',
                }
            },
            'server_entity': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'entities'),
                'extension': {
                    0: '.behavior.json',
                    1: '.behavior.json'
                }
            },
            'client_entity': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'entity'),
                'extension': {
                    0: '.entity.json',
                    1: '.entity.json'
                }
            },
            'dialogue': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'dialogue'),
                'extension': {
                    0: '.dialogue.json',
                    1: '.dialogue.json'
                }
            },
            'bp_item_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'items'),
                'extension': {
                    0: '.bp_item.json',
                    1: '.bp_item.json'
                }
            },
            'bp_block_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'blocks'),
                'extension': {
                    0: '.block.json',
                    1: '.block.json'
                }
            },
            'loot_table': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'loot_tables'),
                'extension': {
                    0: '.loot_table.json',
                    1: '.loot_table.json'
                }
            },
            'bp_animation_controllers': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animation_controllers'),
                'extension': {
                    0: '.bp_ac.json',
                    1: '.animation_controller.json'
                }
            },
            'bp_animations': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animations'),
                'extension': {
                    0: '.bp_anim.json',
                    1: '.animation.json'
                }
            },
            'spawn_rules': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'spawn_rules'),
                'extension': {
                    0: '.spawn_rule.json',
                    1: '.spawn_rules.json'
                }
            },
            'recipe': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'recipe'),
                'extension': {
                    0: '.recipe.json',
                    1: '.recipe.json'
                }
            },
            'language': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'texts'),
                'extension': {
                    0: '.lang',
                    1: '.lang'
                }
            },
            'rp_item_v1': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'items'),
                'extension': {
                    0: '.rp_item.json',
                    1: '.rp_item.json'
                }
            },
            'rp_animation_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animation_controllers'),
                'extension': {
                    0: '.rp_ac.json',
                    1: '.animation_controller.json'
                }
            },
            'render_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'render_controllers'),
                'extension': {
                    0: '.render.json',
                    1: '.render_controller.json'
                }
            },
            'rp_animation': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animations'),
                'extension': {
                    0: '.rp_anim.json',
                    1: '.animation.json'
                }
            },
            'attachable': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'attachables'),
                'extension': {
                    0: '.attachable.json',
                    1: '.attachable.json'
                }
            },
            'particle': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'particles'),
                'extension': {
                    0: '.particle.json',
                    1: '.particle.json'
                }
            },
            'assets': {
                'path': MakePath('assets'),
            },
            'ui': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'ui'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'uivars': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'ui'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'item_texture': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'terrain_texture': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'flipbook_textures': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'sound_definitions': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'music_definitions': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'sounds'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'blocks': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'dialogue': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'dialogue'),
                'extension': {
                    0: '.dialogue.json',
                    1: '.dialogue.json'
                }
            },
            'font': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'font'),
                'extension': {
                    0: '.json',
                    1: '.json'
                }
            },
            'fog': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'fogs'),
                'extension': {
                    0: '.fog.json',
                    1: '.fog.json',
                }
            },
            'server_block': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'blocks'),
                'extension': {
                    0: '.block.json',
                    1: '.block.json'
                }
            },
            'materials': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'materials'),
                'extension': {
                    0: '.material',
                    1: '.material'
                }
            },
            'geometry': {
                'path': MakePath('assets', 'models'),
                'extension': {
                    0: '.geo.json',
                    1: '.geo.json'
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
        self._directory = directory
        self._path = MakePath(self._valids[self._type]['path'], self._directory)
        ANVIL._queue(self)
        return self

    def _export(self):
        if self._shorten and type(self._content) is dict:
            self._content = ShortenDict(self._content)
        File(f'{self._name}{self._valids[self._type]["extension"][NAMESPACE_FORMAT_BIT]}', self._content, self._path, 'w')


class RawTextConstructor():
    def __init__(self):
        self._raw_text = []

    def style(self, *styles: Style):
        self._raw_text.append({'text': ''.join(styles)})
        return self

    def text(self, text):
        self._raw_text.append({'text': text})
        return self

    def translate(self, text):
        is_present = False
        new_t = ''
        for t in ANVIL._langs:
            if t.split('=')[1].replace('\n', '') == text:
                is_present = True
                new_t = t.replace('\n', '')
        if not is_present:
            self.id = f'raw_text_{ANVIL._tellraw_index}'
            ANVIL.localize(f'{self.id}={text}')
            ANVIL._tellraw_index += 1
        else:
            self.id = new_t.split('=')[0]
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

# General


class _MinecraftDescription():
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        self._identifier = identifier
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._description: dict = Schemes(
            'description', self._namespace_format, self._identifier)

    @property
    def _export(self):
        return self._description


class _ItemTextures(Exporter):
    def __init__(self) -> None:
        super().__init__('item_texture', 'item_texture')
        self.content(Schemes('item_texture', PROJECT_NAME))

    def add_item(self, item_name: str, directory, *item_sprites: str):
        for item in item_sprites:
            CheckAvailability(f'{item}.png', 'sprite',
                              MakePath('assets', 'textures', 'items'))
        self._content['texture_data'][item_name] = [
            *[
                MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}',
                         'textures', 'items', directory, f'{sprite}.png')
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
                    CopyFiles(MakePath('assets', 'textures', 'items'), sprite.rstrip(
                        sprite.split('/')[-1]), sprite.split('/')[-1])
        return super()._export()


class _TerrainTextures(Exporter):
    def __init__(self) -> None:
        super().__init__('terrain_texture', 'terrain_texture')
        self.content(Schemes('terrain_texture', PROJECT_NAME))

    def add_block(self, block_name: str, directory: str, *block_textures: str):
        self._content['texture_data'][block_name] = {
            "textures": [
                *[
                    MakePath('textures', 'blocks', directory, face)
                    for face in block_textures
                ]
            ]}

    @property
    def queue(self):
        return super().queue()


class _BlocksJSON(Exporter):
    def __init__(self) -> None:
        super().__init__('blocks', 'blocks')
        self.content(Schemes('blocks', PROJECT_NAME))

    def add_block(self, block_name: str):
        self._content['texture_data'][block_name] = {
            "sound": "",
            # "textures":{},
            # "carried_textures":{},
            # "brightness_gamma": 0,
            # "isotropic":True
        }


class _SoundDefinition():
    def __init__(self, sound_definition: str, category, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999) -> None:
        self._category = category
        if category not in SoundCategory.list:
            RaiseError(SOUND_CATEGORY_ERROR)
        self._sound_definition = sound_definition
        self._sound = Schemes('sound', self._sound_definition, category)

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
        CheckAvailability(f'{sound_name}.ogg', 'audio', 'assets/sounds')
        self._sound_name = sound_name
        splits = self._sound_definition.split(".")
        self._path = ''
        for i in range(len(splits)-1):
            self._path += f'{splits[i]}/'
        sound = {
            "name": MakePath('sounds', self._path, self._sound_name)
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
            CopyFiles('assets/sounds', MakePath('resource_packs',
                      f'RP_{PASCAL_PROJECT_NAME}', 'sounds', self._path), f'{sound["name"].split("/")[-1]}.ogg')
        self._sound[self._sound_definition]['sounds'] = self._sounds
        return self._sound


class _Sound(Exporter):
    def __init__(self) -> None:
        super().__init__('sound_definitions', 'sound_definitions')
        self.content(Schemes('sound_definitions'))
        self._sounds: list[_SoundDefinition] = []

    def sound_definition(self, sound_definition: str, category: SoundCategory(), use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
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


class _Music(Exporter):
    def __init__(self) -> None:
        super().__init__('music_definitions', 'music_definitions')
        self.content(Schemes('music_definitions'))
        self._sounds: list[_SoundDefinition] = []

    def music_definition(self, music_category: MusicCategory(), min_delay: int = 60, max_delay: int = 180):
        if music_category not in MusicCategory.list:
            RaiseError(MUSIC_CATEGORY_ERROR)

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


class _DialogueButton():
    def __init__(self, button_name: str, *commands: str):
        self._button_name = button_name
        self._commands = [
            f'/{command}' if not str(command).startswith('/') else command for command in commands
        ]

    def _export(self):
        return Schemes(
            'dialogue_button',
            self._button_name,
            self._commands
        )


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
        if len(self._buttons) > 6:
            RaiseError(DIALOGUE_MAX_BUTTONS(self._tag, len(self._buttons)))
        # Buttons cannot be translated
        button = _DialogueButton(button_name, *commands)
        self._buttons.append(button)
        return self

    def on_open_commands(self, *commands):
        self._on_open_commands = commands
        return self

    def on_close_commands(self, *commands):
        self._on_close_commands = commands
        return self

    def _export(self):
        return Schemes(
            'dialogue_scene',
            self._tag,
            self._npc_name.__str__(),
            self._text.__str__(),
            self._on_open_commands,
            self._on_close_commands,
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
        self._material_name = f'{material_name}' + f':{base_material}' if not base_material is None else ''
        self._material = {
            self._material_name : {}
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
        self._material[self._material_name]['frontFace'] = {key: value for key, value in a.items() if value != None}
        return self

    def backFace(self, stencilFunc: MaterialFunc = None, stencilFailOp: MaterialOperation = None, stencilDepthFailOp: MaterialOperation = None, stencilPassOp: MaterialOperation = None, stencilPass: MaterialOperation = None):
        a = {
            'stencilFunc': stencilFunc,
            'stencilFailOp': stencilFailOp,
            'stencilDepthFailOp': stencilDepthFailOp,
            'stencilPassOp': stencilPassOp,
            'stencilPass': stencilPass
        }
        self._material[self._material_name]['backFace'] = {key: value for key, value in a.items() if value != None}
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


class _Materials(Exporter):
    def __init__(self) -> None:
        super().__init__('entity', 'materials')
        self._materials : list[_Material] = []
    
    def add_material(self, material_name, base_material):
        material = _Material(material_name, base_material)
        self._materials.append(material)
        return material
    
    @property
    def queue(self):
        if len(self._materials) > 0:
            self._content = Schemes('materials')
            for m in self._materials:
                self._content['materials'].update(m._queue)
            super().queue('')


class _Bone():
    def __init__(self, name, pivot) -> None:
        self._bone = {
	    	"name": name,
	    	"pivot": pivot,
	    	"cubes": []
	    }
    
    def add_cube(self, 
                 origin: list[float, float, float], 
                 size: list[float, float, float], 
                 uv: list[int, int], 
                 pivot: list[float, float, float] = (0,0,0), 
                 rotation: list[float, float, float] = (0,0,0),
                 inflate: float = 0,
                 mirror: bool = False,
                 reset: bool = False):
        self._bone['cubes'].append({
            'origin': origin,
            'size': size,
            'uv': uv,
            'pivot': pivot if not pivot == (0,0,0) else {},
            'rotation': rotation if not rotation == (0,0,0) else {},
            'inflate': inflate if not inflate == 0 else {},
            'mirror': mirror if mirror else {},
            'reset': reset if reset else {},
        })
        return self

    @property
    def _queue(self):
        return self._bone


class _Geo():
    def __init__(self, geometry_name: str, texture_size: list[int, int] = (16,16)) -> None:
        self._geo = {
            "description": {
                "identifier": f"geometry.{NAMESPACE}.{geometry_name}",
		        "texture_width": texture_size[0],
		        "texture_height": texture_size[1],
            },
            "bones": [],
        }
        self._bones : list[_Bone] = []
    
    def set_visible_bounds(self, visible_bounds_wh: list[float, float], visible_bounds_offset: list[float, float, float]):
        self._geo['description']['visible_bounds_width'] = visible_bounds_wh[0]
        self._geo['description']['visible_bounds_height'] = visible_bounds_wh[1]
        self._geo['description']['visible_bounds_offset'] = visible_bounds_offset
        return self

    def add_bone(self, name: str, pivot: list[int, int, int]):
        bone = _Bone(name, pivot)
        self._bones.append(bone)
        return bone

    @property
    def _queue(self):
        for bone in self._bones:
            self._geo['bones'].append(bone._queue)
        return self._geo

# =============================================
class SkinPack():
    def __init__(self) -> None:
        self._skins = []

    def add_skin(self, filename: str, display_name: str, is_slim: bool = False, free: bool = False):
        self._skins.append({
            "localization_name": filename,
            "geometry": f"geometry.humanoid.{ 'customSlim' if is_slim else 'custom'}",
            "texture": f"{filename}.png",
            "type": "free" if free else "paid"
        })
        ANVIL._skins_langs.append(
            f'skin.{PROJECT_NAME}.{filename}={display_name}\n')

    def queue(self):
        ANVIL._queue(self)

    def _export(self):
        CreateDirectory('assets/skin_pack/texts')
        File('languages.json', Defaults('languages'),
             'assets/skin_pack/texts', 'w')
        if FileExists('assets/skin_pack/manifest.json') is False:
            File("manifest.json", Schemes('manifest_skins',
                 PROJECT_NAME), "assets/skin_pack", "w")
        File('en_US.lang', Schemes('skin_language', PROJECT_NAME, DISPLAY_NAME +
             ' Skin Pack') + ''.join(ANVIL._skins_langs), 'assets/skin_pack/texts', 'w')
        File('skins.json', Schemes('skins', PROJECT_NAME,
             self._skins), 'assets/skin_pack', 'w')


class Dialogue(Exporter):
    def __init__(self, name: str) -> None:
        self._dialogues = Schemes('dialogues')
        self._scenes = []
        super().__init__(name, 'dialogue')

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


class Function(Exporter):
    def __init__(self, name: str) -> None:
        self._name = name
        self._function: list[str] = []
        self._sub_functions: list[Function] = [self]
        super().__init__(name, 'function')

    def add(self, *functions: str):
        if len(self._sub_functions[-1]._function) >= 10000-len(functions)-1:
            self._sub_functions.append(
                Function(f'{self._name}_{len(self._sub_functions)}'))

        self._sub_functions[-1]._function.extend([str(func)
                                                 for func in functions])
        return self

    @property
    def path(self):
        return MakePath(self._directory, self._name)

    @property
    def execute(self):
        return f'function {self.path}'

    @property
    def tick(self):
        ANVIL._tick(self)
        return self

    def queue(self, directory: str = None):
        self._directory = directory
        return super().queue(self._directory)

    def _export(self):
        for function in self._sub_functions[1:]:
            function.content('\n'.join(function._function)
                             ).queue(self._directory)
        self.content('\n'.join(self._function))

        return super()._export()


class Fonts():
    def __init__(self) -> None:
        self._image = None

    def generate_font(self, font_name: str, character_size: int = 32):
        if character_size % 16 != 0:
            RaiseError(UNSUPPORTED_FONT_SIZE)

        if not FileExists(MakePath('assets', 'textures', 'ui', f'{font_name}.ttf')):
            RaiseError(MISSING_FILE('font', f'{font_name}.ttf', MakePath('assets', 'textures', 'ui')))

        font_size = round(character_size*.8)
        image_size = character_size*16
        self._image = Image.new("RGBA", (image_size, image_size))
        font = ImageFont.truetype(f'assets/textures/ui/{font_name}.ttf', font_size)
        backup_font = ImageFont.truetype('arial.ttf', font_size)
        default8 = u'ÀÁÂÈÉÊÍÓÔÕÚßãõǧÎ¹ŒœŞşŴŵŽê§©      !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂ÇüéâäàåçêëèïîìÄÅÉ§ÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴├├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■	'
        offset = [0, 0]
        for i in default8:
            d1 = ImageDraw.Draw(self._image)
            if font.getsize(i) == (27, 29):
                d1.text((offset[0]*character_size+3, offset[1]*character_size), i, fill =(255, 255, 255), font=backup_font, align='left')
            else:
                d1.text((offset[0]*character_size+3, offset[1]*character_size), i, fill =(255, 255, 255), font=font, align='left')
            offset[0] += 1
            if offset[0] >= 16:
                offset[0] = 0
                offset[1] += 1
        
        return self
        
    @property
    def queue(self):
        if not self._image is None:
            self._image.save(MakePath('assets', 'textures', 'ui', 'default8.png'))

        for file in ['glyph_E1.png', 'default8.png']:
            if FileExists(MakePath('assets', 'textures', 'ui', file)):
                CopyFiles(MakePath('assets', 'textures', 'ui'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'font'), file)


class Fog(Exporter):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, 'fog')
        self._identifier = identifier
        self._description = _MinecraftDescription(self._identifier, is_vanilla)
        self._fog = Schemes('fog')
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


class Structure():
    def __init__(self, structure_name):
        self._structure_name = structure_name
        CheckAvailability(f'{self._structure_name}.mcstructure',
                          'structure', MakePath('assets', 'structures'))

    @property
    def queue(self):
        ANVIL._queue(self)

    @property
    def identifier(self):
        return f'{NAMESPACE_FORMAT}:{self._structure_name}'

    def _export(self):
        CopyFiles(
            MakePath('assets', 'structures'),
            MakePath('behavior_packs', f"BP_{PASCAL_PROJECT_NAME}", 'structures',
                     NAMESPACE_FORMAT, f"{self._structure_name}.mcstructure")
        )


class Geometry(Exporter):
    def __init__(self, name: str) -> None:
        super().__init__(name, 'geometry')
        self._geos : list[_Geo] = []
    
    def add_geo(self, geometry_name: str, texture_size: tuple[int, int] = (16,16)):
        geo = _Geo(geometry_name, texture_size)
        self._geos.append(geo)
        return geo
    
    def queue(self, type: str):
        if not type in ['entity', 'attachables', 'blocks']:
            RaiseError('Unsupported model type') 
        
        if len(self._geos) == 0:
            RaiseError(f'The Geometry file {self._name} does not have any geometry.')

        self.content(Schemes('geometry'))
        for g in self._geos:
            self._content['minecraft:geometry'].append(g._queue)
        super().queue(type)
        super()._export()

# Core Functionalities
# TODO: Replace/remove


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
            RaiseError('Component type must be one of %r.' %
                       [self._valid_bp+self._valid_rp])
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
                self._path += MakePath('/functions',
                                       PROJECT_NAME, self._directory)
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
        File(f'{self._name}{self._file_type}',
             self._content, self._path, self._export_mode)


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


class Particle(EngineComponent):
    def __init__(self, particle_name, use_vanilla_texture: bool = False):
        super().__init__(particle_name, 'asset', '.particle.json')
        self._name = particle_name
        self._content = ''
        self._use_vanilla_texture = use_vanilla_texture

    def queue(self):
        return super().queue('particles')

    def _export(self):
        if self._content != '':
            super()._export()
        if not self._use_vanilla_texture:
            CheckAvailability(f'{self._name}.png',
                              'texture', 'assets/particles')
            CopyFiles('assets/particles',
                      f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/particle', f'{self._name}.png')
        CheckAvailability(f'{self._name}.particle.json',
                          'particle', 'assets/particles')
        CopyFiles('assets/particles',
                  f'resource_packs/RP_{PASCAL_PROJECT_NAME}/particles', f'{self._name}.particle.json')


class Item():
    def __new__(self, identifier: str, display_name: str = None, is_vanilla: bool = False):
        self._identifier, self._display_name = RawText(identifier)
        ANVIL._items.update(
            {self._display_name: f'{NAMESPACE_FORMAT}:{self._identifier}'})
        CheckAvailability(f'{self._identifier}.png',
                          'texture', 'assets/textures/items')
        if is_vanilla:
            ANVIL._items.update(
                {self._display_name: f'minecraft:{self._identifier}'})
        self._item_rp = Item.__RP_Item(
            self._identifier, display_name, is_vanilla)
        self._item_bp = Item.__BP_Item(
            self._item_rp, self._identifier, is_vanilla)
        return self._item_bp

    class __RP_Item(EngineComponent):
        def __init__(self, identifier, display_name, is_vanilla):
            if display_name is None:
                self._identifier, self._display_name = RawText(identifier)
            else:
                self._identifier = identifier
                self._display_name = display_name

            super().__init__(self._identifier, 'rp_item_v1', '.item.json')
            self.content(Defaults(
                'rp_item_v1', NAMESPACE_FORMAT if not is_vanilla else 'minecraft', self._identifier))

        def queue(self, directory):
            ANVIL.localize(
                (f'item.{NAMESPACE_FORMAT}:{self._identifier}.name={self._display_name}'))
            super().queue(directory=directory)
            CopyFiles('assets/textures/items',
                      f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/items/{directory}', f'{self._identifier}.png')
            if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json'):
                File('item_texture.json', Schemes('item_texture', PROJECT_NAME),
                     f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
            with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json', 'r') as file:
                data = json.load(file)
                data['texture_data'][f'{self._identifier}'] = {'textures': []}
                data['texture_data'][f'{self._identifier}']['textures'].append(
                    MakePath('textures/items', directory, self._identifier))
            File('item_texture.json', data,
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')

    class __BP_Item(EngineComponent):
        def __init__(self, parent, identifier, is_vanilla):
            self._identifier = identifier
            self._parent = parent
            super().__init__(self._identifier, 'bp_item_v1', '.item.json')
            self.content(Defaults(
                'bp_item_v1', NAMESPACE_FORMAT if not is_vanilla else 'minecraft', self._identifier))

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


class Anvil():
    def get_github_file(self, path: str):
        from github import Github
        if self._github is None:
            self._github = Github().get_repo('Mojang/bedrock-samples')
        r = json.loads(self._github.get_contents(
            path, BUILD.lower()).decoded_content.decode())
        return r

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

        global COMPANY, NAMESPACE, PROJECT_NAME, PASCAL_PROJECT_NAME, DISPLAY_NAME, PROJECT_DESCRIPTION, VANILLA_VERSION, LATEST_BUILD, NAMESPACE_FORMAT, NAMESPACE_FORMAT_BIT, BUILD, DEBUG
        COMPANY = CONFIG.get('ANVIL', 'COMPANY')
        NAMESPACE = CONFIG.get('ANVIL', 'NAMESPACE')
        PROJECT_NAME = CONFIG.get('ANVIL', 'PROJECT_NAME')
        PASCAL_PROJECT_NAME = CONFIG.get('ANVIL', 'PASCAL_PROJECT_NAME')
        DISPLAY_NAME = CONFIG.get('ANVIL', 'DISPLAY_NAME')
        PROJECT_DESCRIPTION = CONFIG.get('ANVIL', 'PROJECT_DESCRIPTION')
        VANILLA_VERSION = CONFIG.get('ANVIL', 'VANILLA_VERSION')
        LATEST_BUILD = VANILLA_VERSION
        LAST_CHECK = CONFIG.get('ANVIL', 'LAST_CHECK')
        NAMESPACE_FORMAT_BIT = int(CONFIG.get('ANVIL', 'NAMESPACE_FORMAT'))
        BUILD = CONFIG.get('ANVIL', 'BUILD')
        DEBUG = CONFIG.get('ANVIL', 'DEBUG')
        NAMESPACE_FORMAT = NAMESPACE + f'.{PROJECT_NAME}' * NAMESPACE_FORMAT_BIT


        self._setup = Function('setup')
        self._setup_scores = Function('setup_scores')
        self._remove_scores = Function('remove_scores')
        self._remove_tags = Function('remove_tags')
        self._item_texture = _ItemTextures()
        self._terrain_texture = _TerrainTextures()
        self._sound_definition = _Sound()
        self._music_definition = _Music()
        self._materials = _Materials()

        self._functions: list[Function] = []
        self._scores = {}
        self._objects_list: list[Exporter] = []
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
        self._setup_scores.add(
            f'scoreboard objectives add {PROJECT_NAME} dummy "{PROJECT_NAME.replace("_"," ").title()}"')
        self._remove_scores.add(
            f'scoreboard objectives remove {PROJECT_NAME}\n')
        self._deltatime = int(
            (datetime.now() - datetime.strptime(LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds())
        self._github = None
        self._compiled = False
        click.echo(EXECUTION_TIME(datetime.now().strptime(
            LAST_CHECK, "%Y-%m-%d %H:%M:%S")))
        # 12 Hours
        if (self._deltatime > 12*3600):
            click.echo(CHECK_UPDATE)
            LATEST_BUILD = self.get_github_file('version.json')['latest']['version']

            if VANILLA_VERSION < LATEST_BUILD:
                click.echo(NEW_BUILD(VANILLA_VERSION, LATEST_BUILD))
                #DownloadFile(self._github.clone_url, MakePath('assets', 'vanilla'))
            else:
                click.echo(UP_TO_DATE)
                
            CONFIG.set('ANVIL', 'VANILLA_VERSION', LATEST_BUILD)
            CONFIG.set('ANVIL', 'LAST_CHECK', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def sound(self, sound_definition: str, category: SoundCategory(), use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
        return self._sound_definition.sound_definition(sound_definition, category, use_legacy_max_distance, max_distance, min_distance)

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
                self._remove_scores.add(
                    f'scoreboard objectives remove {score_id}')
                self._setup_scores.add(
                    f'scoreboard objectives add {score_id} dummy "{score_id.replace("_"," ").title()}"')
                self._setup_scores.add(
                    f'scoreboard players set {PROJECT_NAME} {score_id} {score_value}')

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
            self._tick_functions.append(
                function.execute.split(' ')[-1].replace('\n', ''))

    def add_material(self, material_name, base_material: str | None = None):
        return self._materials.add_material(material_name=material_name, base_material=base_material)

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

    def _translate(self, include_skin_pack: bool = False) -> None:
        """
        Translates en_US to all supported Minecraft languages.
        This is a time consuming function, it will be executed with anvil.package(), so it's better to avoid it unless you really want to use it.


        Usage:
        ---------
        >>> ANVIL.translate
        """
        from deep_translator import GoogleTranslator
        self._translation_timer = time.time()
        languages = Defaults('languages')
        self._langs.sort()
        for language in languages:
            click.echo(TRANSLATING(language))
            destination_language = language.split('_')[0]
            if language == 'zh_CN':
                destination_language = 'zh-CN'
            if language == 'zh_TW':
                destination_language = 'zh-TW'
            if language == 'nb_NO':
                destination_language = 'no'
            new_data = ''
            Translator = GoogleTranslator(target=destination_language)
            if not FileExists(MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'texts', f'{language}.lang')):
                for line in self._langs:
                    if len(line) > 0 and '=' in line:
                        id, text = line.split("=")
                        text = text.replace('\n', '')
                        translated = Translator.translate(text)
                        new_data += f'{id}={translated}\n'
                    else:
                        new_data += f'{line}\n'
                    time.sleep(0.3)
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, Translator.translate(
                    PROJECT_DESCRIPTION)) + new_data, MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'texts'), 'w')
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, Translator.translate(
                    PROJECT_DESCRIPTION)), MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'texts'), 'w')
                File(f'{language}.lang', Defaults('language', DISPLAY_NAME, Translator.translate(
                    PROJECT_DESCRIPTION)), MakePath('texts'), 'w')
            if include_skin_pack:
                if not FileExists(MakePath('assets', 'skin_pack', 'texts', f'{language}.lang')):
                    for line in self._skins_langs:
                        if len(line) > 0 and '=' in line:
                            id, text = line.split("=")
                            text = text.replace('\n', '')
                            translated = Translator.translate(text)
                            new_data += f'{id}={translated}\n'
                        else:
                            new_data += f'{line}\n'
                        time.sleep(0.3)
                    File(f'{language}.lang', Schemes('skin_language', PROJECT_NAME, DISPLAY_NAME + ' Skin Pack') +
                         new_data, MakePath('assets', 'skin_pack', 'texts', f'{language}.lang'), 'w')
        click.echo(TRANSLATION_TIME(
            round(time.time() - self._translation_timer, 2)))

    @property
    def compile(self) -> None:
        """
        Compiles queued anvil objects.
        This function must be called last at the very end of your script.


        Usage:
        ---------
        >>> ANVIL.compile
        """
        self._langs.sort()
        CreateDirectory(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts')
        CreateDirectory(f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts')
        CreateDirectory('texts')
        File('languages.json', Defaults('languages'),
             f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('languages.json', Defaults('languages'),
             f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('languages.json', Defaults('languages'), 'texts', 'w')
        File('en_US.lang', Defaults('language', DISPLAY_NAME, PROJECT_DESCRIPTION) +
             ''.join(self._langs), f'resource_packs/RP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', Defaults('language', DISPLAY_NAME, PROJECT_DESCRIPTION),
             f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/texts', 'w')
        File('en_US.lang', Defaults('language', DISPLAY_NAME,
             PROJECT_DESCRIPTION), 'texts', 'w')

        if VANILLA_VERSION < LATEST_BUILD or not all([
            FileExists(MakePath('resource_packs',
                       f'RP_{PASCAL_PROJECT_NAME}', 'manifest.json')),
            FileExists(MakePath('behavior_packs',
                       f'BP_{PASCAL_PROJECT_NAME}', 'manifest.json')),
            FileExists(MakePath('manifest.json')),
        ]):
            File("manifest.json", Schemes('manifest_rp'),
                 f"resource_packs/RP_{PASCAL_PROJECT_NAME}", "w")
            with open(f"resource_packs/RP_{PASCAL_PROJECT_NAME}/manifest.json", 'r') as file:
                data = json.load(file)
                uuid = data["header"]["uuid"]
                version = data["header"]["version"]
                File("world_resource_packs.json", Schemes(
                    'world_packs', uuid, version), ".", "w")
            File("manifest.json", Schemes('manifest_bp'),
                 f"behavior_packs/BP_{PASCAL_PROJECT_NAME}", "w")
            with open(f"./behavior_packs/BP_{PASCAL_PROJECT_NAME}/manifest.json", 'r') as file:
                data = json.load(file)
                uuid = data["header"]["uuid"]
                version = data["header"]["version"]
                File("world_behavior_packs.json", Schemes(
                    'world_packs', uuid, version), ".", "w")
            File("manifest.json", Schemes(
                'manifest_world', [COMPANY]), "", "w")

        if FileExists('assets/textures/gui'):
            CopyFolder('assets/textures/gui',
                       f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/gui')
        if FileExists('assets/textures/environment'):
            CopyFolder('assets/textures/environment',
                       f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/environment')
        
        self._materials.queue
        self._setup_scores.queue('StateMachine/misc')
        self._remove_scores.queue('StateMachine/misc')
        self._remove_tags.queue('StateMachine/misc')
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
        if len(self._terrain_texture._content['texture_data']) > 0:
            self._terrain_texture.queue
        if len(self._sound_definition._sounds) > 0:
            self._sound_definition.queue
        if len(self._music_definition._sounds) > 0:
            self._music_definition.queue

        for object in self._objects_list:
            object._export()
            click.echo(EXPORTING(object._name))

        click.echo(COMPILATION_TIME(round(time.time() - self._start_timer, 2)))
        self._compiled = True

    def package(self, skip_translation: bool = False, include_skin_pack: bool = False) -> None:
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
        content_structure = {}

        def art():
            pack_icon_size = (256, 256)
            marketing_screenshot_size = (1920, 1080)
            store_screenshot_size = (800, 450)

            source = MakePath('assets', 'marketing')
            output_store = MakePath('assets', 'output', 'Store Art')
            output_marketing = MakePath('assets', 'output', 'Marketing Art')

            CreateDirectory(output_store)
            CreateDirectory(output_marketing)

            if FileExists(MakePath(source, 'pack_icon.png')):
                CopyFiles(source, MakePath('behavior_packs',
                          f'BP_{PASCAL_PROJECT_NAME}'), 'pack_icon.png')
                CopyFiles(source, MakePath('resource_packs',
                          f'RP_{PASCAL_PROJECT_NAME}'), 'pack_icon.png')
                original = Image.open(MakePath(source, 'pack_icon.png'))
                resized = original.resize(pack_icon_size)
                resized.convert("RGB").save(MakePath(
                    output_store, f'{PROJECT_NAME}_packicon_0.jpg'), dpi=(72, 72), quality=95)
            else:
                click.echo(FILE_EXIST_WARNING('pack_icon.png'))
            if FileExists(MakePath(source, 'keyart.png')):
                original = Image.open(MakePath(source, 'keyart.png'))
                resized = original.resize(store_screenshot_size)
                resized.convert('RGB').save('world_icon.jpeg')
                resized.convert('RGB').save(MakePath(
                    output_store, f'{PROJECT_NAME}_Thumbnail_0.jpg'), dpi=(72, 72), quality=95)
                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(MakePath(
                    output_marketing, f'{PROJECT_NAME}_MarketingKeyArt.jpg'), dpi=(300, 300), quality=95)
            else:
                click.echo(FILE_EXIST_WARNING('keyart.png'))
            if FileExists(MakePath(source, 'panorama.png')):
                original = Image.open(MakePath(source, 'panorama.png'))
                scale_factor = 450/original.size[1]
                resized = original.resize(
                    (round(original.size[0]*scale_factor), 450))
                resized.convert("RGB").save(MakePath(
                    output_store, f'{PROJECT_NAME}_panorama_0.jpg'), dpi=(72, 72), quality=95)
            else:
                click.echo(FILE_EXIST_WARNING('panorama.png'))
            for i in range(5):
                if FileExists(MakePath(source, f'{i}.png')):
                    original = Image.open(MakePath(source, f'{i}.png'))
                    resized = original.resize(store_screenshot_size)
                    resized.convert("RGB").save(MakePath(
                        output_store, f'{PROJECT_NAME}_screenshot_{i}.jpg'), dpi=(72, 72), quality=95)
                    resized = original.resize(marketing_screenshot_size)
                    resized.convert("RGB").save(MakePath(
                        output_marketing, f'{PROJECT_NAME}_MarketingScreenshot_{i}.jpg'), dpi=(300, 300), quality=100)
                else:
                    click.echo(FILE_EXIST_WARNING(f'{i}.png'))
            if FileExists(MakePath(source, 'partner_art.png')):
                original = Image.open(MakePath(source, 'partner_art.png'))
                resized = original.resize(marketing_screenshot_size)
                resized.convert("RGB").save(MakePath(
                    output_marketing, f'{PROJECT_NAME}_PartnerArt.jpg'), dpi=(300, 300), quality=100)
            else:
                click.echo(FILE_EXIST_WARNING('partner_art.png'))

        def generate_submission_notes():
            with open('assets/output/submission_notes.txt', "w", encoding='utf-8') as file:
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
        if not self._compiled:
            RaiseError(NOT_COMPILED)
        if not skip_translation:
            self._translate(include_skin_pack)
        if include_skin_pack:
            content_structure.update({
                MakePath('assets', 'skin_pack'): MakePath('Content', 'world_tskin_packemplate'),
            })

        click.echo(PACKAGING_ZIP)
        generate_submission_notes()
        art()
        content_structure.update({
            MakePath('assets', 'output', 'Store Art'):              MakePath('Store Art'),
            MakePath('assets', 'output', 'Marketing Art'):          MakePath('Marketing Art'),
            'resource_packs':                                       MakePath('Content', 'world_template', 'resource_packs'),
            'behavior_packs':                                       MakePath('Content', 'world_template', 'behavior_packs'),
            'texts':                                                MakePath('Content', 'world_template', 'texts'),
            'db':                                                   MakePath('Content', 'world_template', 'db'),
            'level.dat':                                            MakePath('Content', 'world_template'),
            'levelname.txt':                                        MakePath('Content', 'world_template'),
            'manifest.json':                                        MakePath('Content', 'world_template'),
            'world_icon.jpeg':                                      MakePath('Content', 'world_template'),
            'world_behavior_packs.json':                            MakePath('Content', 'world_template'),
            'world_resource_packs.json':                            MakePath('Content', 'world_template'),
        })

        zipit(MakePath('assets', 'output',f'{PROJECT_NAME}.zip'), content_structure)

        RemoveDirectory(MakePath('assets', 'output', 'Store Art'))
        RemoveDirectory(MakePath('assets', 'output', 'Marketing Art'))

    @property
    def mcaddon(self):
        if not self._compiled:
            RaiseError(NOT_COMPILED)
        click.echo(PACKAGING_MCADDON)

        source = MakePath('assets', 'marketing')
        output = MakePath('assets', 'output')
        if FileExists(MakePath(source, 'pack_icon.png')):
            CopyFiles(source, MakePath('behavior_packs',
                      f'BP_{PASCAL_PROJECT_NAME}'), 'pack_icon.png')
            CopyFiles(source, MakePath('resource_packs',
                      f'RP_{PASCAL_PROJECT_NAME}'), 'pack_icon.png')

        resource_packs_structure = {
            MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}'): '', }
        behavior_packs_structure = {
            MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}'): '', }
        content_structure = {
            MakePath(output, f'{DISPLAY_NAME}_RP.mcpack'): '',
            MakePath(output, f'{DISPLAY_NAME}_BP.mcpack'): '',
        }

        zipit(MakePath(output, f'{DISPLAY_NAME}_RP.mcpack'),
              resource_packs_structure)
        zipit(MakePath(output, f'{DISPLAY_NAME}_BP.mcpack'),
              behavior_packs_structure)
        zipit(MakePath(output, f'{DISPLAY_NAME}.mcaddon'), content_structure)
        RemoveFile(MakePath(output, f'{DISPLAY_NAME}_RP.mcpack'))
        RemoveFile(MakePath(output, f'{DISPLAY_NAME}_BP.mcpack'))

    @property
    def mcworld(self):
        click.echo(PACKAGING_MCWORLD)

        if not self._compiled:
            RaiseError(NOT_COMPILED)

        content_structure = {
            'resource_packs':                                       MakePath('resource_packs'),
            'behavior_packs':                                       MakePath('behavior_packs'),
            'texts':                                                MakePath('texts'),
            'db':                                                   MakePath('db'),
            'level.dat':                                            MakePath(''),
            'levelname.txt':                                        MakePath(''),
            'manifest.json':                                        MakePath(''),
            'world_icon.jpeg':                                      MakePath(''),
            'world_behavior_packs.json':                            MakePath(''),
            'world_resource_packs.json':                            MakePath(''),
        }

        zipit(MakePath('assets', 'output',f'{PROJECT_NAME}.mcworld'), content_structure)

    def _queue(self, object: object):
        self._objects_list.append(object)
        click.echo(COMPILING(object._name))


ANVIL = Anvil()
