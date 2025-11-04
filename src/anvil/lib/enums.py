import json
from enum import StrEnum

from anvil.lib.lib import clamp, normalize_180
from anvil.lib.translator import AnvilTranslator
from anvil.lib.types import Coordinate, Identifier


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
    N = "@n"


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
    Body = "slot.armor.body"


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

    Nether = "minecraft:nether"
    Overworld = "minecraft:overworld"
    TheEnd = "minecraft:the_end"


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
    Hardcore = "hardcore"


class DamageCause(StrEnum):
    """
    Enumeration for the different causes of damage in the game.
    """

    All = "all"
    Anvil = "anvil"
    EntityAttack = "entity_attack"
    BlockExplosion = "block_explosion"
    Contact = "contact"
    Drowning = "drowning"
    EntityExplosion = "entity_explosion"
    Fall = "fall"
    FallingBlock = "falling_block"
    Fatal = "fatal"
    Fire = "fire"
    Firetick = "firetick"
    FlyIntoWall = "fly_into_wall"
    Lava = "lava"
    Magic = "magic"
    Nothing = "none"
    Override = "override"
    Piston = "piston"
    Projectile = "projectile"
    SonicBoom = "sonic_boom"
    Stalactite = "stalactite"
    Stalagmite = "stalagmite"
    Starve = "starve"
    Suffocation = "suffocation"
    SelfDestruct = "self_destruct"
    Thorns = "thorns"
    Void = "void"
    Wither = "wither"


