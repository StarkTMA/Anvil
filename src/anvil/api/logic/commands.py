import json
from math import inf

from anvil.api.blocks.blocks import Block
from anvil.lib.enums import (
    Anchor,
    CameraEasing,
    CameraPresets,
    CameraShakeType,
    CloneMode,
    DamageCause,
    Dimension,
    Effects,
    FillMode,
    Gamemodes,
    HudElement,
    HudVisibility,
    InputPermissions,
    MaskMode,
    MusicRepeatMode,
    RawTextConstructor,
    ScoreboardOperation,
    ScoreboardOperator,
    Selector,
    Slots,
    Target,
    TimeSpec,
)
from anvil.lib.lib import clamp, normalize_180
from anvil.lib.schemas import (
    BlockDescriptor,
    MinecraftBlockDescriptor,
    MinecraftItemDescriptor,
)
from anvil.lib.types import (
    Color,
    Coordinates,
    Event,
    Identifier,
    RelativePosition,
    RelativeRotation,
    Seconds,
    Tick,
)


class Command:
    def __init__(self, prefix: str, *commands) -> None:
        self._prefix = prefix
        self._components = {}
        self._command = f"{self._prefix} {' '.join([str(cmd) for cmd in commands])}"

    def _new_cmd(self, *commands):
        self._command = f"{self._prefix} {' '.join([str(cmd) for cmd in commands])}"
        return self

    def _append_cmd(self, *commands):
        self._command += f" {' '.join([str(cmd) for cmd in commands])}"
        return self

    def _add_nbt_component(self, component: dict):
        self._components.update(component)
        return self

    def __str__(self):
        self._command = self._command.lstrip("/")
        if len(self._components) > 0:
            self._append_cmd(json.dumps(self._components))
            self._components = {}
        return self._command


class ItemComponents(Command):
    def can_place_on(self, *blocks):
        self._add_nbt_component({"minecraft:can_place_on": {"blocks": blocks}})
        return self

    def can_destroy(self, *blocks):
        self._add_nbt_component({"minecraft:can_destroy": {"blocks": blocks}})
        return self

    def item_lock(self, *, lock_in_slot: bool = False, lock_in_inventory: bool = False):
        if lock_in_slot or lock_in_inventory:
            self._add_nbt_component(
                {
                    "minecraft:item_lock": {
                        "mode": "lock_in_slot" if lock_in_slot else "lock_in_inventory"
                    }
                }
            )
        return self

    @property
    def keep_on_death(self):
        self._add_nbt_component({"minecraft:keep_on_death": {}})
        return self


# special
class _RawText(RawTextConstructor):
    def __init__(self, texttype: str, target):
        self._type = texttype
        self._target = target
        if self._type in ["actionbar", "subtitle", "title"]:
            self._command = f"titleraw {self._target} {self._type} "
        elif self._type == "tellraw":
            self._command = f"tellraw {self._target} "
        super().__init__()

    def __str__(self) -> str:
        return self._command + super().__str__()


class TitleRaw(Command):
    def __init__(self) -> None:
        super().__init__("titleraw")

    def title(self, target: Selector | Target):
        return _RawText("title", target)

    def subtitle(self, target: Selector | Target):
        return _RawText("subtitle", target)

    def actionbar(self, target: Selector | Target):
        return _RawText("actionbar", target)

    def times(self, target: Selector | Target, fade_in: int, stay: int, fade_out: int):
        self._append_cmd(target, "times", fade_in, stay, fade_out)
        return self


class Tellraw(Command):
    def __init__(self, target: str):
        self._target = target

    @property
    def text(self):
        return _RawText("tellraw", self._target)


