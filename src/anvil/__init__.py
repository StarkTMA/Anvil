from .lib import __version__, sys

if sys.argv[0].endswith('.py'):
    from .api.molang import Math, Query, Variable, molang_conditions
    from .core import *