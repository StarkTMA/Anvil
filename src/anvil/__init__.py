from .packages import  __version__, os, sys

if sys.argv[0].endswith('.py'):
    from .core import *
    from .submodules import commands
    from .submodules import components
    from .submodules.actors import *
    from .submodules.ui import *
    from .submodules.tools import *