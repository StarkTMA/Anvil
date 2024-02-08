import json
from enum import StrEnum

from anvil.api.types import Identifier, coordinate, coordinates
from anvil.lib.lib import clamp, normalize_180


class Target(StrEnum):
    """
    Enumeration for the types of targets that can be selected in Minecraft.
    """

    P = "@p"
    R = "@r"
    A = "@a"
    E = "@e"
    S = "@s"
    C = "@c"
    V = "@v"
    Initiator = "@initiator"


class Style(StrEnum):
    """
    Enumeration for the different styles of text in the game.
    """

    Black: str = "§0"
    DarkBlue: str = "§1"
    DarkGreen: str = "§2"
    DarkAqua: str = "§3"
    DarkRed: str = "§4"
    DarkPurple: str = "§5"
    Gold: str = "§6"
    Gray: str = "§7"
    DarkGray: str = "§8"
    Blue: str = "§9"
    Green: str = "§a"
    Aqua: str = "§b"
    Red: str = "§c"
    Purple: str = "§d"
    Yellow: str = "§e"
    White: str = "§f"
    MineconGold: str = "§g"
    Obfuscated: str = "§k"
    Bold: str = "§l"
    Italic: str = "§o"
    Reset: str = "§r"


class FogCameraLocation(StrEnum):
    """
    Enumeration for the different locations of the fog camera in the game.
    """

    Air = "air"
    Lava = "lava"
    Lava_resistance = "lava_resistance"
    Powder_snow = "powder_snow"
    Water = "water"
    Weather = "weather"


class RenderDistanceType(StrEnum):
    """
    Enumeration for the different types of render distances in the game.
    """

    Render = "render"
    Fixed = "fixed"


class LootPoolType(StrEnum):
    """
    Enumeration for the different types of loot pools.
    """

    Empty = "empty"
    Item = "item"
    LootTable = "loot_table"


class Slots(StrEnum):
    """
    Enumeration for the different types of inventory slots in the game.
    """

    Mainhand = "slot.weapon.mainhand"
    Offhand = "slot.weapon.offhand"
    Head = "slot.armor.head"
    Chest = "slot.armor.chest"
    Legs = "slot.armor.legs"
    Feet = "slot.armor.feet"
    Hotbar = "slot.hotbar"
    Inventory = "slot.inventory"
    Enderchest = "slot.enderchest"
    Saddle = "slot.saddle"
    Armor = "slot.armor"
    EquippedChest = "slot.chest"
    Equippable = "slot.equippable"
    Container = "slots.container"


class Gamemodes(StrEnum):
    """
    Enumeration for the different types of game modes.
    """

    Adventure = "adventure"
    Creative = "creative"
    Default = "default"
    Survival = "survival"
    Spectator = "spectator"

    A = Adventure
    C = Creative
    D = Default
    S = Survival


class ScoreboardOperator(StrEnum):
    """
    Enumeration for the different types of mathematical operators.
    """

    Less = "<"
    LessEqual = "<="
    Equals = "="
    Greater = ">"
    GreaterEqual = ">="


class Dimension(StrEnum):
    """
    Enumeration for the different dimensions in the game.
    """

    Overworld = "overworld"
    Nether = "nether"
    End = "the_end"


class FillMode(StrEnum):
    Replace = "replace"
    Outline = "outline"
    Hollow = "hollow"
    Destroy = "destroy"
    Keep = "keep"


class MusicRepeatMode(StrEnum):
    Once = "play_once"
    Loop = "loop"


class Difficulty(StrEnum):
    """
    Enumeration for the different levels of game difficulty.
    """

    Peaceful = "peaceful"
    Easy = "easy"
    Normal = "normal"
    Hard = "hard"


class DamageCause(StrEnum):
    """
    Enumeration for the different causes of damage in the game.
    """

    All = "all"
    Anvil = "anvil"
    EntityAttack = "entity_attack"
    Block_explosion = "block_explosion"
    Contact = "contact"
    Drowning = "drowning"
    Entity_explosion = "entity_explosion"
    Fall = "fall"
    Falling_block = "falling_block"
    Fatal = "fatal"
    Fire = "fire"
    Firetick = "firetick"
    Fly_into_wall = "fly_into_wall"
    Lava = "lava"
    Magic = "magic"
    Nothing = "none"
    Override = "override"
    Piston = "piston"
    Projectile = "projectile"
    Sonic_boom = "sonic_boom"
    Stalactite = "stalactite"
    Stalagmite = "stalagmite"
    Starve = "starve"
    Suffocation = "suffocation"
    Suicide = "suicide"
    Thorns = "thorns"
    Void = "void"
    Wither = "wither"


