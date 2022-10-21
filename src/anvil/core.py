from .packages import *
from .submodules import components

# Rework
# File System Exporter for the rework
class Exporter():
    def __init__(self, name: str, type: str, filetype: str) -> None:
        self._valids = {
            'function': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'functions', 'NAMESPACE')
            },
            'server_entity': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'entities')
            },
            'client_entity': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'entity')
            },
            'dialogue': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'dialogue')
            },
            'bp_item_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'items')
            },
            'bp_block_v1': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'blocks')
            },
            'loot_table': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'loot_tables')
            },
            'bp_animation_controllers': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animation_controllers')
            },
            'bp_animations': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'animations')
            },
            'spawn_rules': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'spawn_rules')
            },
            'recipe': {
                'path': MakePath('behavior_packs', f'BP_{PASCAL_PROJECT_NAME}', 'recipe')
            },
            'language': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'texts')
            },
            'rp_item_v1': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'items')
            },
            'rp_animation_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animation_controllers')
            },
            'render_controllers': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'render_controllers')
            },
            'rp_animation': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'animations')
            },
            'attachable': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'attachables')
            },
            'particle': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'particles')
            },
            'assets': {
                'path': MakePath('assets')
            },
            'ui': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'ui')
            },
            'item_textures': {
                'path': MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures')
            }
        }
        self._name = name
        self._type = type
        self._filetype = filetype
        self._directory = ''
        if self._type not in self._valids:
            raise TypeError(f'{self._type} is not a supported type.')

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
        File(f'{self._name}{self._filetype}', self._content, self._path, 'w')


class ItemTextures(Exporter):
    def __init__(self) -> None:
        self._content = Schemes('item_textures', PROJECT_NAME)
        super().__init__('', 'item_textures', '.json')

    def add_item(self, item_name: str, *item_sprites: str):
        for item in item_sprites:
            CheckAvailability(item, 'sprite', MakePath('assets', 'textures', 'items'))
        self._content['texture_data'][item_name]=item_sprites

    def queue(self, directory: str = ''):
        return super().queue(directory)
    
    def _export(self):
        if len(self._content['texture_data']) > 0:
            for item in self._content['texture_data']:
                for sprite in item:
                    CopyFiles(MakePath('assets', 'textures', 'items'), MakePath('resource_packs', f'RP_{PASCAL_PROJECT_NAME}', 'textures', 'items', 'spawn_eggs'), f'{sprite}.png')
        return super()._export()

# Descriptions
#Basic Description class
class _MinecraftDescription():
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
        self._description : dict = Schemes('description', NAMESPACE_FORMAT, self._identifier)

    @property
    def _export(self):
        return self._description


class _SpawnRuleDescription(_MinecraftDescription):
    def __init__(self, spawn_rule_obj , name: str) -> None:
        super().__init__(name)
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


class _EntityDescription(_MinecraftDescription):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)
        self._animation_controllers_list = []
        self._animations_list = []
        self._description['description'].update({
            'animations': {},
            'scripts': {'animate':{}}
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
            {animation_shortname: f'animation.{NAMESPACE_FORMAT}.{self._name}.{animation_shortname}'}
        )


class _EntityServerDescription(_EntityDescription):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)

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

    def RuntimeIdentifier(self, identifier: Vanilla.Entities._list):
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
        elif 'minecraft:' + identifier in Vanilla.Entities._list:
            self._description['description']['runtime_identifier'] = identifier
            return self
        else:
            raise ValueError('The runtime identifier is not a valid minecraft entity.')