class Execute(Command):
    class _ExecuteIfUnless:
        def __init__(self, parent: "Execute", condition: str) -> None:
            self._parent = parent
            self._condition = condition

        def Entity(self, target: Selector):
            self._parent._append_cmd(self._condition, "entity", target)
            return self._parent

        def Block(
            self, block_position: Coordinates, tile: Block | Identifier, **properties
        ):

            if isinstance(tile, Block):
                name = tile.identifier
                states = tile.states
            elif isinstance(tile, str):
                name = tile
                states = ""
            else:
                raise TypeError(
                    f"Unsupported block type: {type(tile).__name__}. Command [{self._prefix}]."
                )

            for k, v in properties.items():
                states.append(f'"{k}" : "{v}"')

            self._parent._append_cmd(
                self._condition,
                "block",
                *block_position,
                name,
                f'[{", ".join(states)}]',
            )
            return self._parent

        def Blocks(
            self,
            begin: Coordinates,
            end: Coordinates,
            destination: Coordinates,
            masked: bool = False,
        ):
            self._parent._append_cmd(
                self._condition,
                "blocks",
                *begin,
                *end,
                *destination,
                masked if masked == True else "",
            )
            return self._parent

        def ScoreMatches(self, target: str, objective: str, matches: range):
            self._parent._append_cmd(
                self._condition,
                "score",
                target,
                objective,
                "matches",
                round(matches) if isinstance(matches, float) else matches,
            )
            return self._parent

        def Score(
            self,
            target: str,
            target_objective: str,
            operator: ScoreboardOperator,
            source: str,
            source_objective: str,
        ):
            self._parent._append_cmd(
                self._condition,
                "score",
                target,
                target_objective,
                operator,
                source,
                source_objective,
            )
            return self._parent

    def __init__(self) -> None:
        super().__init__("execute")

    def As(self, target: str):
        super()._append_cmd("as", target)
        return self

    def At(self, target: str):
        super()._append_cmd("at", target)
        return self

    def In(self, dimension: Dimension = Dimension.Overworld):
        super()._append_cmd("in", dimension)
        return self

    def Positioned(self, poistion: Coordinates):
        super()._append_cmd("positioned", " ".join(map(str, poistion)))
        return self

    def PositionedAs(self, target: str):
        super()._append_cmd("positioned", "as", target)
        return self

    def Align(self, axes: str = "xyz"):
        super()._append_cmd("align", "".join(set(axes)))
        return self

    def Anchored(self, anchored: Anchor = Anchor.Feet):
        super()._append_cmd("anchored", anchored)
        return self

    def Rotated(self, yaw: float | str = "~", pitch: float | str = "~"):
        super()._append_cmd("rotated", yaw, pitch)
        return self

    def RotatedAs(self, target: str):
        super()._append_cmd("rotated", "as", target)
        return self

    def Facing(self, poistion: Coordinates):
        super()._append_cmd("facing", " ".join(map(str, poistion)))
        return self

    def FacingEntity(self, target: str, anchor: Anchor = Anchor.Feet):
        super()._append_cmd("facing", "entity", target, anchor)
        return self

    @property
    def If(self):
        return self._ExecuteIfUnless(self, "if")

    @property
    def Unless(self):
        return self._ExecuteIfUnless(self, "unless")

    def run(self, command: Command | str):
        super()._append_cmd("run", command)
        return self


class AlwaysDay(Command):
    def __init__(self, lock: bool = True):
        super().__init__("alwaysday", lock)


class CameraShake(Command):
    def __init__(self) -> None:
        super().__init__("camerashake")

    def add(
        self, target: str, intensity: float, seconds: float, shakeType: CameraShakeType
    ):
        super()._append_cmd("add", target, intensity, seconds, shakeType)
        return self

    def stop(self, target: str):
        super()._append_cmd("stop", target)
        return self


