from .packages import __version__, os, sys

if sys.argv[0].endswith('.py'):
    from .api.molang import Math, Query, Variable, molang_conditions
    from .api.tools import *
    from .core import *