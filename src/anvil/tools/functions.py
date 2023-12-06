from anvil import *
from anvil.api.commands import Clear, Execute, Scoreboard, Tag, Tellraw
from anvil.api.features import Function


class StateMachine:
    """Class for creating a state machine for managing game levels and logic.
    Useful scores:
    - game_level
    - game_state
    - side_level
    - side_state
    - player_level
    - player_state
    - active_players
    - players_odd

    """

    class _state:
        """Represent a state in the game."""

        def __init__(self, index: int, type: str, auto_progress: bool = True) -> None:
            """Initialize a state with an index, type, and auto progress flag."""

            self._index = index
            self._auto_progress = auto_progress

            # Create root, player initialization, world initialization, world exit, and game loop functions for this state.
            # Each of these functions corresponds to a certain behavior the game should take at different stages.
            path = os.path.join(f"StateMachine", f"{type}_{self._index}")
            self._root = Function("root").queue(path)
            self._init_player = Function("init_player").queue(path)
            self._init_world = Function("init_world").queue(path)
            self._exit_world = Function("exit_world").queue(path)
            self._game_loop = Function("game_loop").queue(path)
            self._jumphere = Function("jumphere").queue(path)
            self._next_state: Function = None

        # Getter methods for each function
        @property
        def init_world(self):
            return self._init_world

        @property
        def exit_world(self):
            return self._exit_world

        @property
        def init_player(self):
            return self._init_player

        @property
        def game_loop(self):
            return self._game_loop

        @property
        def index(self):
            return self._index

        @property
        def next_state(self):
            return self._next_state

    class MainState(_state):
        """Represent a main level in the game."""

        def __init__(self, index: int, next_state: Function, auto_progress: bool = True) -> None:
            """Initialize a main level.

            Parameters:
            index (int): The index of the main level in the game.
            auto_progress (bool): Determines if the game should automatically progress to the next level."""
            super().__init__(index, "level", auto_progress)
            self._next_state = next_state
            # Add commands to the root function of this main level.
            # These commands are to sync players, run the level, and initialize new players.
            self._root.add(
                # Sync players
                Execute()
                .As(Target.A)
                .If.Score(Target.S, "player_level", Operator.Less, ANVIL.PROJECT_NAME, "game_level")
                .run(Scoreboard().players.set(Target.S, "player_state", 0)),
                Execute()
                .As(Target.A)
                .If.Score(Target.S, "player_level", Operator.Less, ANVIL.PROJECT_NAME, "game_level")
                .run(Scoreboard().players.set(Target.S, "player_level", self.index)),
                # Run Level
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", 0).run(self._init_world.execute),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", 1).run(self._game_loop.execute),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", 2).run(self._exit_world.execute),
                # Init player
                Execute().As(Selector(Target.A).scores(player_level=self._index, player_state=0)).run(self._init_player.execute),
            )
            self._jumphere.add(
                Scoreboard().players.set(Target.A, "player_level", self._index),
                Scoreboard().players.set(Target.A, "player_state", 0),
                Scoreboard().players.set(ANVIL.PROJECT_NAME, "game_level", self._index),
                Scoreboard().players.set(ANVIL.PROJECT_NAME, "game_state", 0),
            )

    class SideState(_state):
        """Represent a side level in the game."""
        def __init__(self, index: int, next_state: Function, auto_progress: bool = True) -> None:
            """
            Initialize a side level.

            Parameters:
            index (int): The index of the side level in the game.
            all_players (bool): Determines if all players should be pulled into the side level.
            auto_progress (bool): Determines if the game should automatically progress to the next level.
            """
            super().__init__(index, "side_level", auto_progress)
            self._next_state = next_state
            self._root.add(
                # Sync players
                Execute()
                .As(Target.A)
                .If.Score(Target.S, "player_level", Operator.Greater, ANVIL.PROJECT_NAME, "side_level")
                .run(Scoreboard().players.set(Target.S, "player_state", 0)),
                Execute()
                .As(Target.A)
                .If.Score(Target.S, "player_level", Operator.Greater, ANVIL.PROJECT_NAME, "side_level")
                .run(Scoreboard().players.set(Target.S, "player_level", self.index)),
                # Run Level
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", 0).run(self._init_world.execute),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", 1).run(self._game_loop.execute),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", 2).run(self._exit_world.execute),
                # Init player
                Execute().As(Selector(Target.A).scores(player_level=self._index, player_state=0)).run(self._init_player.execute),
            )

            self._jumphere.add(
                Scoreboard().players.set(Target.A, "player_level", self._index),
                Scoreboard().players.set(Target.A, "player_state", 0),
                Scoreboard().players.set(ANVIL.PROJECT_NAME, "side_level", self._index),
                Scoreboard().players.set(ANVIL.PROJECT_NAME, "side_state", 0),
            )

    def __init__(self, max_player_count: int = 0):
        """Initialize a state machine.

        Args:
            max_player_count (int, optional): The maximum number of players allowed in the world. If the number of player is greater than the maximum allowed, the State Machine logic will completely freeze. Defaults to 0.
        """
        self._max_player_count = max_player_count
        # Set up scores and tag for the state machine.
        ANVIL.tag("player_init")
        ANVIL.score(
            even=2,
            game_level=0,
            game_state=0,
            side_level=0,
            side_state=0,
            player_level=0,
            player_state=0,
            player_id=0,
            active_players=0,
            players_odd=0,
        )

        # Player init setup
        # This function runs only once for ever completely new player
        # that joins the world. adds player_init tag at the end to mark it.
        self.init_player = (
            Function("init_player")
            .add(
                Clear(Target.S),
                Scoreboard().players.operation(Target.S, "player_id", ScoreboardOperation.Assign, ANVIL.PROJECT_NAME, "player_id"),
                Scoreboard().players.add(ANVIL.PROJECT_NAME, "player_id", 1),
                Scoreboard().players.set(Target.S, "player_level", 0),
                Scoreboard().players.set(Target.S, "player_state", 0),
                Tellraw(Target.A).text.text("A new player joined: [").selector(Target.S).text("]") if ANVIL.DEBUG else "",
            )
            .queue(os.path.join("StateMachine", "misc"))
        )

        # Active players function
        # Keeps track of the number of players in the world
        # Return 2 useful scores, active_players and players_odd.
        self.active_players = (
            Function("active_players")
            .add(
                Scoreboard().players.set(ANVIL.PROJECT_NAME, "active_players", 0),
                Execute().As(Selector(Target.A).tag("player_init")).run(Scoreboard().players.add(ANVIL.PROJECT_NAME, "active_players", 1)),
                Scoreboard().players.operation(ANVIL.PROJECT_NAME, "players_odd", ScoreboardOperation.Assign, ANVIL.PROJECT_NAME, "active_players"),
                Scoreboard().players.operation(ANVIL.PROJECT_NAME, "players_odd", ScoreboardOperation.Modulus, ANVIL.PROJECT_NAME, "even"),
            )
            .queue(os.path.join("StateMachine", "misc"))
        )

        # Acts as a helper function, moves to the next state
        # or next level if exhausted all states.
        self._next_main_state = (
            Function("next_main_state")
            .add(
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", "2..").run(Scoreboard().players.add(ANVIL.PROJECT_NAME, "game_level", 1)),
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", "2..")
                .run(Scoreboard().players.set(ANVIL.PROJECT_NAME, "game_state", -1)),
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", "0..1")
                .run(Scoreboard().players.add(ANVIL.PROJECT_NAME, "game_state", 1)),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "game_state", -1).run(Scoreboard().players.set(ANVIL.PROJECT_NAME, "game_state", 0)),
            )
            .queue(os.path.join("StateMachine", "misc"))
        )

        self._next_side_state = (
            Function("next_side_state")
            .add(
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", "2..").run(Scoreboard().players.set(ANVIL.PROJECT_NAME, "side_level", 0)),
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", "2..")
                .run(Scoreboard().players.set(ANVIL.PROJECT_NAME, "side_state", -1)),
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", "0..1")
                .run(Scoreboard().players.add(ANVIL.PROJECT_NAME, "side_state", 1)),
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_state", -1).run(Scoreboard().players.set(ANVIL.PROJECT_NAME, "side_state", 0)),
            )
            .queue(os.path.join("StateMachine", "misc"))
        )

        # Root function that controls the game.
        self.root = (
            Function("root")
            .add(
                Execute().As(Selector(Target.A).tag("!player_init")).run(self.init_player.execute),
            )
            .queue("StateMachine")
        )
        self.validator = (
            Function("validator")
            .add(
                Execute().If.ScoreMatches(PROJECT_NAME, "active_players", f"..{self._max_player_count}").run(self.root.execute)
                if self._max_player_count > 0
                else self.root.execute,
                self.active_players.execute,
            )
            .tick.queue("StateMachine")
        )
        # Levels
        self.main_levels: list["StateMachine.MainState"] = []
        self.side_levels: list["StateMachine.SideState"] = []

    def add_main_level(self, auto_progress: bool = True):
        """Add a main level to the state machine."""

        state = self.MainState(len(self.main_levels), self._next_main_state, auto_progress)
        self.main_levels.append(state)
        self.root.add(
            Execute()
            .If.ScoreMatches(ANVIL.PROJECT_NAME, "side_level", 0)
            .If.ScoreMatches(ANVIL.PROJECT_NAME, "game_level", state.index)
            .run(state._root.execute)
        )
        return state

    def add_side_level(self, auto_progress: bool = True):
        """
        Add a side level to the state machine.

        Parameters:
        auto_progress (bool): Determines if the game should automatically progress to the next level.

        Returns:
        The created side level.
        """
        side_state = self.SideState(-len(self.side_levels) - 1, self._next_side_state, auto_progress)
        self.side_levels.append(side_state)
        self.root.add(Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, "side_level", side_state.index).run(side_state._root.execute))
        return side_state

    def tick(self, *commands):
        """Add commands to the root function of the state machine.

        This is helpful if you want some commands and function to run at all times regardless of the level"""
        self.validator.add(*commands)
        return self

    @property
    def queue(self):
        """Set the behavior of the game at the end of each state."""
        # Queueing for main levels
        for level in self.main_levels:
            level.init_player.add(Scoreboard().players.set(Target.S, "player_state", 1))
            # If the game does not auto progress, you must run self.next_state yourself.
            if level._auto_progress:
                level.init_world.add(level.next_state.execute)
                level.exit_world.add(level.next_state.execute)

        # Queueing for side levels
        for level in self.side_levels:
            level.init_player.add(Scoreboard().players.set(Target.S, "player_state", 1))
            # If the game does not auto progress, you must run self.next_state yourself.
            if level._auto_progress:
                level.init_world.add(level.next_state.execute)
                level.exit_world.add(level.next_state.execute)

        self.init_player.add(Tag(Target.S).add("player_init"))
        if ANVIL.DEBUG:
            ANVIL._debug.text("Main Levels => ").text("game_level: ").score("game_level", ANVIL.PROJECT_NAME).text(" | ").text("game_state: ").score(
                "game_state", ANVIL.PROJECT_NAME
            ).text("\n")
            ANVIL._debug.text("Side Levels => ").text("side_level: ").score("side_level", ANVIL.PROJECT_NAME).text(" | ").text("side_state: ").score(
                "side_state", ANVIL.PROJECT_NAME
            ).text("\n")
            ANVIL._debug.text("Player Levels => ").text("player_level: ").score("player_level", Target.S).text(" | ").text("player_state: ").score(
                "player_state", Target.S
            ).text("\n")

    def __len__(self):
        """Return the number of main levels in the state machine."""
        return len(self.main_levels)


