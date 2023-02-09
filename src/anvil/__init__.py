from .packages import  __version__, os, sys

if sys.argv[0].endswith('.py'):
    from .core import *
    from .api.actors import *
    from .api import blocks
    from .api import commands
    from .api import components
    from .api.ui import *
    from .api.tools import *
    from .api.molang import Query, Variable, Math