class Summon(Command):
    def __init__(self, entity: Identifier, coordinates: Coordinates = ("~", "~", "~")):
        self.argument = {
            "coordinates": (str(c) for c in coordinates),
            "lookAtEntity": None,
            "lookAtPosition": None,
            "rotation": None,
            "spawnEvent": None,
            "nameTag": None,
        }
        super().__init__("summon", entity)

    def nameTag(self, nameTag: str):
        self.argument["nameTag"] = f'"{nameTag}"'
        return self

    def spawnEvent(self, spawnEvent: str):
        self.argument["spawnEvent"] = spawnEvent
        return self

    def lookAtEntity(self, entity: Selector | Target):
        self.argument["lookAtEntity"] = entity
        return self

    def lookAtPosition(self, coordinates: Coordinates):
        self.argument["lookAtPosition"] = coordinates
        return self

    def rotation(self, ry="~", rx="~"):
        self.argument["rotation"] = (str(ry), str(rx))
        return self

    def __str__(self):
        rots = sum(
            [
                x is not None
                for x in (
                    self.argument.get("lookAtEntity"),
                    self.argument.get("lookAtPosition"),
                    self.argument.get("rotation"),
                )
            ]
        )
        nameTag = self.argument.get("nameTag")
        spawnEvent = self.argument.get("spawnEvent")

        if rots > 1:
            raise ValueError(
                f"Only one of 'lookAtEntity', 'lookAtPosition', or 'rotation' can be set at a time. Found {rots} set."
            )

        if rots == 0 and not nameTag is None and spawnEvent is None:
            self._append_cmd(nameTag)
            self._append_cmd(" ".join(self.argument.get("coordinates")))

        else:
            if rots == 0:
                self.argument["rotation"] = ("~", "~")

            self._append_cmd(" ".join(self.argument.get("coordinates")))

            if self.argument.get("lookAtEntity") != None:
                self._append_cmd("facing", self.argument.get("lookAtEntity"))

            elif self.argument.get("lookAtPosition") != None:
                self._append_cmd(
                    "facing", " ".join(self.argument.get("lookAtPosition"))
                )

            else:
                self._append_cmd(" ".join(self.argument.get("rotation")))

            if spawnEvent != None:
                self._append_cmd(spawnEvent)

            if nameTag != None:
                if spawnEvent == None:
                    self._append_cmd("minecraft:entity_spawned")
                self._append_cmd(nameTag)

        return super().__str__()


class XP(Command):
    def __init__(self):
        """Adds or removes player experience."""
        super().__init__("xp")

    def add(self, target: Selector | Target | str, amount: int) -> Command:
        """Adds experience to a player.

        Parameters:
            target (Selector | Target | str): The target to add experience to.
            amount (int): The amount of experience to add.

        Returns:
            Command: The command.
        """
        super()._new_cmd(amount, target)
        return self

    def remove(self, target: Selector | Target | str, amount: int) -> Command:
        """Removes experience from a player.

        Parameters:
            target (Selector | Target | str): The target to remove experience from.
            amount (int): The amount of experience to remove.

        Returns:
            Command: The command.
        """
        super()._new_cmd(f"-{amount}", target)
        return self


class Weather(Command):
    def __init__(self) -> None:
        super().__init__("weather")

    @property
    def clear(self):
        return super()._new_cmd("clear")

    def rain(self, duration: Tick = inf):
        return super()._new_cmd("rain", duration if duration != inf else "")

    def thunder(self, duration: Tick = inf):
        return super()._new_cmd("thunder", duration if duration != inf else "")


class Clone(Command):
    def __init__(
        self,
        begin: Coordinates,
        end: Coordinates,
        destination: Coordinates,
        cloneMode: CloneMode = CloneMode.normal,
        maskMode: MaskMode = MaskMode.replace,
    ):
        """Clones a region of blocks."""
        super().__init__(
            "clone",
            " ".join(map(str, begin)),
            " ".join(map(str, end)),
            " ".join(map(str, destination)),
            cloneMode,
            maskMode,
        )


class Msg(Command):
    def __init__(self, text: str, target: str):
        super().__init__("msg", target, text)


class DebugMsg(Command):
    def __init__(self, text: str) -> None:
        super().__init__("msg", "@a[tag=dev]", f"[§2Anvil§r]: {text}")


class Spawnpoint(Command):
    def __init__(self, target: str, spawnPos: Coordinates):
        super().__init__("spawnpoint", target, " ".join(map(str, spawnPos)))


class Say(Command):
    def __init__(self, text: str):
        super().__init__("say", f'"{text}"')


class Gamerule(Command):
    def __init__(self) -> None:
        super().__init__("gamerule")

    def SendCommandFeedback(self, value: bool = True):
        return super()._new_cmd("sendcommandfeedback", value)

    def CommandBlockOutput(self, value: bool = True):
        return super()._new_cmd("commandblockoutput", value)

    def ShowTags(self, value: bool = True):
        return super()._new_cmd("showtags", value)

    def PlayerSleepingPercentage(self, percentage: int = 0):
        return super()._new_cmd("sendcommandfeedback", clamp(percentage, 0, 100))

    def dodaylightcycle(self, value: bool = True):
        return super()._new_cmd("dodaylightcycle", value)