class _EntityClientDescription(_EntityDescription):
    def _check_model(self, entity_name, model_name):
        geo_namespace = f'geometry.{NAMESPACE_FORMAT}.{model_name}'
        with open(f'assets/geometries/{entity_name}.geo.json') as file:
            data = json.load(file)
            for geo in data['minecraft:geometry']:
                if geo_namespace not in geo['description']["identifier"] :
                    RaiseError(f'The geometry file {entity_name}.geo.json doesn\'t contain a geometry called {geo_namespace}')
    
    def _check_animation(self, animation_name):
        anim_namespace = f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{animation_name}'
        with open(f'assets/animations/{self._identifier}.animation.json') as file:
            if animation_name not in file.read():
                RaiseError(f'The animation file {self._identifier}.animation.json doesn\'t contain an animation called {anim_namespace}')

    def _render_append(self, key):
        if key not in self._description['description']['render_controllers']:
            self._description['description']['render_controllers'].append(key)

    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)
        self._animation_controllers = _RP_AnimationControllers(self._identifier)
        self._render_controllers = _RenderControllers(self._identifier)
        self._description.update({
            'materials': {
                'default': 'entity_alphatest'
            },
            'scripts':{
                'pre_animation':[],
                'initialize': []
            },
            'textures': {},
            'geometry': {},
            'render_controllers': []
        })
        self._is_dummy = False

    @property
    def dummy(self):
        self._is_dummy = True
        File('dummy.geo.json', Schemes('geometry','dummy',{"name": "root", "pivot": [0, 0, 0], "locators": {"root": [0, 0, 0]}}), 'models/entity', 'w')
        CreateImage('dummy', 8, 8, (0, 0, 0, 0), 'assets/textures/entity')
        self.geometry('dummy', 'dummy')
        self.texture('dummy', 'dummy')
        self.render_controller('dummy').geometry('dummy').textures('dummy')

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
        self._description['description']['is_experimental'] = True
        return self
    
    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
        self._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(self, animation_name: str, animate: bool = False, condition: str = None):
        CheckAvailability(f'{self._identifier}.animation.json', 'animation', 'assets/animations')
        self._check_animation(animation_name)
        self._animations(animation_name, animate, condition)
        return self

    def material(self, material_id: str, material_name: str):
        self._description['materials'].update({material_id: material_name})
        return self

    def geometry(self, geometry_id: str, geometry_name: str):
        CheckAvailability(f'{self._identifier}.geo.json', 'geometry', MakePath('assets','models','entity'))
        self._check_model(self._identifier, geometry_name)
        self._description['geometry'].update({geometry_id: f'geometry.{NAMESPACE_FORMAT}.{geometry_name}'})
        return self

    def texture(self, texture_id: str, texture_name: str):
        self._spawn_egg_colors = texture_id
        CheckAvailability(f'{texture_name}.png','texture', MakePath('assets','textures','entity'))
        self._description['textures'].update({texture_id: MakePath('textures','entity',self._identifier,texture_name)})
        return self

    def script(self, *scripts: str):
        for script in scripts:
            self._description['scripts']['pre_animation'].append(f'{script};')
        return self

    def init_vars(self, **vars):
        for var, value in vars.items():
            self._description['scripts']['pre_animation'].append(f'v.{var}={value};')
        return self
    
    def scale(self, scale: str = '1'):
        if not scale == '1':
            self._description['scripts'].update({"scale": scale})

    def render_controller(self, controller_name: str, condition: str = None):
        if condition is None:
            self._animate_append(controller_name)
        else:
            self._animate_append({controller_name: condition})

        return self._render_controllers.add_controller(controller_name)

    def particle_effect(self, particle_identifier: str):
        self._particle_name = particle_identifier
        Particle(self._particle_name).queue()
        self._description.update({self._particle_name: f'{NAMESPACE_FORMAT}:{self._particle_name}'})

    def sound_effect(self, sound_shortname: str, sound_identifier: str):
        self._description.update({sound_shortname: sound_identifier})
        return self

    def spawn_egg(self, item_sprite: str):
        ANVIL._item_textures.add_item(f'{self._identifier}_spawn_egg', item_sprite)
        self._description['spawn_egg'] = {"texture": f'{self._identifier}_spawn_egg'}
    
    def queue(self, directory):
        if len(self._description['geometry']) == 0:
            RaiseError(f'{self._identifier} missing a geometry')
        if len(self._description['textures']) == 0:
            RaiseError(f'{self._identifier} missing a texture')
        if len(self._description['render_controllers']) == 0:
            RaiseError(f'{self._identifier} missing a render controller')
        if self._is_dummy:
            CopyFiles(MakePath('assets','geometries'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','models','entity',directory), 'dummy.geo.json')
        else:
            CopyFiles(MakePath('assets','geometries'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','models','entity',directory), f'{self._identifier}.geo.json')
        
        for text in self._description['textures']:
            CopyFiles(MakePath('assets','textures', 'entity'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures','entity',self._identifier),f'{self._description["textures"][text].split("/")[-1]}.png')
            
        if 'animations' in self._description:
            for animation in self._description['animations']:
                if self._description['animations'][animation].split('.')[0] != 'controller':
                    CopyFiles(MakePath('assets','animations'), MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','animations',directory),f'{self._identifier}.animation.json')
                    
        if 'spawn_egg' not in self._description:
            spawn_egg_colors = GetColors(MakePath('resource_packs',f'RP_{PASCAL_PROJECT_NAME}','textures','entity', self._identifier, f'{self._description["textures"][self._spawn_egg_colors].split("/")[-1]}.png'))
            self._description['spawn_egg'] = {
                'base_color': spawn_egg_colors[0],
                'overlay_color': spawn_egg_colors[1]
            }
        self._render_controllers.queue(directory)
        self._animation_controllers.queue(directory)


# Render Controllers
class _RenderController():
    def __init__(self, identifier, controller_name):
        self._identifier = identifier
        self._controller_name = controller_name
        self._controller = Schemes('render_controller', NAMESPACE_FORMAT, self._identifier, self._controller_name)
        self.controller_identifier = f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{self._controller_name}'

    def texture_array(self, array_name: str, *textures_short_names: str):
        self._controller[self.controller_identifier]['arrays']['textures'].update({f'Array.{array_name}': [f'Texture.{texture}' for texture in textures_short_names]})
        return self
    
    def material(self, bone: str, material_shortname: str):
        self._controller[self.controller_identifier]['materials'].append({bone: f'Material.{material_shortname}'})
        return self
    
    def geometry_array(self, array_name: str, *geometries_short_names: str):
        self._controller[self.controller_identifier]['arrays']['geometries'].update({f'Array.{array_name}': [f'Geometry.{geometry}' for geometry in geometries_short_names]})
        return self

    def geometry(self, short_name: str = 'default'):
        if "Array" not in short_name : name = short_name
        else : name = f'Geometry.{short_name}'
            
        self._controller[self.controller_identifier].update(name)
        return self

    def textures(self, short_name: str = 'default'):
        if "Array" not in short_name : name = short_name
        else : name = f'Texture.{short_name}'

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
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
        self._controllers : list[_RenderController] = []
        self.render_controller = Schemes('render_controllers')
        super().__init__(self._identifier, 'render_controllers', FileExtension('render_controllers'))
        
    def add_controller(self, controller_name: str):
        self._render_controller = _RenderController(self._identifier, controller_name)
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
        self._controller_state = Schemes('animation_controller_state', self._state_name)

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
            if command.startswith('@s'):
                self._controller_state[self._state_name]['on_entry'].append(f'{command}')
            elif any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_entry'].append(f'{command};')
            else:
                self._controller_state[self._state_name]['on_entry'].append(
                    f'/{command}')
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
            if command.startswith('@s'):
                self._controller_state[self._state_name]['on_exit'].append(f'{command}')
            elif any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]['on_exit'].append(f'{command};')
            else:
                self._controller_state[self._state_name]['on_exit'].append(
                    f'/{command}')
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
        self._controller_state[self._state_name]['particles']=[]
        self._controller_state[self._state_name]['sound_effect']=[]

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
                RaiseError('Unrecognized operation.')
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
                RaiseError('Unrecognized operation.')
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
        self._controller_state[self._state_name]['particles'].append(particle)
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
        self._controller_state[self._state_name]['sound_effect'].append({'effect': effect})
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
    def __init__(self, identifier, controller_shortname):
        self._identifier = identifier
        self._controller_shortname = controller_shortname
        self._controllers = Schemes('animation_controller', NAMESPACE_FORMAT, self._identifier, self._controller_shortname)
        self._controller_states: list[_BP_ControllerState] = []

    def add_state(self, state_name: str):
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
        for state in self._controller_states:
            self._controllers[f'controller.animation.{NAMESPACE_FORMAT}.{self._identifier}.{self._controller_shortname}']['states'].update(state._export)
        return self._controllers


class _RP_Controller(_BP_Controller):
    def __init__(self, name, controller_shortname):
        super().__init__(name, controller_shortname)
        self._controller_states: list[_RP_ControllerState] = []

    def add_state(self, state_name: str):
        self._controller_state = _RP_ControllerState(state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state


class _BP_AnimationControllers(Exporter):
    def __init__(self, identifier) -> None:
        super().__init__(identifier, 'bp_animation_controllers', FileExtension('bp_animation_controllers'))
        self._identifier = identifier
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
        self._controller = _BP_Controller(self._name, controller_shortname)
        self._controllers_list.append(self._controller)
        return self._controller

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            for controller in self._controllers_list:
                self._animation_controllers['animation_controllers'].update(controller._export)
            self.content(self._animation_controllers)
            return super().queue(directory=directory)


class _RP_AnimationControllers(Exporter):
    def __init__(self, name) -> None:
        super().__init__(name, 'rp_animation_controllers', FileExtension('rp_animation_controllers'))
        self._name = name
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
        self._animation_controller = _RP_Controller(self._name, controller_shortname)
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
    def __init__(self, animation_short_name: str, loop: bool = False):
        self._animation_short_name = animation_short_name
        self._animation_length = 0.01
        self._animation = Schemes('bp_animation', NAMESPACE_FORMAT, self._animation_short_name, loop)

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
        from .commands import validate
        if self._animation_length < timestamp:
            self._animation_length = timestamp+0.1
        self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['animation_length'] = self._animation_length
        if timestamp not in self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['timeline']:
            self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['timeline'][timestamp] = []
        for command in commands:
            if command.endswith(';') or command.startswith('@s'):
                self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['timeline'][timestamp].append(f'{command}')
            else:
                self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['timeline'][timestamp].append(f'/{validate(command)}')
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
        self._animation[f'animation.{NAMESPACE_FORMAT}.{self._animation_short_name}']['animation_length'] = animation_length
        return self

    @property
    def _export(self):
        return self._animation


class _BPAnimations(Exporter):
    def __init__(self, identifier) -> None:
        super().__init__(identifier, 'bp_animations', FileExtension('bp_animations'))
        self._identifier = identifier
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
        self._animation = _BPAnimation(animation_short_name, loop)
        self._animations_list.append(self._animation)
        return self._animation

    def queue(self, directory: str = None):
        if len(self._animations_list) > 0:
            for animation in self._animations_list:
                self._animations['animations'].update(animation._export)
            self.content(self._animations)
            return super().queue(directory=directory)


# Spawn Rules
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
    
    def DelayFilter(self, min: int, max: int, identifier: str, spawn_chance: int):
        '''Unknown behavior.
        
        Parameters
        ----------
        min : int
            The minimum time required to use.
        max : int
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
                'min': min,
                'max': max,
                'identifier': identifier,
                'spawn_chance': int(np.clip(spawn_chance,0,100))
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
    def __init__(self, identifier):
        super().__init__(identifier, 'spawn_rules', FileExtension('spawn_rules'))
        self._identifier = identifier
        self._description = _SpawnRuleDescription(self, self._identifier)
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
        self._event = {self._event_name: {}}

    def add(self, *component_groups: str):
        if 'add' not in self._event[self._event_name]:
            self._event[self._event_name].update({'add': {'component_groups':[]}})

        self._event[self._event_name]['add']['component_groups'].extend(component_groups)
        return self

    def remove(self, *component_groups: str):
        if 'remove' not in self._event[self._event_name]:
            self._event[self._event_name].update({'remove': {'component_groups':[]}})

        self._event[self._event_name]['remove']['component_groups'].extend(component_groups)
        return self

    def trigger(self, event: str):
        self._event[self._event_name]['trigger'] = event
        return self

    def update(self, components: dict):
        self._event[self._event_name] = components

    #experimental
    def _run_command(self, *commands: str):
        from .commands import validate
        if 'run_command' not in self._event[self._event_name]:
            self._event[self._event_name].update({'run_command': {'command':[]}})
        self._event[self._event_name]['run_command']['command'].extend(validate(cmd) for cmd in commands)
        return self

    @property
    def _export(self):
        return self._event


class _Randomize(_BaseEvent):
    def __init__(self, parent):
        self._event = {"weight": 1}
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
        self._event = {}

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
        self._components[self._component_group_name].update(*components)
        return self

    def remove(self, *components: object):
        for component in components:
            self._components[self._component_group_name].pop(component)
        return self

    def overwrite(self, *components: object):
        self._components[self._component_group_name] = components

    def _export(self):
        return self._components


class _ComponentGroup(_Components):
    def __init__(self, component_group_name: str):
        super().__init__()
        self._component_group_name = component_group_name
        self._components = {self._component_group_name: {}}


# Entity
class _Entity(Exporter):
    def __init__(self, identifier: str, type: str, filetype: str) -> None:
        self._internal_name, self._display_name = RawText(identifier)
        super().__init__(identifier, type, filetype)


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

    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, 'server_entity', FileExtension('server_entity'))
        self._server_entity = Schemes('server_entity')
        self._description = _EntityServerDescription(self._internal_name)
        self._animation_controllers = _BP_AnimationControllers(self._internal_name)
        self._animations = _BPAnimations(self._internal_name)
        self._spawn_rule = _SpawnRule(self._internal_name)
        self._components = _Components()
        self._events : list[_Event] = []
        self._component_groups : list[_ComponentGroup] = []
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

    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
        self._description._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(self, animation_name: str, loop: bool = False, animate: bool = False, condition: str = None):
        self._description._animations(animation_name, animate, condition)
        return self._animations.add_animation(animation_name, loop)

    def init_vars(self, **vars):
        self.animation_controller('variables', True).add_state('default').on_entry(*[f'v.{var}={value}' for var, value in vars.items()])
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
        self._animations.queue(directory=directory)
        self._animation_controllers.queue(directory=directory)
        self._spawn_rule.queue(directory=directory)

        self._server_entity['minecraft:entity'].update(self.description._export)
        self._server_entity['minecraft:entity'].update(self._components._export())

        for event in self._events:
            self._server_entity['minecraft:entity']['events'].update(event._export)
        for component_group in self._component_groups:
            self._server_entity['minecraft:entity']['component_groups'].update(component_group._export())

        self.content(self._server_entity)
        super().queue(directory=directory)


class _EntityClient(_Entity):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, 'client_entity', FileExtension('client_entity'))
        self._identifier = identifier
        self._client_entity = Schemes('client_entity')
        self._description = _EntityClientDescription(self._internal_name)
        
    def queue(self, directory: str = None):
        self._client_entity['minecraft:client_entity'].update(self._description.queue(directory))

        self.content(self._client_entity)
        super().queue(directory=directory)



class NewEntity():
    def _validate_name(self, identifier):
        if ':' in identifier:
            raise ValueError('Namespaces are not allowed.')
        if identifier in Vanilla.Entities._list:
            raise UserWarning(
                'Using a vanilla entity name. If you wish to overwrite the vanilla entity, use get_vanilla() otherwise a new entity with the same name but different namespace will be created.'
            )

    def __init__(self, identifier: str) -> None:
        self._validate_name(identifier)
        self._server = _EntityServer(identifier)
        self._client = _EntityClient(identifier)

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

    def queue(self, directory: str = None):
        self.Client.queue(directory)
        self.Server.queue(directory)


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


# Core Classes
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


class Sound():
    def __init__(self, sound_definition: str, category: str, use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999) -> None:
        self._sound_category = ['ambient', 'block', 'player',
                                'neutral', 'hostile', 'music', 'record', 'ui']
        self._category = category
        if category not in self._sound_category:
            RaiseError(
                f'Sound category must be one of {self._sound_category}.')
        self._sound_definition = sound_definition
        self._sound = {
            self._sound_definition: {
                'category': category,
                'sounds': []
            }
        }
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

    def add_sound(self, sound_name, volume: int = 1, weight: int = 1, pitch: int = [1, 1], is_3d: bool = False, stream: bool = False, load_on_low_memory: bool = False):
        CheckAvailability(f'{sound_name}.ogg', 'audio', 'assets/sounds')
        self._sound_name = sound_name
        splits = self._sound_definition.split(".")
        self._path = ''
        for i in range(len(splits)-1):
            self._path += f'{splits[i]}/'
        sound = {
            "name": f'sounds/{self._path}{self._sound_name.split("_")[0]}/{self._sound_name}',
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
    def queue(self):
        ANVIL._queue(self)

    def _export(self):
        if FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds/sound_definitions.json') is False:
            File('sound_definitions.json', Defaults('sound_definitions'),
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds', 'w')
        self._sound[self._sound_definition]['sounds'] = self._sounds
        with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds/sound_definitions.json', 'r') as file:
            data = json.load(file)
            data['sound_definitions'].update(self._sound)
        File('sound_definitions.json', data,
             f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds', 'w')
        for sound in self._sounds:
            CopyFiles(
                'assets/sounds', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds/{self._path}{self._sound_name.split("_")[0]}', f'{sound["name"].split("/")[-1]}.ogg')


class Music():
    def __init__(self, event_type: str, music_name: str, min_delay: int = 10, max_delay: int = 20):
        self._event_types = [
            'creative',
            'credits',
            'crimson_forest',
            'dripstone_caves',
            'end',
            'endboss',
            'frozen_peaks',
            'game',
            'grove',
            'hell',
            'jagged_peaks',
            'lush_caves',
            'meadow',
            'menu',
            'nether',
            'snowy_slopes',
            'soulsand_valley',
            'stony_peaks',
            'water'
        ]
        if event_type not in self._event_types:
            RaiseError(f'Music event type must be one of {self._event_types}.')
        self._music_name = music_name
        CreateDirectory(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds')
        self._music = {
            event_type: {
                'event_name': f'music.{event_type}.{self._music_name}',
                "min_delay": min_delay,
                "max_delay": max_delay
            }
        }
        self.music_sounds = Sound(
            f'music.{event_type}.{self._music_name}', 'music')

    def add_sounds(self, sound_name, volume: int = 1, weight: int = 1, pitch: int = 1, is_3d: bool = False, stream: bool = False, load_on_low_memory: bool = False):
        self.music_sounds.add_sound(
            sound_name, volume, weight, pitch, is_3d, stream, load_on_low_memory)
        return self

    @property
    def queue(self):
        ANVIL._queue(self.music_sounds)
        ANVIL._queue(self)

    def _export(self):
        if FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds/music_definitions.json') is False:
            File('music_definitions.json', Defaults('music_definitions'),
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds', 'w')
        with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds/music_definitions.json', 'r') as file:
            data = json.load(file)
            data.update(self._music)
        File('music_definitions.json', data,
             f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds', 'w')


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
        CheckAvailability(f'{self._identifier}.png', 'texture', 'assets/items')
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
                'assets/items', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/items/{directory}', f'{self._identifier}.png')
            if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json'):
                File('item_texture.json', Defaults('item_textures', PROJECT_NAME),
                     f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
            with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json', 'r') as file:
                data = json.load(file)
                data['texture_data'][f'{self._identifier}'] = {'textures': []}
                data['texture_data'][f'{self._identifier}']['textures'].append(MakePath('textures/items',directory,self._identifier))
            File('item_texture.json', data,
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')

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
                    File('blocks.json', Defaults('blocks'),
                         f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')
                with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/blocks.json', 'r') as file:
                    data = json.load(file)
                    if len(kwargs.keys()) == 0:
                        data[f'{NAMESPACE_FORMAT}:{identifier}'] = {
                            'textures': identifier, 'sound': sound}
                    else:
                        data[f'{NAMESPACE_FORMAT}:{identifier}'] = {
                            'textures': {}, 'sound': sound}
                        keys = ['side', 'up', 'down',
                                'east', 'north', 'south', 'west']
                        for key in kwargs:
                            if key in keys:
                                data[f'{NAMESPACE_FORMAT}:{identifier}']['textures'][key] = kwargs[key]
                            else:
                                RaiseError(
                                    'Texture keys type must be one of %r.' % keys)
                File('blocks.json', data,
                     f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')

        class _TerrainTexture():
            def __init__(self, identifier: str, directory: str, **kwargs):
                if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/terrain_texture.json'):
                    File('terrain_texture.json', Defaults('terrain_texture', PROJECT_NAME),
                         f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
                with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/terrain_texture.json', 'r') as file:
                    data = json.load(file)
                    if len(kwargs.keys()) == 0:
                        data['texture_data'][f'{identifier}'] = {'textures': []}
                        data['texture_data'][f'{identifier}']['textures'].append(
                            os.path.join('textures/blocks',directory,identifier).replace('\\','/')
                        )
                    else:
                        keys = ['side', 'up', 'down',
                                'east', 'north', 'south', 'west']
                        for key in kwargs:
                            if key in keys:
                                data['texture_data'][kwargs[key]] = {
                                    'textures': []}
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
                if FileExists(f'assets/blocks/{self._identifier}.png'):
                    CopyFiles(
                        'assets/blocks', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/blocks/{directory}', f'{self._identifier}.png')
            else:
                for texture in self._textures:
                    CopyFiles('assets/blocks', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/blocks/{directory}',
                              f'{self._textures[texture]}.png')

    class __BP_Block(EngineComponent):
        def __init__(self, parent, identifier):
            self._identifier = identifier
            self._parent = parent
            super().__init__(self._identifier, 'bp_block_v1', '.block.json')
            self._content = Defaults('bp_block_v1', NAMESPACE_FORMAT, self._identifier)
            if FileExists(f'assets/blocks/{self._identifier}.png'):
                self._most_dominant_color, self._least_dominant_color = GetColors(
                    f'assets/blocks/{self._identifier}.png')
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

        if not FileExists(f'assets/blocks/{self._identifier}.png'):
            if 'up' in textures:
                CheckAvailability(f'{textures["up"]}.png', 'texture', 'assets/blocks')
            else:
                RaiseError(
                    f'A texture with the name {self._identifier} cannot be found in assets/blocks')

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

    def tick(self):
        ANVIL.tick(self)
        return self

    @property
    def execute(self):
        return f'function {MakePath(PROJECT_NAME,self._directory,self._name)}'

    @property
    def identifier(self):
        return self._name

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


class Attachable(EngineComponent):
    class _AnimationController(EngineComponent):
        def __init__(self, entity_name: str):
            self._entity_name = entity_name
            self._controllers = []
            self._animation_controllers = Defaults('animation_controllers_rp')
            super().__init__(self._entity_name,
                             'rp_animation_controller', '.rp_ac.json')

        def add_controller(self, controller_name: str):
            self._animation_controller = self._Controller(
                self._entity_name, controller_name)
            self._controllers.append(self._animation_controller)
            return self._animation_controller

        def queue(self, directory: str = ''):
            if len(self._controllers) > 0:
                for controller in self._controllers:
                    self._animation_controllers['animation_controllers'].update(
                        controller._export())
                self.content(self._animation_controllers)
                return super().queue(directory=directory)

        class _Controller():
            def __init__(self, entity_name, controller_name):
                self._entity_name = entity_name
                self._controller_name = controller_name
                self._controller_states = []
                self._controller = {f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}': {
                    'initial_state': 'default', 'states': {}}}

            def add_state(self, state_name):
                self._controller_state = self._State(state_name)
                self._controller_states.append(self._controller_state)
                return self._controller_state

            def _export(self):
                for state in self._controller_states:
                    self._controller[f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['states'].update(
                        state._export())
                return self._controller

            class _State():
                def __init__(self, state_name: str):
                    self._state_name = state_name
                    self._transitions = []
                    self._on_entry = []
                    self._on_exit = []
                    self._animations = []
                    self._particles = []
                    self._blend_transition = 0

                def particle(self, effect: str, locator: str, pre_anim_script: str = None):
                    particle = {'effect': effect, 'locator': locator}
                    if pre_anim_script is not None:
                        particle.update(
                            {'pre_effect_script': pre_anim_script})
                    self._particles.append(particle)
                    return self

                def on_entry(self, commands: str):
                    self._on_entry.append(commands)
                    return self

                def on_exit(self, commands: str):
                    self._on_exit.append(commands)
                    return self

                def animations(self, animation: str, condition: str = ''):
                    if condition == '':
                        self._animations.append(animation)
                    else:
                        self._animations.append({animation: condition})
                    return self

                def transition(self, state: object, condition: str):
                    self._transitions.append({state: str(condition)})
                    return self

                def blend_transition(self, blend_value: float or int):
                    self._blend_transition = blend_value
                    return self

                def _export(self):
                    state = {
                        self._state_name: {
                        }
                    }
                    if len(self._on_entry) > 0:
                        state[self._state_name].update(
                            {'on_entry': self._on_entry})
                    if len(self._on_exit) > 0:
                        state[self._state_name].update(
                            {'on_exit': self._on_exit})
                    if len(self._animations) > 0:
                        state[self._state_name].update(
                            {'animations': self._animations})
                    if len(self._transitions) > 0:
                        state[self._state_name].update(
                            {'transitions': self._transitions})
                    if len(self._particles) > 0:
                        state[self._state_name].update(
                            {'particle_effects': self._particles})
                    if self._blend_transition > 0:
                        state[self._state_name].update(
                            {"blend_transition": self._blend_transition})
                    return state

    class _RenderController(EngineComponent):
        def __init__(self, entity_name: str):
            self._entity_name = entity_name
            self._controllers = []
            self.render_controller = Defaults('render_controller')
            super().__init__(self._entity_name, 'render_controller', '.render.json')

        def add_controller(self, controller_name: str):
            self._render_controller = self._controller(
                self._entity_name, controller_name)
            self._controllers.append(self._render_controller)
            return self._render_controller

        def queue(self, directory: str = ''):
            for controller in self._controllers:
                self.render_controller['render_controllers'].update(
                    controller._export())
            self.content(self.render_controller)
            return super().queue(directory=directory)

        class _controller():
            def __init__(self, entity_name, controller_name):
                self._entity_name = entity_name
                self._controller_name = controller_name
                self._controller = {
                    f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}': {
                        'arrays': {},
                        'materials': [{'*': 'Material.default'}],
                        'geometry': {},
                        'textures': []
                    }
                }

            def texture_array(self, array_name: str, *textures_short_names: str):
                if 'textures' not in self._controller:
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['textures'] = {
                    }
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['textures'].update(
                    {f'Array.{array_name}': [f'Texture.{texture}' for texture in textures_short_names]})
                return self

            def material(self, material_shortname: str):
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['materials'] = [
                    {'*': f'Material.{material_shortname}'}]
                return self

            def overlay_color(self, a, r, g, b):
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                    "overlay_color": {
                        "a": a,
                        "r": r,
                        "g": g,
                        "b": b
                    }
                })
                return self

            def geometry_array(self, array_name: str, *geometries_short_names: str):
                if 'geometries' not in self._controller:
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['geometries'] = {
                    }
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['geometries'].update(
                    {f'Array.{array_name}': [f'Geometry.{geometry}' for geometry in geometries_short_names]})
                return self

            def geometry(self, short_name: str = 'default'):
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update(
                    {'geometry': f'Geometry.{short_name}' if short_name.split('.')[0] != 'Array' else short_name})
                return self

            def textures(self, short_name: str = 'default'):
                self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['textures'].append(
                    f'{"Texture." if short_name.split(".")[0] != "Array" else ""}{short_name}')
                return self

            def _export(self):
                return self._controller

    class _Animation():
        def __init__(self, entity_name: str):
            self._entity_name = entity_name
            self._animations = []

        def add_animation(self, animation_name: str):
            self._animations.append(animation_name)

    def __init__(self, identifier: str | Item, is_vanilla : bool = False):
        if type(identifier) is str:
            self._identifier = identifier.split(':')[0]
        elif type(identifier) is Item:
            self._identifier = identifier.split(':')[0]

        self._animation_controller = self._AnimationController(self._identifier)
        self._animation = self._Animation(self._identifier)
        self._render_controller = self._RenderController(self._identifier)
        ANVIL._entities.update({f'{NAMESPACE_FORMAT}:{self._identifier}': {"Display Name": self._identifier, "Sounds": {}}})
        
        self._scripts = []
        self._sound_effect = {}
        self._particle_effects = {}
        self._init_vars = []
        self._content = Defaults('attachable', NAMESPACE_FORMAT if not is_vanilla else 'minecraft', self._identifier) 
        super().__init__(self._identifier, 'attachable', '.attachable.json')

    def init_vars(self, **vars):
        for var, value in vars.items():
            self._init_vars.append(f'v.{var}={value};')
        return self

    def animation_controller(self, controller_name: str, animate: bool = False, condition: str = ''):
        if 'animations' not in self._content['minecraft:attachable']['description']:
            self._content['minecraft:attachable']['description']['animations'] = {
            }
        if animate:
            if 'scripts' not in self._content['minecraft:attachable']['description']:
                self._content['minecraft:attachable']['description']['scripts'] = {
                    'animate': []}
            if condition == '':
                self._content['minecraft:attachable']['description']['scripts']['animate'].append(
                    controller_name)
            else:
                self._content['minecraft:attachable']['description']['scripts']['animate'].append({
                    controller_name: condition})
        self._content['minecraft:attachable']['description']['animations'].update(
            {controller_name: f'controller.animation.{NAMESPACE_FORMAT}.{self._identifier}.{controller_name}'})
        return self._animation_controller.add_controller(controller_name)

    def animation(self, animation_name: str, animate: bool = False, condition: str = ''):
        if 'animations' not in self._content['minecraft:attachable']['description']:
            self._content['minecraft:attachable']['description']['animations'] = {}
        if 'scripts' not in self._content['minecraft:attachable']['description']:
            self._content['minecraft:attachable']['description']['scripts'] = {
                'animate': []}
        CheckAvailability(
            f'{self._identifier}.animation.json', 'animation', 'assets/animations')
        with open(f'assets/animations/{self._identifier}.animation.json') as file:
            data = json.load(file)
            if animation_name not in [animation.split('.')[-1] for animation in data['animations'].keys()]:
                RaiseError(
                    f'The animation file {self._identifier}.animation.json doesn\'t contain an animation called animation.{NAMESPACE_FORMAT}.{self._identifier}.{animation_name}')
        if condition == '':
            if animate is True:
                self._content['minecraft:attachable']['description']['scripts']['animate'].append(
                    animation_name)
        else:
            self._content['minecraft:attachable']['description']['scripts']['animate'].append(
                {animation_name: condition})
        self._content['minecraft:attachable']['description']['animations'].update(
            {animation_name: f'animation.{NAMESPACE_FORMAT}.{self._identifier}.{animation_name}'})
        return self

    def geometry(self, geometry_id: str, geometry_name: str):
        CheckAvailability(f'{self._identifier}.geo.json',
                          'geometry', 'assets/geometries')
        with open(f'assets/geometries/{self._identifier}.geo.json') as file:
            data = file.read()
            if f'{NAMESPACE_FORMAT}.{geometry_name}' not in data:
                RaiseError(
                    f'The geometry file {geometry_name}.geo.json doesn\'t contain a geometry called {NAMESPACE_FORMAT}.{geometry_name}')
        self._content['minecraft:attachable']['description']['geometry'].update(
            {geometry_id: f'geometry.{NAMESPACE_FORMAT}.{geometry_name}'})
        return self

    def texture(self, texture_id: str, texture_name: str):
        self._spawn_egg_colors = texture_id
        CheckAvailability(f'{texture_name}.png', 'texture', 'assets/textures')
        self._content['minecraft:attachable']['description']['textures'].update(
            {texture_id: f'textures/attachables/{self._identifier}/{texture_name}'})
        return self
    
    def material(self, material_id: str, material_name: str):
        self._content['minecraft:attachable']['description']['materials'].update({material_id: material_name})
        return self

    def script(self, *scripts: str):
        for script in scripts:
            self._scripts.append(script)
        return self

    def sound_effect(self, sound_shortname: str, sound_identifier: str):
        self._sound_effect.update({sound_shortname: sound_identifier})
        ANVIL._entities[f'{NAMESPACE_FORMAT}:{self._identifier}']["Sounds"].update({sound_shortname: f'mob.{self._identifier}.{sound_identifier}'})
        return self

    def particle_effect(self, particle_identifier: str):
        self._particle_name = particle_identifier
        Particle(self._particle_name).queue()
        self._particle_effects.update(
            {self._particle_name: f'{NAMESPACE_FORMAT}:{self._particle_name}'})

    def render_controller(self, controller_name: str, condition: str = ''):
        if condition == '':
            self._content['minecraft:attachable']['description']['render_controllers'].append(
                f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{controller_name}')
        else:
            self._content['minecraft:attachable']['description']['render_controllers'].append(
                {f'controller.render.{NAMESPACE_FORMAT}.{self._identifier}.{controller_name}': condition})
        return self._render_controller.add_controller(controller_name)

    def queue(self):
        geos = self._content['minecraft:attachable']['description']['geometry']
        if len(geos) == 0:
            RaiseError(f'{self._identifier} missing a geometry')
        else:
            for geo in geos:
                CopyFiles('assets/geometries', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/models/entity/attachables',
                          f'{self._identifier}.geo.json')
        if len(self._content['minecraft:attachable']['description']['textures']) == 0:
            RaiseError(f'{self._identifier} missing a texture')
        else:
            for text in self._content['minecraft:attachable']['description']['textures']:
                CopyFiles('assets/textures', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/attachables/{self._identifier}',
                          f'{self._content["minecraft:attachable"]["description"]["textures"][text].split("/")[-1]}.png')
        if len(self._content['minecraft:attachable']['description']['render_controllers']) == 0:
            RaiseError(f'{self._identifier} missing a render controller')
        if 'animations' in self._content['minecraft:attachable']['description']:
            for animation in self._content['minecraft:attachable']['description']['animations']:
                if self._content['minecraft:attachable']['description']['animations'][animation].split('.')[0] != 'controller':
                    CopyFiles(
                        'assets/animations', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/animations/attachables', f'{self._identifier}.animation.json')
        if len(self._scripts) > 0:
            self._content['minecraft:attachable']['description']['scripts'] = {
                'pre_animation': []}
            self._content['minecraft:attachable']['description']['scripts']['pre_animation'] = self._scripts
        if len(self._sound_effect.items()) > 0:
                self._content['minecraft:attachable']['description']['sound_effects'] = self._sound_effect
        if len(self._particle_effects.items()) > 0:
                self._content['minecraft:attachable']['description']['particle_effects'] = self._particle_effects
        if len(self._init_vars) > 0:
                if 'initialize' not in self._content['minecraft:attachable']['description']['scripts']:
                    self._content['minecraft:attachable']['description']['scripts'].update({
                                                                                              "initialize": []})
                self._content['minecraft:attachable']['description']['scripts']['initialize'].extend(
                    self._init_vars)
               
        self._render_controller.queue('attachables')
        self._animation_controller.queue('attachables')
        super().content(self._content)
        return super().queue('')


class Entity():
    class _ServerEntity(EngineComponent):
        class _Description():
            def __init__(self, entity_name: str):
                self._entity_name = entity_name
                self._description = {
                    'identifier': f'{NAMESPACE_FORMAT}:{entity_name}'
                }

            @property
            def Summonable(self):
                self._description['is_summonable'] = True
                return self

            @property
            def Spawnable(self):
                self._description['is_spawnable'] = True
                return self

            @property
            def Experimental(self):
                self._description['is_experimental'] = True
                return self

            def RuntimeIdentifier(self, identifier: str):
                self._description['runtime_identifier'] = identifier
                return self

            def animation_controllers(self, controller: str, animate: bool, condition: str = ''):
                if 'animations' not in self._description:
                    self._description['animations'] = {}

                if 'scripts' not in self._description:
                    self._description['scripts'] = {'animate': []}
                if animate is True:
                    if condition == '':
                        self._description['scripts']['animate'].append(
                            controller)
                    else:
                        self._description['scripts']['animate'].append(
                            {controller: condition})
                self._description['animations'].update(
                    {controller: f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{controller}'})

            def animations(self, controller: str, animate: bool, condition: str = ''):
                if 'animations' not in self._description:
                    self._description['animations'] = {}

                if 'scripts' not in self._description:
                    self._description['scripts'] = {'animate': []}
                if animate is True:
                    if condition == '':
                        self._description['scripts']['animate'].append(
                            controller)
                    else:
                        self._description['scripts']['animate'].append(
                            {controller: condition})
                self._description['animations'].update(
                    {controller: f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{controller}'})

            def identifier(self, namespace: str, entity_name: str):
                if namespace.lower() in ['minecraft']:
                    RaiseError(
                        f'{namespace} is a reserved keyword, please use a different namespace')
                else:
                    self._description.update(
                        {'identifier': f'{namespace}:{entity_name}'})

            def update(self, description: dict):
                self._description = description

            def _export(self):
                return self._description

        class _ComponentGroup():
            def __init__(self, component_group_name: str):
                self._component_group_name = component_group_name
                self._component_group = {self._component_group_name: {}}

            def get_name(self):
                return self._component_group_name

            def add(self, *components: dict):
                for component in components:
                    self._component_group[self._component_group_name].update(component)
                return self
            
            def remove(self, component: str):
                self._component_group[self._component_group_name].pop(component)
                return self
            def update(self, component_group: dict):
                self._component_group = {self._component_group_name: component_group}
                return self

            def _export(self):
                return self._component_group

        class _Components():

            def __init__(self):
                self._components = {}

            def add(self, *components: object):
                for component in components:
                    self._components.update(component)
                return self

            def update(self, components: dict):
                self._components = components

            def _export(self):
                return self._components

        class _AnimationController(EngineComponent):
            def __init__(self, entity_name: str):
                self._entity_name = entity_name
                self._controllers = []
                self._animation_controllers = {
                    'format_version': '1.10.0', 'animation_controllers': {}}
                super().__init__(self._entity_name,
                                 'bp_animation_controller', '.bp_ac.json')

            def add_controller(self, controller_name: str):
                self._animation_controller = self._Controller(
                    self._entity_name, controller_name)
                self._controllers.append(self._animation_controller)
                return self._animation_controller

            def queue(self, directory: str = ''):
                if len(self._controllers) > 0:
                    for controller in self._controllers:
                        self._animation_controllers['animation_controllers'].update(
                            controller._export())
                    self.content(self._animation_controllers)
                    return super().queue(directory=directory)

            class _Controller():
                def __init__(self, entity_name, controller_name):
                    self._entity_name = entity_name
                    self._controller_name = controller_name
                    self._controller_states = []
                    self._controller = {f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}': {
                        'initial_state': 'default', 'states': {}}}

                def add_state(self, state_name: str):
                    self._controller_state = self._State(state_name)
                    self._controller_states.append(self._controller_state)
                    return self._controller_state

                def _export(self):
                    for state in self._controller_states:
                        self._controller[f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['states'].update(
                            state._export())
                    return self._controller

                class _State():
                    def __init__(self, state_name):
                        self._state_name = state_name
                        self._transitions = []
                        self._on_entry = []
                        self._on_exit = []
                        self._animations = []

                    def on_entry(self, *commands: str):
                        for command in commands:
                            if ';' in str(command):
                                self._on_entry.append(f'{command}')
                            else:
                                self._on_entry.append(f'/{command}')
                        return self

                    def on_exit(self, *commands: str):
                        for command in commands:
                            if ';' in str(command):
                                self._on_exit.append(f'{command}')
                            else:
                                self._on_exit.append(f'/{command}')
                        return self

                    def animation(self, animation: str, condition: str = ''):
                        if condition == '':
                            self._animations.append(animation)
                        else:
                            self._animations.append({animation: condition})
                        return self

                    def transition(self, state: object, condition: str):
                        self._transitions.append({state: str(condition)})
                        return self

                    def _export(self):
                        state = {
                            self._state_name: {
                            }
                        }
                        if len(self._on_entry) > 0:
                            state[self._state_name].update(
                                {'on_entry': self._on_entry})
                        if len(self._on_exit) > 0:
                            state[self._state_name].update(
                                {'on_exit': self._on_exit})
                        if len(self._animations) > 0:
                            state[self._state_name].update(
                                {'animations': self._animations})
                        if len(self._transitions) > 0:
                            state[self._state_name].update(
                                {'transitions': self._transitions})
                        return state

        class _Animations(EngineComponent):
            def __init__(self, entity_name: str):
                self._entity_name = entity_name
                self._animations = []
                self._animation_file = {
                    'format_version': '1.10.0', 'animations': {}}
                super().__init__(self._entity_name, 'bp_animation', '.animation.json')

            def add_animation(self, animation_name, loop):
                self._animation = self._Animation(
                    self._entity_name, animation_name, loop)
                self._animations.append(self._animation)
                return self._animation

            def queue(self, directory: str = ''):
                if len(self._animations) > 0:
                    for animation in self._animations:
                        self._animation_file['animations'].update(
                            animation._export())
                    self.content(self._animation_file)
                    return super().queue(directory=directory)

            class _Animation():
                def __init__(self, entity_name, animation_name, loop):
                    self._entity_name = entity_name
                    self._animation_name = animation_name
                    self._animation_length = 0.01
                    self._animation = {
                        f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}': {
                            'loop': loop,
                            'timeline': {}
                        }
                    }

                def timeline(self, timestamp: int, *functions: str):
                    if self._animation_length < timestamp:
                        self._animation_length = timestamp+0.01
                    self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['animation_length'] = self._animation_length
                    if timestamp not in self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['timeline']:
                        self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['timeline'][timestamp] = []
                    for function in functions:
                        if isinstance(function, Function):
                            self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['timeline'][timestamp].append(f'/{function.execute}')
                        elif ';' in str(function):
                            self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['timeline'][timestamp].append(f'{function}')
                        else:
                            self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['timeline'][timestamp].append(f'/{function}')
                    return self

                def animation_length(self, animation_length: int):
                    self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['animation_length'] = animation_length
                    return self

                def anim_time_update(self, condition: str):
                    self._animation[f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._animation_name}']['anim_time_update'] = condition
                    return self

                def _export(self):
                    return self._animation

        class _SpawnRule(EngineComponent):
            class _Condition():
                def __init__(self):
                    self._condition = {}

                @property
                def SpawnOnSurface(self):
                    self._condition.update({'minecraft:spawns_on_surface': {}})
                    return self

                @property
                def SpawnUnderground(self):
                    self._condition.update(
                        {'minecraft:spawns_underground': {}})
                    return self

                @property
                def SpawnUnderwater(self):
                    self._condition.update({'minecraft:spawns_underwater': {}})
                    return self

                def SpawnsOnBlockFilter(self, block):
                    if 'minecraft:spawns_on_block_filter' not in self._condition:
                        self._condition.update(
                            {'minecraft:spawns_on_block_filter': []})
                    self._condition['minecraft:spawns_on_block_filter'].append(
                        block)
                    return self

                def DensityLimit(self, surface=-1, underground=-1):
                    density = {'minecraft:density_limit': {}}
                    if surface != -1:
                        density['minecraft:density_limit'].update(
                            {'surface': surface})
                    if underground != -1:
                        density['minecraft:density_limit'].update(
                            {'underground': underground})
                    self._condition.update(density)
                    return self

                def BrightnessFilter(self, min_brightness: int = 0, max_brightness: int = 15, adjust_for_weather: bool = True):
                    min_brightness = max(0, min_brightness)
                    max_brightness = min(15, max_brightness)
                    self._condition.update({'minecraft:brightness_filter': {
                                           'min': min_brightness, 'max': max_brightness, 'adjust_for_weather': adjust_for_weather}})
                    return self

                def DifficultyFilter(self, min_difficulty: str = 'easy', max_difficulty: str = 'hard'):
                    self._difficulties = ['peaceful', 'easy', 'normal', 'hard']
                    if (min_difficulty or max_difficulty) not in self._difficulties:
                        RaiseError('Difficulties must be one of %r.' %
                                   self._difficulties)
                    self._condition.update({'minecraft:difficulty_filter': {
                                           'min': min_difficulty, 'max': max_difficulty}})
                    return self

                def Weight(self, weight: int = 0):
                    self._condition.update(
                        {'minecraft:weight': {'default': weight}})
                    return self

                def Herd(self, min_size: int = 1, max_size: int = 4, spawn_event: str = None, event_skip_count: int = 0):
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
                    if 'minecraft:biome_filter' not in self._condition:
                        self._condition.update({'minecraft:biome_filter': []})
                    self._condition['minecraft:biome_filter'].append(filter)
                    return self

                def HeightFilter(self, min: int, max: int):
                    self._condition.update(
                        {'minecraft:height_filter': {'min': min, 'max': max}})
                    return self

                def export(self):
                    return self._condition

            def __init__(self, entity):
                self._entity_name = entity
                self._spawn_rule = Defaults(
                    'spawn_rules', NAMESPACE_FORMAT, self._entity_name)
                self._conditions = []
                super().__init__(self._entity_name, 'spawn_rule', '.spawn_rule.json')

            @property
            def add_condition(self):
                self._condition = self._Condition()
                self._conditions.append(self._condition)
                return self._condition

            def queue(self, directory: str = ''):
                if len(self._conditions) > 0:
                    self._spawn_rule['minecraft:spawn_rules']['conditions'] = [
                        condition.export() for condition in self._conditions]
                    self.content(self._spawn_rule)
                    return super().queue(directory=directory)

        def __init__(self, entity_name: str):
            self._entity_name = entity_name
            self._description = self._Description(self._entity_name)
            self._animation_controller = self._AnimationController(self._entity_name)
            self._animations = self._Animations(self._entity_name)
            self._spawn_rule = self._SpawnRule(self._entity_name)
            self._events = []
            self._component_groups = []
            self._components = []
            self._content = Defaults('entity_bp')
            super().__init__(entity_name, 'behavior', '.behavior.json')

        @property
        def description(self):
            return self._description

        def component_group(self, component_group_name):
            self._component_group = self._ComponentGroup(component_group_name)
            self._component_groups.append(self._component_group)
            return self._component_group

        def event(self, event_name):
            self._event = _Event(event_name)
            self._events.append(self._event)
            return self._event

        @property
        def components(self):
            self._component = self._Components()
            self._components.append(self._component)
            return self._component

        def animation_controller(self, controller_name: str, animate: bool = False, condition: str = ''):
            self._description.animation_controllers(
                controller_name, animate, condition)
            return self._animation_controller.add_controller(controller_name)

        def animation(self, animation_name: str, animate: bool = False, loop: bool = False, condition: str = ''):
            self._description.animations(animation_name, animate, condition)
            return self._animations.add_animation(animation_name, loop)

        def init_vars(self, **vars):
            self.animation_controller('variables', True).add_state('default').on_entry(
                *[f'v.{var}={value};' for var, value in vars.items()])
            return self

        @property
        def spawn_rule(self):
            return self._spawn_rule

        @property
        def dummy(self):
            self.description.Summonable
            self.components.add({
                "minecraft:collision_box": {
                    "height": 0.1,
                    "width": 0.1
                },
                "minecraft:conditional_bandwidth_optimization": {
                    "default_values": {
                        "use_motion_prediction_hints": True
                    }
                },
                "minecraft:damage_sensor": {
                    "triggers": [{"deals_damage": False}]
                },
                "minecraft:health": {
                    "value": 1
                },
                "minecraft:physics": {},
                "minecraft:pushable": {
                    "is_pushable": False,
                    "is_pushable_by_piston": False
                },
                "minecraft:type_family": {
                    "family": [
                        "inanimate"
                    ]
                }
            })
            self.event('despawn').add('despawn')
            self.component_group('despawn').add({"minecraft:instant_despawn":{}})
            return self

        def queue(self, directory: str = ''):
            self._content['minecraft:entity']['description'] = self._description._export()
            if len(self._events) > 0:
                self._content['minecraft:entity']['events'] = {}
            if len(self._component_groups) > 0:
                self._content['minecraft:entity']['component_groups'] = {}
                self._content['minecraft:entity']['events'] = {}
            if len(self._components) > 0:
                self._content['minecraft:entity']['components'] = {}
            self._spawn_rule.queue(directory)
            for event in self._events:
                self._content['minecraft:entity']['events'].update(event._export)
            for component_group in self._component_groups:
                self._content['minecraft:entity']['component_groups'].update(
                    component_group._export())
            for components in self._components:
                self._content['minecraft:entity']['components'].update(
                    components._export())
            self._animation_controller.queue(directory)
            self._animations.queue(directory)
            super().content(self._content)
            return super().queue(directory=directory)

    class _ClientEntity(EngineComponent):
        class _RenderController(EngineComponent):
            def __init__(self, entity_name: str):
                self._entity_name = entity_name
                self._controllers = []
                self.render_controller = Defaults('render_controller')
                super().__init__(self._entity_name, 'render_controller', '.render.json')

            def add_controller(self, controller_name: str):
                self._render_controller = self._controller(
                    self._entity_name, controller_name)
                self._controllers.append(self._render_controller)
                return self._render_controller

            def queue(self, directory: str = ''):
                if len(self._controllers) > 0:
                    for controller in self._controllers:
                        self.render_controller['render_controllers'].update(controller._export())
                    self.content(self.render_controller)
                    return super().queue(directory=directory)

            class _controller():
                def __init__(self, entity_name, controller_name):
                    self._entity_name = entity_name
                    self._controller_name = controller_name
                    self._controller = {
                        f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}': {
                            'arrays': {},
                            'materials': [{'*': 'Material.default'}],
                            'geometry': {},
                            'textures': [],
                            'part_visibility': [
                                {'*': True}
                            ]
                        }
                    }

                def texture_array(self, array_name: str, *textures_short_names: str):
                    if 'textures' not in self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']:
                        self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['textures'] = {
                        }
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['textures'].update(
                        {f'Array.{array_name}': [f'Texture.{texture}' for texture in textures_short_names]})
                    return self

                def material(self, bone: str, material_shortname: str):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['materials'].append(
                        {bone: f'Material.{material_shortname}'})
                    return self

                def geometry_array(self, array_name: str, *geometries_short_names: str):
                    if 'geometries' not in self._controller:
                        self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['geometries'] = {
                        }
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['arrays']['geometries'].update(
                        {f'Array.{array_name}': [f'Geometry.{geometry}' for geometry in geometries_short_names]})
                    return self

                def geometry(self, short_name: str = 'default'):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update(
                        {'geometry': f'Geometry.{short_name}' if short_name.split('.')[0] != 'Array' else short_name})
                    return self

                def textures(self, short_name: str = 'default'):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['textures'].append(
                        f'{"Texture." if "Array" not in short_name else ""}{short_name}')
                    return self

                def part_visibility(self, bone: str, condition: str | bool):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['part_visibility'].append(
                        {bone: condition}
                    )
                    return self

                def overlay_color(self, a, r, g, b):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                        "overlay_color": {
                            "a": a,
                            "r": r,
                            "g": g,
                            "b": b
                        }
                    })
                    return self

                def on_fire_color(self, a, r, g, b):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                        "on_fire_color": {
                            "a": a,
                            "r": r,
                            "g": g,
                            "b": b
                        }
                    })
                    return self

                @property
                def filter_lighting(self):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                                                                                                                                         "filter_lighting": True})
                    return self

                @property
                def ignore_lighting(self):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                                                                                                                                         "ignore_lighting": True})
                    return self

                def light_color_multiplier(self, multiplier: int):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'].update({
                                                                                                                                         "light_color_multiplier": multiplier})
                    return self
                
                def uv_anim(self,offset:list[2],scale:list[2]):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['uv_anim']={
                        "offset":offset,
                        "scale": scale
                    }
                    
                def update(self, content: dict):
                    self._controller[f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}'] = content
                    return self

                def _export(self):
                    return self._controller

        class _AnimationController(EngineComponent):
            def __init__(self, entity_name: str):
                self._entity_name = entity_name
                self._controllers = []
                self._animation_controllers = Defaults('animation_controllers_rp')
                super().__init__(self._entity_name,
                                 'rp_animation_controller', '.rp_ac.json')

            def add_controller(self, controller_name: str):
                self._animation_controller = self._Controller(
                    self._entity_name, controller_name)
                self._controllers.append(self._animation_controller)
                return self._animation_controller

            def queue(self, directory: str = ''):
                if len(self._controllers) > 0:
                    for controller in self._controllers:
                        self._animation_controllers['animation_controllers'].update(
                            controller._export())
                    self.content(self._animation_controllers)
                    return super().queue(directory=directory)

            class _Controller():
                def __init__(self, entity_name, controller_name):
                    self._entity_name = entity_name
                    self._controller_name = controller_name
                    self._controller_states = []
                    self._controller = {f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}': {
                        'initial_state': 'default', 'states': {}}}

                def add_state(self, state_name):
                    self._controller_state = self._State(state_name)
                    self._controller_states.append(self._controller_state)
                    return self._controller_state

                def _export(self):
                    for state in self._controller_states:
                        self._controller[f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{self._controller_name}']['states'].update(
                            state._export())
                    return self._controller

                class _State():
                    def __init__(self, state_name: str):
                        self._state_name = state_name
                        self._transitions = []
                        self._on_entry = []
                        self._on_exit = []
                        self._animations = []
                        self._particles = []
                        self._sounds = []
                        self._blend_transition = 0
                        self._blend_via_shortest_path = False

                    def particle(self, effect: str, locator: str, pre_anim_script: str = None):
                        particle = {'effect': effect, 'locator': locator}
                        if pre_anim_script is not None:
                            particle.update(
                                {'pre_effect_script': pre_anim_script})
                        self._particles.append(particle)
                        return self
                    
                    def sound_effect(self, effect: str):
                        particle = {'effect': effect}
                        self._sounds.append(particle)
                        return self

                    def on_entry(self, commands: str):
                        self._on_entry.append(commands)
                        return self

                    def on_exit(self, commands: str):
                        self._on_exit.append(commands)
                        return self

                    def animations(self, animation: str, condition: str = ''):
                        if condition == '':
                            self._animations.append(animation)
                        else:
                            self._animations.append({animation: condition})
                        return self

                    def transition(self, state: object, condition: str):
                        self._transitions.append({state: str(condition)})
                        return self

                    def blend_transition(self, blend_value: float or int):
                        self._blend_transition = blend_value
                        return self

                    @property
                    def blend_via_shortest_path(self):
                        self._blend_via_shortest_path = True
                        return self

                    def _export(self):
                        state = {
                            self._state_name: {
                            }
                        }
                        if len(self._on_entry) > 0:
                            state[self._state_name].update(
                                {'on_entry': self._on_entry})
                        if len(self._on_exit) > 0:
                            state[self._state_name].update(
                                {'on_exit': self._on_exit})
                        if len(self._animations) > 0:
                            state[self._state_name].update(
                                {'animations': self._animations})
                        if len(self._transitions) > 0:
                            state[self._state_name].update(
                                {'transitions': self._transitions})
                        if len(self._particles) > 0:
                            state[self._state_name].update(
                                {'particle_effects': self._particles})
                        if len(self._sounds) > 0:
                            state[self._state_name].update(
                                {'sound_effects': self._sounds})
                        if self._blend_transition > 0:
                            state[self._state_name].update(
                                {"blend_transition": self._blend_transition})
                        if self._blend_via_shortest_path:
                            state[self._state_name].update(
                                {"blend_via_shortest_path": True})
                        return state

        class _Sound():
            def __init__(self, entity_name, category: str, volume, pitch_range):
                self._entity_name = entity_name
                self._category = category
                self._sound = {
                    f'{NAMESPACE_FORMAT}:{self._entity_name}': {
                        "events": {},
                        "pitch": 1 if pitch_range == [1, 1] else pitch_range,
                        "volume": volume
                    }
                }
                self._sounds = []

            def event(self, event_name: str, volume=1, pitch_range=[1, 1], use_legacy_max_distance: bool = False, max_distance: int = 0, min_distance: int = 9999):
                ANVIL._entities[self._entity_name]["Sounds"].update(
                    {event_name: f'mob.{self._entity_name}.{event_name}'})
                self._sound[f'{NAMESPACE_FORMAT}:{self._entity_name}']['events'].update(
                    {event_name: f'mob.{self._entity_name}.{event_name}'})
                sound = Sound(f'mob.{self._entity_name}.{event_name}', self._category,
                              use_legacy_max_distance, max_distance, min_distance)
                self._sounds.append(sound)
                return sound

            def queue(self):
                ANVIL._queue(self)
                for sound in self._sounds:
                    sound.queue()

            def _export(self):
                if FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds.json') is False:
                    File('sounds.json', Defaults('sounds'),
                         f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')
                with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/sounds.json', 'r') as file:
                    data = json.load(file)
                    data['entity_sounds']['entities'].update(self._sound)
                File('sounds.json', data,
                     f'resource_packs/RP_{PASCAL_PROJECT_NAME}', 'w')

        def __init__(self, entity_name: str):
            self._entity_name, self._display_name = RawText(entity_name)
            self._animation_controller = self._AnimationController(
                self._entity_name)
            self._render_controller = self._RenderController(self._entity_name)
            self._scripts = []
            self._init_vars = []
            self._content = Defaults('entity_rp', NAMESPACE_FORMAT, entity_name)
            self._particle_effects = {}
            self._particle_emitters = {}
            self._sound_effect = {}
            self._added_sounds = []
            self._skip_client = False
            self._is_vanilla = False
            self._scale = None
            self.is_dummy = False
            super().__init__(entity_name, 'client_entity', '.entity.json')

        @property
        def Attachable(self):
            self._content['minecraft:client_entity']['description']['enable_attachables'] = True

        @property
        def HideArmor(self):
            self._content['minecraft:client_entity']['description']['hide_armor'] = True

        @property
        def dummy(self):
            self.is_dummy = True
            File('dummy.geo.json', {'format_version': '1.12.0', 'minecraft:geometry': [{'description': {'identifier': f'geometry.{NAMESPACE_FORMAT}.dummy'}, "bones": [{"name": "root", "pivot": [0, 0, 0], "locators": {"root": [0, 0, 0]}}]}]}, 'assets/geometries', 'w')
            self.geometry('dummy', 'dummy')
            CreateImage('dummy', 8, 8, (0, 0, 0, 0), 'assets/textures')
            self.texture('dummy', 'dummy')
            self.render_controller('dummy').geometry('dummy').textures('dummy')

        @property
        def skip_client(self):
            self._skip_client = True

        @property
        def is_vanilla(self):
            self._is_vanilla = True
            self._content = Defaults('entity_rp', 'minecraft', self._entity_name)

        def animation_controller(self, controller_name: str, animate: bool = False, condition: str = ''):
            if 'animations' not in self._content['minecraft:client_entity']['description']:
                self._content['minecraft:client_entity']['description']['animations'] = {
                }
            if animate:
                if 'animate' not in self._content['minecraft:client_entity']['description']['scripts']:
                    self._content['minecraft:client_entity']['description']['scripts'].update({
                                                                                              'animate': []})
                if condition == '':
                    self._content['minecraft:client_entity']['description']['scripts']['animate'].append(
                        controller_name)
                else:
                    self._content['minecraft:client_entity']['description']['scripts']['animate'].append({
                                                                                                         controller_name: condition})
            self._content['minecraft:client_entity']['description']['animations'].update(
                {controller_name: f'controller.animation.{NAMESPACE_FORMAT}.{self._entity_name}.{controller_name}'})
            return self._animation_controller.add_controller(controller_name)

        def animation(self, animation_name: str, animate: bool = False, condition: str = ''):
            if 'animations' not in self._content['minecraft:client_entity']['description']:
                self._content['minecraft:client_entity']['description']['animations'] = {
                }
            if not self._skip_client:
                CheckAvailability(
                    f'{self._entity_name}.animation.json', 'animation', 'assets/animations')
                with open(f'assets/animations/{self._entity_name}.animation.json') as file:
                    if animation_name not in file.read():
                        RaiseError(
                            f'The animation file {self._entity_name}.animation.json doesn\'t contain an animation called animation.{NAMESPACE_FORMAT}{self._entity_name}.{animation_name}')
            if animate is True:
                if 'animate' not in self._content['minecraft:client_entity']['description']['scripts']:
                    self._content['minecraft:client_entity']['description']['scripts'].update({
                                                                                              'animate': []})
                if condition == '':
                    self._content['minecraft:client_entity']['description']['scripts']['animate'].append(
                        animation_name)
                else:
                    self._content['minecraft:client_entity']['description']['scripts']['animate'].append({
                                                                                                         animation_name: condition})
            self._content['minecraft:client_entity']['description']['animations'].update(
                {animation_name: f'animation.{NAMESPACE_FORMAT}.{self._entity_name}.{animation_name}'})
            return self

        def material(self, material_id: str, material_name: str):
            self._content['minecraft:client_entity']['description']['materials'].update({material_id: material_name})
            return self

        def geometry(self, geometry_id: str, geometry_name: str):
            if self.is_dummy:
                CheckAvailability('dummy.geo.json',
                                  'geometry', 'assets/geometries')
                with open('assets/geometries/dummy.geo.json') as file:
                    data = json.load(file)
                    if f'geometry.{NAMESPACE_FORMAT}.dummy' not in [geo['description']["identifier"] for geo in data['minecraft:geometry']]:
                        RaiseError(
                            f'The geometry file dummy.geo.json doesn\'t contain a geometry called {NAMESPACE_FORMAT}.dummy')
            else:
                if not self._skip_client:
                    CheckAvailability(
                        f'{self._entity_name}.geo.json', 'geometry', 'assets/geometries')
                    with open(f'assets/geometries/{self._entity_name}.geo.json') as file:
                        if f'geometry.{NAMESPACE_FORMAT}.{geometry_name}' not in file.read():
                            RaiseError(
                                f'The geometry file {self._entity_name}.geo.json doesn\'t contain a geometry called {NAMESPACE_FORMAT}.{geometry_name}')
            self._content['minecraft:client_entity']['description']['geometry'].update(
                {geometry_id: f'geometry.{NAMESPACE_FORMAT}.{geometry_name}'})
            return self

        def texture(self, texture_id: str, texture_name: str):
            if not self._skip_client:
                self._spawn_egg_colors = texture_id
                CheckAvailability(f'{texture_name}.png',
                                  'texture', 'assets/textures')
            self._content['minecraft:client_entity']['description']['textures'].update(
                {texture_id: f'textures/entity/{self._entity_name}/{texture_name}'})
            return self

        def script(self, *scripts: str):
            for script in scripts:
                self._scripts.append(f'{script};')
            return self

        def init_vars(self, **vars):
            for var, value in vars.items():
                self._init_vars.append(f'v.{var}={value};')
            return self

        def scale(self, scale: str):
            self._scale = scale

        def render_controller(self, controller_name: str, condition: str = ''):
            if condition == '':
                self._content['minecraft:client_entity']['description']['render_controllers'].append(
                    f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{controller_name}')
            else:
                self._content['minecraft:client_entity']['description']['render_controllers'].append(
                    {f'controller.render.{NAMESPACE_FORMAT}.{self._entity_name}.{controller_name}': condition})
            return self._render_controller.add_controller(controller_name)

        def particle_effect(self, particle_identifier: str):
            self._particle_name = particle_identifier
            Particle(self._particle_name).queue()
            self._particle_effects.update({self._particle_name: f'{NAMESPACE_FORMAT}:{self._particle_name}'})

        def particle_emitter(self, particle_identifier: str):
            self._particle_name = particle_identifier
            Particle(self._particle_name).queue()
            self._particle_emitters.update(
                {self._particle_name: f'{NAMESPACE_FORMAT}:{self._particle_name}'})

        def sound_effect(self, sound_shortname: str, sound_identifier: str):
            self._sound_effect.update({sound_shortname: sound_identifier})
            ANVIL._sounds.update({ f'{self._entity_name} - {sound_shortname}': f'mob.{self._entity_name}.{sound_identifier}'})
            return self

        def spawn_egg(self, item_sprite: str):
            CopyFiles(
                'assets/items', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/items/spawn_eggs/', f'{item_sprite}.png')
            if not FileExists(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json'):
                File('item_texture.json', Defaults('item_textures', PROJECT_NAME),
                     f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
            with open(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/item_texture.json', 'r') as file:
                data = json.load(file)
                data['texture_data'][f'{item_sprite}'] = {'textures': []}
                data['texture_data'][f'{item_sprite}']['textures'].append(
                    f'textures/items/spawn_eggs/{item_sprite}')
            File('item_texture.json', data,
                 f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures', 'w')
            self._content['minecraft:client_entity']['description']['spawn_egg'] = {
                "texture": f'{item_sprite}'
            }

        def _get_entity(self):
            return self._entity_name

        def queue(self, directory: str = ''):
            if len(self._scripts) > 0:
                if 'pre_animation' not in self._content['minecraft:client_entity']['description']['scripts']:
                    self._content['minecraft:client_entity']['description']['scripts'].update({"pre_animation": []})
                self._content['minecraft:client_entity']['description']['scripts']['pre_animation'].extend(self._scripts)
            if len(self._init_vars) > 0:
                if 'initialize' not in self._content['minecraft:client_entity']['description']['scripts']:
                    self._content['minecraft:client_entity']['description']['scripts'].update({
                                                                                              "initialize": []})
                self._content['minecraft:client_entity']['description']['scripts']['initialize'].extend(
                    self._init_vars)
            if len(self._particle_effects.items()) > 0:
                self._content['minecraft:client_entity']['description']['particle_effects'] = self._particle_effects
            if len(self._particle_emitters.items()) > 0:
                self._content['minecraft:client_entity']['description']['particle_emitters'] = self._particle_emitters
            if len(self._sound_effect.items()) > 0:
                self._content['minecraft:client_entity']['description']['sound_effects'] = self._sound_effect
            if self._scale != None:
                self._content['minecraft:client_entity']['description']['scripts'].update({
                                                                                          "scale": self._scale})
            if not self._is_vanilla:
                geos = self._content['minecraft:client_entity']['description']['geometry']
                if len(geos) == 0:
                    RaiseError(f'{self._entity_name} missing a geometry')
                if len(self._content['minecraft:client_entity']['description']['textures']) == 0:
                    RaiseError(f'{self._entity_name} missing a texture')
                if len(self._content['minecraft:client_entity']['description']['render_controllers']) == 0:
                    RaiseError(f'{self._entity_name} missing a render controller')
                if self.is_dummy:
                    CopyFiles('assets/geometries', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/models/entity/{directory}', 'dummy.geo.json')
                else:
                    CopyFiles('assets/geometries', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/models/entity/{directory}', f'{self._entity_name}.geo.json')
                for text in self._content['minecraft:client_entity']['description']['textures']:
                    if self._entity_name == 'fade_in_out':
                        MoveFiles('assets/textures', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/entity/{self._entity_name}',
                                  f'{self._content["minecraft:client_entity"]["description"]["textures"][text].split("/")[-1]}.png')
                    else:
                        CopyFiles('assets/textures', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/entity/{self._entity_name}',
                                  f'{self._content["minecraft:client_entity"]["description"]["textures"][text].split("/")[-1]}.png')
                if 'animations' in self._content['minecraft:client_entity']['description']:
                    for animation in self._content['minecraft:client_entity']['description']['animations']:
                        if self._content['minecraft:client_entity']['description']['animations'][animation].split('.')[0] != 'controller':
                            CopyFiles('assets/animations', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/animations/{directory}',
                                      f'{self._entity_name}.animation.json')
                if 'spawn_egg' not in self._content['minecraft:client_entity']['description']:
                    self._content['minecraft:client_entity']['description']['spawn_egg'] = {
                        'base_color': GetColors(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/entity/{self._entity_name}/{self._content["minecraft:client_entity"]["description"]["textures"][self._spawn_egg_colors].split("/")[-1]}.png')[0],
                        'overlay_color': GetColors(f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/entity/{self._entity_name}/{self._content["minecraft:client_entity"]["description"]["textures"][self._spawn_egg_colors].split("/")[-1]}.png')[1]
                    }
            else:
                CopyFiles(
                    'assets/animations', f'resource_packs/RP_{PASCAL_PROJECT_NAME}/animations/{directory}', f'{self._entity_name}.animation.json')

            for sound in self._added_sounds:
                sound.queue()
            self._render_controller.queue(directory)
            self._animation_controller.queue(directory)
            if not self._skip_client:
                super().content(self._content)
                return super().queue(directory=directory)

    def __init__(self, entity_name: str):
        """
        Creates an entity.

        Parameters:
        ---------
        `entity_name` : `str`
            Entity name, no namespace.

        Methodes:
        ---------
        Entity.Client -> Client side Entity object

        Entity.Server -> Server side Entity object

        Examples:
        ---------
        >>> Entity('car')
        """
        self._entity_codename, self._display_name = RawText(entity_name)

        self.raw_text_name = f'entity.{NAMESPACE_FORMAT}:{self._entity_codename}.name'
        self.raw_text_spawn_egg = f'item.spawn_egg.entity.{NAMESPACE_FORMAT}:{self._entity_codename}.name'

        self.Server = self._ServerEntity(self._entity_codename)
        self.Client = self._ClientEntity(self._entity_codename)
        self._available_int_components = [
            'variant',
            'mark_variant',
            'skin_id'
        ],
        self._available_bit_components = [
            'is_illager_captain',
            'is_baby',
            'is_sheared',
            'is_saddled',
            'is_tamed',
            'is_chested',
            'is_powered',
            'is_stunned',
            'can_climb',
            'can_fly',
            'can_power_jump',
            'is_ignited',
            'out_of_control'
        ]

    @property
    def identifier(self) -> components:
        """
        Return the full entity identifier.

        Examples:
        ---------
        >>> Entity.identifier
        """
        return f'{NAMESPACE_FORMAT}:{self._entity_codename}'

    def _load_server(self, entity):
        entity = json.loads(entity.decode('utf-8'))
        self.Server._description.update(entity['minecraft:entity']['description'])
        if 'events' in entity['minecraft:entity']:
            for i in entity['minecraft:entity']['events']:
                self.Server.event(i).update(entity['minecraft:entity']['events'][i])
        if 'component_groups' in entity['minecraft:entity']:
            for i in entity['minecraft:entity']['component_groups']:
                self.Server.component_group(i).update(entity['minecraft:entity']['component_groups'][i])
        if 'components' in entity['minecraft:entity']:
            for i in entity['minecraft:entity']['components']:
                self.Server.components.update({i: entity['minecraft:entity']['components'][i]})
        self.Server.content(entity)

    def _load_client(self, entity):
        entity = json.loads(entity.decode('utf-8'))
        self.Client.content(entity)

    def get_vanilla(self, include_client_entity: bool = False, skip_client: bool = True):
        if 'minecraft:' + self._entity_codename in Vanilla.Entities._list:
            self.Client.is_vanilla
            with zipfile.ZipFile(f'./assets/vanilla/BP.zip') as myzip:
                jsonContent = myzip.open(
                    f'entities/{self._entity_codename}.json').read()
                self._load_server(jsonContent)
            if include_client_entity:
                with zipfile.ZipFile('./assets/vanilla/RP.zip') as myzip:
                    jsonContent = myzip.open(
                        f'entity/{self._entity_codename}.entity.json').read()
                    self._load_client(jsonContent)
            #if skip_client:
            #    self.Client.skip_client
            return self
        else:
            RaiseError(f'Error at {self._entity_codename}, Entity name must be at least one of {Vanilla.Entities._list}.')

    def load_entity(self, include_client_entity: bool = False):
        pass

    def queue(self, directory: str = ''):
        ANVIL._entities.update({
            f'{NAMESPACE_FORMAT if not self.Client._is_vanilla else "minecraft"}:{self._entity_codename}': {"Display Name": self._display_name}
        })
        self.Server.queue(directory)
        self.Client.queue(directory)

        ANVIL.localize(f'{self.raw_text_name}={self._display_name}')
        ANVIL.localize(f'{self.raw_text_spawn_egg}=Spawn {self._display_name}')


class SkinPack():
    def __init__(self) -> None:
        self._skins = []
        CreateDirectory('assets/skin_pack/texts')
        File('languages.json', Defaults('languages'), 'assets/skin_pack/texts', 'w')
        if FileExists('assets/skin_pack/manifest.json') is False:
            File("manifest.json", Schemes('manifest_skins', PROJECT_NAME),"assets/skin_pack", "w")

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
        File('en_US.lang', Schemes('skin_language', PROJECT_NAME, DISPLAY_NAME+ ' Skin Pack') + ''.join(ANVIL._skins_langs),'assets/skin_pack/texts', 'w')
        File('skins.json', Schemes('skins', PROJECT_NAME, self._skins), 'assets/skin_pack', 'w')


class UI():
    class UIScreen(Exporter):
        class UIElement():
            def __init__(self, element_name: str) -> None:
                self._element_name = element_name
                self._element = {
                    self._element_name: {}
                }
                self.element = self._element[self._element_name]
                self._bindings = []
            
            @property
            def should_steal_mouse(self):
                self.element['should_steal_mouse'] = True
                return self
                
            @property
            def absorbs_input(self):
                self.element['absorbs_input'] = True
                return self

            def visible(self, visible: bool = True):
                self.element['visible'] = visible
                return self

            def queue(self):
                if len(self._bindings)>0:
                    self._element.update({
                        'bindings': self._bindings
                    })
                return self._element

        def __init__(self, name: str, namespace: str) -> None:
            super().__init__(name, 'ui', FileExtension('ui'))
            self.namespace = namespace
            self._elements = []
            self._content = {
                "namespace": namespace,
            }

        def add_element(self, element_name: str):
            self._element = self.UIElement(element_name)
            self._elements.append(self._element)
            return self._element
        
        def queue(self, directory: str = ''):
            for element in self._elements:
                self._content.update(element.queue())
            return super().queue(directory)

    class HUDScreen(UIScreen):
        def __init__(self) -> None:
            super().__init__('hud_screen', 'hud')

        @property
        def steal_mouse(self):
            self.add_element('hud_screen@common.base_screen').should_steal_mouse.absorbs_input

        @property
        def disable_cursor(self):
            self.add_element('cursor_renderer').visible(False)


    def __init__(self) -> None:
        self.hud_screen = self.HUDScreen()
        #self._anvil_screen = self.UIScreen('hud', 'anvil_hud')
        #self._animations_screen = self.UIScreen('animations', 'anvil_animations')
        #self._variables = self.UIScreen('_global_variables', 'variables')
        #self._defs = self.UIScreen('_ui_defs', 'ui_defs')


    def add_title_logo():
        pas
    def queue(self):
        self.hud_screen.queue()
        #self._anvil_screen.queue('anvil')
        #self._animations_screen.queue('anvil')
        #self._variables.queue()
        #self._defs.queue()


class Anvil():
    def __init__(self):
        """
        Provides a way to controll different aspects of the project, setting up project scores, tags, ticking functions, languages and so on...

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

            COMPANY = data['COMPANY']
            NAMESPACE = data['NAMESPACE']
            PROJECT_NAME = data['PROJECT_NAME']
            PASCAL_PROJECT_NAME = ''.join(x for x in PROJECT_NAME.title().replace('_', '').replace('-', '') if x.isupper())
            DISPLAY_NAME = data['DISPLAY_NAME']
            PROJECT_DESCRIPTION = data['PROJECT_DESCRIPTION']
            VANILLA_VERSION = data['VANILLA_VERSION']
            LAST_CHECK = data['LAST_CHECK']
            NAMESPACE_FORMAT_BIT = data['NAMESPACE_FORMAT']

            if NAMESPACE_FORMAT_BIT == 0:
                NAMESPACE_FORMAT = f'{NAMESPACE}'
            elif NAMESPACE_FORMAT_BIT == 1:
                NAMESPACE_FORMAT = f'{NAMESPACE}.{PROJECT_NAME}'
            elif NAMESPACE_FORMAT_BIT == 2:
                NAMESPACE_FORMAT = ''
        
        self._setup = Function('setup')
        self._setup_scores = Function('setup_scores')
        self._remove_scores = Function('remove_scores')
        self._remove_tags = Function('remove_tags')
        self._item_textures = ItemTextures()
        self._functions = []
        self._scores = {}
        self._objects_list = []
        self._tick = []
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
        self._setup_scores.content(
            f'scoreboard objectives add {PROJECT_NAME} dummy "{PROJECT_NAME.replace("_"," ").title()}"\n')
        self._remove_scores.content(f'scoreboard objectives remove {PROJECT_NAME}\n')

        self._deltatime = int(
            (datetime.now() - datetime.strptime(LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds())

        # 12 Hours
        if (self._deltatime > 12*3600):
            click.echo('Checking for updates...')
            LATEST_BUILD = request.urlopen(BP).url.split(
                '/')[-1].lstrip('Vanilla_Behavior_Pack_').rstrip('.zip')
            if VANILLA_VERSION < LATEST_BUILD:
                click.echo(
                    f'A newer vanilla packages were found. Updating from {VANILLA_VERSION} to {LATEST_BUILD}')
                DownloadFile(BP, f"assets/vanilla/BP.zip", "Behavior")
                DownloadFile(RP, f"assets/vanilla/RP.zip", "Resource")
            else:
                click.echo('Packages up to date')
            File("config.json", Schemes('config', NAMESPACE, COMPANY, PROJECT_NAME, DISPLAY_NAME, PROJECT_DESCRIPTION, LATEST_BUILD, NAMESPACE_FORMAT_BIT), ".", "w")

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
                RaiseError(click.style(f'Score objective must be 16 characters or less, Error at {score_id}', fg='red'))
            if score_id not in self._scores:
                self._scores.update({score_id: score_value})
                self._remove_scores.add(f'scoreboard objectives remove {score_id}')
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

    def tick(self, *functions: Function) -> None:
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
                RaiseError(
                    f'Value Error: Anvil.tick() accepts Function objects only. Error at {function}:{type(function)}.')
            self._tick.append(function.execute.split(' ')[-1].replace('\n', ''))

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
                RaiseError(f'Value Error: localized string. Error at {text}.')
            if f'{text}\n' not in self._langs:
                self._langs.append(f'{text}\n')

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
                RaiseError(f'Value Error: Anvil.setup() accepts Function objects only. Error at {function}:{type(function)}.')
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
        if FileExists('assets/ui'):
            CopyFolder('assets/ui',f'resource_packs/RP_{PASCAL_PROJECT_NAME}/textures/ui')
        if FileExists('assets/textures/glyph_E1.png'):
            CopyFiles('assets/textures',f'resource_packs/RP_{PASCAL_PROJECT_NAME}/font', 'glyph_E1.png')
        
            
        self._setup_scores.queue('StateManager/misc')
        self._remove_scores.queue('StateManager/misc')
        self._remove_tags.queue('StateManager/misc')
        for function in self._functions:
            self._setup.add(function.execute)
        File('tick.json', {'values': self._tick},
             f'behavior_packs/BP_{PASCAL_PROJECT_NAME}/functions', 'w')
        self._setup.add(self._remove_tags.execute).add(
            self._remove_scores.execute).add(self._setup_scores.execute)
        self._setup.queue()
        self._item_textures.queue()

        for object in self._objects_list:
            object._export()
        click.echo(f'Compiling time: {round(time.time() - self._start_timer,2)} s')

    @property
    def addon(self):
        with zipfile.ZipFile(f'{PROJECT_NAME}_RP.mcpack', 'w') as rp:
            for folder_name, subfolders, filenames in os.walk(f'./resource_packs/RP_{PASCAL_PROJECT_NAME}/'):
                for filename in filenames:
                    filepath = os.path.join(folder_name, filename)
                    rp.write(filepath, os.path.basename(filepath))

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
            if FileExists(path):
                return True
            #else:
            #    filename = path.split("/")[-1]
            #    raise SystemExit(click.style(f'{filename} is missing.', fg='red'))

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
        

    def _queue(self, object: object):
        self._objects_list.append(object)


ANVIL = Anvil()