class Effects(StrEnum):
    """
    Enumeration for the different types of effects in the game.
    """

    Hunger = "hunger"
    JumpBoost = "jump"
    Saturation = "saturation"
    Regeneration = "regeneration"
    Speed = "speed"
    Strength = "strength"
    Slowness = "slowness"
    Weakness = "weakness"
    Levitation = "levitation"
    Wither = "wither"
    Poison = "poison"
    Absorption = "absorption"
    Invisibility = "invisibility"
    SlowFalling = "slow_falling"
    Nausea = "nausea"


class ScoreboardOperation(StrEnum):
    """
    Enumeration for the different operations that can be performed on a scoreboard.
    """

    Addition = "+="
    Subtraction = "-="
    Multiplication = "*="
    Division = "/="
    Modulus = "%="
    Assign = "="
    Min = "<"
    Max = ">"
    Swaps = "><"


class Anchor(StrEnum):
    """
    Enumeration representing the two anchor points that can be used in Minecraft: the feet and the eyes.
    """

    Feet = "feet"
    Eyes = "eyes"


class CameraShakeType(StrEnum):
    """
    Enumeration representing the types of camera shakes that can occur in Minecraft.
    """

    positional = "positional"
    rotational = "rotational"


class MaskMode(StrEnum):
    """
    Enumeration representing the different mask modes that can be applied in Minecraft.
    """

    replace = "replace"
    masked = "masked"


class CloneMode(StrEnum):
    """
    Enumeration representing the different modes that can be used when cloning in Minecraft.
    """

    force = "force"
    move = "move"
    normal = "normal"


class InputPermissions(StrEnum):
    """
    Enumeration representing the different input permissions that can be set for a player in Minecraft.
    """

    Camera = "camera"
    Movement = "movement"


class CameraPresets(StrEnum):
    FirstPerson = "minecraft:first_person"
    ThirdPerson = "minecraft:third_person"
    ThirdPersonFront = "minecraft:third_person_front"
    Free = "minecraft:free"


class CameraEasing(StrEnum):
    Linear = "linear"
    Spring = "spring"
    InQuad = "in_quad"
    OutQuad = "out_quad"
    InOutQuad = "in_out_quad"
    InCubic = "in_cubic"
    OutCubic = "out_cubic"
    InOutCubic = "in_out_cubic"
    InQuart = "in_quart"
    OutQuart = "out_quart"
    InOutQuart = "in_out_quart"
    InQuint = "in_quint"
    OutQuint = "out_quint"
    InOutQuint = "in_out_quint"
    InSine = "in_sine"
    OutSine = "out_sine"
    InOutSine = "in_out_sine"
    InExpo = "in_expo"
    OutExpo = "out_expo"
    InOutExpo = "in_out_expo"
    InCirc = "in_circ"
    OutCirc = "out_circ"
    InOutCirc = "in_out_circ"
    InBounce = "in_bounce"
    OutBounce = "out_bounce"
    InOutBounce = "in_out_bounce"
    InBack = "in_back"
    OutBack = "out_back"
    InOutBack = "in_out_back"
    InElastic = "in_elastic"
    OutElastic = "out_elastic"
    InOutElastic = "in_out_elastic"