class Fog(Command):
    def __init__(self) -> None:
        super().__init__("fog")

    def Push(self, target: str, fog_identifie: str, name: str):
        super()._new_cmd(target, "push", fog_identifie, f'"{name}"')
        return self

    def Pop(self, target: str, name: str):
        super()._new_cmd(target, "pop", f'"{name}"')
        return self

    def Remove(self, target: str, name: str):
        super()._new_cmd(target, "remove", f'"{name}"')
        return self


class Tag(Command):
    def __init__(self, target: str) -> None:
        super().__init__("tag")
        self._target = target

    def add(self, tag: str):
        super()._new_cmd(self._target, "add", tag)
        return self

    def remove(self, tag: str):
        super()._new_cmd(self._target, "remove", tag)
        return self


class Clear(Command):
    def __init__(
        self, target: Target, itemname: str = "", date: int = -1, max_count: int = -1
    ) -> None:
        super().__init__(
            "clear",
            target,
            itemname,
            date if not date == -1 else "",
            max_count if not max_count == -1 else "",
        )


class Effect(Command):
    def __init__(self, target: Selector) -> None:
        super().__init__("effect", target)

    def clear(self, effect: Effects = None):
        self._append_cmd("clear")
        if effect:
            self._append_cmd(effect)
        return self

    def give(
        self,
        effect: Effects,
        seconds: int = "infinite",
        amplifier: int = 1,
        hide_particles: bool = False,
    ):
        self._append_cmd(effect, seconds, amplifier)
        if amplifier != 1:
            self._append_cmd(amplifier)
        if hide_particles:
            self._append_cmd("true")
        return self


class Gamemode(Command):
    def __init__(self, target: str, gamemode: Gamemodes):
        super().__init__("gamemode", gamemode, target)


class Teleport(Command):
    def __init__(
        self,
        target,
        destination: Coordinates | Target | Selector,
        rotation: RelativeRotation = ("~", "~"),
    ) -> None:
        super().__init__("teleport", target)
        if isinstance(destination, tuple):
            self._append_cmd(
                " ".join(map(str, destination)),
                (
                    " ".join(map(str, (normalize_180(rotation[0]), rotation[1])))
                    if not rotation == ("~", "~")
                    else ""
                ),
            )
        elif isinstance(destination, Target | Selector):
            self._append_cmd(destination)

    def Facing(self, poistion: Coordinates):
        super()._append_cmd("facing", " ".join(map(str, poistion)))
        return self

    def FacingEntity(self, target: str):
        super()._append_cmd("facing", target)
        return self


class Event(Command):
    def __init__(self, target: Selector | Target | str, event: Event) -> None:
        super().__init__("event", "entity", target, event)


class Function(Command):
    def __init__(self, path) -> None:
        super().__init__("function", path)


class Give(ItemComponents):
    def __init__(
        self, target: Selector | Target | str, item: str, amount: int = 1, data: int = 0
    ) -> None:
        super().__init__("give", target, item, amount, data)


class ReplaceItem(ItemComponents):
    def __init__(self) -> None:
        super().__init__("replaceitem")

    def block(
        self,
        poistion: Coordinates,
        slot_id: int,
        item_name: str,
        amount: int = 1,
        data: int = 0,
    ):
        super()._new_cmd(
            "block", *poistion, Slots.Container, slot_id, item_name, amount, data
        )
        return self

    def entity(
        self,
        target: Selector | Target | str,
        slot: Slots,
        slot_id: int,
        item_name: str,
        amount: int = 1,
        data: int = 0,
    ):
        super()._new_cmd("entity", target, slot, slot_id, item_name, amount, data)
        return self


class Damage(ItemComponents):
    def __init__(
        self, target: Selector | Target | str, amount: int, cause: DamageCause
    ) -> None:
        super().__init__("damage", target, amount, cause.value)

    def damager(self, damager: Selector | Target) -> None:
        self._append_cmd("entity", damager)
        return self