class Effects(StrEnum):
    """
    Enumeration for the different types of effects in the game.
    """

    Absorption = "minecraft:absorption"
    BadOmen = "minecraft:bad_omen"
    Blindness = "minecraft:blindness"
    ConduitPower = "minecraft:conduit_power"
    Darkness = "minecraft:darkness"
    FatalPoison = "minecraft:fatal_poison"
    FireResistance = "minecraft:fire_resistance"
    Haste = "minecraft:haste"
    HealthBoost = "minecraft:health_boost"
    Hunger = "minecraft:hunger"
    Infested = "minecraft:infested"
    InstantDamage = "minecraft:instant_damage"
    InstantHealth = "minecraft:instant_health"
    Invisibility = "minecraft:invisibility"
    JumpBoost = "minecraft:jump_boost"
    Levitation = "minecraft:levitation"
    MiningFatigue = "minecraft:mining_fatigue"
    Nausea = "minecraft:nausea"
    NightVision = "minecraft:night_vision"
    Oozing = "minecraft:oozing"
    Poison = "minecraft:poison"
    RaidOmen = "minecraft:raid_omen"
    Regeneration = "minecraft:regeneration"
    Resistance = "minecraft:resistance"
    Saturation = "minecraft:saturation"
    SlowFalling = "minecraft:slow_falling"
    Slowness = "minecraft:slowness"
    Speed = "minecraft:speed"
    Strength = "minecraft:strength"
    TrialOmen = "minecraft:trial_omen"
    VillageHero = "minecraft:village_hero"
    WaterBreathing = "minecraft:water_breathing"
    Weakness = "minecraft:weakness"
    Weaving = "minecraft:weaving"
    WindCharged = "minecraft:wind_charged"
    Wither = "minecraft:wither"


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
    ControlSchemeCamera = "minecraft:control_scheme_camera"
    FirstPerson = "minecraft:first_person"
    FixedBoom = "minecraft:fixed_boom"
    FollowOrbit = "minecraft:follow_orbit"
    Free = "minecraft:free"
    ThirdPerson = "minecraft:third_person"
    ThirdPersonFront = "minecraft:third_person_front"


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

        Parameters:
            target (Target, optional): The target type. Defaults to Target.S (self).
        """
        self.target = target
        self.arguments = []

    def _Parameters(self, **Parameters):
        for key, value in Parameters.items():
            if not value is None and {key: value} not in self.arguments:
                self.arguments.append({key: value})
        return self

    def type(self, *types: str | Identifier):
        """Sets the type of the target."""
        for type in types:
            self._Parameters(type=type)
        return self

    def name(self, name: str):
        """Sets the name of the target.

        Parameters:
            name (str): The name of the target.

        """
        self._Parameters(name=f'"{name}"')
        return self

    def family(self, family: str):
        """Sets the family of the target.

        Parameters:
            family (str): The family of the target.

        """
        self._Parameters(family=family)
        return self

    def count(self, count: int):
        """Sets the count of the target.

        Parameters:
            count (int): The number of targets to select.

        """
        self._Parameters(c=count)
        return self

    def coordinates(
        self, *, x: Coordinate = None, y: Coordinate = None, z: Coordinate = None
    ):
        """Sets the coordinates of the target.

        Parameters:
            x (Coordinate, optional): The x Coordinate. Defaults to None.
            y (Coordinate, optional): The y Coordinate. Defaults to None.
            z (Coordinate, optional): The z Coordinate. Defaults to None.

        """
        self._Parameters(x=x, y=y, z=z)
        return self

    def distance(self, *, r: Coordinate = None, rm: Coordinate = None):
        """Sets the distance of the target.

        Parameters:
            r (Coordinate, optional): The maximum distance. Defaults to None.
            rm (Coordinate, optional): The minimum distance. Defaults to None.

        """
        self._Parameters(r=r, rm=rm)
        return self

    def volume(self, *, dx: float = None, dy: float = None, dz: float = None):
        """Sets the volume of the target.

        Parameters:
            dx (float, optional): The x volume. Defaults to None.
            dy (float, optional): The y volume. Defaults to None.
            dz (float, optional): The z volume. Defaults to None.

        """
        self._Parameters(dx=dx, dy=dy, dz=dz)
        return self

    def scores(self, **scores):
        """Sets the scores of the target.

        Example:
            >>> selector.scores(score1=1, score2=2, score3=3)
        """
        score_values = {}
        for score, value in scores.items():
            score_values.update({score: value})
        self._Parameters(scores=score_values)
        return self

    def tag(self, *tags: str):
        """Sets the tags of the target.

        Example:
            >>> selector.tag("tag1", "!tag2")
        """
        for tag in tags:
            self._Parameters(tag=tag)
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

        Parameters:
            ry (float, optional): The maximum yaw. Defaults to None.
            rym (float, optional): The minimum yaw. Defaults to None.
            rx (float, optional): The maximum pitch. Defaults to None.
            rxm (float, optional): The minimum pitch. Defaults to None.

        """
        self._Parameters(
            ry=normalize_180(round(ry, 2)) if not ry is None else ry,
            rym=normalize_180(round(rym, 2)) if not rym is None else rym,
            rx=clamp(round(rx, 2), -90, 90) if not rx is None else rx,
            rxm=clamp(round(rxm, 2), -90, 90) if not rxm is None else rxm,
        )
        return self

    def has_permission(self, *, camera: bool = None, movement: bool = None):
        """Selects targets that have the specified permissions.

        Parameters:
            camera (bool, optional): Defaults to None.
            movement (bool, optional): Defaults to None.

        """
        permission = {}
        if not camera is None:
            permission.update({"camera": "enabled" if camera else "disabled"})
        if not movement is None:
            permission.update({"movement": "enabled" if movement else "disabled"})

        self._Parameters(haspermission=permission)
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

        Parameters:
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
        self._Parameters(hasitem=test_item)
        return self

    def gamemode(self, gamemode: Gamemodes):
        """Selects targets that have the specified gamemode.

        Parameters:
            gamemode (Gamemodes): The gamemode to check for.

        """
        self._Parameters(m=gamemode)
        return self

    def has_property(self, **properties):
        """Selects targets that have the specified property.

        Parameters:
            property (str): The property to check for.
            value (str): The value of the property.

        """
        from anvil import ANVIL

        property_values = {}
        for property, value in properties.items():
            property_values.update(
                {f"{ANVIL.config.NAMESPACE}:{property}": json.dumps(value)}
            )
        self._Parameters(has_property=property_values)
        return self

    def __str__(self) -> str:
        """Returns the target selector as a string."""
        if len(self.arguments) > 0:
            Parameters = []
            for i in self.arguments:
                for key, value in i.items():
                    values = value
                    if type(value) is dict:
                        values = f"{{{', '.join(f'{k} = {v}' for k, v in value.items() if not v is None)}}}"
                    Parameters.append(f"{key} = {values}")

            self.target = f"{self.target} [{', '.join(Parameters)}]"
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

        Parameters:
            styles (Style): The styles to be applied.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": "".join(map(lambda a: a.value, styles))})
        return self

    def text(self, text):
        """
        Appends the given text to the raw text.

        Parameters:
            text (str): The text to be appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        self._raw_text.append({"text": str(text)})
        return self

    def translate(self, key: str, text: str):
        """
        Localizes the given text and appends it to the raw text.

        Parameters:
            text (str): The text to be localized and appended.

        Returns:
            self: The instance of the current RawTextConstructor.
        """
        AnvilTranslator().add_localization_entry(key, text)
        self._raw_text.append({"translate": key, "with": ["\n"]})
        return self

    def score(self, objective, target: Selector | Target | str):
        """
        Appends the score of the given target under the given objective to the raw text.

        Parameters:
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

        Parameters:
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
    AlphaTestSingleSided = "alpha_test_single_sided"
    BlendToOpaque = "blend_to_opaque"
    AlphaTestToOpaque = "alpha_test_to_opaque"
    AlphaTestSingleSidedToOpaque = "alpha_test_single_sided_to_opaque"


