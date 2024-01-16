import sys

from .__version__ import __version__

if sys.argv[0].endswith(".py"):
    from anvil.lib.config import _AnvilConfig

    CONFIG = _AnvilConfig()

    from anvil.lib.core import _Anvil

    ANVIL = _Anvil(CONFIG)