class Playsound(Command):
    def __init__(
        self,
        sound: str,
        target: Selector | Target = Target.S,
        position: RelativePosition = None,
        volume: int = 1,
        pitch: int = 1,
        minimumVolume: int = 0,
    ) -> None:
        super().__init__("playsound", sound, target)

        if position != None:
            self._append_cmd(*position, volume, pitch, minimumVolume)


class InputPermission(Command):
    def __init__(self) -> None:
        super().__init__("inputpermission", "set")

    def enable(
        self, permission: InputPermissions, target: Selector | Target = Target.S
    ):
        self._append_cmd(target, permission, "enabled")
        return self

    def disable(
        self, permission: InputPermissions, target: Selector | Target = Target.S
    ):
        self._append_cmd(target, permission, "disabled")
        return self


class Scoreboard(Command):
    class _ScoreboardObjective:
        class _ScoreboardObjectiveDisplay:
            def __init__(self, parent: "Scoreboard") -> None:
                self.parent = parent

            def list(self, objective, ascending: bool = True):
                self.parent._append_cmd(
                    "list", objective, "ascending" if ascending else "descending"
                )
                return self.parent

            def sidebar(self, objective: str, ascending: bool = True):
                self.parent._append_cmd(
                    "sidebar", objective, "ascending" if ascending else "descending"
                )
                return self.parent

            def belowName(self, objective):
                self.parent._append_cmd("belowName", objective)
                return self.parent

        def __init__(self, parent: "Scoreboard") -> None:
            self.parent = parent

        def add(self, objective: str, display_name: str = None):
            cmd_Parameters = [objective, "dummy"]
            if display_name:
                cmd_Parameters.append(display_name)
            self.parent._append_cmd("add", *cmd_Parameters)
            return self.parent

        def remove(self, objective: str):
            self.parent._append_cmd("remove", objective)
            return self.parent

        @property
        def list(self):
            self.parent._append_cmd("list")
            return self.parent

        @property
        def setdisplay(self):
            self.parent._append_cmd("setdisplay")
            return self._ScoreboardObjectiveDisplay(self.parent)

    class _ScoreboardPlayers:
        def __init__(self, parent: "Scoreboard") -> None:
            self.parent = parent

        def set(self, target: Selector | Target | str, objective: str, count: int):
            self.parent._append_cmd("set", target, objective, count)
            return self.parent

        def add(self, target: Selector | Target | str, objective: str, count: int):
            self.parent._append_cmd("add", target, objective, count)
            return self.parent

        def remove(self, target: Selector | Target | str, objective: str, count: int):
            self.parent._append_cmd("remove", target, objective, count)
            return self.parent

        def list(self, target: Selector | Target):
            self.parent._append_cmd("list", target)
            return self.parent

        def operation(
            self,
            target: Selector | Target | str,
            objective1: str,
            operation: ScoreboardOperation,
            source: str,
            objective2: str,
        ):
            self.parent._append_cmd(
                "operation", target, objective1, operation, source, objective2
            )
            return self.parent

        def random(
            self, target: Selector | Target | str, objective: str, min: int, max: int
        ):
            self.parent._append_cmd("random", target, objective, min, max)
            return self.parent

        def reset(self, target: Selector | Target | str, objective: str):
            self.parent._append_cmd("reset", target, objective)
            return self.parent

    def __init__(self) -> None:
        super().__init__("scoreboard")

    @property
    def objective(self):
        self._append_cmd("objectives")
        return self._ScoreboardObjective(self)

    @property
    def players(self):
        self._append_cmd("players")
        return self._ScoreboardPlayers(self)


class Setblock(Command):
    def __init__(
        self,
        tile: Block | Identifier,
        position: RelativePosition = ("~", "~", "~"),
        **properties: str,
    ) -> None:
        super().__init__("setblock")

        if isinstance(tile, (BlockDescriptor, MinecraftBlockDescriptor)):
            name = tile.identifier
            states = tile.states
        elif isinstance(tile, str):
            name = tile
            states = ""
        else:
            raise TypeError(
                f"Unsupported block type: {type(tile).__name__}. Command [{self._prefix}]."
            )

        for k, v in properties.items():
            states.append(f'"{k}" = "{v}"')

        self._append_cmd(" ".join(map(str, position)), name, f'[{", ".join(states)}]')