class ItemCategory(StrEnum):
    """
    Enumeration representing the categories of blocks and items that can be used in Minecraft.
    """

    Construction = "construction"
    Equipment = "equipment"
    Items = "items"
    Nature = "nature"
    none = "none"


class ItemGroups(StrEnum):
    Anvil = "itemGroup.name.anvil"
    Arrow = "itemGroup.name.arrow"
    Axe = "itemGroup.name.axe"
    Banner = "itemGroup.name.banner"
    BannerPattern = "itemGroup.name.banner_pattern"
    Bed = "itemGroup.name.bed"
    Boat = "itemGroup.name.boat"
    Boots = "itemGroup.name.boots"
    Buttons = "itemGroup.name.buttons"
    Candles = "itemGroup.name.candles"
    Chalkboard = "itemGroup.name.chalkboard"
    Chest = "itemGroup.name.chest"
    ChestBoat = "itemGroup.name.chestboat"
    Chestplate = "itemGroup.name.chestplate"
    Concrete = "itemGroup.name.concrete"
    ConcretePowder = "itemGroup.name.concretePowder"
    CookedFood = "itemGroup.name.cookedFood"
    Copper = "itemGroup.name.copper"
    Coral = "itemGroup.name.coral"
    CoralDecorations = "itemGroup.name.coral_decorations"
    Crop = "itemGroup.name.crop"
    Door = "itemGroup.name.door"
    Dye = "itemGroup.name.dye"
    EnchantedBook = "itemGroup.name.enchantedBook"
    Fence = "itemGroup.name.fence"
    FenceGate = "itemGroup.name.fenceGate"
    Firework = "itemGroup.name.firework"
    FireworkStars = "itemGroup.name.fireworkStars"
    Flower = "itemGroup.name.flower"
    Glass = "itemGroup.name.glass"
    GlassPane = "itemGroup.name.glassPane"
    GlazedTerracotta = "itemGroup.name.glazedTerracotta"
    GoatHorn = "itemGroup.name.goatHorn"
    Grass = "itemGroup.name.grass"
    HangingSign = "itemGroup.name.hanging_sign"
    Helmet = "itemGroup.name.helmet"
    Hoe = "itemGroup.name.hoe"
    HorseArmor = "itemGroup.name.horseArmor"
    Leaves = "itemGroup.name.leaves"
    Leggings = "itemGroup.name.leggings"
    LingeringPotion = "itemGroup.name.lingeringPotion"
    Log = "itemGroup.name.log"
    Minecart = "itemGroup.name.minecart"
    MiscFood = "itemGroup.name.miscFood"
    MobEgg = "itemGroup.name.mobEgg"
    MonsterStoneEgg = "itemGroup.name.monsterStoneEgg"
    Mushroom = "itemGroup.name.mushroom"
    NetherWartBlock = "itemGroup.name.netherWartBlock"
    Ore = "itemGroup.name.ore"
    Permission = "itemGroup.name.permission"
    Pickaxe = "itemGroup.name.pickaxe"
    Planks = "itemGroup.name.planks"
    Potion = "itemGroup.name.potion"
    PotterySherds = "itemGroup.name.potterySherds"
    PressurePlate = "itemGroup.name.pressurePlate"
    Rail = "itemGroup.name.rail"
    RawFood = "itemGroup.name.rawFood"
    Record = "itemGroup.name.record"
    Sandstone = "itemGroup.name.sandstone"
    Sapling = "itemGroup.name.sapling"
    Sculk = "itemGroup.name.sculk"
    Seed = "itemGroup.name.seed"
    Shovel = "itemGroup.name.shovel"
    ShulkerBox = "itemGroup.name.shulkerBox"
    Sign = "itemGroup.name.sign"
    Skull = "itemGroup.name.skull"
    Slab = "itemGroup.name.slab"
    SmithingTemplates = "itemGroup.name.smithing_templates"
    SplashPotion = "itemGroup.name.splashPotion"
    StainedClay = "itemGroup.name.stainedClay"
    Stairs = "itemGroup.name.stairs"
    Stone = "itemGroup.name.stone"
    StoneBrick = "itemGroup.name.stoneBrick"
    Sword = "itemGroup.name.sword"
    Trapdoor = "itemGroup.name.trapdoor"
    Walls = "itemGroup.name.walls"
    Wood = "itemGroup.name.wood"
    Wool = "itemGroup.name.wool"
    WoolCarpet = "itemGroup.name.woolCarpet"
    none = "None"