class TimedFunction:
    """Class for creating a function that runs on a timer."""

    def __init__(self, function_name: str, auto_finish: bool = True) -> None:
        """Initialize a timed function.

        Args:
            function_name (str): The name of the function.
            auto_finish (bool, optional): Determines if the function should automatically finish (sets the score to -1 at the end of the function). Defaults to True.
        """
        self._function_name = function_name
        self._auto_finish = auto_finish
        self._function = Function(self._function_name)
        self._function_id = ANVIL.new_score
        self._function_limit = 0
        self._function.add(
            Execute()
            .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, "0..")
            .run(Scoreboard().players.add(ANVIL.PROJECT_NAME, self._function_id, 1))
        )

    def time(self, timestamp: Seconds, *commands: str) -> "TimedFunction":
        """Run a function at a certain time.

        Args:
            timestamp (Seconds): The time in seconds to run the function.

        Returns:
            self: The timed function.
        """
        self._tick = round(timestamp * 20)
        if self._function_limit < self._tick:
            self._function_limit = self._tick
        for function in commands:
            self._function.add(Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, self._tick).run(function))
        return self

    def interval(self, starttime: Seconds, endtime: Seconds, *commands: str) -> "TimedFunction":
        """Run a function at a certain interval.

        Args:
            starttime (Seconds): The start time in seconds to run the function.
            endtime (Seconds): The end time in seconds to run the function.

        Returns:
            self: The timed function.
        """
        if endtime <= starttime:
            raise ValueError("End time cannot be greater or equal to start time")
        starttick = round(starttime * 20)
        endtick = round(endtime * 20)
        if self._function_limit < endtick:
            self._function_limit = endtick
        for function in commands:
            self._function.add(Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, f"{starttick}..{endtick}").run(function))
        return self

    def queue(self, directory: str = None):
        """Queue the function.

        Args:
            directory (str, optional): The directory to queue the function in. Defaults to None.
        """
        if self._auto_finish:
            self._function.add(
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, f"{self._function_limit}..")
                .run(Scoreboard().players.set(ANVIL.PROJECT_NAME, self._function_id, -1)),
            )
        else:
            self._function.add(
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, f"{self._function_limit}..")
                .run(Scoreboard().players.set(ANVIL.PROJECT_NAME, self._function_id, self._function_limit + 1)),
            )
        self._function.queue(directory)

    @property
    def execute(self) -> str:
        """Return the execute command for the function.

        Returns:
            str: The execute command for the function.
        """
        return self._function.execute

    def __str__(self) -> str:
        """Returns the score objective used in the function.

        Returns:
            str: The score that tracks time for the function.
        """
        return self._function_id