class Fill(Command):
    def __init__(
        self,
        tile: str | Block,
        start: RelativePosition = ("~", "~", "~"),
        end: RelativePosition = ("~", "~", "~"),
        old_block_handling: FillMode = FillMode.Replace,
        **properties: str,
    ) -> None:
        super().__init__("fill")

        if isinstance(tile, Block):
            name = tile.identifier
            states = tile.states
        elif isinstance(tile, str):
            name = tile
            states = ""
        else:
            raise TypeError(
                f"Unsupported block type: {type(tile).__name__}. Command [{self._prefix}]."
            )

        for k, v in properties.items():
            states.append(f'"{k}" = "{v}"')

        self._append_cmd(
            *start,
            *end,
            name,
            f'[{", ".join(states)}]',
            old_block_handling if old_block_handling != FillMode.Replace else "",
        )

    def replace(
        self,
        tile: str | Block,
        **properties: str,
    ):
        if isinstance(tile, Block):
            name = tile.identifier
            states = tile.states
        elif isinstance(tile, str):
            name = tile
            states = ""
        else:
            raise TypeError(
                f"Unsupported block type: {type(tile).__name__}. Command [{self._prefix}]."
            )

        for k, v in properties.items():
            states.append(f'"{k}" = "{v}"')

        self._append_cmd(FillMode.Replace, name, f'[{", ".join(states)}]')


class Music(Command):
    def __init__(self) -> None:
        super().__init__("music")

    def _base(
        self,
        track_name: str,
        volume: float = 1,
        fade_seconds: float = 1,
        repeat_mode: MusicRepeatMode = MusicRepeatMode.Once,
    ):
        self._append_cmd(track_name)
        if volume != 1:
            self._append_cmd(volume)

        if fade_seconds != 1:
            self._append_cmd(fade_seconds)

        if repeat_mode != MusicRepeatMode.Once:
            self._append_cmd(repeat_mode)

        return self

    def queue(
        self,
        track_name: str,
        volume: float = 1,
        fade_seconds: float = 1,
        repeat_mode: MusicRepeatMode = MusicRepeatMode.Once,
    ):
        self._append_cmd("queue")
        return self._base(track_name, volume, fade_seconds, repeat_mode)

    def play(
        self,
        track_name: str,
        volume: float = 1,
        fade_seconds: float = 1,
        repeat_mode: MusicRepeatMode = MusicRepeatMode.Once,
    ):
        self._append_cmd("play")
        return self._base(track_name, volume, fade_seconds, repeat_mode)

    def stop(self, fade_seconds: float = 1):
        self._append_cmd("stop")

        if fade_seconds != 1:
            self._append_cmd(fade_seconds)

        return self

    def volume(self, volume: float):
        self._append_cmd("volume", volume)

        return self


class ScriptEvent(Command):
    def __init__(self, message_id: str, message: str = None) -> None:
        """Causes an event to fire within script with the specified message ID and payload. This can be used to connect scripting with any location where commands are used.

        Parameters:
            message_id (str): identifier of the message to send. This is custom and dependent on the kinds of behavior packs and content you may have installed within the world.
            message (str): Data component of the message to send. This is custom and dependent on the kinds of behavior packs and content you may have installed within the world.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/commands/commands/scriptevent
        """
        super().__init__("scriptevent", message_id, message if message != None else "")


