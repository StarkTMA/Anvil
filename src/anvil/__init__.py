from .packages import os,sys,__version__

if os.path.isfile(sys.argv[0]):
    from .submodules import commands
    from .submodules import components
    from .core import *