class StepTimedFunction:
    """Class for creating a function that runs on a timer with steps."""

    def __init__(self, function_name: str) -> None:
        """Initialize a step timed function.

        Args:
            function_name (str): The name of the function.
        """
        self._function_name = function_name
        self._function = Function(self._function_name)
        self._function_id = ANVIL.new_score
        self._function_limit = 0
        self._functions_steps = [{"start": 0, "end": 0, "commands": [], "condition": []}]

    @property
    def next_step(self) -> str:
        """Add a new step to the function. This must be called before writing the logic for the next step.

        Raises:
            RuntimeError: If the current step has no commands, this will raise an error.

        Returns:
            str: The command that starts the second step.
        """
        if not len(self._functions_steps[-1]["commands"]) > 0:
            raise RuntimeError("The current step has no commands, please populate it with commands before adding a new step.")

        self._functions_steps.append({"start": self._function_limit + 1, "end": 0, "commands": [], "condition": []})

        return Scoreboard().players.operation(
            ANVIL.PROJECT_NAME, self._function_id, ScoreboardOperation.Multiplication, ANVIL.PROJECT_NAME, "negative_one"
        )

    def condition(self, *commands: str) -> "StepTimedFunction":
        """Add a condition to the current step.

        Returns:
            
        """
        for command in commands:
            self._functions_steps[-2]["condition"].append(
                Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, -self._function_limit - 1).run(command)
            )
        return self

    def time(self, timestamp: Seconds, *commands: str) -> "StepTimedFunction":
        """Run a function at a certain time.

        Args:
            timestamp (Seconds): The time in seconds to run the function.

        Returns:
            StepTimedFunction: The timed function.
        """
        tick = round(timestamp * 20)
        for function in commands:
            self._functions_steps[-1]["commands"].append(Execute().If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, tick).run(function))

        self._function_limit = tick if self._function_limit < tick else self._function_limit

        self._functions_steps[-1]["end"] = tick

        return self

    def queue(self, directory: str = None):
        """Queue the function.

        Args:
            directory (str, optional): The directory to queue the function in. Defaults to None.
        """
        self._functions_steps[-1]["condition"].append(
            Execute()
            .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, -self._function_limit - 1)
            .run(Scoreboard().players.set(ANVIL.PROJECT_NAME, self._function_id, -1))
        )
        for i, step in enumerate(self._functions_steps):
            self._function.add(
                f"# Step {i} --------------------------------------------------",
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, f"{step['start']}..{step['end']}")
                .run(Scoreboard().players.add(ANVIL.PROJECT_NAME, self._function_id, 1)),
            )
            self._function.add(
                *step["commands"],
                Execute()
                .If.ScoreMatches(ANVIL.PROJECT_NAME, self._function_id, step["end"] + 1)
                .run(
                    Scoreboard().players.operation(
                        ANVIL.PROJECT_NAME, self._function_id, ScoreboardOperation.Multiplication, ANVIL.PROJECT_NAME, "negative_one"
                    )
                ),
                *step["condition"],
                "",
            )

        self._function.queue(directory)

    @property
    def execute(self) -> str:
        """Return the execute command for the function.

        Returns:
            str: The execute command for the function.
        """
        return self._function.execute

    def __str__(self) -> str:
        """Returns the score objective used in the function.

        Returns:
            str: The score that tracks time for the function.
        """
        return self._function_id