class Camera(Command):
    class _CameraSet(Command):
        def __init__(self, target, preset) -> None:
            super().__init__("camera", target, "set", preset)

            self.argument = {
                "easing": None,
                "easing_time": None,
                "position": None,
                "rotation": None,
                "facing_target": None,
                "facing_position": None,
            }

        def ease(self, easing: CameraEasing, easing_time: float):
            self.argument["easing_time"] = easing_time
            self.argument["easing"] = easing
            return self

        def position(self, position: Coordinates):
            self.argument["position"] = position
            return self

        def rotation(self, xrotation: float, yrotation: float):
            self.argument["rotation"] = (xrotation, yrotation)
            return self

        def facing_target(self, target: Selector | Target):
            self.argument["facing_target"] = target
            return self

        def facing_position(self, position: Coordinates):
            self.argument["facing_position"] = position
            return self

        def __str__(self):
            rotation = self.argument["rotation"]
            facing_target = self.argument["facing_target"]
            facing_position = self.argument["facing_position"]

            if (
                sum([x is not None for x in (facing_target, facing_position, rotation)])
                > 1
            ):
                raise ValueError(
                    f"Only one of 'facing_target', 'facing_position', or 'rotation' can be set at a time. Found {sum([x is not None for x in (facing_target, facing_position, rotation)])} set."
                )

            if self.argument["easing"] != None:
                self._append_cmd(
                    "ease", self.argument["easing_time"], self.argument["easing"]
                )

            if self.argument["position"] != None:
                self._append_cmd("pos", *self.argument["position"])

            if self.argument["rotation"] != None:
                self._append_cmd("rot", *self.argument["rotation"])

            if self.argument["facing_target"] != None:
                self._append_cmd("facing", self.argument["facing_target"])

            if self.argument["facing_position"] != None:
                self._append_cmd("facing", *self.argument["facing_position"])

            return super().__str__()

    class _CameraClear(Command):
        def __init__(self, target) -> None:
            super().__init__("camera", target, "clear")

    class _CameraFade(Command):
        def __init__(self, target) -> None:
            super().__init__("camera", target, "fade")

            self.argument = {
                "fade_in_time": None,
                "hold_time": None,
                "fade_out_time": None,
                "color": None,
            }

        def time(
            self, fade_in_time: Seconds, hold_time: Seconds, fade_out_time: Seconds
        ):
            self.argument["fade_in_time"] = fade_in_time
            self.argument["hold_time"] = hold_time
            self.argument["fade_out_time"] = fade_out_time
            return self

        def color(self, color: Color):
            self.argument["color"] = color
            return self

        def __str__(self):
            if self.argument["fade_in_time"] != None:
                self._append_cmd(
                    self.argument["fade_in_time"],
                    self.argument["hold_time"],
                    self.argument["fade_out_time"],
                )

            if self.argument["color"] != None:
                self._append_cmd(self.argument["color"])

            return super().__str__()

    def __init__(self, target: Target | Selector) -> None:
        """Transforms the camera for the selected player to a different perspective."""
        self._target = target

    def set(self, preset: CameraPresets):
        return self._CameraSet(self._target, preset)

    @property
    def clear(self):
        return self._CameraClear(self._target)

    @property
    def fade(self):
        return self._CameraFade(self._target)


class Time(Command):
    def __init__(self) -> None:
        """Changes the world's game time.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/commands/commands/time
        """
        super().__init__("time")

    def add(self, amount: int):
        """Add an integer amount of time in-game.

        Parameters:
            amount (int): The amount of time to add.
        """
        self._append_cmd("add", amount)
        return self

    def set(self, amount: TimeSpec | int):
        """Set the time in-game.

        Parameters:
            amount (TimeSpec | int): The time to set.
        """
        self._append_cmd("set", amount)
        return self


class Stopsound(Command):
    def __init__(self, target: Target, sound: str = "") -> None:
        """Stop a sound for a player with an optional sound string .

        Parameters:
            target (Target): A player name string or Target to identify the player.
            sound (str, optional): A string from the sound enum of the sound to stop. Defaults to "".

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/commands/commands/stopsound
        """
        super().__init__("stopsound", target)

        if not sound == "":
            self._append_cmd(f'"{sound}"')


class Hud(Command):
    def __init__(
        self,
        target: Selector | Target,
        visible: HudVisibility = HudVisibility.Reset,
        hud_element: HudElement = HudElement.All,
    ):
        """Changes the visibility of HUD elements for a player.

        Parameters:
            target (Selector | Target): The player to change the HUD visibility for.
            visible (HudVisibility, optional): The visibility state to set. Defaults to HudVisibility.Reset.
            hud_element (HudElement, optional): The HUD element to change the visibility of. Defaults to HudElement.All.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/commands/commands/hud
        """

        super().__init__("hud", target, visible, hud_element)
        return self
