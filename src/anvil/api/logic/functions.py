import os

from anvil.api.logic.commands import Command
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject


class Function(AddonObject):
    _extension = ".mcfunction"
    _path = os.path.join(
        CONFIG.BP_PATH, "functions", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME
    )
    _object_type = "Function"

    _ticking: list["Function"] = set()
    _setup: list["Function"] = set()
    _function_limit: int = 10000

    def __init__(self, name: str) -> None:
        """Inintializes the Function class.
        The function is limited to 10000 commands. If you exceed this limit, the function will be split into multiple functions.

        Parameters:
            name (str): The name of the function.
        """
        super().__init__(name)
        self._function: list[str] = []
        self._sub_functions: list[Function] = [self]

    def add(self, *commands: str | Command):
        """Adds a command to the function."""
        if (
            len(self._sub_functions[-1]._function)
            >= self._function_limit - len(commands) - 1
        ):
            self._sub_functions.append(
                Function(f"{self._name}_{len(self._sub_functions)}")
            )
        self._sub_functions[-1]._function.extend([str(func) for func in commands])
        return self

    @property
    def path(self):
        """Gets the path of the function. To use this properly, the function must be queued."""
        return os.path.join(self._directory, self._name)

    @property
    def execute(self):
        """Returns the execute command of the function."""
        return f"function {self.path}"

    @property
    def tick(self):
        """Adds the function to the tick.json file."""
        Function._ticking.add(self)
        return self

    @property
    def add_to_setup(self):
        """Adds the function to the setup function. Meaning this will run when your execute your setup function."""
        Function._setup.add(self)
        return self

    def queue(self, directory: str = None):
        """Queues the function to be exported.

        Parameters:
            directory (str, optional): The directory to queue the function to. Defaults to None.
        """

        self._directory = directory
        return super().queue(self._directory)

    def __len__(self):
        """Returns the number of commands in the function."""
        return len(self._function)

    def _export(self):
        """Exports the function to the file system."""
        for function in self._sub_functions[1:]:
            function.content("\n".join(function._function)).queue(self._directory)
        self.content("\n".join(self._function))
        if len(self._function) > 0:
            return super()._export()


class Tick(AddonObject):
    """Handles tick functions for the addon.

    Attributes:
        _functions (list): Stores all the tick functions.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "functions")
    _object_type = "Tick Function"

    def __init__(self) -> None:
        """Initializes a _Tick instance."""
        super().__init__("tick")
        self._functions = []
        self.do_not_shorten

    def add_function(self, *functions: "Function"):
        """Adds the provided functions to the tick function list.

        Parameters:
            functions (Function): Functions to add to the list.
        """
        self._functions.extend([f.path for f in functions])
        return self

    @property
    def queue(self):
        """Generates the content and queues the functions.

        Returns:
            object: The parent's queue method result.
        """
        self.content({"values": self._functions})
        return super().queue()
