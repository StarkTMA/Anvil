from ..packages import *
from ..core import NAMESPACE_FORMAT, NAMESPACE, PASCAL_PROJECT_NAME, ANVIL, Exporter, _MinecraftDescription, _SoundDefinition, Particle, components

__all__ = [ 'Entity', 'Attachable' ]

class _ActorDescription(_MinecraftDescription):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, is_vanilla)
        self._animation_controllers_list = []
        self._animations_list = []
        self._description['description'].update({
            'animations': {},
            'scripts': {'animate':[]}
        })

    def _animate_append(self, key):
        if key not in self._description['description']['scripts']['animate']:
            self._description['description']['scripts']['animate'].append(key)

    def _animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
        '''Sets the mapping of internal animation controller references to actual animations.

        Parameters
        ----------
        controller_shortname : str
            The name of the animation controller.
        animate : bool, optional
            bool = False
        condition : str, optional
            str = None

        '''

        if animate is True:
            if condition is None:
                self._animate_append(controller_shortname)
            else:
                self._animate_append({controller_shortname: condition})

        self._description['description']['animations'].update(
            {controller_shortname: f'controller.animation.{NAMESPACE_FORMAT}.{self._identifier}.{controller_shortname}'}
        )

    def _animations(self, animation_shortname: str, animate: bool = False, condition: str = None):
        '''Sets the mapping of internal animation references to actual animations.

        Parameters
        ----------
        animation_shortname : str
            The name of the animation.
        animate : bool, optional
            bool = False
        condition : str, optional
            str = None

        '''
        
        if animate is True:
            if condition is None:
                self._animate_append(animation_shortname)
            else:
                self._animate_append({animation_shortname: condition})
                
        self._description['description']['animations'].update(
            {animation_shortname: f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{animation_shortname}'}
        )
    
class _ActorClientDescription(_ActorDescription):
    def _check_model(self, entity_name, model_name):
        CheckAvailability(f'{entity_name}.geo.json', 'geometry', MakePath('assets','models',self._type))
        geo_namespace = f'geometry.{NAMESPACE_FORMAT}.{model_name}'
        with open(MakePath('assets','models',self._type, f'{entity_name}.geo.json')) as file:
            data = file.read()
            if geo_namespace not in data:
                RaiseError(f'The geometry file {entity_name}.geo.json doesn\'t contain a geometry called {geo_namespace}')
    
    def _check_animation(self, animation_name):
        CheckAvailability(f'{self._identifier}.animation.json', 'animation', 'assets/animations')
        anim_namespace = f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{animation_name}'
        with open(f'assets/animations/{self._identifier}.animation.json') as file:
            if anim_namespace not in file.read():
                RaiseError(MISSING_ANIMATION(anim_namespace, self._identifier, animation_name))

    def _render_append(self, key):
        if key not in self._description['description']['render_controllers']:
            self._description['description']['render_controllers'].append(key)

    def __init__(self, identifier: str, is_vanilla: bool = False, type: str = 'entity') -> None:
        if type not in ['entity', 'attachables']:
            RaiseError(CLIENT_TYPE_UNSUPPORTED(type, f"{self._namespace_format}:{self._identifier}"))
        super().__init__(identifier, is_vanilla)
        self._type = type
        self._is_vanilla = is_vanilla
        self._animation_controllers = _RP_AnimationControllers(self._identifier, self._is_vanilla)
        self._render_controllers = _RenderControllers(self._identifier, self._is_vanilla)
        self._description['description'].update({
            'materials': {
                'default': 'entity_alphatest'
            },
            'scripts':{
                'pre_animation':[],
                'initialize': [],
                'animate':[]
            },
            'textures': {},
            'geometry': {},
            'particle_effects': {},
            'sound_effects': {},
            'render_controllers': []
        })
        self._is_dummy = False
        self._added_geos = 0
        self._added_textures = []
        self._added_anims = []
        self._sounds : list[_SoundDefinition] = []

    @property
    def dummy(self):
        self._is_dummy = True
        File('dummy.geo.json', Schemes('geometry', NAMESPACE_FORMAT, 'dummy',{"name": "root", "pivot": [0, 0, 0], "locators": {"root": [0, 0, 0]}}), MakePath('assets', 'models', self._type), 'w')
        CreateImage('dummy', 8, 8, (0, 0, 0, 0), MakePath('assets', 'textures', self._type))
        self.geometry('dummy', 'dummy')
        self.texture('dummy', 'dummy')
        self.render_controller('dummy').geometry('dummy').textures('dummy')

    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
        self._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(self, animation_name: str, animate: bool = False, condition: str = None):
        self._check_animation(animation_name)
        self._animations(animation_name, animate, condition)
        self._added_anims.append(animation_name)
        return self

    def material(self, material_id: str, material_name: str):
        self._description['description']['materials'].update({material_id: material_name})
        return self

    def geometry(self, geometry_id: str, geometry_name: str, reuse: str = None):
        if not reuse is None:
            self._check_model(reuse, geometry_name)
            CopyFiles(MakePath('assets', 'models', self._type), MakePath('assets', 'models', self._type), f'{reuse}.geo.json', f'{self._identifier}.geo.json')
        if not self._is_dummy:
            self._check_model(self._identifier, geometry_name)
        self._description['description']['geometry'].update({geometry_id: f'geometry.{NAMESPACE_FORMAT}.{geometry_name}'})
        self._added_geos = 1
        return self

    def texture(self, texture_id: str, texture_name: str):
        CheckAvailability(f'{texture_name}.png','texture', MakePath('assets','textures',self._type))
        self._spawn_egg_colors = texture_id
        self._description['description']['textures'].update({texture_id: MakePath('textures', self._type, self._identifier, texture_name)})
        self._added_textures.append(texture_name)
        return self

    def script(self, *scripts: str):
        for script in scripts:
            self._description['description']['scripts']['pre_animation'].append(f'{script};')
        return self

    def init_vars(self, **vars):
        for var, value in vars.items():
            self._description['description']['scripts']['initialize'].append(f'v.{var}={value};')
        return self
    
    def scale(self, scale: str = '1'):
        if not scale == '1':
            self._description['description']['scripts'].update({"scale": scale})

    def render_controller(self, controller_name: str, condition: str = None):
        if condition is None:
            self._render_append(f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{controller_name}')
        else:
            self._render_append({f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{controller_name}': condition})

        return self._render_controllers.add_controller(controller_name)

    def particle_effect(self, particle_identifier: str):
        self._particle_name = particle_identifier
        self._description['description']['particle_effects'].update({self._particle_name: f'{NAMESPACE_FORMAT}:{self._particle_name}'})
        return self

    def sound_effect(self, sound_shortname: str, sound_identifier: str, category: SoundCategory = SoundCategory.Neutral):
        self._description['description']['sound_effects'].update({sound_shortname: sound_identifier})
        sound  : _SoundDefinition = ANVIL.sound(sound_identifier, category)
        self._sounds.append(sound)
        return sound

    def queue(self, directory: str = None):
        if len(self._description['description']['geometry']) == 0:
            RaiseError(MISSING_MODEL(f"{self._namespace_format}:{self._identifier}"))

        if len(self._description['description']['textures']) == 0:
            RaiseError(MISSING_TEXTURE(f"{self._namespace_format}:{self._identifier}"))

        if len(self._description['description']['render_controllers']) == 0:
            RaiseError(MISSING_RENDER_CONTROLLER(f"{self._namespace_format}:{self._identifier}"))
        
        if self._is_dummy:
            CopyFiles(MakePath('assets', 'models', self._type), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'models', self._type, directory), 'dummy.geo.json')
        
        elif self._added_geos == 1:
            if self._type == 'entity':
                CopyFiles(MakePath('assets', 'models', self._type), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'models', self._type, directory), f'{self._identifier}.geo.json')
            else:
                CopyFiles(MakePath('assets', 'models', self._type), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'models', 'entity', self._type, directory), f'{self._identifier}.geo.json')
        
        for text in self._added_textures:
            CopyFiles(MakePath('assets','textures', self._type), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures',self._type,self._identifier), f'{text}.png')
            
        for animation in self._added_anims:
            if animation != 'controller':
                CopyFiles(MakePath('assets', 'animations'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animations', directory), f'{self._identifier}.animation.json')
              
        if 'particle_effects' in self._description['description']:
            for particle in self._description['description']['particle_effects']:
                Particle(particle).queue()

        for sound in self._sounds:
            sound._export
        self._render_controllers.queue(directory)
        self._animation_controllers.queue(directory)
        return self._description

class _EntityServerDescription(_ActorDescription):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, is_vanilla)
        self._properties = _Properties()
        self._description['description'].update({
            'properties': {},
        })

    @property
    def Summonable(self):
        '''Sets whether or not we can summon this entity using commands such as /summon.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['is_summonable'] = True
        return self

    @property
    def Spawnable(self):
        '''Sets whether or not this entity has a spawn egg in the creative ui.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['is_spawnable'] = True
        return self

    @property
    def Experimental(self):
        '''Sets whether or not this entity is experimental. Experimental entities are only enabled when the experimental toggle is enabled.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['is_experimental'] = True
        return self

    def RuntimeIdentifier(self, identifier: Vanilla.Entities):
        '''Sets the name for the Vanilla Minecraft identifier this entity will use to build itself from.

        Parameters
        ----------
        identifier : Vanilla.Entities
            The identifier of the entity.

        Returns
        -------
            Entity description object.

        '''
        if not type(identifier) is str:
            raise TypeError('Runtime Identifier type must be a Vanilla.Entities')
        elif identifier in Vanilla.Entities._list:
            self._description['description']['runtime_identifier'] = f'minecraft:{identifier}'
            return self
        else:
            raise ValueError('The runtime identifier is not a valid minecraft entity.')

    @property
    def add_property(self):
        return self._properties

    @property
    def _export(self):
        self._description['description']['properties']=self._properties._export
        return super()._export

class _EntityClientDescription(_ActorClientDescription):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, is_vanilla, 'entity')

    @property
    def EnableAttachables(self):
        '''This determines if the entity can equip attachables when this is set to true. This allows the entity to render armor and weapons.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['enable_attachables'] = True
        return self

    @property
    def HeldItemIgnoresLighting(self):
        '''This determines if the item held by an entity should render fully lit up (if true), or depending on surrounding lighting.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['held_item_ignores_lighting'] = True
        return self

    @property
    def HideArmor(self):
        '''This determines if the armor attached to an entity should be hidden when set to true. This overrides the rendering settings specified by `EnableAttachables`.

        Returns
        -------
            Entity description object.

        '''
        self._description['description']['hide_armor'] = True
        return self
    
    @property
    def get_vanilla(self):
        vanilla_entity = ANVIL.get_github_file(f'resource_pack/entity/{self._identifier}.entity.json')
        self._description['description'].update(vanilla_entity['minecraft:client_entity']['description'])

    def spawn_egg(self, item_sprite: str):
        ANVIL._item_texture.add_item(item_sprite, 'spawn_eggs', item_sprite)
        self._description['description']['spawn_egg'] = {"texture": item_sprite}
    
    def queue(self, directory):
        super().queue(directory)
        if 'spawn_egg' not in self._description['description'] and not self._is_vanilla:
            spawn_egg_colors = GetColors(MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures',self._type, self._identifier, f'{self._description["description"]["textures"][self._spawn_egg_colors].split("/")[-1]}.png'))
            self._description['description']['spawn_egg'] = {
                'base_color': spawn_egg_colors[0],
                'overlay_color': spawn_egg_colors[1]
            }
        return self._description

class _AttachableClientDescription(_ActorClientDescription):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, is_vanilla, 'attachables')

class _Entity(Exporter):
    def __init__(self, identifier: str, type: str) -> None:
        self._identifier = identifier
        super().__init__(identifier, type)

class _EntityServer(_Entity):
    def _add_despawn_function(self):
        self.component_group("despawn").add(components.InstantDespawn())
        self.event("despawn").add("despawn")

    def _optimize_entity(self):
        self.components.add({
            "minecraft:conditional_bandwidth_optimization": {
                "default_values": {
                    "use_motion_prediction_hints": True
                }
            }
        })
    
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, 'server_entity')
        self._is_vanilla = is_vanilla
        self._server_entity = Schemes('server_entity')
        self._description = _EntityServerDescription(self._identifier, self._is_vanilla)
        self._animation_controllers = _BP_AnimationControllers(self._identifier, self._is_vanilla)
        self._animations = _BPAnimations(self._identifier, self._is_vanilla)
        self._spawn_rule = _SpawnRule(self._identifier, self._is_vanilla)
        self._components = _Components()
        self._events : list[_Event] = []
        self._component_groups : list[_ComponentGroup] = []
        self._vars = []
        self._add_despawn_function()
        self._optimize_entity()

    @property
    def description(self):
        return self._description

    @property
    def spawn_rule(self):
        return self._spawn_rule

    @property
    def dummy(self):
        self.description.Summonable
        self.components.overwrite(
            components.CollisionBox(0.1, 0.1),
            components.Health(1),
            components.Physics(),
            components.Pushable(False, False),
            components.TypeFamily('inanimate'),
            {
                "minecraft:damage_sensor": {
                    "triggers": [{"deals_damage": False}]
                }
            }
        )
        self._add_despawn_function()
        self._optimize_entity()
        return self

    @property
    def get_vanilla(self):
        vanilla_entity = ANVIL.get_github_file(f'behavior_pack/entities/{self._identifier}.json')
        self._server_entity['minecraft:entity'] = vanilla_entity['minecraft:entity']

    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
        self._description._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(self, animation_name: str, loop: bool = False, animate: bool = False, condition: str = None):
        self._description._animations(animation_name, animate, condition)
        return self._animations.add_animation(animation_name, loop)

    def init_vars(self, **vars):
        self._vars.extend([f'v.{var}={value}' for var, value in vars.items()])
        return self
    
    def event(self, event_name: str):
        self._event = _Event(event_name)
        self._events.append(self._event)
        return self._event

    @property
    def components(self):
        return self._components

    def component_group(self, component_group_name):
        self._component_group = _ComponentGroup(component_group_name)
        self._component_groups.append(self._component_group)
        return self._component_group

    def queue(self, directory: str = None):
        if len(self._vars) > 0:
            self.animation_controller('variables', True).add_state('default').on_entry(*self._vars)
        self._animations.queue(directory=directory)
        self._animation_controllers.queue(directory=directory)
        self._spawn_rule.queue(directory=directory)

        self._server_entity['minecraft:entity'].update(self.description._export)
        self._server_entity['minecraft:entity']['components'].update(self._components._export()['components'])

        for event in self._events:
            self._server_entity['minecraft:entity']['events'].update(event._export)
        for component_group in self._component_groups:
            self._server_entity['minecraft:entity']['component_groups'].update(component_group._export())
        


        self.content(self._server_entity)
        super().queue(directory=directory)

class _EntityClient(_Entity):
    def __init__(self, identifier: str, is_vanilla: bool = False) -> None:
        super().__init__(identifier, 'client_entity')
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._client_entity = Schemes('client_entity')
        self._description = _EntityClientDescription(self._identifier, self._is_vanilla)

    @property
    def description(self):
        return self._description

    def queue(self, directory: str = None):
        self._client_entity['minecraft:client_entity'].update(self._description.queue(directory))

        self.content(self._client_entity)
        super().queue(directory=directory)

# Render Controllers
class _RenderController():
    def __init__(self, identifier, controller_name, is_vanilla):
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._controller_name = controller_name
        self._controller = Schemes('render_controller', NAMESPACE_FORMAT, self._identifier, self._controller_name)
        self.controller_identifier = f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{self._controller_name}'

    def texture_array(self, array_name: str, *textures_short_names: str):
        self._controller[self.controller_identifier]['arrays']['textures'].update({f'Array.{array_name}': [f'Texture.{texture}' for texture in textures_short_names]})
        return self
    
    def material(self, bone: str, material_shortname: str):
        self._controller[self.controller_identifier]['materials'].append({bone: material_shortname if material_shortname.startswith(('v', 'q')) else f'Material.{material_shortname}'})
        return self
    
    def geometry_array(self, array_name: str, *geometries_short_names: str):
        self._controller[self.controller_identifier]['arrays']['geometries'].update({f'Array.{array_name}': [f'Geometry.{geometry}' for geometry in geometries_short_names]})
        return self

    def geometry(self, short_name: str = 'default'):
        if "Array" not in short_name : 
            name = f'Geometry.{short_name}'
        else : 
            name = short_name
        self._controller[self.controller_identifier]['geometry'] = name
        return self

    def textures(self, short_name: str = 'default'):
        if "Array" not in short_name : 
            name = f'Texture.{short_name}'
        else : name = short_name

        self._controller[self.controller_identifier]['textures'].append(name)
        return self

    def part_visibility(self, bone: str, condition: str | bool):
        self._controller[self.controller_identifier]['part_visibility'].append({bone: condition})
        return self

    def overlay_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({
            "overlay_color": {
                "a": a, "r": r, "g": g, "b": b
            }
        })
        return self

    def on_fire_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({
            "on_fire_color": {
                "a": a, "r": r,  "g": g, "b": b
            }
        })
        return self

    def is_hurt_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({
            "is_hurt_color": {
                "a": a, "r": r,  "g": g, "b": b
            }
        })
        return self

    def color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({
            "color": {
                "a": a, "r": r,  "g": g, "b": b
            }
        })
        return self
    
    @property
    def filter_lighting(self):
        self._controller[self.controller_identifier]['filter_lighting'] = True
        return self
    
    @property
    def ignore_lighting(self):
        self._controller[self.controller_identifier]['ignore_lighting'] = True
        return self
    
    def light_color_multiplier(self, multiplier: int):
        self._controller[self.controller_identifier]['light_color_multiplier'] = multiplier
        return self
    
    def uv_anim(self,offset:list[str, str],scale:list[str, str]):
        self._controller[self.controller_identifier]['uv_anim']={
            "offset":offset,
            "scale": scale
        }
    
    @property
    def _export(self):
        return self._controller

class _RenderControllers(Exporter):
    def __init__(self, identifier: str, is_vanilla) -> None:
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._controllers : list[_RenderController] = []
        self.render_controller = Schemes('render_controllers')
        super().__init__(self._identifier, 'render_controllers')
        
    def add_controller(self, controller_name: str):
        self._render_controller = _RenderController(self._identifier, controller_name, self._is_vanilla)
        self._controllers.append(self._render_controller)
        return self._render_controller

    def queue(self, directory: str = ''):
        if len(self._controllers) > 0:
            for controller in self._controllers:
                self.render_controller['render_controllers'].update(controller._export)
            self.content(self.render_controller)
            return super().queue(directory=directory)

# Animation Controllers
class _BP_ControllerState():
    def __init__(self, state_name):
        self._state_name = state_name
        self._controller_state : dict = Schemes('animation_controller_state', self._state_name)

    def on_entry(self, *commands: str):
        '''Events, commands or molang to preform on entry of this state.
        
        Parameters
        ----------
        commands : str
            param commands: The Events, commands or molang to preform on entry of this state.
            
        Returns
        -------
            This state.
        
        '''
        for command in commands:
            if str(command).startswith('@s'):
                self._controller_state[self._state_name]['on_entry'].append(f'{command}')
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_entry'].append(f'{command};')
            else:
                self._controller_state[self._state_name]['on_entry'].append(f'/{command}')
        return self

    def on_exit(self, *commands: str):
        '''Events, commands or molang to preform on exit of this state.
        
        Parameters
        ----------
        commands : str
            param commands: The Events, commands or molang to preform on exit of this state.
            
        Returns
        -------
            This state.
        
        '''
        for command in commands:
            if str(command).startswith('@s'):
                self._controller_state[self._state_name]['on_exit'].append(f'{command}')
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_exit'].append(f'{command};')
            else:
                self._controller_state[self._state_name]['on_exit'].append(f'/{command}')
        return self

    def animation(self, animation: str, condition: str = None):
        '''Animation short name to play during this state.
        
        Parameters
        ----------
        animation : str
            The name of the animation to play.
        condition : str , optional
            The condition on which this animation plays.
        
        Returns
        -------
            This state.
        
        '''
        if condition is None:
            self._controller_state[self._state_name]['animations'].append(animation)
        else:
            self._controller_state[self._state_name]['animations'].append(
                {animation: condition})
        return self

    def transition(self, state: str, condition: str):
        '''Target state to switch to and the condition to do so.
        
        Parameters
        ----------
        state : str
            The name of the state to transition to.
        condition : str
            The condition that must be met for the transition to occur.
        
        Returns
        -------
            This state.
        
        '''
        self._controller_state[self._state_name]['transitions'].append({
                                                                       state: condition})
        return self

    @property
    def _export(self):
        return self._controller_state

class _RP_ControllerState():
    def __init__(self, state_name):
        self._state_name = state_name
        self._controller_state = Schemes('animation_controller_state', self._state_name)
        self._controller_state[self._state_name]['particle_effects']=[]
        self._controller_state[self._state_name]['sound_effects']=[]

    def on_entry(self, *commands: str):
        '''Molang to preform on entry of this state.
        
        Parameters
        ----------
        commands : str
            param commands: Molang to preform on entry of this state.
            
        Returns
        -------
            This state.
        
        '''
        for command in commands:
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_entry'].append(f'{command};')
            else:
                RaiseError(MOLANG_ONLY(command))
        return self

    def on_exit(self, *commands: str):
        '''Molang to preform on exit of this state.
        
        Parameters
        ----------
        commands : str
            param commands: Molang to preform on exit of this state.
            
        Returns
        -------
            This state.
        
        '''
        for command in commands:
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_exit'].append(f'{command};')
            else:
                RaiseError(MOLANG_ONLY(command))
        return self

    def animation(self, animation: str, condition: str = None):
        '''Animation short name to play during this state.
        
        Parameters
        ----------
        animation : str
            The name of the animation to play.
        condition : str , optional
            The condition on which this animation plays.
        
        Returns
        -------
            This state.
        
        '''
        if condition is None:
            self._controller_state[self._state_name]['animations'].append(animation)
        else:
            self._controller_state[self._state_name]['animations'].append({animation: condition})
        return self

    def transition(self, state: str, condition: str):
        '''Target state to switch to and the condition to do so.
        
        Parameters
        ----------
        state : str
            The name of the state to transition to.
        condition : str
            The condition that must be met for the transition to occur.
        
        Returns
        -------
            This state.
        
        '''
        self._controller_state[self._state_name]['transitions'].append({state: condition})
        return self

    def particle(self, effect: str, locator: str, pre_anim_script: str = None, bind_to_actor : bool = True):
        '''The effect to be emitted during this state.
        
        Parameters
        ----------
        effect : str
            The shortname of the particle effect to be played, defined in the Client Entity.
        locator : str
            The name of a locator on the actor where the effect should be located.
        pre_anim_script : str , optional
            A molang script that will be run when the particle emitter is initialized.
        bind_to_actor : bool , optional
            Set to false to have the effect spawned in the world without being bound to an actor.
        
        Returns
        -------
            This state.
        
        '''
        particle = {'effect': effect, 'locator': locator}
        if pre_anim_script is not None:
            particle.update({'pre_effect_script': pre_anim_script})
        if bind_to_actor is False:
            particle.update({'bind_to_actor': False})
        self._controller_state[self._state_name]['particle_effects'].append(particle)
        return self

    def sound_effect(self, effect: str):
        '''Collection of sounds to trigger on entry to this animation state.
        
        Parameters
        ----------
        effect : str
            The shortname of the sound effect to be played, defined in the Client Entity.
        
        Returns
        -------
            This state.
        
        '''
        self._controller_state[self._state_name]['sound_effects'].append({'effect': effect})
        return self
            
    def blend_transition(self, blend_value: float):
        '''Sets the amount of time to fade out if the animation is interrupted.
        
        Parameters
        ----------
        blend_value : float
            Blend out time.
        
        Returns
        -------
            This state.
        
        '''
        self._controller_state[self._state_name]['blend_transition'] = blend_value
        return self

    @property
    def blend_via_shortest_path(self):
        '''When blending a transition to another state, animate each euler axis through the shortest rotation, instead of by value.
        
        Returns
        -------
            This state.
        
        '''
        self._controller_state[self._state_name]['blend_via_shortest_path'] = True
        return self

    @property
    def _export(self):
        return self._controller_state

class _BP_Controller():
    def __init__(self, identifier, controller_shortname, is_vanilla):
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._controller_shortname = controller_shortname
        self._controllers = Schemes('animation_controller', NAMESPACE_FORMAT, self._identifier, self._controller_shortname)
        self._controller_states: list[_BP_ControllerState] = []
        self._controller_namespace = f'controller.animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._controller_shortname}'
        self._states_names = []

    def add_state(self, state_name: str):
        self._states_names.append(state_name)
        '''Adds a new state to the animation controller.
        
        Parameters
        ----------
        state_name : str
            The name of the state to add.
        
        Returns
        -------
            Animation controller state.
        
        '''
        self._controller_state = _BP_ControllerState(state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state

    @property
    def _export(self):
        collected_states = []
        for state in self._controller_states:
            self._controllers[self._controller_namespace]['states'].update(state._export)
            for tr in state._export.values():
                if 'transitions' in tr:
                    for st in tr['transitions']:
                        collected_states.extend(st.keys())

        for state in collected_states:    
            if state not in self._states_names:
                print(MISSING_STATE(f'{self._namespace_format}:{self._identifier}',self._controller_namespace,*st.keys()))

        return self._controllers

class _RP_Controller(_BP_Controller):
    def __init__(self, name, controller_shortname, is_vanilla):
        super().__init__(name, controller_shortname, is_vanilla)
        self._controller_states: list[_RP_ControllerState] = []

    def add_state(self, state_name: str):
        self._states_names.append(state_name)
        self._controller_state = _RP_ControllerState(state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state

class _BP_AnimationControllers(Exporter):
    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier, 'bp_animation_controllers')
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._animation_controllers = Schemes('animation_controllers')
        self._controllers_list: list[_BP_Controller] = []

    def add_controller(self, controller_shortname: str) -> _BP_Controller:
        '''Adds a new animation controller to the current actor with `default` as the `initial_state`.
        
        Parameters
        ----------
        controller_shortname : str
            The shortname of the controller you want to add.
        
        Returns
        -------
            Animation controller.
        
        '''
        self._controller = _BP_Controller(self._name, controller_shortname, self._is_vanilla)
        self._controllers_list.append(self._controller)
        return self._controller

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            for controller in self._controllers_list:
                self._animation_controllers['animation_controllers'].update(controller._export)
            self.content(self._animation_controllers)
            return super().queue(directory=directory)

class _RP_AnimationControllers(Exporter):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, 'rp_animation_controllers')
        self._name = name
        self._is_vanilla = is_vanilla
        self._animation_controllers = Schemes('animation_controllers')
        self._controllers_list: list[_RP_Controller] = []

    def add_controller(self, controller_shortname: str) -> _RP_Controller:
        '''Adds a new animation controller to the current actor with `default` as the `initial_state`.
        
        Parameters
        ----------
        controller_shortname : str
            The shortname of the controller you want to add.
        
        Returns
        -------
            Animation controller.
        
        '''
        self._animation_controller = _RP_Controller(self._name, controller_shortname, self._is_vanilla)
        self._controllers_list.append(self._animation_controller)
        return self._animation_controller

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            for controller in self._controllers_list:
                self._animation_controllers['animation_controllers'].update(controller._export)
            self.content(self._animation_controllers)
            return super().queue(directory=directory)

# Animations
class _BPAnimation():
    def __init__(self, identifier, animation_short_name: str, loop: bool, is_vanilla):
        self._is_vanilla = is_vanilla
        self._identifier = identifier
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._animation_short_name = animation_short_name
        self._animation_length = 0.01
        self._animation = Schemes('bp_animation', NAMESPACE_FORMAT, self._identifier, self._animation_short_name, loop)

    def timeline(self, timestamp: float, *commands: str):
        '''Takes a timestamp and a list of events, command or molang to run at that time.
        
        Parameters
        ----------
        timestamp : int
            The timestamp of the event.
        commands : str
            param commands: The Events, commands or molang to run on exit of this state.
        
        Returns
        -------
            This animation.
        
        '''
        if self._animation_length < timestamp:
            self._animation_length = timestamp+0.1
        self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['animation_length'] = self._animation_length
        if timestamp not in self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['timeline']:
            self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['timeline'][timestamp] = []
        for command in commands:
            if str(command).startswith('@s'):
                self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['timeline'][timestamp].append(f'{command}')
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['timeline'][timestamp].append(f'{command};')
            else:
                self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['timeline'][timestamp].append(f'/{command}')
        return self

    def animation_length(self, animation_length: float):
        '''This function sets the length of the animation.
        
        Parameters
        ----------
        animation_length : int
            The length of the animation in seconds.
        
        Returns
        -------
            This animation.
        
        '''
        self._animation[f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._animation_short_name}']['animation_length'] = animation_length
        return self

    @property
    def _export(self):
        return self._animation

class _BPAnimations(Exporter):
    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier, 'bp_animations')
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._animations = Schemes('bp_animations')
        self._animations_list: list[_BPAnimation] = []

    def add_animation(self, animation_short_name: str, loop: bool = False):
        '''Adds a new animation to the current actor.
        
        Parameters
        ----------
        animation_short_name : str
            The shortname of the animation you want to add.
        loop : bool, optional
            If the animation should loop or not.
        
        Returns
        -------
            Animation.
        
        '''
        self._animation = _BPAnimation(self._identifier, animation_short_name, loop, self._is_vanilla)
        self._animations_list.append(self._animation)
        return self._animation

    def queue(self, directory: str = None):
        if len(self._animations_list) > 0:
            for animation in self._animations_list:
                self._animations['animations'].update(animation._export)
            self.content(self._animations)
            return super().queue(directory=directory)

# Spawn Rules
class _SpawnRuleDescription(_MinecraftDescription):
    def __init__(self, spawn_rule_obj , name: str, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._spawn_rule_obj : _SpawnRule = spawn_rule_obj
        self._description['description']['population_control'] = Population.Ambient

    def population_control(self, population: Population):
        '''Setting an entity to a pool it will spawn as long as that pool hasn't reached the spawn limit.
        
        Parameters
        ----------
        population : Population
            Population Control
                `Animal`, `UnderwaterAnimal`, `Monster`, `Ambient`
        
        Returns
        -------
            Spawn Rule
        
        '''
        self._description['description']['population_control'] = population
        return self._spawn_rule_obj

class _Condition():
    def __init__(self):
        self._condition = {}

    @property
    def SpawnOnSurface(self):
        '''Sets the actor to spawn on surfaces.

        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({'minecraft:spawns_on_surface': {}})
        return self

    @property
    def SpawnUnderground(self):
        '''Sets the actor to spawn underground.

        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:spawns_underground': {}})
        return self

    @property
    def SpawnUnderwater(self):
        '''Sets the actor to spawn underwater.

        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({'minecraft:spawns_underwater': {}})
        return self

    @property
    def SpawnInLava(self):
        '''Sets the actor to spawn in lava.

        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({'minecraft:spawns_lava': {}})
        return self

    def SpawnsOnBlockFilter(self, *block):
        '''Sets the list of blocks the actor can spawn on top of.

        Parameters
        ----------
        block : str
            Valid blocks to activate this component.
        
        Returns
        -------
            Spawn rule condition.

        '''
        if 'minecraft:spawns_on_block_filter' not in self._condition:
            self._condition.update(
                {'minecraft:spawns_on_block_filter': []})
        self._condition['minecraft:spawns_on_block_filter']=block
        return self

    def DensityLimit(self, surface : int=-1, underground : int=-1):
        '''Sets the density limit number of this mob type to spawn.
        
        Parameters
        ----------
        surface : int
            The maximum number of mob of this mob type spawnable on the surface. `-1` for an unlimited number.
        underground : int
            The maximum number of mob of this mob type spawnable underground. `-1` for an unlimited number.
        
        Returns
        -------
            Spawn rule condition.

        '''
        density = {'minecraft:density_limit': {}}
        if surface != -1:
            density['minecraft:density_limit']['surface'] = surface
        if underground != -1:
            density['minecraft:density_limit']['underground'] = underground
        self._condition.update(density)
        return self

    def BrightnessFilter(self, min_brightness: int = 0, max_brightness: int = 15, adjust_for_weather: bool = True):
        '''This function filters the image by brightness
        
        Parameters
        ----------
        min_brightness : int
            The minimum light level value that allows the mob to spawn. Allowed range is (0,15)
        max_brightness : int
            The maximum light level value that allows the mob to spawn. Allowed range is (0,15)
        adjust_for_weather : bool, optional
            This determines if weather can affect the light level conditions that cause the mob to spawn (e.g. Allowing hostile mobs to spawn during the day when it rains.)
        
        Returns
        -------
            Spawn rule condition.

        '''
        min_brightness = max(0, min_brightness)
        max_brightness = min(15, max_brightness)
        self._condition.update({'minecraft:brightness_filter': {
                               'min': min_brightness, 'max': max_brightness, 'adjust_for_weather': adjust_for_weather}})
        return self

    def DifficultyFilter(self, min_difficulty: Difficulty = Difficulty.Easy, max_difficulty: Difficulty = Difficulty.Hard):
        '''Sets the range of difficulties this mob type should spawn in.
        
        Parameters
        ----------
        min_difficulty : Difficulty
            The minimum difficulty level that this mob spawns in. 
        max_difficulty : Difficulty
            The maximum difficulty level that this mob spawns in.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({'minecraft:difficulty_filter': {
                               'min': min_difficulty, 'max': max_difficulty}})
        return self

    def Weight(self, weight: int = 0):
        '''The weight on how likely the spawn rule chooses this condition over other valid conditions. The higher the value the more likely it will be chosen.
        
        Parameters
        ----------
        weight : int
            The weight of the item.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:weight': {'default': weight}})
        return self

    def Herd(self, min_size: int = 1, max_size: int = 4, spawn_event: str = None, event_skip_count: int = 0):
        '''Determines the herd size of this mob.
        
        Parameters
        ----------
        min_size : int
            The minimum number of mobs of this type that can spawn in the herd.
        max_size : int
            The maximum number of mobs of this type that can spawn in the herd.
        spawn_event : str, optional
            	This is an event that can be triggered from spawning.
        event_skip_count : int, optional
            This is the number of mobs spawned before the Specifies event is triggered.
        
        Returns
        -------
            Spawn rule condition.

        '''
        if 'minecraft:herd' not in self._condition:
            self._condition.update(
                {'minecraft:herd': []})
        self_herd = {'min_size': min_size, 'max_size': max_size}
        if spawn_event != None:
            self_herd.update(
                {'event': spawn_event, 'event_skip_count': event_skip_count})
        self._condition['minecraft:herd'].append(self_herd)
        return self

    def BiomeFilter(self, filter: dict):
        '''Specifies which biomes the mob spawns in.
        
        Parameters
        ----------
        filter : dict
            Filter dict
        
        Returns
        -------
            Spawn rule condition.

        '''
        if 'minecraft:biome_filter' not in self._condition:
            self._condition.update({'minecraft:biome_filter': []})
        self._condition['minecraft:biome_filter'].append(filter)
        return self

    def HeightFilter(self, min: int, max: int):
        '''Specifies the height range this mob spawn in.
        
        Parameters
        ----------
        min : int
            The minimum height that allows the mob to spawn.
        max : int
            The maximum height that allows the mob to spawn.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:height_filter': {'min': min, 'max': max}})
        return self
    
    def WorldAgeFilter(self, min: int):
        '''Specifies the minimum age of the world before this mob can spawn.
        
        Parameters
        ----------
        min : int
            The minimum age of the world.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:world_age_filter': {'min': min}})
        
        return self

    def SpawnsOnBlockPreventedFilter(self, *block):
        '''Sets the list of blocks the actor should not spawn on.

        Returns
        -------
            Spawn rule condition.

        '''
        if 'minecraft:spawns_on_block_prevented_filter' not in self._condition:
            self._condition.update(
                {'minecraft:spawns_on_block_prevented_filter': []})
        self._condition['minecraft:spawns_on_block_prevented_filter']=block
        return self

    @property
    def DisallowSpawnsInBubble(self):
        '''Prevents this mob from spawning in water bubbles.

        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({'minecraft:disallow_spawns_in_bubble': {}})
        return self

    def MobEventFilter(self, event: str):
        '''Specifies the event to call on spawn.
        
        Parameters
        ----------
        event : str
            The event to call.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:mob_event_filter': {'event': event}})
    
        return self
    
    def DistanceFilter(self, min: int, max: int):
        '''Specifies the distance range from a player this mob spawn in.
        
        Parameters
        ----------
        min : int
            The minimum distance from a player that allows the mob to spawn.
        max : int
            The maximum distance from a player that allows the mob to spawn.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:distance_filter': {'min': min, 'max': max}})
        return self
    
    def DelayFilter(self, minimum: int, maximum: int, identifier: str, spawn_chance: int):
        '''Unknown behavior.
        
        Parameters
        ----------
        minimum : int
            The minimum time required to use.
        maximum : int
            The maximum time required to use
        identifier : str
            	The * identifier.
        spawn_chance : int
            This is spawn chance. range of (0-100)
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({
            'minecraft:delay_filter': {
                'min': minimum,
                'max': maximum,
                'identifier': identifier,
                'spawn_chance': max(min(spawn_chance, 100), 0)
            }
        })
        
        return self

    def PermuteType(self, entity_type: str, weight: int = 10, spawn_event: str = None):
        '''Sets a chance to mutate the spawned entity into another.
        
        Parameters
        ----------
        entity_type : str
            The entity identifier.
        weight : str
            	The weight of permutation.
        spawn_event : str, optional
            The event to call on the entity spawning.
        
        Returns
        -------
            Spawn rule condition.

        '''
        if 'minecraft:permute_type' not in self._condition:
            self._condition.update(
                {'minecraft:permute_type': []})
        self_permute_type = {'entity_type': entity_type, 'weight': weight}
        if spawn_event != None:
            self_permute_type.update(
                {'entity_type': f'{entity_type}<{spawn_event}>'})
        self._condition['minecraft:permute_type'].append(self_permute_type)
        return self

    def SpawnEvent(self, event: str = 'minecraft:entity_spawned'):
        '''Sets the event to call when the entity spawn in the world. By default the event called is `minecraft:entity_spawned` event without using this component.
        
        Parameters
        ----------
        event : str
            the event to call on entity spawn.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:spawn_event': {'event': event}})
        return self

    def PlayerInVillageFilter(self, distance: int, village_border_tolerance: int):
        '''Specifies the distance range the player must be from a village for this entity to spawn.
        
        Parameters
        ----------
        distance : int
            The distance from the village.
        village_border_tolerance : int
            The distance tolerance from the village borders.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update(
            {'minecraft:player_in_village_filter': {'distance': distance, 'village_border_tolerance': village_border_tolerance}})
        return self
    
    def SpawnsAboveBlockFilter(self, distance: int, *block):
        '''Sets the list of blocks the actor can spawn above.

        Parameters
        ----------
        distance : int
            The vertical distance to check for valid blocks.
        block : str
            Valid blocks to activate this component.
        
        Returns
        -------
            Spawn rule condition.

        '''
        self._condition.update({
            'minecraft:spawns_above_block_filter': {
                'distance': distance,
                'blocks': block
            }
        })
        return self

    def export(self):
        return self._condition

class _SpawnRule(Exporter):
    def __init__(self, identifier, is_vanilla):
        super().__init__(identifier, 'spawn_rules')
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = NAMESPACE_FORMAT
        if is_vanilla:
            self._namespace_format = 'minecraft'
        self._description = _SpawnRuleDescription(self, self._identifier, self._is_vanilla)
        self._spawn_rule = Schemes('spawn_rules', NAMESPACE_FORMAT, self._identifier)
        self._conditions = []

    @property
    def description(self):
        return self._description

    @property
    def add_condition(self):
        self._condition = _Condition()
        self._conditions.append(self._condition)
        return self._condition

    def queue(self, directory: str = None):
        if len(self._conditions) > 0:
            self._spawn_rule['minecraft:spawn_rules'].update(self._description._export)
            self._spawn_rule['minecraft:spawn_rules']['conditions'] = [condition.export() for condition in self._conditions]
            self.content(self._spawn_rule)
            return super().queue(directory=directory)

# Events
class _BaseEvent():
    def __init__(self, event_name: str):
        self._event_name = event_name
        self._event = {self._event_name: {
            'add': {'component_groups':[]},
            'remove': {'component_groups':[]},
            'run_command': {'command':[]},
            'set_property': {}
        }}

    def add(self, *component_groups: str):
        self._event[self._event_name]['add']['component_groups'].extend(component_groups)
        return self

    def remove(self, *component_groups: str):
        self._event[self._event_name]['remove']['component_groups'].extend(component_groups)
        return self

    def trigger(self, event: str):
        self._event[self._event_name]['trigger'] = event
        return self

    def set_property(self, property, value):
        self._event[self._event_name]['set_property'].update({
            f'{NAMESPACE}:{property}':value
        })
        return self

    def update(self, components: dict):
        self._event[self._event_name] = components

    #experimental
    def _run_command(self, *commands: str):
        self._event[self._event_name]['run_command']['command'].extend(cmd for cmd in commands)
        return self

    @property
    def _export(self):
        return self._event

class _Randomize(_BaseEvent):
    def __init__(self, parent):
        self._event = {"weight": 1, 'set_property':{}}
        self._sequences : list[_Sequence] = []
        self._parent_class : _Event = parent

    def add(self, *component_groups):
        self._event.update({'add': {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({'remove': {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event):
        self._event.update({'trigger': event})
        return self

    def weight(self, weight: int):
        self._event.update({'weight': weight})
        return self
    
    def set_property(self, property, value):
        self._event['set_property'].update({
            f'{NAMESPACE}:{property}':value
        })
        return self

    @property
    def randomize(self):
        return self._parent_class.randomize

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def _export(self):
        if len(self._sequences) > 0:
            self._event.update({'sequence': []})
            for sequence in self._sequences:
                self._event['sequence'].append(sequence._export)
        return self._event

class _Sequence(_BaseEvent):
    def __init__(self, parent_event) -> None:
        self._randomizes : list[_Randomize] = []
        self._parent_class : _Event = parent_event
        self._event = {'set_property':{}}

    def add(self, *component_groups):
        self._event.update({'add': {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({'remove': {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event):
        self._event.update({'trigger': event})
        return self

    def filters(self, filter: dict):
        self._event.update({'filters': filter})
        return self

    def set_property(self, property, value):
        self._event['set_property'].update({
            f'{NAMESPACE}:{property}':value
        })
    @property
    def sequence(self):
        return self._parent_class.sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    @property
    def _export(self):
        if len(self._randomizes) > 0:
            self._event.update({'randomize': []})
            for randomize in self._randomizes:
                self._event['randomize'].append(randomize._export)
        return self._event

class _Event(_BaseEvent):
    def __init__(self, event_name: str):
        super().__init__(event_name)
        self._sequences : list[_Sequence] = []
        self._randomizes : list[_Randomize] = []

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    @property
    def _export(self):
        if len(self._sequences) > 0 and len(self._randomizes) > 0:
            raise  SyntaxError('Sequences and Randomizes cannot coexist in the same event.')
        if len(self._sequences) > 0:
            self._event[self._event_name].update({'sequence': []})
            for sequence in self._sequences:
                self._event[self._event_name]['sequence'].append(sequence._export)
        if len(self._randomizes) > 0:
            self._event[self._event_name].update({'randomize': []})
            for randomize in self._randomizes:
                self._event[self._event_name]['randomize'].append(randomize._export)
        return super()._export

# Components
class _Components():
    def __init__(self):
        self._component_group_name = 'components'
        self._components = {self._component_group_name: {}}

    def add(self, *components: object):
        for component in components:
            self._components[self._component_group_name].update(component)
        return self

    def remove(self, *components: object):
        for component in components:
            self._components[self._component_group_name].pop(component._component_namespace)
        return self

    def overwrite(self, *components: object):
        self._components[self._component_group_name] = {}
        for component in components:
            self._components[self._component_group_name].update(component)

    def _export(self):
        return self._components

class _ComponentGroup(_Components):
    def __init__(self, component_group_name: str):
        super().__init__()
        self._component_group_name = component_group_name
        self._components = {self._component_group_name: {}}

class _Properties():
    def __init__(self):
        self._properties = {}

    def enum(self, name : str, range : tuple[str], *, default: str, client_sync : bool = False):
        self._properties[f'{NAMESPACE}:{name}'] = {
                "type": "enum", 
                'default': default,
                'range': range,
                'client_sync': client_sync
            }
        return self
    
    def int(self, name : str, range : tuple[int, int], *, default: int = 0, client_sync : bool = False):
        self._properties[f'{NAMESPACE}:{name}'] = {
            "type": "int", 
            'default': int(default),
            'range': range,
            'client_sync': client_sync
        }
        return self
        
    def float(self, name : str, range : tuple[float, float], *, default: float = 0, client_sync : bool = False):
        self._properties[f'{NAMESPACE}:{name}'] = {
            "type": "float", 
            'default': float(default),
            'range': range,
            'client_sync': client_sync
        }
        return self

    def bool(self, name : str, *, default: bool = False, client_sync : bool = False):
        self._properties[f'{NAMESPACE}:{name}'] = {
            "type": "bool", 
            'default': default,
            'client_sync': client_sync
        }
        return self

    @property
    def _export(self):
        return self._properties

# ==========================
class Entity():
    def _validate_name(self, identifier):
        if ':' in identifier:
            raise ValueError(NAMESPACES_NOT_ALLOWED(identifier))

    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
        self._is_vanilla = False
        if identifier in Vanilla.Entities._list:
            self._is_vanilla = True

        self._namespace_format = NAMESPACE_FORMAT
        if self._is_vanilla:
            self._namespace_format = 'minecraft'

        self._validate_name(self._identifier)
        self._server = _EntityServer(self._identifier, self._is_vanilla)
        self._client = _EntityClient(self._identifier, self._is_vanilla)

    @property
    def Server(self):
        '''Server-side logic.

        Returns
        -------
            Server Entity.
        '''
        return self._server

    @property
    def Client(self):
        '''Client-side.

        Returns
        -------
            Client Entity.
        '''
        return self._client

    @property
    def identifier(self):
        return f'{self._namespace_format}:{self._identifier}'

    def queue(self, directory: str = None):
        display_name = RawText(self._identifier)[1]
        ANVIL.localize(f'entity.{self._namespace_format}:{self._identifier}.name={display_name}')
        ANVIL.localize(f'item.spawn_egg.entity.{self._namespace_format}:{self._identifier}.name=Spawn {display_name}')
        ANVIL._entities.update({f'{self._namespace_format}:{self._identifier}': {"Display Name": display_name}})
        self.Client.queue(directory)
        self.Server.queue(directory)

class Attachable(Exporter):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, 'attachable')
        self._identifier = identifier
        self._attachable = Schemes('attachable')
        self._description = _AttachableClientDescription(self._identifier, False)
    
    @property
    def description(self):
        return self._description

    @property
    def queue(self):
        self._attachable['minecraft:attachable'].update(self._description.queue('attachables'))
        self.content(self._attachable)
        super().queue('attachables')
