from enum import StrEnum
from typing import Optional, overload

from anvil.lib.config import CONFIG
from anvil.lib.enums import InputModes, Slots
from anvil.lib.lib import *


class Molang(str):
    def __invert__(self):
        return Molang(f"!({self})")

    def __eq__(self, other):
        o = f"'{other}'" if isinstance(other, (str, StrEnum)) else f"{other}"
        return Molang(f"{self} == {o}")

    def __ne__(self, other):
        o = f"'{other}'" if type(other) is str else f"{other}"
        return Molang(f"{self} != {o}")

    def __lt__(self, other):
        return Molang(f"{self} < {other}")

    def __gt__(self, other):
        return Molang(f"{self} > {other}")

    def __le__(self, other):
        return Molang(f"{self} <= {other}")

    def __ge__(self, other):
        return Molang(f"{self} >= {other}")

    def __and__(self, other):
        return Molang(f"({self} && {other})")

    def __or__(self, other):
        return Molang(f"({self} || {other})")

    def __add__(self, other):
        return Molang(f"({self} + {other})")

    def __sub__(self, other):
        return Molang(f"({self} - {other})")

    def __mul__(self, other):
        return Molang(f"({self} * {other})")

    def __neg__(self):
        return Molang(f"-{self}")

    def __truediv__(self, other):
        return Molang(f"({self} / {other})")

    def __floordiv__(self, other):
        return Math.floor(self / other)

    def __mod__(self, other):
        return Math.mod(self, other)

    def __pow__(self, other):
        return Math.pow(self, other)

    def __radd__(self, other):
        return Molang(f"({other} + {self})")

    def __rsub__(self, other):
        return Molang(f"({other} - {self})")

    def __rmul__(self, other):
        return Molang(f"({other} * {self})")

    def __rtruediv__(self, other):
        return Molang(f"({other} / {self})")

    def __rfloordiv__(self, other):
        return Math.floor(f"({other} / {self})")

    def __rmod__(self, other):
        return Math.mod(other, self)

    def __rpow__(self, other):
        return Math.pow(other, self)

    def __abs__(self):
        return Math.abs(self)

    def __round__(self):
        return Math.round(self)

    def _struct(self, *Parameters):
        return Molang(f"{self}.{'.'.join(Parameters)}")

    def _query(self, qtype, query, *arguments):
        a = f"{qtype}.{query}"
        if len(arguments):
            Parameters = ", ".join(
                (
                    f"'{arg}'"
                    if isinstance(arg, (str, StrEnum))
                    and not isinstance(arg, Molang)
                    and not arg.startswith(MOLANG_PREFIXES)
                    else f"{arg}"
                )
                for arg in arguments
                if arg is not None
            )
            a += f"({Parameters})"
        return Molang(a)


class vec3:
    def __init__(self, molang: Molang) -> None:
        self.m = molang

    @property
    def x(self):
        return self.m._struct("x")

    @property
    def y(self):
        return self.m._struct("y")

    @property
    def z(self):
        return self.m._struct("z")

    def __str__(self) -> str:
        return self.m


class _TRS:
    def __init__(self, molang: Molang) -> None:
        self.m = molang

    @property
    def translation(self):
        return vec3(self.m._struct("t"))

    @property
    def rotation(self):
        return vec3(self.m._struct("r"))

    @property
    def scale(self):
        return vec3(self.m._struct("s"))

    def __str__(self) -> str:
        return self.m