class TimeSpec(StrEnum):
    DAY = "day"
    SUNRISE = "sunrise"
    NOON = "noon"
    SUNSET = "sunset"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class Selector:
    """
    A class used to construct a target selector for Minecraft commands. The class offers various methods to set target
    parameters such as its type, name, count, coordinates, distance, volume, scores, rotation, permissions, and gamemode.
    """

    def __init__(self, target: Target = Target.S) -> None:
        """
        Initializes a Selector object.

        Args:
            target (Target, optional): The target type. Defaults to Target.S (self).
        """
        self.target = target
        self.arguments = []

    def _args(self, **args):
        for key, value in args.items():
            if not value is None and {key: value} not in self.arguments:
                self.arguments.append({key: value})
        return self

    def type(self, *types: str | Identifier):
        """Sets the type of the target."""
        for type in types:
            self._args(type=type)
        return self

    def name(self, name: str):
        """Sets the name of the target.

        Args:
            name (str): The name of the target.

        """
        self._args(name=f'"{name}"')
        return self

    def family(self, family: str):
        """Sets the family of the target.

        Args:
            family (str): The family of the target.

        """
        self._args(family=family)
        return self

    def count(self, count: int):
        """Sets the count of the target.

        Args:
            count (int): The number of targets to select.

        """
        self._args(c=count)
        return self

    def coordinates(self, *, x: coordinate = None, y: coordinate = None, z: coordinate = None):
        """Sets the coordinates of the target.

        Args:
            x (coordinate, optional): The x coordinate. Defaults to None.
            y (coordinate, optional): The y coordinate. Defaults to None.
            z (coordinate, optional): The z coordinate. Defaults to None.

        """
        self._args(x=x, y=y, z=z)
        return self

    def distance(self, *, r: coordinate = None, rm: coordinate = None):
        """Sets the distance of the target.

        Args:
            r (coordinate, optional): The maximum distance. Defaults to None.
            rm (coordinate, optional): The minimum distance. Defaults to None.

        """
        self._args(r=r, rm=rm)
        return self

    def volume(self, *, dx: float = None, dy: float = None, dz: float = None):
        """Sets the volume of the target.

        Args:
            dx (float, optional): The x volume. Defaults to None.
            dy (float, optional): The y volume. Defaults to None.
            dz (float, optional): The z volume. Defaults to None.

        """
        self._args(dx=dx, dy=dy, dz=dz)
        return self

    def scores(self, **scores):
        """Sets the scores of the target.

        Example:
            >>> selector.scores(score1=1, score2=2, score3=3)
        """
        score_values = {}
        for score, value in scores.items():
            score_values.update({score: value})
        self._args(scores=score_values)
        return self

    def tag(self, *tags: str):
        """Sets the tags of the target.

        Example:
            >>> selector.tag("tag1", "!tag2")
        """
        for tag in tags:
            self._args(tag=tag)
        return self

    def rotation(
        self,
        *,
        ry: float = None,
        rym: float = None,
        rx: float = None,
        rxm: float = None,
    ):
        """Sets the rotation of the target.

        Args:
            ry (float, optional): The maximum yaw. Defaults to None.
            rym (float, optional): The minimum yaw. Defaults to None.
            rx (float, optional): The maximum pitch. Defaults to None.
            rxm (float, optional): The minimum pitch. Defaults to None.

        """
        self._args(
            ry=normalize_180(round(ry, 2)) if not ry is None else ry,
            rym=normalize_180(round(rym, 2)) if not rym is None else rym,
            rx=clamp(round(rx, 2), -90, 90) if not rx is None else rx,
            rxm=clamp(round(rxm, 2), -90, 90) if not rxm is None else rxm,
        )
        return self

    def has_permission(self, *, camera: bool = None, movement: bool = None):
        """Selects targets that have the specified permissions.

        Args:
            camera (bool, optional): Defaults to None.
            movement (bool, optional): Defaults to None.

        """
        permission = {}
        if not camera is None:
            permission.update({"camera": "enabled" if camera else "disabled"})
        if not movement is None:
            permission.update({"movement": "enabled" if movement else "disabled"})

        self._args(haspermission=permission)
        return self

    def has_item(
        self,
        *,
        item: str | Identifier,
        data: int = -1,
        quantity: int = None,
        location: Slots = None,
        slot: int = None,
    ):
        """Selects targets that have the specified item.

        Args:
            item (str | Identifier): The item to check for.
            data (int, optional): The data value of the item. Defaults to -1.
            quantity (int, optional): The quantity of the item. Defaults to None.
            location (Slots, optional): The location of the item. Defaults to None.
            slot (int, optional): The slot of the item. Defaults to None.

        """
        test_item = {
            "item": item,
            "data": data if data != -1 else None,
            "quantity": quantity,
            "location": location,
            "slot": slot,
        }
        self._args(hasitem=test_item)
        return self

    def gamemode(self, gamemode: Gamemodes):
        """Selects targets that have the specified gamemode.

        Args:
            gamemode (Gamemodes): The gamemode to check for.

        """
        self._args(m=gamemode)
        return self

    def __str__(self) -> str:
        """Returns the target selector as a string."""
        if len(self.arguments) > 0:
            args = []
            for i in self.arguments:
                for key, value in i.items():
                    values = value
                    if type(value) is dict:
                        values = f"{{{', '.join(f'{k} = {v}' for k, v in value.items() if not v is None)}}}"
                    args.append(f"{key} = {values}")

            self.target = f"{self.target} [{', '.join(args)}]"
        return self.target