class Weather(StrEnum):
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


class BlockSoundEvent(StrEnum):
    BreakPot = "break_pot"
    Break = "break"
    ButtonClickOff = "button.click_off"
    ButtonClickOn = "button.click_on"
    Default = "default"
    DoorClose = "door.close"
    DoorOpen = "door.open"
    Fall = "fall"
    FenceGateClose = "fence_gate.close"
    FenceGateOpen = "fence_gate.open"
    Hit = "hit"
    ItemUseOn = "item.use.on"
    Place = "place"
    PowerOff = "power.off"
    PowerOn = "power.on"
    PressurePlateClickOff = "pressure_plate.click_off"
    PressurePlateClickOn = "pressure_plate.click_on"
    ShatterPot = "shatter_pot"
    Step = "step"
    TrapdoorClose = "trapdoor.close"
    TrapdoorOpen = "trapdoor.open"


class BlockInteractiveSoundEvent(StrEnum):
    Default = "default"
    Fall = "fall"
    Jump = "jump"
    Land = "land"
    Step = "step"


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


class SmeltingTags(StrEnum):
    FURNACE = "furnace"
    BLAST_FURNACE = "blast_furnace"
    SMOKER = "smoker"
    CAMPFIRE = "campfire"
    SOUL_CAMPFIRE = "soul_campfire"


class ContainerType(StrEnum):
    Horse = "horse"
    MinecartChest = "minecart_chest"
    ChestBoat = "chest_boat"
    MinecartHopper = "minecart_hopper"
    Inventory = "inventory"
    Container = "container"
    Hopper = "hopper"


class EnchantsSlots(StrEnum):
    """
    Enumeration of enchantment slots available in Minecraft.

    This enum defines all possible equipment slots that can receive enchantments,
    organized by equipment type and usage category.

    Armor Slots:
        ArmorHead: Helmet slot enchantments
        ArmorTorso: Chestplate slot enchantments
        ArmorLegs: Leggings slot enchantments
        ArmorFeet: Boots slot enchantments
        GArmor: General armor enchantments (applicable to any armor piece)

    Weapon Slots:
        Sword: Sword-specific enchantments
        Bow: Bow-specific enchantments
        Spear: Spear/trident enchantments
        Crossbow: Crossbow-specific enchantments
        MeleeSpear: Melee trident enchantments

    Tool Slots:
        GTool: General tool enchantments (applicable to multiple tool types)
        Hoe: Hoe-specific enchantments
        Shears: Shears-specific enchantments
        Flintandsteel: Flint and steel enchantments
        Shield: Shield-specific enchantments

    Digging Tools:
        GDigging: General digging tool enchantments
        Axe: Axe-specific enchantments
        Pickaxe: Pickaxe-specific enchantments
        Shovel: Shovel-specific enchantments

    Special Items:
        FishingRod: Fishing rod enchantments
        CarrotStick: Carrot on a stick enchantments
        Elytra: Elytra wing enchantments
        CosmeticHead: Cosmetic head item enchantments
    """

    ArmorHead = "armor_head"
    ArmorTorso = "armor_torso"
    ArmorLegs = "armor_legs"
    ArmorFeet = "armor_feet"
    GArmor = "g_armor"
    Sword = "sword"
    Bow = "bow"
    Spear = "spear"
    Crossbow = "crossbow"
    MeleeSpear = "melee_spear"
    GTool = "g_tool"
    Hoe = "hoe"
    Shears = "shears"
    Flintandsteel = "flintsteel"
    Shield = "shield"
    GDigging = "g_digging"
    Axe = "axe"
    Pickaxe = "pickaxe"
    Shovel = "shovel"
    FishingRod = "fishing_rod"
    CarrotStick = "carrot_stick"
    Elytra = "elytra"
    CosmeticHead = "cosmetic_head"


