from ..packages import *
from anvil.api.commands import Teleport

def snap_rotation_to_grid():
    return [Teleport(Selector(Target.S).rotation(rym=-45, ry=45), ('~', '~', '~'), (0, 0)),
        Teleport(Selector(Target.S).rotation(rym=45, ry=135), ('~', '~', '~'), (90, 0)),
        Teleport(Selector(Target.S).rotation(rym=135, ry=-135), ('~', '~', '~'), (180, 0)),
        Teleport(Selector(Target.S).rotation(rym=-135, ry=-45), ('~', '~', '~'), (-90, 0))]