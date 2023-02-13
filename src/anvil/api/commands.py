from ..packages import *
from ..core import ANVIL, RawTextConstructor

class Command:
    def __init__(self, prefix: str, *commands) -> None:
        self._prefix = prefix
        self._command: str = f'{prefix}'
        for cmd in commands:
            self._command += f' {cmd}'
            
    def _new_cmd(self, *commands):
        self._command = f'{self._prefix}'
        for cmd in commands:
            self._command += f' {cmd}'
        return self
   
    def _append_cmd(self, *commands):
        for cmd in commands:
            self._command += f' {cmd}'
        return self

    def __str__(self):
        self._command = self._command.lstrip('/')
        return self._command

#special
class _RawText(RawTextConstructor):
    def __init__(self, texttype: str, target):
        self._type = texttype
        self._target = target
        if self._type in ['actionbar', 'subtitle', 'title']:
            self._command = f'titleraw {self._target} {self._type} '
        elif self._type == 'tellraw':
            self._command = f'tellraw {self._target} '
        super().__init__()
    
    def __str__(self) -> str:
        return self._command + super().__str__()

class TitleRaw(Command):
    def __init__(self) -> None:
        super().__init__('titleraw')

    def title(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('title', target)

    def subtitle(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('subtitle', target)

    def actionbar(self, target: str = '@a' or '@p' or '@s' or '@e'):
        return _RawText('actionbar', target)

class Tellraw(Command):
    def __init__(self, target: str):
        self._target = target

    @property
    def text(self):
        return _RawText('tellraw', self._target)

class Execute(Command):
    class _ExecuteIfUnless():
        def __init__(self, parent: 'Execute', condition:str) -> None:
            self._parent = parent
            self._condition = condition

        def Entity(self, target: Selector):
            self._parent._append_cmd(self._condition, 'entity', target)
            return self._parent

        def Block(self, block_position: coordinates, block: str, data: int = -1):
            self._parent._append_cmd(self._condition, 'block', ' '.join(map(str, block_position)), block, data if not data == 1 else '')
            return self._parent

        def Blocks(self, begin: coordinates, end: coordinates, destination: coordinates, masked: bool = False):
            self._parent._append_cmd(
                self._condition, 
                'blocks', 
                ' '.join(map(str, begin)),
                ' '.join(map(str, end)), 
                ' '.join(map(str, destination)), 
                masked if masked == True else ''
            )
            return self._parent

        def ScoreMatches(self, target: str, objective: str, matches: range):
            self._parent._append_cmd(self._condition, 'score', target, objective, 'matches', matches)
            return self._parent

        def Score(self, target: str, target_objective: str, operator: Operator, source: str, source_objective: str):
            self._parent._append_cmd(self._condition, 'score', target, target_objective, operator, source, source_objective)
            return self._parent

    def __init__(self) -> None:
        super().__init__('execute')
    
    def As(self, target: str):
        super()._append_cmd('as', target)
        return self

    def At(self, target: str):
        super()._append_cmd('at', target)
        return self

    def In(self, dimension: Dimension = Dimension.Overworld):
        super()._append_cmd('in', dimension)
        return self

    def Positioned(self, poistion: coordinates):
        super()._append_cmd('positioned', ' '.join(map(str, poistion)))
        return self

    def PositionedAs(self, target: str):
        super()._append_cmd('positioned', 'as', target)
        return self
        
    def Align(self, axes: str = 'xyz'):
        super()._append_cmd('align', "".join(set(axes)))
        return self

    def Anchored(self, anchored: Anchor = Anchor.Feet):
        super()._append_cmd('anchored', anchored)
        return self
        
    def Rotated(self, yaw: float | str = '~', pitch: float | str = '~'):
        super()._append_cmd('rotated', yaw, pitch)
        return self

    def RotatedAs(self, target: str):
        super()._append_cmd('rotated', 'as', target)
        return self
        
    def Facing(self, poistion: coordinates):
        super()._append_cmd('facing', ' '.join(map(str, poistion)))
        return self
    
    def FacingEntity(self, target: str, anchor: Anchor = Anchor.Feet):
        super()._append_cmd('facing', 'entity', target, anchor)
        return self

    @property
    def If(self):
        return self._ExecuteIfUnless(self, 'if')

    @property
    def Unless(self):
        return self._ExecuteIfUnless(self, 'unless')

    def run(self, command: Command | str):
        super()._append_cmd('run', command)
        return self

class AlwaysDay(Command):
    def __init__(self, lock: bool = True):
        super().__init__('alwaysday', lock)

class CameraShake(Command):
    def __init__(self) -> None:
        super().__init__('camerashake')

    def add(self, target: str, intensity: float, seconds: float, shakeType: CameraShakeType):
        super()._new_cmd('add', target, intensity, seconds, shakeType)

    def stop(self, target: str):
        super()._new_cmd('stop', 'target')

class Summon(Command):
    def __init__(self, entity, coordinates: coordinates = ('~', '~', '~'), event: str = 'minecraft:entity_spawned', name: str = '', rotation:rotation=('~', '~')):
        super().__init__('summon', entity)
        if not coordinates == ('~', '~', '~'):
            self._command += f' {" ".join(map(str, coordinates))}'
        if not event == 'minecraft:entity_spawned':
            self._command += f' {event}'
        if not name == '':
            if event == 'minecraft:entity_spawned':
                self._command += f' {event}'
            self._command += f' "{name}"'
        if not rotation == ('~', '~'):
            self._command += f' {" ".join(map(str, rotation))}'

class XP(Command):
    """Adds or removes player experience.

    Args:
        amount (int): Specifies the amount of experience points or levels to be added or removed from the player
        player (str): Target Selector (Must be player type)

    Returns:
        Command: xp command

    Example:
        >>> xp('-2000', '@a')
        >>> xp('-5L', '@a')
    """

    def __init__(self):
        super().__init__('xp')
    
    def add(self, target, amount):
        super()._new_cmd(amount, target)
    
    def remove(self, target, amount):
        super()._new_cmd(f'-{amount}', target)

class Weather(Command):
    def __init__(self) -> None:
        super().__init__('weather')
    @property
    def clear(self):
        super()._new_cmd('clear')

    def rain(self, duration: tick):
        super()._new_cmd('rain', duration)

    def thunder(self, duration: tick):
        super()._new_cmd('thunder', duration)

class Clone(Command):
    def __init__(self, begin: coordinates, end: coordinates, destination: coordinates, cloneMode: CloneMode = CloneMode.normal, maskMode: MaskMode = MaskMode.replace):
        """Clones a region of blocks."""
        super().__init__(
            'clone', 
            ' '.join(map(str,begin)), 
            ' '.join(map(str,end)), 
            ' '.join(map(str,destination)), 
            cloneMode, 
            maskMode
        )

class Msg(Command):
    def __init__(self, text: str, target: str):
        super().__init__('msg', target, text)

class DebugMsg(Command):
    def __init__(self, text: str) -> None:
        super().__init__('msg', '@a[tag=dev]', f"[§2Anvil§r]: {text}")

class Spawnpoint(Command):
    def __init__(self, target: str, spawnPos : coordinates):
        super().__init__(
            'spawnpoint', 
            target, 
            ' '.join(map(str, spawnPos))
        )

class Say(Command):
    def __init__(self, text: str):
        super().__init__('say', text)

class Gamerule(Command):
    def __init__(self) -> None:
        super().__init__('gamerule')

    def SendCommandFeedback(self, value: bool = True):
        super()._new_cmd('sendcommandfeedback', value)

    def CommandBlockOutput(self, value: bool = True):
        super()._new_cmd('commandblockoutput', value)

    def ShowTags(self, value: bool = True):
        super()._new_cmd('showtags', value)

class Fog(Command):
    def __init__(self) -> None:
        super().__init__('fog')

    def Push(self, target: str, fog_identifie: str, name: str):
        super()._new_cmd(target, 'push', fog_identifie, name)
        return self

    def Pop(self, target: str, name: str):
        super()._new_cmd(target, 'pop', name)
        return self

    def Remove(self, target: str, name: str):
        super()._new_cmd(target, 'remove', name)
        return self

class Tag(Command):
    def __init__(self, target: str) -> None:
        super().__init__('tag')
        self._target = target

    def add(self, tag: str):
        super()._new_cmd(self._target, 'add', tag)
        return self

    def remove(self, tag: str):
        super()._new_cmd(self._target, 'remove', tag)
        return self

class Clear(Command):
    def __init__(self ,target: str, itemname: str = '', date : int = -1, max_count: int = -1) -> None:
        super().__init__('clear', target, itemname, date if not date == -1 else '', max_count if not max_count == -1 else '')

class Effect(Command):
    def __init__(self) -> None:
        super().__init__('effect')
    
    def clear(self, target: str):
        super()._new_cmd(target, 'clear')

    def give(self, target: str, effect: Effects, seconds: int, amplifier: int, hide_particles: bool):
        super()._new_cmd(
            target, 
            effect, 
            seconds, 
            amplifier, 
            hide_particles
        )

class Gamemode(Command):
    def __init__(self, target: str, gamemode: Gamemodes):
        super().__init__('gamemode', target, gamemode)

class Teleport(Command):
    def __init__(self, target, destination: coordinates, rotation: rotation = ('~', '~')) -> None:
        super().__init__(
            'teleport',
            target,
            ' '.join(map(str, destination)),
            ' '.join(map(str, rotation)) if not rotation == ('~', '~') else ''
        )

class Event(Command):
    def __init__(self, target: Target, event: event) -> None:
        super().__init__('event', 'entity',target, event)
        
class Function(Command):
    def __init__(self, path) -> None:
        super().__init__('function', path)