class HudElement(StrEnum):
    Hunger = "hunger"
    All = "all"
    Paperdoll = "paperdoll"
    Armor = "armor"
    Tooltips = "tooltips"
    TouchControls = "touch_controls"
    Crosshair = "crosshair"
    Hotbar = "hotbar"
    Health = "health"
    ProgressBar = "progress_bar"
    AirBubbles = "air_bubbles"
    HorseHealth = "horse_health"
    StatusEffects = "status_effects"
    ItemText = "item_text"


class HudVisibility(StrEnum):
    Hide = "hide"
    Reset = "reset"


class ItemRarity(StrEnum):
    Common = "common"
    Uncommon = "uncommon"
    Rare = "rare"
    Epic = "epic"


class ExplosionParticleEffect(StrEnum):
    Explosion = "explosion"
    WindBurst = "wind_burst"
    BreezeWindBurst = "breeze_wind_burst"


class DamageSensor(StrEnum):
    Yes = "yes"
    No = "no"
    NoButSideEffectsApply = "no_but_side_effects_apply"


class LineOfSightObstructionType(StrEnum):
    Outline = "outline"
    Collision = "collision"
    CollisionForCamera = "collision_for_camera"


class LookAtLocation(StrEnum):
    Head = "head"
    Body = "body"
    Feet = "feet"


class LootedAtSetTarget(StrEnum):
    Never = "never"
    OnceAndStopScanning = "once_and_stop_scanning"
    OnceAndKeepScanning = "once_and_keep_scanning"


class AimAssistTargetMode(StrEnum):
    Distance = "distance"
    Angle = "angle"


class Glyph(StrEnum):
    Forward = ":_input_key.forward:"
    Back = ":_input_key.back:"
    Left = ":_input_key.left:"
    Right = ":_input_key.right:"
    Inventory = ":_input_key.inventory:"
    Use = ":_input_key.use:"
    Chat = ":_input_key.chat:"
    Attack = ":_input_key.attack:"
    Sprint = ":_input_key.sprint:"
    Jump = ":_input_key.jump:"
    Sneak = ":_input_key.sneak:"


class BlockLiquidDetectionTouching(StrEnum):
    Blocking = "blocking"
    Broken = "broken"
    Popped = "popped"
    NoReaction = "no_reaction"


class BreedingMutationStrategy(StrEnum):
    None_ = "none"
    Random = "random"


class InputModes(StrEnum):
    KeyboardAndMouse = "keyboard_and_mouse"
    Touch = "touch"
    Gamepad = "gamepad"
    MotionController = "motion_controller"


class TintMethod(StrEnum):
    None_ = "none"
    DefaultFoliage = "default_foliage"
    BirchFoliage = "birch_foliage"
    EvergreenFoliage = "evergreen_foliage"
    DryFoliage = "dry_foliage"
    Grass = "grass"
    Water = "water"


class RecipeUnlockContext(StrEnum):
    AlwaysUnlocked = "AlwaysUnlocked"
    PlayerInWater = "PlayerInWater"
    PlayerHasManyItems = "PlayerHasManyItems"


class RideableDismountMode(StrEnum):
    """
    Enumeration for the different modes of dismounting a rideable entity in Minecraft.
    """

    Default = "default"
    OnTopCenter = "on_top_center"


