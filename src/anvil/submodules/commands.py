from ..packages import *
from ..core import ANVIL
from .actors import Entity

GAMEMODES = ['a', 'c', 'd', 's']
GAMEMODES_FULL = ['adventure', 'creative', 'default', 'survival']
GAMEMODES_NUM = ['adventure', 'creative', 'default', 'survival']

_coordinates = NewType('tuple(x, y, z)', tuple[float, float, float])
_rotation = NewType('tuple(ry,rx)', tuple[float, float])
_level = NewType('tuple(lm,l)', tuple[float, float])

Command = NewType('Command', str)
_tick = NewType('Tick', int)
_xp = NewType('XP', int)
_level = NewType('Level', int)

inf = 99999999999

def validate(command: Command) -> Command:
    cmd = command.lower()
    cmd = cmd.lstrip('/')
    return cmd

class _RawText():
    def __init__(self, texttype: str, target):
        self._type = texttype
        self._target = target
        self._raw_text = []
        if self._type in ['actionbar', 'subtitle', 'title']:
            self._command = f'titleraw {self._target} {self._type}'
        elif self._type == 'tellraw':
            self._command = f'tellraw {self._target}'

    def text(self, text):
        self._raw_text.append({'text':text})
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
        self._raw_text.append({'translate':self.id, 'with': ['\n']})
        return self
    
    def score(self, objective, target):
        self._raw_text.append({'score':{'name': target,'objective': objective}})
        return self
    
    def selector(self, target):
        self._raw_text.append({'selector':target})
        return self
    
    def __str__(self) -> str:
        return self._command + f' {{"rawtext":{json.dumps(self._raw_text)}}}'

class CameraShakeType():
    positional = 'positional'
    rotational = 'rotational'

class MaskMode():
    replace = 'replace'
    masked = 'masked'

class CloneMode():
    force = 'force'
    move = 'move'
    normal = 'normal'

class _AlwaysDay():
    def __call__(self, lock: bool) -> str:
        return f'alwaysday {lock}'

class _CameraShake():
    def add(self, target: str, intensity: float, seconds: float, shakeType: CameraShakeType):
        return f'camerashake add {target} {intensity} {seconds} {shakeType}'

    def stope(self, target: str, intensity: float, seconds: float, shakeType: CameraShakeType):
        return f'camerashake stop {target}'

class _TitleRaw():
    def title(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('title', target)

    def subtitle(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('subtitle', target)

    def actionbar(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('actionbar', target)

class _Tellraw():
    def __call__(self, target: str = '@s' or '@a' or '@p' or '@e'):
        return _RawText('tellraw', target)

class _Summon():
    def __call__(self, entity, coordinates: _coordinates = ('~', '~', '~'), event: str = '', name: str = '', rotation:_rotation=('~', '~')):
        cmd = 'summon'
        if type(entity) is str:
            id = entity
            cmd += f' {id}'
        elif type(entity) is Entity:
            id = entity.identifier
            cmd += f' {id}'
        cmd += (f' {coordinates[0]} {coordinates[1]} {coordinates[2]}')
        if len(event) > 0:
            cmd += f' {event}'
        if len(name) > 0:
            cmd += f' "{name}"'
        if rotation != ('~', '~'):
            cmd += f'\ntp @e[type={id},x={coordinates[0]},y={coordinates[1]},z={coordinates[2]},r=1,c=1] {coordinates[0]} {coordinates[1]} {coordinates[2]} {rotation[0]} {rotation[1]}'
        return cmd

class _XP():
    """Adds or removes player experience.

    Args:
        amount (int): Specifies the amount of experience points or levels to be added or removed from the player
        player (str): Target Selector (Must be player type)

    Returns:
        Command: xp command

    Example:
        >>> xp(-2000, '@a')
        >>> xp.level(5, '@s')
    """

    def __call__(self, amount: _xp, player: str) -> Command:
        return f'xp {amount} {player}'

    def level(self, amount: _level, player: str) -> Command:
        return f'xp {amount}L {player}'

class _Weather():
    def __call__(self, set: str, duration: int) -> Command:
        """Sets the weather.

        Args:
            set (str): clear|rain|thunder
            duration (int): Must be between 0 and 1999999999 (inclusive) in ticks.

        Returns:
            Command: weather command

        Example:
            >>> Weather.clear
            >>> Weather.rain(200)
        """
        return f'weather {set} {duration}'

    @property
    def clear():
        return f'weather clear'

    def rain(self, duration: _tick):
        return f'weather rain {duration}'

    def thunder(self, duration: _tick):
        return f'weather thunder {duration}'

class _Clone():
    def __call__(self, begin: _coordinates = ('~', '~', '~'), end: _coordinates = ('~', '~', '~'), destination: _coordinates = ('~', '~', '~'), cloneMode: CloneMode = CloneMode.normal, maskMode: MaskMode = MaskMode.replace) -> Command:
        """Clones a region of blocks."""
        return f'clone {begin[0]} {begin[1]} {begin[2]} {end[0]} {end[1]} {end[2]} {destination[0]} {destination[1]} {destination[2]} {cloneMode} {maskMode}'

class _Msg():
    def __call__(self, text: str, target: str = '@a' or '@p' or '@s' or '@e'):
        return f'msg {target} {text}'

class _AnvilMsg():
    def __call__(self, text: str):
        return f'msg @a[tag=dev] "[§2Anvil§r]: {text}"'

class _Spawnpoint():
    def __call__(self, target: str, spawnPos : _coordinates = ('~','~','~')) -> str:
        return f'spawnpoint {target} {spawnPos[0]} {spawnPos[1]} {spawnPos[2]}'

class _Say():
    def __call__(self, text: str):
        return f'say {text}'

AlwaysDay = _AlwaysDay()
CameraShake = _CameraShake()
TitleRaw = _TitleRaw()
Tellraw = _Tellraw()
Summon = _Summon()
Clone = _Clone()
msg = _Msg()
Say = _Say()
AnvilMessage = _AnvilMsg()

Weather = _Weather()
xp = _XP()
Spawnpoint = _Spawnpoint()
