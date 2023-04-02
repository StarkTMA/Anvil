
from ..core import ANVIL, NAMESPACE, PROJECT_NAME, Function
from ..packages import *
from .commands import Execute, Tag, Teleport, Clear

class Interpolation:
    interpolations = ['linear', 'nearest', 'nearest-up', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next']

    Linear = 'linear'
    Nearest = 'nearest'
    NearestUP = 'nearest-up'
    Zero = 'zero'
    SLinear = 'slinear'
    Quadratic = 'quadratic'
    Cubic = 'cubic'
    Previous = 'previous'
    Next = 'next'
    

class Cinematics():
    def __init__(self, name: str, interpolation: Interpolation, show_graphs: bool = False):
        if interpolation not in Interpolation.interpolations:
            RaiseError('Unknown interpolation.')

        self._name = name
        self._interpolation = interpolation
        self._show_graphs = show_graphs
        ANVIL.score(**{f'{self._name}_tick': 0})
        ANVIL.tag(f'{self._name}', f'{self._name}_completed')
        self.locations: list[list] = []
        self.additional_data: list[list] = []

    def anchor(self, position_xyz:tuple[float,float,float], rotation_xy:tuple[float,float], *commands):  
        self.locations[-1].append(
            {
                'x': position_xyz[0], 'y': position_xyz[1], 'z': position_xyz[2],
                'rx': rotation_xy[0], 'ry': rotation_xy[1],
                'cmd': commands
            }
        )
        return self

    def breakpoint(self, duration: Seconds = 2, camera_interpolation: Interpolation = None, interpolation = None):
        self.locations.append([])
        self.additional_data.append({
            'duration': duration,
            'camera_interpolation': self._interpolation if camera_interpolation is None else camera_interpolation,
            'interpolation': self._interpolation if interpolation is None else interpolation
        })
        return self
    
    def function(self):
        from scipy.interpolate import interp1d
        ANVIL.tag(self._name, f'{self._name}_completed')
        function = Function(self._name)
        function.add(
            Execute().As(Selector(Target.S).tag(f'!{self._name}', f'!{self._name}_completed')).run(Tag(Target.S).add(self._name)),
            f'scoreboard players add @s[tag={self._name}] {self._name}_tick 1'
        )
        function_tick = 1

        for phase, data in zip(self.locations, self.additional_data):
            #phase.insert(0, phase[0])
            #phase.append(phase[len(phase)-1])
            # Returns a list of point dicts
            # Create empty lists to host coordinates
            x_data = []
            y_data = []
            z_data = []
            rx_data = []
            ry_data = []
            commands = []
            
            # Collect coordinates nto individual lists
            for point in phase:
                x_data.append(point['x'])
                y_data.append(point['y'])
                z_data.append(point['z'])
                rx_data.append(point['rx'])
                ry_data.append(point['ry'])
                commands.append(point['cmd'])

            # Create a time list the size of input data with evenly spaced values
            # Create a new time list with 20*duration samples
            
            time = frange(0, len(x_data)-1, len(x_data))
            new_time = frange(0, len(x_data)-1, 20*data['duration'])

            # Calculate the prediction function for each list
            x_f = interp1d(time, x_data, kind = data['interpolation'])
            y_f = interp1d(time, y_data, kind = data['interpolation'])
            z_f = interp1d(time, z_data, kind = data['interpolation'])
            rx_f = interp1d(time, rx_data, kind = data['camera_interpolation'])
            ry_f = interp1d(time, ry_data, kind = data['camera_interpolation'])

            # Calculate prediction values
            new_x_data = x_f(new_time)
            new_y_data = y_f(new_time)
            new_z_data = z_f(new_time)
            new_rx_data = rx_f(new_time)
            new_ry_data = ry_f(new_time)
            
            if self._show_graphs:
                import matplotlib.pyplot as plt
                plt.figure(f'{self._interpolation} Interpolation')
                ax = plt.axes(projection ='3d')
                ax.plot(x_data, z_data, y_data, 'bo:', label='Data')
                ax.plot(new_x_data, new_z_data, new_y_data, 'r.:', label='Interpolation')
                ax.set_xlabel('X coordinates')
                ax.set_ylabel('Z coordinates')
                ax.legend()
                plt.show()

            a = 20*data['duration']//(len(commands)-1)
            for i, (x, y, z, rx, ry) in enumerate(zip(new_x_data, new_y_data, new_z_data, new_rx_data, new_ry_data)):
                if i % a == 1:
                    if commands[0] != None:
                        function.add(
                            *[Execute().As(Selector(Target.S).tag(self._name)).If.ScoreMatches(Target.S, f'{self._name}_tick', function_tick).run(cmd) for cmd in commands.pop(0)]
                        )
                    else: commands.pop(0)

                function.add(
                    Execute().As(Selector(Target.S).tag(self._name)).If.ScoreMatches(Target.S, f'{self._name}_tick', function_tick).run(Teleport(Target.S, (round(x,2), round(y,2), round(z,2)), (round(ry), round(rx))))
                )
                function_tick += 1

        function.add(
            Execute().As(Selector(Target.S).tag(self._name)).If.ScoreMatches(Target.S, f'{self._name}_tick', function_tick).run(Tag(Target.S).add(f'{self._name}_completed')),
            Execute().As(Selector(Target.S).tag(self._name)).If.ScoreMatches(Target.S, f'{self._name}_tick', function_tick).run(Tag(Target.S).remove(self._name))
        )
        
        return(function)


class StateManager():
    class _state():
        def __init__(self, index: int, type: str) -> None:
            self._index = index
            self._root = Function('root').queue(f'StateManager/{type}_{self._index}')
            self._exit_emergency = Function('exit_emergency').queue(f'StateManager/{type}_{self._index}')
            self._exit_player = Function('exit_player').queue(f'StateManager/{type}_{self._index}')
            self._exit_world = Function('exit_world').queue(f'StateManager/{type}_{self._index}')
            self._game = Function('game').queue(f'StateManager/{type}_{self._index}')
            self._init_player = Function('init_player').queue(f'StateManager/{type}_{self._index}')
            self._init_world = Function('init_world').queue(f'StateManager/{type}_{self._index}')
        @property
        def init_world(self):
            return self._init_world
        @property
        def init_player(self):
            return self._init_player
        @property
        def game(self):
            return self._game
        @property
        def exit_player(self):
            return self._exit_player
        @property
        def exit_world(self):
            return self._exit_world
        @property
        def index(self):
            return self._index

    class MainState(_state):
        def __init__(self, index: int) -> None:
            super().__init__(index, 'level')
            self._root.add(
                '#Skip init world if already initiated',
                f'execute @a[scores={{game_level={self._index}..,game_state=1..}}] ~ ~ ~ scoreboard players set @a[scores={{game_level={self._index},game_state=0}}] game_state 1',
                '#Emergency exit if player is on the next level',
                f'execute @a[scores={{game_level={self._index+1}..}}] ~ ~ ~ scoreboard players set @a[scores={{game_level={self._index}}}] game_state 5',
                '# Init world',
                f'execute @s[scores={{game_state=0}}] ~ ~ ~ {self._init_world.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=1}}] ~ ~ ~ {self._init_player.execute}',
                f'execute @s[scores={{game_state=2}}] ~ ~ ~ {self._game.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=3}}] ~ ~ ~ {self._exit_player.execute}',
                f'execute @s[scores={{game_state=4}}] ~ ~ ~ {self._exit_world.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=5}}] ~ ~ ~ {self._exit_emergency.execute}',
                f'scoreboard players operation @a[scores={{game_level={self._index},sync=1}}] game_state > {PROJECT_NAME} game_state'
            )

    class SideState(_state):
        def __init__(self, index: int) -> None:
            super().__init__(index, 'side_level')
            self._root.add(
                f'execute @s[scores={{game_level={self._index}..,game_state=1..}}] ~ ~ ~ scoreboard players set @a[scores={{game_level={self._index},game_state=0}}] game_state 1',
                '# Init world',
                f'execute @s[scores={{game_state=0}}] ~ ~ ~ {self._init_world.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=1}}] ~ ~ ~ {self._init_player.execute}',
                f'execute @s[scores={{game_state=2}}] ~ ~ ~ {self._game.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=3}}] ~ ~ ~ {self._exit_player.execute}',
                f'execute @s[scores={{game_state=4}}] ~ ~ ~ {self._exit_world.execute}',
                f'execute @a[scores={{game_level={self._index},game_state=5}}] ~ ~ ~ {self._exit_emergency.execute}',
                f'scoreboard players operation @a[scores={{game_level={self._index},sync=0,game_state=1..}}] game_state > @a[scores={{game_level={self._index},sync=0}}] game_state'
            )

    def __init__(self):
        ANVIL.tag('self_init')
        ANVIL.score(
            even = 2,
            game_level = 0,
            game_state = 0,
            sync = 1,
            player_id = 0,
            active_players = 0,
            player_count = 0,
            players_odd = 0,
        )
        # init Function, initialise player scores
        self.init_player = Function('init_player').add(
            '# Init players',
            '    # Make the game engine Sync by default',
            'clear @s',
            f'scoreboard players operation @s player_id = {PROJECT_NAME} player_id',
            f'scoreboard players add {PROJECT_NAME} player_id 1',
            'scoreboard players set @s sync 1',
            'scoreboard players set @s game_state 0',
            'scoreboard players set @s game_level 0',
            'tag @s add self_init'
        ).queue('StateManager/misc')
        # Controls active players count
        self.active_players = Function('active_players').add(
            # Resets active players count
            f'scoreboard players set {PROJECT_NAME} active_players 0',
            # Counts every player who self initialized through self_init function
            f'execute @a[tag=self_init] ~ ~ ~ scoreboard players add {PROJECT_NAME} active_players 1',
            # Calculate even or odd player count
            f'scoreboard players operation {PROJECT_NAME} players_odd = {PROJECT_NAME} active_players',
            f'scoreboard players operation {PROJECT_NAME} players_odd %= {PROJECT_NAME} even',
            # Return the active player count and odd state to every player
            # This is to be removed once the nex execute commands are out of experimental.
            f'scoreboard players operation @a active_players = {PROJECT_NAME} active_players',
            f'scoreboard players operation @a players_odd = {PROJECT_NAME} players_odd',
        ).queue('StateManager/misc')
        # Root Function, controls which game state logic works
        self.root = Function('root').add(
            '# Init new players',
            f'execute @a[tag=!self_init] ~ ~ ~ {self.init_player.execute}',
            self.active_players.execute,
            '# Engine always syncs to players',
            f'scoreboard players set {PROJECT_NAME} sync 1',
            '# Sync Engine to all players if players are syncing',
            f'scoreboard players operation @a[scores={{sync=1}}] game_level > {PROJECT_NAME} game_level'
        ).queue('StateManager').tick
        # Levels
        self.main_levels : list['StateManager.MainState'] = []
        self.side_levels : list['StateManager.SideState'] = []

    @property
    def lobby(self):
        ix = len(self.main_levels)
        state = self.MainState(ix)
        self.main_levels.append(state)
        self.root.add(f'execute @p[scores={{game_level={ix},player_id=0}}] ~ ~ ~ {state._root.execute}')
        state.init_player.add(
            'effect @s clear',
            'effect @s saturation 100000 255 true',
            'effect @s regeneration 100000 255 true',
            'xp -1000L',
            'clear @s',
            'gamemode a @a',
            Gamerule.CommandBlockOutput(False),
            Gamerule.SendCommandFeedback(False),
            Gamerule.ShowTags(False),
        )
        state.exit_player.add('effect @s clear')
        return state

    @property
    def add_main_level(self):
        ix = len(self.main_levels)
        state = self.MainState(ix)
        self.main_levels.append(state)
        self.root.add(f'execute @p[scores={{game_level={ix},player_id=0}}] ~ ~ ~ {state._root.execute}')
        return state

    @property
    def add_side_level(self):
        ix = len(self.side_levels)+1
        state = self.SideState(-ix)
        self.side_levels.append(state)
        self.root.add(f'execute @p[scores={{game_level={-ix},player_id=0}}] ~ ~ ~ {state._root.execute}')
        return state

    @property 
    def queue(self):
        self.root.add(
            '# Sync players progress back to the Engine',
            f'scoreboard players operation {PROJECT_NAME} game_level > @a[scores={{sync=1}}] game_level'
        )
        for level in self.main_levels:
            level._exit_emergency._content = level.exit_player._content
            level.init_world.add(f'scoreboard players set {PROJECT_NAME} game_state 1')
            level.init_player.add(f'scoreboard players set {PROJECT_NAME} game_state 2')
            level._exit_emergency.add(f'scoreboard players set @s game_level {level._index+1}','scoreboard players set @s game_state 0')
            level.exit_player.add(f'scoreboard players set {PROJECT_NAME} game_state 4')
            level.exit_world.add(f'scoreboard players set {PROJECT_NAME} game_state 0',f'scoreboard players set @a[scores={{game_level={level._index}}}] game_state 0',f'scoreboard players set {PROJECT_NAME} game_level {level._index+1}')
        
        for level in self.side_levels:
            level._exit_emergency._content = level.exit_player._content
            level.init_world.add(f'scoreboard players set @s game_state 1')
            level.init_player.add(f'scoreboard players set @s game_state 2')
            level._exit_emergency.add(f'scoreboard players set @s game_level 0','scoreboard players set @s game_state 0')
            level.exit_player.add(f'scoreboard players set @s game_state 4')
            level.exit_world.add(f'scoreboard players set @a[scores={{game_level={level._index}}}] game_state 1',f'scoreboard players set @a[scores={{game_level={level._index}}}] sync 1')

# This is just an update of StateManager with the new execute. Will be removed
class StateManager2():
    class _state():
        def __init__(self, index: int, type: str) -> None:
            self._index = index
            self._root = Function('root').queue(f'StateManager/{type}_{self._index}')
            self._exit_emergency = Function('exit_emergency').queue(f'StateManager/{type}_{self._index}')
            self._exit_player = Function('exit_player').queue(f'StateManager/{type}_{self._index}')
            self._exit_world = Function('exit_world').queue(f'StateManager/{type}_{self._index}')
            self._game = Function('game').queue(f'StateManager/{type}_{self._index}')
            self._init_player = Function('init_player').queue(f'StateManager/{type}_{self._index}')
            self._init_world = Function('init_world').queue(f'StateManager/{type}_{self._index}')
        @property
        def init_world(self):
            return self._init_world
        @property
        def init_player(self):
            return self._init_player
        @property
        def game(self):
            return self._game
        @property
        def exit_player(self):
            return self._exit_player
        @property
        def exit_world(self):
            return self._exit_world
        @property
        def index(self):
            return self._index

    class MainState(_state):
        def __init__(self, index: int) -> None:
            super().__init__(index, 'level')
            self._root.add(
                '#Skip init world if already initiated',
                Execute().As(f'@a[scores={{game_level={self._index}..,game_state=1..}}]').run(f'scoreboard players set @a[scores={{game_level={self._index},game_state=0}}] game_state 1'),
                '#Emergency exit if player is on the next level',
                Execute().As(f'@a[scores={{game_level={self._index+1}..}}]').run(f'scoreboard players set @a[scores={{game_level={self._index}}}] game_state 5'),
                '# Init world',
                Execute().If.ScoreMatches('@s', 'game_state', 0).run(self._init_world.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 1).run(self._init_player.execute),
                Execute().If.ScoreMatches('@s', 'game_state', 2).run(self._game.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 3).run(self._exit_player.execute),
                Execute().If.ScoreMatches('@s', 'game_state', 4).run(self._exit_world.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 5).run(self._exit_emergency.execute),
                f'scoreboard players operation @a[scores={{game_level={self._index},sync=1}}] game_state > {PROJECT_NAME} game_state'
            )

    class SideState(_state):
        def __init__(self, index: int) -> None:
            super().__init__(index, 'side_level')
            self._root.add(
                Execute().If.ScoreMatches('@s', 'game_level', f'{self._index}..').If.ScoreMatches('@s', 'game_state', '1..').run(f'scoreboard players set @a[scores={{game_level={self._index},game_state=0}}] game_state 1'),
                '# Init world',
                Execute().If.ScoreMatches('@s', 'game_state', 0).run(self._init_world.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 1).run(self._init_player.execute),
                Execute().If.ScoreMatches('@s', 'game_state', 2).run(self._game.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 3).run(self._exit_player.execute),
                Execute().If.ScoreMatches('@s', 'game_state', 4).run(self._exit_world.execute),
                Execute().As('@a').If.ScoreMatches('@s', 'game_level', self._index).If.ScoreMatches('@s', 'game_state', 5).run(self._exit_emergency.execute),
                f'scoreboard players operation @a[scores={{game_level={self._index},sync=0,game_state=1..}}] game_state > @a[scores={{game_level={self._index},sync=0}}] game_state'
            )

    def __init__(self):
        ANVIL.tag('self_init')
        ANVIL.score(
            even = 2,
            game_level = 0,
            game_state = 0,
            sync = 1,
            player_id = 0,
            active_players = 0,
            player_count = 0,
            players_odd = 0,
        )
        # init Function, initialise player scores
        self.init_player = Function('init_player').add(
            # Init players
            # Make the game engine Sync by default
            Clear('@s'),
            f'scoreboard players operation @s player_id = {PROJECT_NAME} player_id',
            f'scoreboard players add {PROJECT_NAME} player_id 1',
            'scoreboard players set @s sync 1',
            'scoreboard players set @s game_state 0',
            'scoreboard players set @s game_level 0',
            Tag('@s').add('self_init')
        ).queue('StateManager/misc')
        # Controls active players count
        self.active_players = Function('active_players').add(
            # Resets active players count
            f'scoreboard players set {PROJECT_NAME} active_players 0',
            # Counts every player who self initialized through self_init function
            Execute().As('@a[tag=self_init]').run(f'scoreboard players add {PROJECT_NAME} active_players 1'),
            # Calculate even or odd player count
            f'scoreboard players operation {PROJECT_NAME} players_odd = {PROJECT_NAME} active_players',
            f'scoreboard players operation {PROJECT_NAME} players_odd %= {PROJECT_NAME} even',
            # Return the active player count and odd state to every player
            # This is to be removed once the nex execute commands are out of experimental.
            f'scoreboard players operation @a active_players = {PROJECT_NAME} active_players',
            f'scoreboard players operation @a players_odd = {PROJECT_NAME} players_odd',
        ).queue('StateManager/misc')
        # Root Function, controls which game state logic works
        self.root = Function('root').add(
            '# Init new players',
            Execute().As('@a[tag=!self_init]').run(self.init_player.execute),
            self.active_players.execute,
            '# Engine always syncs to players',
            f'scoreboard players set {PROJECT_NAME} sync 1',
        ).queue('StateManager').tick
        # Levels
        self.main_levels : list['StateManager.MainState'] = []
        self.side_levels : list['StateManager.SideState'] = []

    @property
    def lobby(self):
        ix = len(self.main_levels)
        state = self.MainState(ix)
        self.main_levels.append(state)
        self.root.add(f'execute @p[scores={{game_level={ix}}}] ~ ~ ~ {state._root.execute}')
        state.init_player.add(
            Effect().clear('@s'),
            Effect().give('@s', Effects.Saturation, 100000, 255, True),
            Effect().give('@s', Effects.Regeneration, 100000, 255, True),
            XP('@s').remove('1000L'),
            Clear('@s'),
            Gamemode('@s', Gamemodes.Adventure),
            Gamerule().CommandBlockOutput(False),
            Gamerule().SendCommandFeedback(False),
            Gamerule().ShowTags(False),
        )
        state.exit_player.add(Effect().clear('@s'))
        return state

    @property
    def add_main_level(self):
        ix = len(self.main_levels)
        state = self.MainState(ix)
        self.main_levels.append(state)
        self.root.add(
            Execute().As(f'@p[scores={{game_level={ix}}}]').run(state._root.execute)
        )
        return state

    @property
    def add_side_level(self):
        ix = len(self.side_levels)+1
        state = self.SideState(-ix)
        self.side_levels.append(state)
        self.root.add(
            Execute().As(f'@p[scores={{game_level={-ix}}}]').run(state._root.execute)
        )
        return state

    @property 
    def queue(self):
        self.root.add(
            '# Sync Engine to all players if players are syncing',
            f'scoreboard players operation @a[scores={{sync=1}}] game_level > {PROJECT_NAME} game_level',
            '# Sync players progress back to the Engine',
            f'scoreboard players operation {PROJECT_NAME} game_level > @a[scores={{sync=1}}] game_level'
        )
        for level in self.main_levels:
            level._exit_emergency._content = level.exit_player._content
            level.init_world.add(f'scoreboard players set {PROJECT_NAME} game_state 1')
            level.init_player.add(f'scoreboard players set {PROJECT_NAME} game_state 2')
            level._exit_emergency.add(
                f'scoreboard players set @s game_level {level._index+1}',
                'scoreboard players set @s game_state 0'
            )
            level.exit_player.add(f'scoreboard players set {PROJECT_NAME} game_state 4')
            level.exit_world.add(
                f'scoreboard players set {PROJECT_NAME} game_state 0',
                f'scoreboard players set @a[scores={{game_level={level._index}}}] game_state 0',
                f'scoreboard players set {PROJECT_NAME} game_level {level._index+1}'
            )
        
        for level in self.side_levels:
            level._exit_emergency._content = level.exit_player._content
            level.init_world.add(f'scoreboard players set @s game_state 1')
            level.init_player.add(f'scoreboard players set @s game_state 2')
            level._exit_emergency.add(f'scoreboard players set @s game_level 0','scoreboard players set @s game_state 0')
            level.exit_player.add(f'scoreboard players set @s game_state 4')
            level.exit_world.add(
                f'scoreboard players set @a[scores={{game_level={level._index}}}] game_state 1',
                f'scoreboard players set @a[scores={{game_level={level._index}}}] sync 1'
            )

#A complete rewrite to leverage the new commands power
class StateMachine():
    class _state():
        def __init__(self, index: int, type: str) -> None:
            self._index = index
            self._root = Function('root').queue(f'StateMachine/{type}_{self._index}')
            self._init_player = Function('init_player').queue(f'StateMachine/{type}_{self._index}')
            self._init_world = Function('init_world').queue(f'StateMachine/{type}_{self._index}')
            self._exit_world = Function('exit_world').queue(f'StateMachine/{type}_{self._index}')
            self._game_loop = Function('game_loop').queue(f'StateMachine/{type}_{self._index}')
        @property
        def init_world(self):
            return self._init_world
        @property
        def exit_world(self):
            return self._exit_world
        @property
        def init_player(self):
            return self._init_player
        @property
        def game_loop(self):
            return self._game_loop
        @property
        def index(self):
            return self._index

    class MainState(_state):
        def __init__(self, index: int) -> None:
            super().__init__(index, 'level')
            self._root.add(
                Execute().As('@a[scores={sync = 1}]').If.Score('@s', 'game_level', Operator.Less, PROJECT_NAME, 'game_level').run(f'scoreboard players set @s player_state 0'),
                Execute().As('@a[scores={sync = 1}]').If.Score('@s', 'game_level', Operator.Less, PROJECT_NAME, 'game_level').run(f'scoreboard players set @s game_level {self.index}'),
                Execute().As(f'@a[scores={{game_level = {self._index}, player_state = 0, sync = 1}}]').run(self._init_player.execute),
                Execute().If.ScoreMatches(PROJECT_NAME, 'game_state', 0).run(self._init_world.execute),
                Execute().If.ScoreMatches(PROJECT_NAME, 'game_state', 1).run(self._game_loop.execute),
                Execute().If.ScoreMatches(PROJECT_NAME, 'game_state', 2).run(self._exit_world.execute),
            )

    def __init__(self):
        ANVIL.tag('self_init')
        ANVIL.score(
            even = 2,
            game_level = 0,
            game_state = 0,
            player_state = 0,
            player_id = 0,
            active_players = 0,
            players_odd = 0,
            sync = 1,
        )
        self.init_player = Function('init_player').add(
            Clear('@s'),
            f'scoreboard players operation @s player_id = {PROJECT_NAME} player_id',
            f'scoreboard players add {PROJECT_NAME} player_id 1',
            'scoreboard players set @s player_state 0',
            'scoreboard players set @s game_level 0',
            'scoreboard players set @s sync 1',
            Tag(Target.S).add('self_init')
        ).queue('StateMachine/misc')
        self.active_players = Function('active_players').add(
            f'scoreboard players set {PROJECT_NAME} active_players 0',
            Execute().As('@a[tag=self_init]').run(f'scoreboard players add {PROJECT_NAME} active_players 1'),
            f'scoreboard players operation {PROJECT_NAME} players_odd = {PROJECT_NAME} active_players',
            f'scoreboard players operation {PROJECT_NAME} players_odd %= {PROJECT_NAME} even',
        ).queue('StateMachine/misc')
        self.root = Function('root').add(
            '# Init new players',
            Execute().As('@a[tag=!self_init]').run(self.init_player.execute),
            self.active_players.execute,
        ).queue('StateMachine').tick
        # Levels
        self.main_levels : list['StateMachine.MainState'] = []

    @property
    def add_main_level(self):
        ix = len(self.main_levels)
        state = self.MainState(ix)
        self.main_levels.append(state)
        self.root.add(
            Execute().If.ScoreMatches(PROJECT_NAME, 'game_level', state.index).run(state._root.execute)
        )
        return state

    @property 
    def queue(self):
        for level in self.main_levels:
            level.init_world.add(f'scoreboard players set {PROJECT_NAME} game_state 1')
            level.init_player.add(f'scoreboard players set @s player_state 1')
            level.exit_world.add(
                f'scoreboard players add {PROJECT_NAME} game_level 1',
                f'scoreboard players set {PROJECT_NAME} game_state 0'
            )


class TimedFunction():
    def __init__(self, function_name: str) -> None:
        self._function_name = function_name
        self._function = Function(self._function_name)
        self._function_id = f'{NAMESPACE}{ANVIL._score_index}'
        ANVIL._score_index += 1
        ANVIL.score(**{f'{self._function_id}': 0})
        ANVIL.tag(self._function_id, self._function_name)
        self._function_limit = 0
        self._function.add(
            Execute().If.Entity(f'@s[tag=!{self._function_id}]').run(f'scoreboard objectives add {self._function_id} dummy'),
            Execute().If.Entity(f'@s[tag=!{self._function_id}]').run(Tag('@s').add(self._function_id)),
            Execute().If.Entity(f'@s[tag={self._function_id}]').run(f'scoreboard players add @s {self._function_id} 1'),
        )

    def time(self, timestamp: int, *functions: str):
        self._tick = round(timestamp*20)
        if self._function_limit < self._tick:
            self._function_limit = self._tick
        for function in functions:
            self._function.add(
                Execute().If.ScoreMatches('@s', self._function_id, self._tick).run(function)
            )
        return self

    def interval(self, starttime: int, endtime: int, *functions: str):
        if endtime <= starttime:
            RaiseError('End time cannot be greater or equal to start time')
        self._starttick = round(starttime*20)
        self._endtick = round(endtime*20)
        if self._function_limit < self._endtick:
            self._function_limit = self._endtick
        for function in functions:
            self._function.add(
                Execute().If.ScoreMatches('@s', self._function_id, f'{self._starttick}..{self._endtick}').run(function)
            )
        return self

    def queue(self, directory: str = ""):
        self._function.add(
            Execute().If.ScoreMatches('@s', self._function_id, f'{self._function_limit}..').run(Tag('@s').remove(self._function_id)),
            Execute().If.ScoreMatches('@s', self._function_id, f'{self._function_limit}..').run(Tag('@s').add(self._function_name)),
            Execute().If.ScoreMatches('@s', self._function_id, f'{self._function_limit}..').run(f'scoreboard objectives remove {self._function_id}'),
        )
        self._function.queue(directory)
        return self

    def force_time(self, timestamp: int, forced_timestamp: int):
        self._tick = round(timestamp*20)
        if self._function_limit < self._tick:
            self._function_limit = self._tick
        self._function.add(
            Execute().If.ScoreMatches('@s', self._function_id, self._tick).run(f'scoreboard players set @s {self._function_id} {round(forced_timestamp*20)}'),
            
        )
        return self

        
    @property
    def execute(self):
        return self._function.execute


class ScoreClock(Function):
    """
        Converts a score to a clock for display. To control the clock, set, add, remove scores from `sec_t`.
        To display the clock, use the scores this way: `min_0 min_1 : sec_0 sec_1`.

        Parameters:
        ---------
        `add_hours` : `bool`
            Adds hour conversion.
            
        Examples:
        ---------
        >>> f'scoreboard players add {target} sec_t 1'.
    """
    def __init__(self, target: str, add_hours: bool = False) -> None:
        super().__init__(f'tick_clock_{target}'.replace('@', ''))
        ANVIL.score(sec_t=0, sec_0=0, sec_1=0, min_0=0, min_1=0, twenty = 20, ten = 10, six = 6)
        self.add(
            f'scoreboard players operation {target} sec_1 = {target} sec_t',

            f'scoreboard players operation {target} sec_1 /= {PROJECT_NAME} twenty',
            f'scoreboard players operation {target} sec_0 = {target} sec_1',
            f'scoreboard players operation {target} sec_1 %= {PROJECT_NAME} ten',
            
            f'scoreboard players operation {target} sec_0 /= {PROJECT_NAME} ten',
            f'scoreboard players operation {target} min_1 = {target} sec_0',
            f'scoreboard players operation {target} sec_0 %= {PROJECT_NAME} six',
            
            f'scoreboard players operation {target} min_1 /= {PROJECT_NAME} six',
            f'scoreboard players operation {target} min_0 = {target} min_1',
            f'scoreboard players operation {target} min_1 %= {PROJECT_NAME} ten',
            
            f'scoreboard players operation {target} min_0 /= {PROJECT_NAME} ten',
        )
        if add_hours:
            ANVIL.score(hour_0=0, hour_1=0)
            self.add(
            f'scoreboard players operation {target} hour_1 = {target} min_0',
            f'scoreboard players operation {target} min_0 %= {PROJECT_NAME} six',
            
            f'scoreboard players operation {target} hour_1 /= {PROJECT_NAME} six',
            f'scoreboard players operation {target} hour_0 = {target} hour_1',
            f'scoreboard players operation {target} hour_1 %= {PROJECT_NAME} ten',
            )

    @property
    def queue(self):
        return super().queue('StateMachine/misc')