class LeashSpringType(StrEnum):
    """
    Enumeration for the different types of leash springs in Minecraft.

    Bouncy: Simulates a highly elastic spring that never reaches an equilibrium if the leashed entity is suspended mid-air.
    Dampened: Simulates a dampened spring attached to the front of the leashed entity's collision. It reaches an equilibrium if the entity is suspended mid-air and aligns with the movement direction.
    QuadDampened: Simulates four dampened springs connected to the center of each side of the entities' collisions. It reaches an equilibrium if the entity is suspended mid-air and gradually aligns with the leash holder over time.
    """

    Bouncy = "bouncy"
    Dampened = "dampened"
    QuadDampened = "quad_dampened"


class EnchantmentTypes(StrEnum):
    AquaAffinity = "minecraft:aqua_affinity"
    BaneOfArthropods = "minecraft:bane_of_arthropods"
    Binding = "minecraft:binding"
    BlastProtection = "minecraft:blast_protection"
    BowInfinity = "minecraft:infinity"
    Breach = "minecraft:breach"
    Channeling = "minecraft:channeling"
    Density = "minecraft:density"
    DepthStrider = "minecraft:depth_strider"
    Efficiency = "minecraft:efficiency"
    FeatherFalling = "minecraft:feather_falling"
    FireAspect = "minecraft:fire_aspect"
    FireProtection = "minecraft:fire_protection"
    Flame = "minecraft:flame"
    Fortune = "minecraft:fortune"
    FrostWalker = "minecraft:frost_walker"
    Impaling = "minecraft:impaling"
    Knockback = "minecraft:knockback"
    Looting = "minecraft:looting"
    Loyalty = "minecraft:loyalty"
    LuckOfTheSea = "minecraft:luck_of_the_sea"
    Lure = "minecraft:lure"
    Mending = "minecraft:mending"
    Multishot = "minecraft:multishot"
    Piercing = "minecraft:piercing"
    Power = "minecraft:power"
    ProjectileProtection = "minecraft:projectile_protection"
    Protection = "minecraft:protection"
    Punch = "minecraft:punch"
    QuickCharge = "minecraft:quick_charge"
    Respiration = "minecraft:respiration"
    Riptide = "minecraft:riptide"
    Sharpness = "minecraft:sharpness"
    SilkTouch = "minecraft:silk_touch"
    Smite = "minecraft:smite"
    SoulSpeed = "minecraft:soul_speed"
    SwiftSneak = "minecraft:swift_sneak"
    Thorns = "minecraft:thorns"
    Unbreaking = "minecraft:unbreaking"
    Vanishing = "minecraft:vanishing"
    WindBurst = "minecraft:wind_burst"


class BlockMovementType(StrEnum):
    """
    Enumeration for the different types of block movement in Minecraft.

    PushPull: The default value for this field. The block will be pushed and pulled by a piston.
    Push: The block will only be pulled by a piston and will ignore a sticky piston.
    Popped: The block is destroyed when moved by a piston.
    Immovable: The block is unaffected by a piston.
    """

    PushPull = "push_pull"
    Push = "push"
    Popped = "popped"
    Immovable = "immovable"


class BlockStickyType(StrEnum):
    """
    Enumeration for the different types of block stickiness in Minecraft.

    Sticky: The block will stick to a sticky piston.
    NonSticky: The block will not stick to a sticky piston.
    """

    Same = "same"
    None_ = "none"


class ComponentTarget(StrEnum):
    """
    Enumeration for the different component targets in Minecraft.

    """

    Any = "any"
    Client = "client"
    Server = "server"


class ExplorationMapDestinations(StrEnum):
    BuriedTreasure = "buriedtreasure"
    EndCity = "endcity"
    Fortress = "fortress"
    Mansion = "mansion"
    Mineshaft = "mineshaft"
    Monument = "monument"
    PillagerOutpost = "pillageroutpost"
    Ruins = "ruins"
    Shipwreck = "shipwreck"
    Stronghold = "stronghold"
    Temple = "temple"
    Village = "village"


class PlayerAbilities(StrEnum):
    FlySpeed = "flySpeed"
    Flying = "flying"
    Instabuild = "instabuild"
    Invulnerable = "invulnerable"
    Lightning = "lightning"
    Mayfly = "mayfly"
    Mute = "mute"
    Noclip = "noclip"
    VerticalFlySpeed = "verticalFlySpeed"
    WalkSpeed = "walkSpeed"
    Worldbuilder = "worldbuilder"