class Query(Molang):
    handle = "q"

    @classmethod
    def AboveTopSolid(self, x: int, z: int):
        """Returns the height of the block immediately above the highest solid block at the input (x,z) position.

        Parameters:
            x (int): X position.
            z (int): Y position.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "above_top_solid", x, z)

    @classmethod
    def ActorCount(self):
        """Returns the number of actors rendered in the last frame.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "actor_count")

    @classmethod
    def All(self, query: "Query", *Parameters):
        """Requires at least 3 arguments. Evaluates the first argument, then returns 1.0 if all of the following arguments evaluate to the same value as the first. Otherwise it returns 0.0.

        Parameters:
            query (int): Query to evaluate.
            Parameters (int): arguments to test against.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "all", query, *Parameters)

    @classmethod
    def AllAnimationsFinished(self):
        """Only valid in an animation controller. Returns 1.0 if all animations in the current animation controller state have played through at least once, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "all_animations_finished")

    @classmethod
    def AllTags(self, *tags: str):
        """Returns 1.0 if the item or block has all of the tags specified, else it return 0.0.

        Parameters:
            tags (str): entity tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "all_tags", *tags)

    @classmethod
    def AngerLevel(self):
        """If available, returns the anger level of the actor as an integer value from 0 to 1 less than the 'max_anger' defined on the actor, otherwise returns 0. Only returns a non-zero value in behavior packs.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "anger_level")

    @classmethod
    def AnimTime(self):
        """Returns the time in seconds since the current animation started, else 0.0 if not called within an animation.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "anim_time")

    @classmethod
    def Any(self, query: "Query", *Parameters):
        """Requires at least 3 arguments. Evaluates the first argument, then returns 1.0 if any of the following arguments evaluate to the same value as the first. Otherwise it returns 0.0.

        Parameters:
            query (int): Query to evaluate.
            Parameters (int): arguments to test against.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "any", query, *Parameters)

    @classmethod
    def AnyAnimationFinished(self):
        """Only valid in an animation controller. Returns 1.0 if any animation in the current animation controller state has played through at least once, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "any_animation_finished")

    @classmethod
    def AnyTag(self, *tags: str):
        """Returns 1.0 if the item or block has any of the tags specified, else it returns 0.0.

        Parameters:
            tags (str): entity tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "any_tag", *tags)

    @classmethod
    def ApproxEq(self, *Parameters):
        """Returns 1.0 if all of the arguments are within 0.000000 of each other, else it returns 0.0.

        Parameters:
            Parameters (Any): Arguments to test for approximate equality.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "approx_eq", *Parameters)

    @classmethod
    def ArmorColorSlot(self, index: int, colorChannel: int):
        """Takes the armor slot index as a parameter and returns the color of the armor in the requested slot.

        Parameters:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self,
            self.handle,
            "armor_color_slot",
            clamp(index, 0, 3),
            clamp(colorChannel, 0, 3),
        )

    @classmethod
    def ArmorMaterialSlot(self, index: int):
        """Takes the armor slot index as a parameter and returns the armor material type in the requested armor slot.

        Parameters:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "armor_material_slot", index)

    @classmethod
    def ArmorTextureSlot(self, index: int):
        """Takes the armor slot index as a parameter and returns the texture type of the requested slot.

        Parameters:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "armor_texture_slot", index)

    @classmethod
    def AverageFrameTime(self, frame: int = 0):
        """Returns the time in *seconds* of the average frame time over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Parameters:
            frame (int): Frame number.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "average_frame_time", clamp(frame, 0, 30))

    @classmethod
    def BaseSwingDuration(self):
        """Returns the base swing duration of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "base_swing_duration")

    @classmethod
    def BlockFace(self):
        """Returns the block face for this (only valid for certain triggers such as placing blocks, or interacting with block) (Down=0.0, Up=1.0, North=2.0, South=3.0, West=4.0, East=5.0, Undefined=6.0).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "block_face")

    @classmethod
    def BlockState(self, state: str):
        """Returns the value of the associated block's Block State.

        Parameters:
            state (str): The block state to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        state = (
            f"{state}" if isinstance(state, StrEnum) else f"{CONFIG.NAMESPACE}:{state}"
        )
        return self._query(self, self.handle, "block_state", state)

    @classmethod
    def Property(self, property: str):
        """Returns the value of the associated property.

        Parameters:
            property (str): The block property to query, no namespace.


        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "property", f"{CONFIG.NAMESPACE}:{property}"
        )

    @classmethod
    def HasProperty(self, property: str):
        """Returns true if the entity has the property.

        Parameters:
            property (str): The block property to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "has_property", f"{CONFIG.NAMESPACE}:{property}"
        )

    @classmethod
    def Blocking(self):
        """Returns 1.0 if the entity is blocking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "blocking")

    @classmethod
    def BodyXRotation(self):
        """Returns the body pitch rotation if called on an actor, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "body_x_rotation")

    @classmethod
    def BodyYRotation(self):
        """Returns the body yaw rotation if called on an actor, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "body_y_rotation")

    # More info needed
    @classmethod
    def BoneAabb(self):
        """Returns the axis aligned bounding box of a bone as a struct with members '.min', '.max', along with '.x', '.y', and '.z' values for each.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "bone_aabb")

    # More info needed
    @classmethod
    def BoneOrigin(self):
        """Returns the initial (from the .geo) pivot of a bone as a struct with members '.x', '.y', and '.z'.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "bone_origin")

    # More info needed
    @classmethod
    def BoneRotation(self, bone_name: str):
        """Returns the initial (from the .geo) rotation of a bone as a struct with members '.x', '.y', and '.z' in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return vec3(self._query(self, self.handle, "bone_rotation", bone_name))

    @classmethod
    def CameraDistanceRangeLerp(self, d1: int, d2: int):
        """Takes two distances (any order) and return a number from 0 to 1 based on the camera distance between the two ranges clamped to that range.

        For example, 'query.camera_distance_range_lerp(10, 20)' will return 0 for any distance less than or equal to 10, 0.2 for a distance of 12, 0.5 for 15, and 1 for 20 or greater.
        If you pass in (20, 10), a distance of 20 will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "camera_distance_range_lerp", d1, d2)

    @classmethod
    def CameraRotation(self, axis: int):
        """Returns the rotation of the camera. Requires one argument representing the rotation axis you would like.

        Parameters:
            axis (int): 0 for x, 1 for y

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "camera_rotation", clamp(axis, 0, 1))

    @classmethod
    def CanClimb(self):
        """Returns 1.0 if the entity can climb, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_climb")

    @classmethod
    def CanDamageNearbyMobs(self):
        """Returns 1.0 if the entity can damage nearby mobs, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_damage_nearby_mobs")

    @classmethod
    def CanFly(self):
        """Returns 1.0 if the entity can fly, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_fly")

    @classmethod
    def CanPowerJump(self):
        """Returns 1.0 if the entity can power jump, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_power_jump")

    @classmethod
    def CanSwim(self):
        """Returns 1.0 if the entity can swim, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_swim")

    @classmethod
    def CanWalk(self):
        """Returns 1.0 if the entity can walk, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "can_walk")

    @classmethod
    def CapeFlapAmount(self):
        """Returns value between 0.0 and 1.0 with 0.0 meaning "cape is fully down" and 1.0 means "cape is fully up."

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cape_flap_amount")

    @classmethod
    def CardinalBlockFacePlacedOn(self):
        """DEPRECATED (please use query.block_face instead) Returns the block face for this (only valid for on_placed_by_player trigger) (Down=0.0, Up=1.0, North=2.0, South=3.0, West=4.0, East=5.0, Undefined=6.0).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cardinal_block_face_placed_on")

    @classmethod
    def CardinalFacing(self):
        """Returns the current facing of the player

        - Down=0.0
        - Up=1.0
        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cardinal_facing")

    @classmethod
    def CardinalFacing2D(self):
        """Returns the current facing of the player ignoring up/down part of the direction

        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cardinal_facing_2d")

    @classmethod
    def CardinalPlayerFacing(self):
        """Returns the current facing of the player

        - Down=0.0
        - Up=1.0
        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cardinal_player_facing")

    # More info needed
    @classmethod
    def CombineEntities(self):
        """Combines any valid entity references from all arguments into a single array.  Note that order is not preserved, and duplicates and invalid values are removed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "combine_entities")

    @classmethod
    def Count(self, *element):
        """Counts the number of things passed to it (arrays are counted as the number of elements they contain; non-arrays count as 1).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "count", *element)

    @classmethod
    def CurrentSquishValue(self):
        """Returns the squish value for the current entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "current_squish_value")

    @classmethod
    def Day(self):
        """Returns the day of the current level.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "day")

    @classmethod
    def DeathTicks(self):
        """Returns the elapsed ticks since the mob started dying.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "death_ticks")

    @classmethod
    def DebugOutput(self):
        """### Server Client

        Debug log a value to the output debug window for builds that have one.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "debug_output")

    @classmethod
    def DeltaTime(self):
        """Returns the time in seconds since the previous frame.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "delta_time")

    @classmethod
    def DistanceFromCamera(self):
        """Returns the distance of the root of this actor or particle emitter from the camera.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "distance_from_camera")

    @classmethod
    def EffectEmitterCount(self):
        """Returns the total number of active emitters of the callee's particle effect type.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "effect_emitter_count")

    @classmethod
    def EffectParticleCount(self):
        """Returns the total number of active particles of the callee's particle effect type.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "effect_particle_count")

    @classmethod
    def EquipmentCount(self):
        """Returns the number of equipped armor pieces for an actor from 0 to 4, not counting items held in hands. (To query for hand slots, use query.is_item_equipped or query.is_item_name_any).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "equipment_count")

    @classmethod
    def EquippedItemAllTags(self, slot: Slots, *tags: str):
        """Takes a slot name followed by any tag you want to check for in the form of 'tag_name' and returns 1 if all of the tags are on that equipped item, 0 otherwise.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "equipped_item_all_tags", slot, *tags)

    @classmethod
    def EquippedItemAnyTag(self, slot: Slots, *tags: str):
        """Takes a slot name followed by any tag you want to check for in the form of 'tag_name' and returns 0 if none of the tags are on that equipped item or 1 if at least 1 tag exists.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "equipped_item_any_tag", slot, *tags)

    @classmethod
    def EquippedItemIsAttachable(self, hand: int = 0):
        """Takes the desired hand slot as a parameter and returns whether the item is an attachable or not.

        Parameters:
            hand (int): 0 for main hand, 1 for off hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "equipped_item_is_attachable", clamp(hand, 0, 1)
        )

    @classmethod
    def EyeTargetXRotation(self):
        """Returns the X eye rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "eye_target_x_rotation")

    @classmethod
    def EyeTargetYRotation(self):
        """Returns the Y eye rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "eye_target_y_rotation")

    @classmethod
    def FacingTargetToRangeAttack(self):
        """Returns 1.0 if the entity is attacking from range (minecraft:behavior.ranged_attack), else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "facing_target_to_range_attack")

    @classmethod
    def FrameAlpha(self):
        """Returns the ratio (from 0 to 1) of how much between AI ticks this frame is being rendered.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "frame_alpha")

    @classmethod
    def GetActorInfoId(self):
        """Returns the integer ID of an actor by its string name.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_actor_info_id")

    @classmethod
    def GetAnimationFrame(self):
        """Returns the current texture of the item.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_animation_frame")

    # More info needed
    @classmethod
    def GetDefaultBonePivot(self):
        """Gets the specified axis of the specified bone orientation pivot.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_default_bone_pivot")

    @classmethod
    def GetEquippedItemName(self, hand_slot: int, index=0):
        """DEPRECATED (Use query.is_item_name_any instead if possible so names can be changed later without breaking content.) Takes one optional hand slot as a parameter (0 or 'main_hand' for main hand, 1 or 'off_hand' for off hand), and a second parameter (0=default) if you would like the equipped item or any non-zero number for the currently rendered item, and returns the name of the item in the requested slot (defaulting to the main hand if no parameter is supplied) if there is one, otherwise returns ''.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "get_equipped_item_name", clamp(hand_slot, 0, 1), index
        )

    # More info needed
    @classmethod
    def GetLocatorOffset(self):
        """Gets specified axis of the specified locator offset.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_locator_offset")

    @classmethod
    def GetName(self):
        """DEPRECATED (Use query.is_name_any instead if possible so names can be changed later without breaking content.) Get the name of the mob if there is one, otherwise return ''.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_name")

    # More info needed
    @classmethod
    def GetRootLocatorOffset(self):
        """Gets specified axis of the specified locator offset of the root model.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "get_root_locator_offset")

    @classmethod
    def GroundSpeed(self):
        """Returns the ground speed of the entity in meters/second.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "ground_speed")

    @classmethod
    def HadComponentGroup(self, component_group: str):
        """### Server Only.

        Usable only in behavior packs when determining the default value for an entity's Property. Requires one string argument. If the entity is being loaded from data that was last saved with a component_group with the specified name, returns 1.0, otherwise returns 0.0. The purpose of this query is to allow entity definitions to change and still be able to load the correct state of entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "had_component_group", component_group)

    @classmethod
    def HasAnyFamily(self, *family: str):
        """Returns 1 if the entity has any of the specified families, else 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_any_family", *family)

    @classmethod
    def HasArmorSlot(self, slot: Slots):
        """Takes the armor slot index as a parameter and returns 1.0 if the entity has armor in the requested slot, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_armor_slot", slot)

    @classmethod
    def HasBiomeTag(self, tag: str):
        """Returns whether or not a Block Placement Target has a specific biome tag.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_biome_tag", tag)

    @classmethod
    def has_block_state(self, state: str):
        """Returns 1.0 if the associated block has the given block state or 0.0 if not.

        Parameters:
            state (str): The block state to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "has_block_state", f"{CONFIG.NAMESPACE}:{state}"
        )

    @classmethod
    def HasCape(self):
        """Returns 1.0 if the player has a cape, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_cape")

    @classmethod
    def HasCollision(self):
        """Returns 1.0 if the entity has collisions enabled, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_collision")

    @classmethod
    def HasGravity(self):
        """Returns 1.0 if the entity is affected by gravity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_gravity")

    @classmethod
    def HasOwner(self):
        """Returns true if the entity has an owner ID, else it returns false.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_owner")

    @classmethod
    def HasRider(self):
        """Returns 1.0 if the entity has a rider, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_rider")

    @classmethod
    def HasTarget(self):
        """Returns 1.0 if the entity has a target, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_target")

    @classmethod
    def HeadRollAngle(self):
        """Returns the roll angle of the head of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "head_roll_angle")

    @classmethod
    def HeadXRotation(self, head_number: int = 0):
        """Takes one argument as a parameter. Returns the nth head x rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "head_x_rotation", head_number)

    @classmethod
    def HeadYRotation(self, head_number: int = 0):
        """Takes one argument as a parameter. Returns the nth head y rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "head_y_rotation", head_number)

    @classmethod
    def Health(self):
        """Returns the health of the entity, or 0.0 if it doesn't make sense to call on this entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "health")

    @classmethod
    def HeartbeatInterval(self):
        """Returns the heartbeat interval of the actor in seconds. Returns 0 when the actor has no heartbeat.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "heartbeat_interval")

    @classmethod
    def HeartbeatPhase(self):
        """### Client Only

        Returns the heartbeat phase of the actor. 0.0 if at start of current heartbeat, 1.0 if at the end. Returns 0 on errors or when the actor has no heartbeat.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "heartbeat_phase")

    @classmethod
    def Heightmap(self, x: int, z: int):
        """Takes two arguments: X and Z world values. Returns the world height (Y value) of the terrain at the specified position.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "heightmap", x, z)

    @classmethod
    def HurtDirection(self):
        """Returns the hurt direction for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "hurt_direction")

    @classmethod
    def HurtTime(self):
        """Returns the hurt time for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "hurt_time")

    @classmethod
    def InRange(self, value: float, min: float, max: float):
        """Requires 3 numerical arguments: some value, a minimum, and a maximum. If the first argument is between the minimum and maximum (inclusive), returns 1.0. Otherwise it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "in_range", value, min, max)

    @classmethod
    def InvulnerableTicks(self):
        """Returns the number of ticks of invulnerability the entity has left if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "invulnerable_ticks")

    @classmethod
    def IsAdmiring(self):
        """Returns 1.0 if the entity is admiring, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_admiring")

    @classmethod
    def IsAlive(self):
        """Returns 1.0 if the entity is alive, and 0.0 if it's dead.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_alive")

    @classmethod
    def IsAngry(self):
        """Returns 1.0 if the entity is angry, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_angry")

    @classmethod
    def IsAttachedToEntity(self):
        """Returns 1.0 if the actor is attached to an entity, else it will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_attached_to_entity")

    @classmethod
    def IsAvoidingBlock(self):
        """Returns 1.0 if the entity is fleeing from a block, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_avoiding_block")

    @classmethod
    def IsAvoidingMobs(self):
        """Returns 1.0 if the entity is fleeing from mobs, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_avoiding_mobs")

    @classmethod
    def IsBaby(self):
        """Returns 1.0 if the entity is a baby, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_baby")

    @classmethod
    def IsBreathing(self):
        """Returns 1.0 if the entity is breathing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_breathing")

    @classmethod
    def IsBribed(self):
        """Returns 1.0 if the entity has been bribed, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_bribed")

    @classmethod
    def IsCarryingBlock(self):
        """Returns 1.0 if the entity is carrying a block, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_carrying_block")

    @classmethod
    def IsCasting(self):
        """Returns 1.0 if the entity is casting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_casting")

    @classmethod
    def IsCelebrating(self):
        """Returns 1.0 if the entity is celebrating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_celebrating")

    @classmethod
    def IsCelebratingSpecial(self):
        """Returns 1.0 if the entity is doing a special celebration, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_celebrating_special")

    @classmethod
    def IsCharged(self):
        """Returns 1.0 if the entity is charged, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_charged")

    @classmethod
    def IsCharging(self):
        """Returns 1.0 if the entity is charging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_charging")

    @classmethod
    def IsChested(self):
        """Returns 1.0 if the entity has chests attached to it, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_chested")

    @classmethod
    def IsCritical(self):
        """Returns 1.0 if the entity is critical, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_critical")

    @classmethod
    def IsCroaking(self):
        """Returns 1.0 if the entity is croaking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_croaking")

    @classmethod
    def IsDancing(self):
        """Returns 1.0 if the entity is dancing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_dancing")

    @classmethod
    def IsDelayedAttacking(self):
        """Returns 1.0 if the entity is attacking using the delayed attack, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_delayed_attacking")

    @classmethod
    def IsDigging(self):
        """Returns 1.0 if the entity is digging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_digging")

    @classmethod
    def IsEating(self):
        """Returns 1.0 if the entity is eating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_eating")

    @classmethod
    def IsEatingMob(self):
        """Returns 1.0 if the entity is eating a mob, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_eating_mob")

    @classmethod
    def IsElder(self):
        """Returns 1.0 if the entity is an elder version of it, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_elder")

    @classmethod
    def IsEmerging(self):
        """Returns 1.0 if the entity is emerging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_emerging")

    @classmethod
    def IsEmoting(self):
        """Returns 1.0 if the entity is emoting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_emoting")

    @classmethod
    def IsEnchanted(self):
        """Returns 1.0 if the entity is enchanted, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_enchanted")

    @classmethod
    def IsFireImmune(self):
        """Returns 1.0 if the entity is immune to fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_fire_immune")

    @classmethod
    def IsFirstPerson(self):
        """Returns 1.0 if the entity is being rendered in first person mode, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_first_person")

    @classmethod
    def IsGhost(self):
        """Returns 1.0 if an entity is a ghost, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_ghost")

    @classmethod
    def IsGliding(self):
        """Returns 1.0 if the entity is gliding, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_gliding")

    @classmethod
    def IsGrazing(self):
        """Returns 1.0 if the entity is grazing, or 0.0 if not.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_grazing")

    @classmethod
    def IsIdling(self):
        """Returns 1.0 if the entity is idling, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_idling")

    @classmethod
    def IsIgnited(self):
        """Returns 1.0 if the entity is ignited, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_ignited")

    @classmethod
    def IsIllagerCaptain(self):
        """Returns 1.0 if the entity is an illager captain, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_illager_captain")

    @classmethod
    def IsInContactWithWater(self):
        """Returns 1.0 if the entity is in contact with any water (water, rain, splash water bottle), else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_in_contact_with_water")

    @classmethod
    def IsInLove(self):
        """Returns 1.0 if the entity is in love, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_in_love")

    @classmethod
    def IsInUI(self):
        """Returns 1.0 if the entity is rendered as part of the UI, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_in_ui")

    @classmethod
    def IsInWater(self):
        """Returns 1.0 if the entity is in water, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_in_water")

    @classmethod
    def IsInWaterOrRain(self):
        """Returns 1.0 if the entity is in water or rain, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_in_water_or_rain")

    @classmethod
    def IsInterested(self):
        """Returns 1.0 if the entity is interested, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_interested")

    @classmethod
    def IsInvisible(self):
        """Returns 1.0 if the entity is invisible, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_invisible")

    @classmethod
    def IsItemEquipped(self, hand: int = 0):
        """Takes one optional hand slot as a parameter and returns 1.0 if there is an item in the requested slot, otherwise returns 0.0.

        - 0 = main_hand
        - 1 = off_hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_item_equipped", clamp(hand, 0, 1))

    @classmethod
    def IsItemNameAny(self, slot: Slots, index: int, *item_identifiers):
        """Takes an equipment slot name (see the replaceitem command) and an optional slot index value. After that, takes one or more full name (with 'namespace:') strings to check for. Returns 1.0 if an item in the specified slot has any of the specified names, otherwise returns 0.0. An empty string '' can be specified to check for an empty slot. Note that querying slot.enderchest, slot.saddle, slot.armor, or slot.chest will only work in behavior packs. A preferred query to query.get_equipped_item_name, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "is_item_name_any", slot, index, *item_identifiers
        )

    @classmethod
    def IsJumping(self):
        """Returns 1.0 if the entity is jumping, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_jumping")

    @classmethod
    def IsLayingDown(self):
        """Returns 1.0 if the entity is laying down, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_laying_down")

    @classmethod
    def IsLayingEgg(self):
        """Returns 1.0 if the entity is laying an egg, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_laying_egg")

    @classmethod
    def IsLeashed(self):
        """Returns 1.0 if the entity is leashed to something, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_leashed")

    @classmethod
    def IsLevitating(self):
        """Returns 1.0 if the entity is levitating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_levitating")

    @classmethod
    def IsLingering(self):
        """Returns 1.0 if the entity is lingering, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_lingering")

    @classmethod
    def IsLocalPlayer(self):
        """### Client Only
        Takes no arguments. Returns 1.0 if the entity is the local player for the current game window, else it returns 0.0. In splitscreen returns 0.0 for the other local players for other views. Always returns 0.0 if used in a behavior pack.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_local_player")

    @classmethod
    def IsMoving(self):
        """Returns 1.0 if the entity is moving, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_moving")

    @classmethod
    def IsNameAny(self, *names: str):
        """Takes one or more arguments. If the entity's name is any of the specified string values, returns 1.0. Otherwise returns 0.0.

        A preferred query to query.get_name, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_name_any", *names)

    @classmethod
    def IsOnFire(self):
        """Returns 1.0 if the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_on_fire")

    @classmethod
    def IsOnGround(self):
        """Returns 1.0 if the entity is on the ground, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_on_ground")

    @classmethod
    def IsOnScreen(self):
        """Returns 1.0 if this is called on an entity at a time when it is known if it is on screen, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_on_screen")

    @classmethod
    def IsOnfire(self):
        """Returns 1.0 if the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_onfire")

    @classmethod
    def IsOrphaned(self):
        """Returns 1.0 if the entity is orphaned, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_orphaned")

    @classmethod
    def IsOwnerIdentifierAny(self):
        """Takes one or more arguments. Returns whether the root actor identifier is any of the specified strings. A preferred query to query.owner_identifier, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_owner_identifier_any")

    @classmethod
    def IsPersonaOrPremiumSkin(self):
        """Returns 1.0 if the player has a persona or premium skin, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_persona_or_premium_skin")

    @classmethod
    def IsPlayingDead(self):
        """Returns 1.0 if the entity is playing dead, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_playing_dead")

    @classmethod
    def IsPowered(self):
        """Returns 1.0 if the entity is powered, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_powered")

    @classmethod
    def IsPregnant(self):
        """Returns 1.0 if the entity is pregnant, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_pregnant")

    @classmethod
    def IsRamAttacking(self):
        """Returns 1.0 if the entity is using a ram attack, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_ram_attacking")

    @classmethod
    def IsResting(self):
        """Returns 1.0 if the entity is resting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_resting")

    @classmethod
    def IsRiding(self):
        """Returns 1.0 if the entity is riding, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_riding")

    @classmethod
    def IsRoaring(self):
        """Returns 1.0 if the entity is currently roaring, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_roaring")

    @classmethod
    def IsRolling(self):
        """Returns 1.0 if the entity is rolling, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_rolling")

    @classmethod
    def IsSaddled(self):
        """Returns 1.0 if the entity has a saddle, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_saddled")

    @classmethod
    def IsScared(self):
        """Returns 1.0 if the entity is scared, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_scared")

    @classmethod
    def IsSelectedItem(self):
        """Returns true if the player has selected an item in the inventory, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_selected_item")

    @classmethod
    def IsShaking(self):
        """Returns 1.0 if the entity is casting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_shaking")

    @classmethod
    def IsShakingWetness(self):
        """Returns 1.0 if the entity is shaking water off, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_shaking_wetness")

    @classmethod
    def IsSheared(self):
        """Returns 1.0 if the entity is able to be sheared and is sheared, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sheared")

    @classmethod
    def IsShieldPowered(self):
        """Returns 1.0f if the entity has an active powered shield if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_shield_powered")

    @classmethod
    def IsSilent(self):
        """Returns 1.0 if the entity is silent, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_silent")

    @classmethod
    def IsSitting(self):
        """Returns 1.0 if the entity is sitting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sitting")

    @classmethod
    def IsSleeping(self):
        """Returns 1.0 if the entity is sleeping, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sleeping")

    @classmethod
    def IsSneaking(self):
        """Returns 1.0 if the entity is sneaking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sneaking")

    @classmethod
    def IsSneezing(self):
        """Returns 1.0 if the entity is sneezing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sneezing")

    @classmethod
    def IsSniffing(self):
        """Returns 1.0 if the entity is sniffing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sniffing")

    @classmethod
    def IsSonicBoom(self):
        """Returns 1.0 if the entity is using sonic boom, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sonic_boom")

    @classmethod
    def IsSprinting(self):
        """Returns 1.0 if the entity is sprinting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_sprinting")

    @classmethod
    def IsStackable(self):
        """Returns 1.0 if the entity is stackable, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_stackable")

    @classmethod
    def IsStalking(self):
        """Returns 1.0 if the entity is stalking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_stalking")

    @classmethod
    def IsStanding(self):
        """Returns 1.0 if the entity is standing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_standing")

    @classmethod
    def IsStunned(self):
        """Returns 1.0 if the entity is currently stunned, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_stunned")

    @classmethod
    def IsSwimming(self):
        """Returns 1.0 if the entity is swimming, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_swimming")

    @classmethod
    def IsTamed(self):
        """Returns 1.0 if the entity is tamed, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_tamed")

    @classmethod
    def IsTransforming(self):
        """Returns 1.0 if the entity is transforming, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_transforming")

    @classmethod
    def IsUsingItem(self):
        """Returns 1.0 if the entity is using an item, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_using_item")

    @classmethod
    def IsWallClimbing(self):
        """Returns 1.0 if the entity is climbing a wall, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_wall_climbing")

    @classmethod
    def ItemInUseDuration(self):
        """Returns the amount of time an item has been in use in seconds up to the maximum duration, else 0.0 if it doesn't make sense.

        **Note**: The value exported by this query is calculated by dividing the internal tick count by 200 to convert it to seconds from whatever internal unit is used.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "item_in_use_duration") / 200

    @classmethod
    def ItemIsCharged(self, hand: int = 0):
        """Takes one optional hand slot as a parameter and returns 1.0 if the item is charged in the requested slot (defaulting to the main hand if no parameter is supplied), otherwise returns 0.0.

        - 0 = main_hand
        - 1 = off_hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "item_is_charged", clamp(hand, 0, 1))

    @classmethod
    def ItemMaxUseDuration(self):
        """Returns the maximum amount of time the item can be used, else 0.0 if it doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "item_max_use_duration")

    @classmethod
    def ItemRemainingUseDuration(self, hand: int = 0):
        """Returns the amount of time an item has left to use, else 0.0 if it doesn't make sense. Time remaining is normalized using the normalization value, only if one is given, else it is returned in seconds.

        - main_hand = 0
        - off_hand = 1

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "item_remaining_use_duration", clamp(hand, 0, 1)
        )

    @classmethod
    def ItemSlotToBoneName(self, slot: Slots):
        """Requires one parameter: the name of the equipment slot. This function returns the name of the bone this entity has mapped to that slot.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "item_slot_to_bone_name", slot)

    @classmethod
    def KeyFrameLerpTime(self):
        """Returns the ratio between the previous and next key frames

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "key_frame_lerp_time")

    @classmethod
    def LastFrameTime(self, frame: int = 0):
        """Returns the time in *seconds* of the last frame.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.


        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "last_frame_time", clamp(frame, 0, 30))

    @classmethod
    def LastHitByPlayer(self):
        """### Server Only

        Returns 1.0 if the entity was last hit by the player, else it returns 0.0. If called by the client always returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "last_hit_by_player")

    @classmethod
    def LieAmount(self):
        """Returns the lie down amount for the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "lie_amount")

    @classmethod
    def LifeSpan(self):
        """Returns the limited life span of an entity, or 0.0 if it lives forever

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "life_span")

    @classmethod
    def LifeTime(self):
        """Returns the time in seconds since the current animation started, else 0.0 if not called within an animation.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "life_time")

    @classmethod
    def LodIndex(self, d1: int, d2: int, d3: int):
        """Takes an array of distances and returns the zero - based index of which range the actor is in based on distance from the camera.

        For example, 'query.lod_index(10, 20, 30)' will return 0, 1, or 2 based on whether the mob is less than 10, 20, or 30 units away from the camera, or it will return 3 if it is greater than 30.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "lod_index", d1, d2, d3)

    @classmethod
    def Log(self, query):
        """Debug log a value to the content log.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "log", query)

    @classmethod
    def MainHandItemMaxDuration(self):
        """Returns the use time maximum duration for the main hand item if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "main_hand_item_max_duration")

    @classmethod
    def MainHandItemUseDuration(self):
        """Returns the use time for the main hand item.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "main_hand_item_use_duration")

    @classmethod
    def MarkVariant(self):
        """Returns the entity's mark variant.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "mark_variant")

    @classmethod
    def MaxDurability(self):
        """Returns the max durability an item can take.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "max_durability")

    @classmethod
    def MaxHealth(self):
        """Returns the maximum health of the entity, or 0.0 if it doesn't make sense to call on this entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "max_health")

    @classmethod
    def MaxTradeTier(self):
        """Returns the maximum trade tier of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "max_trade_tier")

    @classmethod
    def MaximumFrameTime(self, frame: int = 0):
        """Returns the time in *seconds* of the most expensive frame over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "maximum_frame_time", clamp(frame, 0, 30))

    @classmethod
    def MinimumFrameTime(self, frame: int = 0):
        """Returns the time in *seconds* of the least expensive frame over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "minimum_frame_time", clamp(frame, 0, 30))

    @classmethod
    def ModelScale(self):
        """Returns the scale of the current entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "model_scale")

    @classmethod
    def ModifiedDistanceMoved(self):
        """Returns the total distance the entity has moved horizontally in meters (since the entity was last loaded, not necessarily since it was originally created) modified along the way by status flags such as is_baby or on_fire.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "modified_distance_moved")

    @classmethod
    def ModifiedMoveSpeed(self):
        """Returns the current walk speed of the entity modified by status flags such as is_baby or on_fire.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "modified_move_speed")

    @classmethod
    def ModifierSwingDuration(self):
        """Returns the duration of the entity's swing modifier.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "modifier_swing_duration")

    @classmethod
    def MoonBrightness(self):
        """Returns the brightness of the moon

        - FULL_MOON = 1.0
        - WANING_GIBBOUS = 0.75
        - FIRST_QUARTER = 0.5
        - WANING_CRESCENT = 0.25
        - NEW_MOON = 0.0
        - WAXING_CRESCENT = 0.25
        - LAST_QUARTER = 0.5
        - WAXING_GIBBOUS = 0.75

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "moon_brightness")

    @classmethod
    def MoonPhase(self):
        """Returns the phase of the moon

        - FULL_MOON = 0
        - WANING_GIBBOUS = 1
        - FIRST_QUARTER = 2
        - WANING_CRESCENT = 3
        - NEW_MOON = 4
        - WAXING_CRESCENT = 5
        - LAST_QUARTER = 6
        - WAXING_GIBBOUS = 7

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "moon_phase")

    @classmethod
    def MovementDirection(self, axis: int):
        """Returns the specified axis of the normalized position delta of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "movement_direction", axis)

    @classmethod
    def Noise(self):
        """Queries Perlin Noise Map.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "noise")

    @classmethod
    def OnFireTime(self):
        """Returns the time that the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "on_fire_time")

    @classmethod
    def OutOfControl(self):
        """Returns 1.0 if the entity is out of control, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "out_of_control")

    @classmethod
    def OverlayAlpha(self):
        """DEPRECATED (Do not use - this function is deprecated and will be removed).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "overlay_alpha")

    @classmethod
    def OwnerIdentifier(self):
        """DEPRECATED (Use query.is_owner_identifier_any instead if possible so names can be changed later without breaking content.) Returns the root actor identifier.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "owner_identifier")

    @classmethod
    def PlayerLevel(self):
        """Returns the players level if the actor is a player, otherwise returns 0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "player_level")

    @classmethod
    def Position(self, axis: int):
        """Returns the absolute position of an actor.  Takes one argument that represents the desired axis (0 == x-axis, 1 == y-axis, 2 == z-axis).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "position", clamp(axis, 0, 2))

    @classmethod
    def PositionDelta(self, axis: int):
        """Returns the position delta for an actor.  Takes one argument that represents the desired axis (0 == x-axis, 1 == y-axis, 2 == z-axis).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "position_delta", clamp(axis, 0, 2))

    @classmethod
    def PreviousSquishValue(self):
        """Returns the previous squish value for the current entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "previous_squish_value")

    @classmethod
    def RemainingDurability(self):
        """Returns the how much durability an item has remaining.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "remaining_durability")

    @classmethod
    def RollCounter(self):
        """Returns the roll counter of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "roll_counter")

    @classmethod
    def RotationToCamera(self, axis: int):
        """Returns the rotation required to aim at the camera.  Requires one argument representing the rotation axis you would like (0 for x, 1 for y)

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "rotation_to_camera", clamp(axis, 0, 1))

    @classmethod
    def ShakeAngle(self):
        """Returns the shaking angle of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "shake_angle")

    @classmethod
    def ShakeTime(self):
        """Returns the shake time of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "shake_time")

    @classmethod
    def ShieldBlockingBob(self):
        """Returns the how much the offhand shield should translate down when blocking and being hit.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "shield_blocking_bob")

    @classmethod
    def ShowBottom(self):
        """Returns 1.0 if we render the entity's bottom, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "show_bottom")

    @classmethod
    def SitAmount(self):
        """Returns the current sit amount of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "sit_amount")

    @classmethod
    def SkinId(self):
        """Returns the entity's skin ID

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "skin_id")

    @classmethod
    def SleepRotation(self):
        """Returns the rotation of the bed the player is sleeping on.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "sleep_rotation")

    @classmethod
    def SneezeCounter(self):
        """Returns the sneeze counter of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "sneeze_counter")

    @classmethod
    def Spellcolor(self):
        """Returns a struct representing the entity spell color for the specified entity. The struct contains '.r' '.g' '.b' and '.a' members, each 0.0 to 1.0. If no actor is specified, each member value will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "spellcolor")

    @classmethod
    def StandingScale(self):
        """Returns the scale of how standing up the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "standing_scale")

    @classmethod
    def StructuralIntegrity(self):
        """Returns the structural integrity for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "structural_integrity")

    @classmethod
    def SurfaceParticleColor(self):
        """### Client Only

        Returns the particle color for the block located in the surface below the actor (scanned up to 10 blocks down). The struct contains '.r' '.g' '.b' and '.a' members, each 0.0 to 1.0. If no actor is specified or if no surface is found, each member value is set to 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "surface_particle_color")

    @classmethod
    def SurfaceParticleTextureCoordinate(self):
        """### Client Only

        Returns the texture coordinate for generating particles for the block located in the surface below the actor (scanned up to 10 blocks down) in a struct with 'u' and 'v' keys. If no actor is specified or if no surface is found, u and v will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "surface_particle_texture_coordinate")

    @classmethod
    def SurfaceParticleTextureSize(self):
        """### Client Only

        Returns the texture size for generating particles for the block located in the surface below the actor (scanned up to 10 blocks down). If no actor is specified or if no surface is found, each member value will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "surface_particle_texture_size")

    @classmethod
    def SwellAmount(self):
        """Returns how swollen the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "swell_amount")

    @classmethod
    def SwellingDir(self):
        """Returns the swelling direction of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "swelling_dir")

    @classmethod
    def SwimAmount(self):
        """Returns the amount the current entity is swimming.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "swim_amount")

    @classmethod
    def TailAngle(self):
        """Returns the angle of the tail of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "tail_angle")

    @classmethod
    def TargetXRotation(self):
        """Returns the x rotation required to aim at the entity's current target if it has one, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "target_x_rotation")

    @classmethod
    def TargetYRotation(self):
        """Returns the y rotation required to aim at the entity's current target if it has one, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "target_y_rotation")

    @classmethod
    def TextureFrameIndex(self):
        """Returns the icon index of the experience orb

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "texture_frame_index")

    @classmethod
    def TimeOfDay(self):
        """Returns the time of day (midnight=0.0, sunrise=0.25, noon=0.5, sunset=0.75) of the dimension the entity is in.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "time_of_day")

    @classmethod
    def TimeSinceLastVibrationDetection(self):
        """### Client Only

        Returns the time in seconds since the last vibration detected by the actor. On errors or if no vibration has been detected yet, returns -1.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "time_since_last_vibration_detection")

    @classmethod
    def TimeStamp(self):
        """Returns the current time stamp of the level.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "time_stamp")

    @classmethod
    def TotalEmitterCount(self):
        """Returns the total number of active emitters in the world.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "total_emitter_count")

    @classmethod
    def TotalParticleCount(self):
        """Returns the total number of active particles in the world.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "total_particle_count")

    @classmethod
    def TradeTier(self):
        """Returns the trade tier of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "trade_tier")

    @classmethod
    def UnhappyCounter(self):
        """Returns how unhappy the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "unhappy_counter")

    @classmethod
    def Variant(self):
        """Returns the entity's variant index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "variant")

    @classmethod
    def VerticalSpeed(self):
        """Returns the speed of the entity up or down in meters/second, where positive is up.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "vertical_speed")

    @classmethod
    def WalkDistance(self):
        """Returns the walk distance of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "walk_distance")

    @classmethod
    def WingFlapPosition(self):
        """Returns the wing flap position of the entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "wing_flap_position")

    @classmethod
    def WingFlapSpeed(self):
        """Returns the wing flap speed of the entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "wing_flap_speed")

    @classmethod
    def YawSpeed(self):
        """Returns the entity's yaw speed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "yaw_speed")

    @classmethod
    def TimerFlag1(self):
        """Returns the value of timer_flag_1 set by behavior.timer_flag_1

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "timer_flag_1")

    @classmethod
    def TimerFlag2(self):
        """Returns the value of timer_flag_2 set by behavior.timer_flag_2

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "timer_flag_2")

    @classmethod
    def TimerFlag3(self):
        """Returns the value of timer_flag_3 set by behavior.timer_flag_3

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "timer_flag_3")

    @classmethod
    def IsSpectator(self):
        """Returns 1.0 if the entity is a spectator, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_spectator")

    @classmethod
    def IsCooldownCategory(self, cooldown_name: str, slot: Slots, slot_id: int = 0):
        """Returns 1.0 if the specified held or worn item has the specified cooldown category name, otherwise returns 0.0. First argument is the cooldown name to check for, second argument is the equipment slot name, and if required third argument is the numerical slot id. For second and third arguments, uses the same name and id that the replaceitem command takes when querying entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "is_cooldown_category", cooldown_name, slot, slot_id
        )

    @classmethod
    def CooldownTime(self, slot: Slots, slot_id: int = 0):
        """Returns the total cooldown time in seconds for the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cooldown_time", slot, slot_id)

    @overload
    @classmethod
    def CooldownTimeRemaining(self, slot: Slots, slot_id: int = 0):
        """Returns the cooldown time remaining in seconds for the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        ...

    @overload
    @classmethod
    def CooldownTimeRemaining(self, cooldown_name: str):
        """Returns the cooldown time remaining in seconds for specified cooldown type, otherwise returns 0. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        ...

    @classmethod
    def CooldownTimeRemaining(self, arg1: Slots | str = None, arg2: int = None):
        """Returns the cooldown time remaining in seconds for specified cooldown type or the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "cooldown_time_remaining", arg1, arg2)

    @classmethod
    def RelativeBlockHasAnyTags(self, x: int, y: int, z: int, *tags: str):
        """Takes an entity-relative position and one or more tag names, and returns either 0 or 1 based on if that block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "relative_block_has_any_tags", x, y, z, *tags
        )

    @classmethod
    def RelativeBlockHasAllTags(self, x: int, y: int, z: int, *tags: str):
        """Takes an entity-relative position and one or more tag names, and returns either 0 or 1 based on if that block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "relative_block_has_all_tags", x, y, z, *tags
        )

    @classmethod
    def BlockNeighborHasAnyTags(self, x: int, y: int, z: int, *tags: str):
        """Takes a block-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "block_neighbor_has_any_tags", x, y, z, *tags
        )

    @classmethod
    def BlockNeighborHasAllTags(self, x: int, y: int, z: int, *tags: str):
        """Takes a block-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(
            self, self.handle, "block_neighbor_has_all_tags", x, y, z, *tags
        )

    @classmethod
    def BlockHasAllTags(self, x: int, y: int, z: int, *tags: str):
        """Takes a world-origin-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "block_has_all_tags", x, y, z, *tags)

    @classmethod
    def BlockHasAnyTags(self, x: int, y: int, z: int, *tags: str):
        """Takes a world-origin-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "block_has_any_tags", x, y, z, *tags)

    @classmethod
    def BoneOrientationTrs(self, bone_name: str):
        """TRS stands for 'Translate/Rotate/Scale.' Takes the name of the bone as an argument. Returns the bone orientation matrix decomposed into the component translation/rotation/scale parts of the desired bone provided it exists in the queryable geometry of the entity, else this returns the identity matrix and throws a content error. The returned value is returned as a variable of type struct with members .t, .r, and .s, each with members .x, .y, and .z, and can be accessed as per this example: v.my_variable = q.bone_orientation_trs('rightarm'); return v.my_variable.r.x;

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _TRS(self._query(self, self.handle, "bone_orientation_trs", bone_name))

    @classmethod
    def BoneOrientationMatrix(self, bone_name: str):
        """Takes the name of the bone as an argument. Returns the bone orientation (as a matrix) of the desired bone provided it exists in the queryable geometry of the entity, else this returns the identity matrix and throws a content error.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "bone_orientation_matrix", bone_name)

    @classmethod
    def IsAttached(self):
        """### Client Only

        Returns 1.0 if the entity is attached to another entity (such as being held or worn), else it will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "is_attached")

    @classmethod
    def HasPlayerRider(self):
        """Returns 1.0 if the entity has a player rider, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "has_player_rider")

    @classmethod
    def Scoreboard(self, score):
        """### Server Only
        Returns the specified scoreboard value for this entity.

        Parameters:
            score (str): The name of the scoreboard to query.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "scoreboard", score)

    @classmethod
    def RideBodyXRotation(self):
        """Returns the body pitch world-rotation of the ride an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "ride_body_x_rotation")

    @classmethod
    def RideBodyYRotation(self):
        """Returns the body pitch world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "ride_body_y_rotation")

    @classmethod
    def RideHeadXRotation(self):
        """Returns the head x world-rotation of the ride of an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "ride_head_x_rotation")

    @classmethod
    def RideHeadYRotation(self, clamp: int = 0):
        """Takes one optional argument as a parameter. Returns the head y world-rotation of the ride of an entity, else it returns 0.0. First parameter only for horses, zombie horses, skeleton horses, donkeys and mules that clamps rotation in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "ride_head_y_rotation", clamp)

    @classmethod
    def RiderBodyXRotation(self, rider: int = 0):
        """Returns the body pitch world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "rider_body_x_rotation", rider)

    @classmethod
    def RiderBodyYRotation(self, rider: int = 0):
        """Returns the body yaw world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "rider_body_y_rotation", rider)

    @classmethod
    def RiderHeadXRotation(self, head: int = 0):
        """Takes one argument as a parameter. Returns the head x world-rotation of the rider entity at the provided index, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "rider_head_x_rotation", head)

    @classmethod
    def RiderHeadYRotation(self, head: int = 0, clamp: int = 0):
        """Takes one or two arguments as parameters. Returns the head y world-rotation of the rider entity at the provided index, else it returns 0.0. Horses, zombie horses, skeleton horses, donkeys and mules require a second parameter that clamps rotation in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "rider_head_y_rotation", head, clamp)

    @classmethod
    def ArmorSlotDamage(self, slot: Slots, slot_id: int = 0):
        """Returns the damage of the item in the specified armor slot name and slot id, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "armor_slot_damage", slot, slot_id)

    @classmethod
    def ClientMemoryTier(self):
        """Returns a number representing the client RAM memory tier, 0 = 'Undetermined', 1 = 'SuperLow', 2 = 'Low', 3 = 'Mid', 4 = 'High', or 5 = 'SuperHigh'. Available on the Client (Resource Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "client_memory_tier")

    @classmethod
    def ServerMemoryTier(self):
        """Returns a number representing the server RAM memory tier, 0 = 'SuperLow', 1 = 'Low', 2 = 'Mid', 3 = 'High', or 4 = 'SuperHigh'. Available on the server side (behavior Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "server_memory_tier")

    @classmethod
    def ClientMaxRenderDistance(self):
        """Returns the max render distance in chunks of the current client. Available on the Client (Resource Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "client_max_render_distance")

    @classmethod
    def LastInputModeIsAny(self, input: InputModes):
        """Returns 1.0 if the last input mode is any of the specified input modes, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "last_input_mode_is_any", input)

    @classmethod
    def TouchOnlyAffectsHotbar(self):
        """Returns 1.0 if the touch only affects hotbar, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return self._query(self, self.handle, "touch_only_affects_hotbar")


class Context(Query):
    handle = "context"

    @classmethod
    def _set_var(self, name):
        setattr(self, name, self._query(self, self.handle, name))

    @classmethod
    def OwningEntity(self, molang: Optional[Molang]):
        if molang:
            return Molang(
                f"({self._query(self, self.handle, "owning_entity")} -> {molang})"
            )
        return Molang._query(self, self.handle, "owning_entity")


class Variable(Molang):
    handle = "v"

    @classmethod
    def _set_var(self, name):
        setattr(self, name, self._query(self, "v", name))
        Context._set_var(name)

    @classmethod
    def IsFirstPerson(self):
        return self._query(self, "v", "is_first_person")

    @classmethod
    def IsPaperdoll(self):
        return self._query(self, "v", "is_paperdoll")

    @classmethod
    def AttackTime(self):
        return self._query(self, "v", "attack_time")


class Math(Molang):
    handle = "math"

    @classmethod
    def abs(self, value):
        return self._query(self, self.handle, "abs", value)

    @classmethod
    def acos(self, value):
        return self._query(self, self.handle, "acos", value)

    @classmethod
    def asin(self, value):
        return self._query(self, self.handle, "asin", value)

    @classmethod
    def atan(self, value):
        return self._query(self, self.handle, "atan", value)

    @classmethod
    def atan2(self, y: str, x):
        return self._query(self, self.handle, "atan2", y, x)

    @classmethod
    def ceil(self, value):
        return self._query(self, self.handle, "ceil", value)

    @classmethod
    def clamp(self, value, min, max):
        return self._query(self, self.handle, "clamp", value, min, max)

    @classmethod
    def cos(self, value):
        return self._query(self, self.handle, "cos", value)

    @classmethod
    def die_roll(self, num, low, high):
        return self._query(self, self.handle, "die_roll", num, low, high)

    @classmethod
    def die_roll_integer(self, num, low, high):
        return self._query(self, self.handle, "die_roll_integer", num, low, high)

    @classmethod
    def exp(self, value):
        return self._query(self, self.handle, "exp", value)

    @classmethod
    def floor(self, value):
        return self._query(self, self.handle, "floor", value)

    @classmethod
    def hermite_blend(self, value):
        return self._query(self, self.handle, "hermite_blend", value)

    @classmethod
    def lerp(self, start, end, factor):
        return self._query(
            self,
            self.handle,
            "lerp",
            start,
            end,
            clamp(factor, 0, 1) if type(factor) in (int, float) else factor,
        )

    @classmethod
    def lerprotate(self, start, end, factor):
        return self._query(
            self,
            self.handle,
            "lerprotate",
            start,
            end,
            clamp(factor, 0, 1) if type(factor) in (int, float) else factor,
        )

    @classmethod
    def ln(self, value):
        return self._query(self, self.handle, "ln", value)

    @classmethod
    def max(self, A, B):
        return self._query(self, self.handle, "max", A, B)

    @classmethod
    def min(self, A, B):
        return self._query(self, self.handle, "min", A, B)

    @classmethod
    def min_angle(self, value):
        return self._query(self, self.handle, "min_angle", value)

    @classmethod
    def mod(self, value, denominator):
        return self._query(self, self.handle, "mod", value, denominator)

    @classmethod
    def pi(self):
        return self._query(self, self.handle, "pi")

    @classmethod
    def pow(self, base, exponent):
        return self._query(self, self.handle, "pow", base, exponent)

    @classmethod
    def random(self, low, high):
        return self._query(self, self.handle, "random", low, high)

    @classmethod
    def random_integer(self, low, high):
        return self._query(self, self.handle, "random_integer", low, high)

    @classmethod
    def round(self, value):
        return self._query(self, self.handle, "round", value)

    @classmethod
    def sin(self, value):
        return self._query(self, self.handle, "sin", value)

    @classmethod
    def sqrt(self, value):
        return self._query(self, self.handle, "sqrt", value)

    @classmethod
    def trunc(self, value):
        return self._query(self, self.handle, "trunc", value)

    @classmethod
    def inverse_lerp(self, start, end, factor):
        return self._query(self, self.handle, "inverse_lerp", start, end, factor)

    @classmethod
    def ease_in_quad(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_quad", start, end, factor)

    @classmethod
    def ease_out_quad(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_quad", start, end, factor)

    @classmethod
    def ease_in_out_quad(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_quad", start, end, factor)

    @classmethod
    def ease_in_cubic(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_cubic", start, end, factor)

    @classmethod
    def ease_out_cubic(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_cubic", start, end, factor)

    @classmethod
    def ease_in_out_cubic(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_cubic", start, end, factor)

    @classmethod
    def ease_in_quart(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_quart", start, end, factor)

    @classmethod
    def ease_out_quart(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_quart", start, end, factor)

    @classmethod
    def ease_in_out_quart(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_quart", start, end, factor)

    @classmethod
    def ease_in_quint(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_quint", start, end, factor)

    @classmethod
    def ease_out_quint(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_quint", start, end, factor)

    @classmethod
    def ease_in_out_quint(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_quint", start, end, factor)

    @classmethod
    def ease_in_sine(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_sine", start, end, factor)

    @classmethod
    def ease_out_sine(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_sine", start, end, factor)

    @classmethod
    def ease_in_out_sine(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_sine", start, end, factor)

    @classmethod
    def ease_in_expo(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_expo", start, end, factor)

    @classmethod
    def ease_out_expo(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_expo", start, end, factor)

    @classmethod
    def ease_in_out_expo(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_expo", start, end, factor)

    @classmethod
    def ease_in_circ(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_circ", start, end, factor)

    @classmethod
    def ease_out_circ(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_circ", start, end, factor)

    @classmethod
    def ease_in_out_circ(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_circ", start, end, factor)

    @classmethod
    def ease_in_bounce(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_bounce", start, end, factor)

    @classmethod
    def ease_out_bounce(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_bounce", start, end, factor)

    @classmethod
    def ease_in_out_bounce(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_bounce", start, end, factor)

    @classmethod
    def ease_in_back(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_back", start, end, factor)

    @classmethod
    def ease_out_back(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_back", start, end, factor)

    @classmethod
    def ease_in_out_back(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_back", start, end, factor)

    @classmethod
    def ease_in_elastic(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_elastic", start, end, factor)

    @classmethod
    def ease_out_elastic(self, start, end, factor):
        return self._query(self, self.handle, "ease_out_elastic", start, end, factor)

    @classmethod
    def ease_in_out_elastic(self, start, end, factor):
        return self._query(self, self.handle, "ease_in_out_elastic", start, end, factor)


def molang_conditions(condition, expression, expression2):
    return Molang(f"{condition} ? {expression} : ({expression2})")


def arrow_operator(left, right):
    """Returns a string representing the arrow operator for Molang."""
    return f"{left} -> {right}"