class RawTextConstructor:
    """
    A class that constructs raw text with various possible styling and structures.

    Attributes:
        _raw_text (list): The raw text being constructed, stored as a list of dictionaries representing different parts.
    """

    def __init__(self):
        """Initializes a new RawTextConstructor instance."""
        self._raw_text = []

    def style(self, *styles: Style):
        """
        Applies the provided styles to the raw text.

        Args:
            styles (Style): The styles to be applied.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": "".join(map(lambda a: a.value, styles))})
        return self

    def text(self, text):
        """
        Appends the given text to the raw text.

        Args:
            text (str): The text to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": str(text)})
        return self

    def translate(self, text):
        """
        Localizes the given text and appends it to the raw text.

        Args:
            text (str): The text to be localized and appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        from anvil import ANVIL
        self.id = ANVIL.definitions.get_new_lang
        ANVIL.definitions.register_lang(self.id, text)
        self._raw_text.append({"translate": self.id, "with": ["\n"]})
        return self

    def score(self, objective, target: Selector | Target | str):
        """
        Appends the score of the given target under the given objective to the raw text.

        Args:
            objective (str): The objective under which the target's score is tracked.
            target (Selector | Target | str): The target whose score is to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        t = target.value if isinstance(target, Target) else target

        self._raw_text.append({"score": {"name": t, "objective": objective}})
        return self

    def selector(self, target: Selector | Target | str):
        """
        Appends the selector of the given target to the raw text.

        Args:
            target (Selector | Target | str): The target whose selector is to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        t = target.value if isinstance(target, Target) else target

        self._raw_text.append({"selector": t})
        return self

    def __str__(self) -> str:
        """
        Converts the RawTextConstructor instance to a string.

        Returns:
            str: A string representation of the raw text.
        """
        return f'{{"rawtext":{json.dumps(self._raw_text, ensure_ascii=False)}}}'


class Population(StrEnum):
    """
    Enumeration for the different types of in-game populations.
    """

    Animal = "animal"
    UnderwaterAnimal = "underwater_animal"
    Monster = "monster"
    Ambient = "ambient"


class PlacementDirectionTrait(StrEnum):
    CardinalDirection = "minecraft:cardinal_direction"  # North, South, East, West
    FacingDirection = "minecraft:facing_direction"  # Up, Down, North, South, East, West


class PlacementPositionTrait(StrEnum):
    BlockFace = "minecraft:block_face"  # Up, Down, North, South, East, West
    VerticalHalf = "minecraft:vertical_half"  # Top, Bottom


class CardinalDirectionsTrait(StrEnum):
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class FacingDirectionsTrait(StrEnum):
    Up = "up"
    Down = "down"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class BlockFacesTrait(StrEnum):
    Up = "up"
    Down = "down"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class VerticalHalfTrait(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"


class BlockFaces(StrEnum):
    """
    Enumeration representing the different faces of a block in Minecraft.
    """

    Up = "up"
    Down = "down"
    North = "north"
    South = "south"
    East = "east"
    West = "west"
    Side = "side"
    All = "all"


class BlockMaterial(StrEnum):
    """
    Enumeration representing the different types of rendering methods a block can use in Minecraft.
    """

    Opaque = "opaque"
    DoubleSided = "double_sided"
    Blend = "blend"
    AlphaTest = "alpha_test"


class BlockCategory(StrEnum):
    """
    Enumeration representing the categories of blocks that can be used in Minecraft.
    """

    Construction = "construction"
    Nature = "nature"
    Equipment = "equipment"
    Items = "items"
    none = "none"


class WeatherSet(StrEnum):
    """
    Enumeration representing the different types of weather that can be set in Minecraft.
    """

    Clear = "clear"
    Rain = "rain"
    Thunder = "thunder"


class FilterSubject(StrEnum):
    """
    Enumeration representing the different subjects that can be used in filters in Minecraft.
    """

    Block = "block"
    Damager = "damager"
    Other = "other"
    Parent = "parent"
    Player = "player"
    Self = "self"
    Target = "target"


class FilterOperation(StrEnum):
    """
    Enumeration representing the different operations that can be used in filters in Minecraft.
    """

    Less = "<"
    LessEqual = "<="
    Greater = ">"
    GreaterEqual = ">="
    Equals = "equals"
    Not = "not"


class FilterEquipmentDomain(StrEnum):
    """
    Enumeration representing the different equipment domains that can be used in filters in Minecraft.
    """

    Any = "any"
    Armor = "armor"
    Feet = "feet"
    Hand = "hand"
    Head = "head"
    Inventory = "inventory"
    Leg = "leg"
    Torso = "torso"


class Biomes(StrEnum):
    BEACH = "beach"
    DESERT = "desert"
    EXTREME_HILLS = "extreme_hills"
    FLAT = "flat"
    FOREST = "forest"
    ICE = "ice"
    JUNGLE = "jungle"
    MESA = "mesa"
    MUSHROOM_ISLAND = "mushroom_island"
    OCEAN = "ocean"
    PLAIN = "plain"
    RIVER = "river"
    SAVANNA = "savanna"
    STONE_BEACH = "stone_beach"
    SWAMP = "swamp"
    TAIGA = "taiga"
    THE_END = "the_end"
    THE_NETHER = "the_nether"


class Vibrations(StrEnum):
    EntityInteract = "entity_interact"
    EntityAct = "entity_act"
    Shear = "shear"
    none = "none"


class ControlFlags(StrEnum):
    Move = "move"
    Look = "look"


class MaterialStates(StrEnum):
    """
    Enumeration representing the different states a material can be in Minecraft.
    """

    EnableStencilTest = "EnableStencilTest"
    StencilWrite = "StencilWrite"
    InvertCulling = "InvertCulling"
    DisableCulling = "DisableCulling"
    DisableDepthWrite = "DisableDepthWrite"
    Blending = "Blending"


class MaterialDefinitions(StrEnum):
    """
    Enumeration representing the different definitions that can be set for a material in Minecraft.
    """

    Fancy = "FANCY"
    USE_OVERLAY = "USE_OVERLAY"
    USE_COLOR_MASK = "USE_COLOR_MASK"
    MULTI_COLOR_TINT = "MULTI_COLOR_TINT"
    COLOR_BASED = "COLOR_BASED"
    USE_UV_ANIM = "USE_UV_ANIM"
    TINTED = "TINTED"
    USE_COLOR_BLEND = "USE_COLOR_BLEND"
    MULTIPLICATIVE_TINT = "MULTIPLICATIVE_TINT"
    MULTIPLICATIVE_TINT_COLOR = "MULTIPLICATIVE_TINT_COLOR"


class MaterialFunc(StrEnum):
    """
    Enumeration representing the different functions that can be set for a material in Minecraft.
    """

    Always = "Always"
    Equal = "Equal"
    NotEqual = "NotEqual"
    Less = "Less"
    Greater = "Greater"
    GreaterEqual = "GreaterEqual"
    LessEqual = "LessEqual"


class MaterialOperation(StrEnum):
    """
    Enumeration representing the different operations that can be set for a material in Minecraft.
    """

    Keep = "Keep"
    Replace = "Replace"


class SoundCategory(StrEnum):
    """
    Enumeration for the different categories of sounds in the game.
    """

    Ambient = "ambient"
    Block = "block"
    Player = "player"
    Neutral = "neutral"
    Hostile = "hostile"
    Music = "music"
    Record = "record"
    UI = "ui"


class EntitySoundEvent(StrEnum):
    Ambient = "ambient"
    Hurt = "hurt"
    Death = "death"
    Takeoff = "takeoff"
    AmbientTame = "ambient.tame"
    Purr = "purr"
    Purreow = "purreow"
    Eat = "eat"
    Step = "step"
    Plop = "plop"
    Fuse = "fuse"
    Breathe = "breathe"
    Attack = "attack"
    Splash = "splash"
    Swim = "swim"
    AmbientInWater = "ambient.in.water"
    HurtInWater = "hurt.in.water"
    DeathInWater = "death.in.water"
    Jump = "jump"
    Mad = "mad"
    Stare = "stare"
    Flap = "flap"
    Fizz = "fizz"
    Sniff = "sniff"
    Screech = "screech"
    Sleep = "sleep"
    Spit = "spit"
    Scream = "scream"
    Warn = "warn"
    Shoot = "shoot"
    GuardianFlop = "guardian.flop"
    Flop = "flop"
    CastSpell = "cast.spell"
    PrepareAttack = "prepare.attack"
    PrepareSummon = "prepare.summon"
    PrepareWololo = "prepare.wololo"
    AmbientInRaid = "ambient.in.raid"
    Celebrate = "celebrate"
    Fang = "fang"
    Charge = "charge"
    Armor = "armor"
    AddChest = "add.chest"
    Saddle = "saddle"
    Land = "land"
    Throw = "throw"
    AttackStrong = "attack.strong"
    Roar = "roar"
    Stun = "stun"
    Thunder = "thunder"
    Explode = "explode"
    Fly = "fly"
    ImitateBlaze = "imitate.blaze"
    ImitateCaveSpider = "imitate.cave_spider"
    ImitateCreeper = "imitate.creeper"
    ImitateElderGuardian = "imitate.elder_guardian"
    ImitateEnderDragon = "imitate.ender_dragon"
    ImitateEnderman = "imitate.enderman"
    ImitateEndermite = "imitate.endermite"
    ImitateEvocationIllager = "imitate.evocation_illager"
    ImitateGhast = "imitate.ghast"
    ImitateHusk = "imitate.husk"
    ImitateIllusionIllager = "imitate.illusion_illager"
    ImitateMagmaCube = "imitate.magma_cube"
    ImitatePolarBear = "imitate.polar_bear"
    ImitatePanda = "imitate.panda"
    ImitateShulker = "imitate.shulker"
    ImitateSilverfish = "imitate.silverfish"
    ImitateSkeleton = "imitate.skeleton"
    ImitateSlime = "imitate.slime"
    ImitateSpider = "imitate.spider"
    ImitateStray = "imitate.stray"
    ImitateVex = "imitate.vex"
    ImitateVindicationIllager = "imitate.vindication_illager"
    ImitateWitch = "imitate.witch"
    ImitateWither = "imitate.wither"
    ImitateWitherSkeleton = "imitate.wither_skeleton"
    ImitateWolf = "imitate.wolf"
    ImitateZombie = "imitate.zombie"
    ImitateDrowned = "imitate.drowned"
    ImitateZombiePigman = "imitate.zombie_pigman"
    ImitateZombieVillager = "imitate.zombie_villager"
    Swoop = "swoop"
    Boost = "boost"
    DeathToZombie = "death.to.zombie"
    AttackNodamage = "attack.nodamage"
    ElderguardianCurse = "elderguardian.curse"
    AmbientBaby = "ambient.baby"
    MobWarning = "mob.warning"
    AmbientAggressive = "ambient.aggressive"
    AmbientWorried = "ambient.worried"
    Presneeze = "presneeze"
    Sneeze = "sneeze"
    CantBreed = "cant_breed"
    ShulkerOpen = "shulker.open"
    ShulkerClose = "shulker.close"
    HurtBaby = "hurt.baby"
    DeathBaby = "death.baby"
    StepBaby = "step.baby"
    Born = "born"
    SquishBig = "squish.big"
    SquishSmall = "squish.small"
    Haggle = "haggle"
    HaggleYes = "haggle.yes"
    HaggleNo = "haggle.no"
    Disappeared = "disappeared"
    Drink = "drink"
    Reappeared = "reappeared"
    DeathMinVolume = "death.min.volume"
    DeathMidVolume = "death.mid.volume"
    Spawn = "spawn"
    BreakBlock = "break.block"
    Shake = "shake"
    Growl = "growl"
    Whine = "whine"
    Pant = "pant"


class MusicCategory(StrEnum):
    """
    Enumeration for the different categories of music in the game.
    """

    Creative = "creative"
    Credits = "credits"
    Crimson_forest = "crimson_forest"
    Dripstone_caves = "dripstone_caves"
    End = "end"
    Endboss = "endboss"
    Frozen_peaks = "frozen_peaks"
    Game = "game"
    Grove = "grove"
    Hell = "hell"
    Jagged_peaks = "jagged_peaks"
    Lush_caves = "lush_caves"
    Meadow = "meadow"
    Menu = "menu"
    Nether = "nether"
    Snowy_slopes = "snowy_slopes"
    Soulsand_valley = "soulsand_valley"
    Stony_peaks = "stony_peaks"
    Water = "water"
