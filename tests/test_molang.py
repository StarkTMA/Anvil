import pytest
from enum import StrEnum
from unittest.mock import MagicMock

from anvil.api.core.enums import InputModes, Slots
from anvil.api.logic.molang import (
    Molang,
    Query,
    Context,
    Variable,
    TempVar,
    Math,
    _AabbStruct,
    _ColorStruct,
    _TRSStruct,
    _UVStruct,
    _Vec3Struct,
    arrow_operator,
    molang_conditions,
)


@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    cfg = MagicMock()
    cfg.NAMESPACE = "test"
    monkeypatch.setattr("anvil.api.logic.molang.CONFIG", cfg)
    return cfg


# ---------------------------------------------------------------------------
# Molang
# ---------------------------------------------------------------------------


class TestMolang:
    # --- arithmetic operators ---

    def test_add(self):
        assert str(Molang("q.health") + 5) == "(q.health + 5)"

    def test_sub(self):
        assert str(Molang("q.health") - 3) == "(q.health - 3)"

    def test_mul(self):
        assert str(Molang("q.health") * 2) == "(q.health * 2)"

    def test_truediv(self):
        assert str(Molang("q.health") / 4) == "(q.health / 4)"

    def test_neg(self):
        assert str(-Molang("q.health")) == "-q.health"

    def test_floordiv(self):
        assert str(Molang("q.health") // 2) == "math.floor((q.health / 2))"

    def test_mod(self):
        assert str(Molang("q.health") % 10) == "math.mod(q.health, 10)"

    def test_pow(self):
        assert str(Molang("q.health") ** 2) == "math.pow(q.health, 2)"

    def test_abs(self):
        assert str(abs(Molang("q.health"))) == "math.abs(q.health)"

    def test_round(self):
        assert str(round(Molang("q.health"))) == "math.round(q.health)"

    def test_radd(self):
        assert str(5 + Molang("q.health")) == "(5 + q.health)"

    def test_rsub(self):
        assert str(10 - Molang("q.health")) == "(10 - q.health)"

    def test_rmul(self):
        assert str(3 * Molang("q.health")) == "(3 * q.health)"

    def test_rtruediv(self):
        assert str(100 / Molang("q.health")) == "(100 / q.health)"

    def test_rfloordiv(self):
        assert str(100 // Molang("q.health")) == "math.floor((100 / q.health))"

    def test_rmod(self):
        assert str(10 % Molang("q.health")) == "math.mod(10, q.health)"

    def test_rpow(self):
        assert str(2 ** Molang("q.health")) == "math.pow(2, q.health)"

    def test_chained(self):
        assert str((Molang("q.health") + 5) * 2) == "((q.health + 5) * 2)"

    # --- comparison / logical operators ---

    def test_eq_string(self):
        assert str(Molang("q.variant") == "red") == "q.variant == 'red'"

    def test_eq_number(self):
        assert str(Molang("q.health") == 20) == "q.health == 20"

    def test_eq_molang(self):
        assert (
            str(Molang("q.health") == Molang("q.max_health"))
            == "q.health == q.max_health"
        )

    def test_eq_bool_true(self):
        assert str(Molang("q.is_alive") == True) == "q.is_alive == true"

    def test_eq_bool_false(self):
        assert str(Molang("q.is_alive") == False) == "q.is_alive == false"

    def test_ne_string(self):
        assert str(Molang("q.variant") != "blue") == "q.variant != 'blue'"

    def test_ne_number(self):
        assert str(Molang("q.health") != 0) == "q.health != 0"

    def test_lt(self):
        assert str(Molang("q.health") < 10) == "q.health < 10"

    def test_gt(self):
        assert str(Molang("q.health") > 10) == "q.health > 10"

    def test_le(self):
        assert str(Molang("q.health") <= 10) == "q.health <= 10"

    def test_ge(self):
        assert str(Molang("q.health") >= 10) == "q.health >= 10"

    def test_invert(self):
        assert str(~Molang("q.is_alive")) == "!(q.is_alive)"

    def test_and(self):
        assert (
            str(Molang("q.is_alive") & Molang("q.is_moving"))
            == "(q.is_alive && q.is_moving)"
        )

    def test_or(self):
        assert (
            str(Molang("q.is_alive") | Molang("q.is_moving"))
            == "(q.is_alive || q.is_moving)"
        )

    def test_xor(self):
        assert str(Molang("v.x") ^ 1.2) == "(v.x ?? 1.2)"

    def test_xor_with_molang(self):
        assert str(Molang("v.x") ^ Molang("v.default")) == "(v.x ?? v.default)"

    def test_getitem(self):
        assert str(Molang("q.get_nearby_entities")[0]) == "q.get_nearby_entities[0]"

    def test_getitem_with_molang(self):
        assert (
            str(Molang("q.get_nearby_entities")[Molang("v.index")])
            == "q.get_nearby_entities[v.index]"
        )

    # --- _query string-quoting rules ---

    def test_query_molang_prefix_not_quoted(self):
        assert (
            str(Molang("q").__query__("q", "test", "q.some_query"))
            == "q.test(q.some_query)"
        )

    def test_query_plain_string_quoted(self):
        assert (
            str(Molang("q").__query__("q", "test", "some_tag")) == "q.test('some_tag')"
        )

    def test_query_none_args_filtered(self):
        assert str(Molang("q").__query__("q", "test", 1, None, 3)) == "q.test(1, 3)"

    # --- type / inheritance ---

    def test_is_str_subclass(self):
        assert isinstance(Molang("q.health"), str)

    def test_prefixes(self):
        assert Molang.prefixes == (
            "q.",
            "v.",
            "c.",
            "t.",
            "query.",
            "variable.",
            "context.",
            "temp.",
            "math.",
        )

    # --- static constants ---

    def test_THIS(self):
        assert str(Molang.this) == "this"

    def test_BREAK(self):
        assert str(Molang.break_) == "break"

    def test_CONTINUE(self):
        assert str(Molang.continue_) == "continue"

    # --- static methods ---

    def test_molang_arrow(self):
        result = Molang.molang_arrow(
            Molang("context.owning_entity"), Molang("q.health")
        )
        assert str(result) == "(context.owning_entity) -> (q.health)"
        assert isinstance(result, Molang)

    def test_molang_arrow_string_args(self):
        assert (
            str(Molang.molang_arrow("context.other", "q.is_alive"))
            == "(context.other) -> (q.is_alive)"
        )

    def test_molang_condition_ternary(self):
        result = Molang.molang_condition(
            Molang("q.is_alive"), Molang("q.health"), Molang("0.0")
        )
        assert str(result) == "(q.is_alive ? q.health : 0.0)"
        assert isinstance(result, Molang)

    def test_molang_condition_binary(self):
        result = Molang.molang_condition(Molang("q.is_alive"), Molang("q.health"))
        assert str(result) == "(q.is_alive ? q.health)"
        assert isinstance(result, Molang)

    def test_molang_condition_string_args(self):
        assert (
            str(Molang.molang_condition("q.is_alive", "1.0", "0.0"))
            == "(q.is_alive ? 1.0 : 0.0)"
        )

    def test_molang_return(self):
        result = Molang.molang_return(Molang("q.health"))
        assert str(result) == "return q.health"
        assert isinstance(result, Molang)

    def test_molang_block(self):
        result = Molang.molang_block([Molang("v.x = 1"), Molang("v.y = 2")])
        assert str(result) == "{ v.x = 1; v.y = 2; }"
        assert isinstance(result, Molang)

    def test_molang_block_single(self):
        result = Molang.molang_block([Molang("v.x = 1")])
        assert str(result) == "{ v.x = 1; }"

    def test_molang_loop(self):
        result = Molang.molang_loop(10, [Molang("v.x = v.x + 1")])
        assert str(result) == "loop(10, { v.x = v.x + 1; })"
        assert isinstance(result, Molang)

    def test_molang_loop_multiple_statements(self):
        result = Molang.molang_loop(5, [Molang("v.x = 1"), Molang("v.y = 2")])
        assert str(result) == "loop(5, { v.x = 1; v.y = 2; })"

    def test_molang_for_each(self):
        result = Molang.molang_for_each(
            Molang("v.item"), Molang("array.items"), [Molang("v.x = 1")]
        )
        assert str(result) == "for_each(v.item, array.items, { v.x = 1; })"
        assert isinstance(result, Molang)


# ---------------------------------------------------------------------------
# Struct types
# ---------------------------------------------------------------------------


class TestVec3Struct:
    def test_x(self):
        assert str(_Vec3Struct("q.bone_origin").x) == "q.bone_origin.x"

    def test_y(self):
        assert str(_Vec3Struct("q.bone_origin").y) == "q.bone_origin.y"

    def test_z(self):
        assert str(_Vec3Struct("q.bone_origin").z) == "q.bone_origin.z"

    def test_is_molang(self):
        assert isinstance(_Vec3Struct("q.bone_origin"), Molang)


class TestAabbStruct:
    def test_min(self):
        aabb = _AabbStruct("q.bone_aabb")
        assert isinstance(aabb.min, _Vec3Struct)
        assert str(aabb.min) == "q.bone_aabb.min"

    def test_max(self):
        aabb = _AabbStruct("q.bone_aabb")
        assert isinstance(aabb.max, _Vec3Struct)
        assert str(aabb.max) == "q.bone_aabb.max"

    def test_min_components(self):
        aabb = _AabbStruct("q.bone_aabb")
        assert str(aabb.min.x) == "q.bone_aabb.min.x"
        assert str(aabb.min.y) == "q.bone_aabb.min.y"
        assert str(aabb.min.z) == "q.bone_aabb.min.z"

    def test_max_components(self):
        assert str(_AabbStruct("q.bone_aabb").max.x) == "q.bone_aabb.max.x"


class TestColorStruct:
    def test_components(self):
        c = _ColorStruct("q.spellcolor")
        assert str(c.r) == "q.spellcolor.r"
        assert str(c.g) == "q.spellcolor.g"
        assert str(c.b) == "q.spellcolor.b"
        assert str(c.a) == "q.spellcolor.a"


class TestUVStruct:
    def test_components(self):
        uv = _UVStruct("q.surface_particle_texture_coordinate")
        assert str(uv.u) == "q.surface_particle_texture_coordinate.u"
        assert str(uv.v) == "q.surface_particle_texture_coordinate.v"


class TestTRSStruct:
    def test_translation(self):
        trs = _TRSStruct("q.bone_orientation_trs")
        assert isinstance(trs.translation, _Vec3Struct)
        assert str(trs.translation) == "q.bone_orientation_trs.t"

    def test_rotation(self):
        trs = _TRSStruct("q.bone_orientation_trs")
        assert isinstance(trs.rotation, _Vec3Struct)
        assert str(trs.rotation) == "q.bone_orientation_trs.r"

    def test_scale(self):
        trs = _TRSStruct("q.bone_orientation_trs")
        assert isinstance(trs.scale, _Vec3Struct)
        assert str(trs.scale) == "q.bone_orientation_trs.s"

    def test_nested(self):
        assert (
            str(_TRSStruct("q.bone_orientation_trs").rotation.x)
            == "q.bone_orientation_trs.r.x"
        )


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------


class TestQuery:
    def test_is_molang_subclass(self):
        assert issubclass(Query, Molang)

    # --- no-argument methods ---

    @pytest.mark.parametrize(
        "method, expected",
        [
            ("ActorCount", "q.actor_count"),
            ("AllAnimationsFinished", "q.all_animations_finished"),
            ("AnyAnimationFinished", "q.any_animation_finished"),
            ("AngerLevel", "q.anger_level"),
            ("AnimTime", "q.anim_time"),
            ("BaseSwingDuration", "q.base_swing_duration"),
            ("BlockFace", "q.block_face"),
            ("Blocking", "q.blocking"),
            ("BodyXRotation", "q.body_x_rotation"),
            ("BodyYRotation", "q.body_y_rotation"),
            ("CanClimb", "q.can_climb"),
            ("CanDamageNearbyMobs", "q.can_damage_nearby_mobs"),
            ("CanFly", "q.can_fly"),
            ("CanPowerJump", "q.can_power_jump"),
            ("CanSwim", "q.can_swim"),
            ("CanWalk", "q.can_walk"),
            ("CapeFlapAmount", "q.cape_flap_amount"),
            ("CardinalBlockFacePlacedOn", "q.cardinal_block_face_placed_on"),
            ("CardinalFacing", "q.cardinal_facing"),
            ("CardinalFacing2D", "q.cardinal_facing_2d"),
            ("CardinalPlayerFacing", "q.cardinal_player_facing"),
            ("CombineEntities", "q.combine_entities"),
            ("CurrentSquishValue", "q.current_squish_value"),
            ("Day", "q.day"),
            ("DeathTicks", "q.death_ticks"),
            ("DebugOutput", "q.debug_output"),
            ("DeltaTime", "q.delta_time"),
            ("DistanceFromCamera", "q.distance_from_camera"),
            ("EffectEmitterCount", "q.effect_emitter_count"),
            ("EffectParticleCount", "q.effect_particle_count"),
            ("EquipmentCount", "q.equipment_count"),
            ("EyeTargetXRotation", "q.eye_target_x_rotation"),
            ("EyeTargetYRotation", "q.eye_target_y_rotation"),
            ("FacingTargetToRangeAttack", "q.facing_target_to_range_attack"),
            ("FrameAlpha", "q.frame_alpha"),
            ("FuseTime", "q.fuse_time"),
            ("GetActorInfoId", "q.get_actor_info_id"),
            ("GetAnimationFrame", "q.get_animation_frame"),
            ("GetDefaultBonePivot", "q.get_default_bone_pivot"),
            ("GetLocatorOffset", "q.get_locator_offset"),
            ("GetName", "q.get_name"),
            ("GetRootLocatorOffset", "q.get_root_locator_offset"),
            ("GroundSpeed", "q.ground_speed"),
            ("HasCape", "q.has_cape"),
            ("HasCollision", "q.has_collision"),
            ("HasGravity", "q.has_gravity"),
            ("HasOwner", "q.has_owner"),
            ("HasRider", "q.has_rider"),
            ("HasTarget", "q.has_target"),
            ("HeadRollAngle", "q.head_roll_angle"),
            ("Health", "q.health"),
            ("HeartbeatInterval", "q.heartbeat_interval"),
            ("HeartbeatPhase", "q.heartbeat_phase"),
            ("HurtDirection", "q.hurt_direction"),
            ("HurtTime", "q.hurt_time"),
            ("InvulnerableTicks", "q.invulnerable_ticks"),
            ("IsAdmiring", "q.is_admiring"),
            ("IsAlive", "q.is_alive"),
            ("IsAngry", "q.is_angry"),
            ("IsAttachedToEntity", "q.is_attached_to_entity"),
            ("IsAvoidingBlock", "q.is_avoiding_block"),
            ("IsAvoidingMobs", "q.is_avoiding_mobs"),
            ("IsBaby", "q.is_baby"),
            ("IsBreathing", "q.is_breathing"),
            ("IsBribed", "q.is_bribed"),
            ("IsCarryingBlock", "q.is_carrying_block"),
            ("IsCasting", "q.is_casting"),
            ("IsCelebrating", "q.is_celebrating"),
            ("IsCelebratingSpecial", "q.is_celebrating_special"),
            ("IsCharged", "q.is_charged"),
            ("IsCharging", "q.is_charging"),
            ("IsChested", "q.is_chested"),
            ("IsCritical", "q.is_critical"),
            ("IsCroaking", "q.is_croaking"),
            ("IsDancing", "q.is_dancing"),
            ("IsDelayedAttacking", "q.is_delayed_attacking"),
            ("IsDigging", "q.is_digging"),
            ("IsEating", "q.is_eating"),
            ("IsEatingMob", "q.is_eating_mob"),
            ("IsElder", "q.is_elder"),
            ("IsEmerging", "q.is_emerging"),
            ("IsEmoting", "q.is_emoting"),
            ("IsEnchanted", "q.is_enchanted"),
            ("IsFireImmune", "q.is_fire_immune"),
            ("IsFirstPerson", "q.is_first_person"),
            ("IsGhost", "q.is_ghost"),
            ("IsGliding", "q.is_gliding"),
            ("IsGrazing", "q.is_grazing"),
            ("IsIdling", "q.is_idling"),
            ("IsIgnited", "q.is_ignited"),
            ("IsIllagerCaptain", "q.is_illager_captain"),
            ("IsInContactWithWater", "q.is_in_contact_with_water"),
            ("IsInLove", "q.is_in_love"),
            ("IsInUI", "q.is_in_ui"),
            ("IsInWater", "q.is_in_water"),
            ("IsInWaterOrRain", "q.is_in_water_or_rain"),
            ("IsInterested", "q.is_interested"),
            ("IsInvisible", "q.is_invisible"),
            ("IsJumping", "q.is_jumping"),
            ("IsLayingDown", "q.is_laying_down"),
            ("IsLayingEgg", "q.is_laying_egg"),
            ("IsLeashed", "q.is_leashed"),
            ("IsLevitating", "q.is_levitating"),
            ("IsLingering", "q.is_lingering"),
            ("IsLocalPlayer", "q.is_local_player"),
            ("IsMoving", "q.is_moving"),
            ("IsOnFire", "q.is_on_fire"),
            ("IsOnGround", "q.is_on_ground"),
            ("IsOnScreen", "q.is_on_screen"),
            ("IsOnfire", "q.is_onfire"),
            ("IsOrphaned", "q.is_orphaned"),
            ("IsPersonaOrPremiumSkin", "q.is_persona_or_premium_skin"),
            ("IsPlayingDead", "q.is_playing_dead"),
            ("IsPowered", "q.is_powered"),
            ("IsPregnant", "q.is_pregnant"),
            ("IsRamAttacking", "q.is_ram_attacking"),
            ("IsResting", "q.is_resting"),
            ("IsRiding", "q.is_riding"),
            ("IsRoaring", "q.is_roaring"),
            ("IsRolling", "q.is_rolling"),
            ("IsSaddled", "q.is_saddled"),
            ("IsScared", "q.is_scared"),
            ("IsSelectedItem", "q.is_selected_item"),
            ("IsShaking", "q.is_shaking"),
            ("IsShakingWetness", "q.is_shaking_wetness"),
            ("IsSheared", "q.is_sheared"),
            ("IsShieldPowered", "q.is_shield_powered"),
            ("IsSilent", "q.is_silent"),
            ("IsSitting", "q.is_sitting"),
            ("IsSleeping", "q.is_sleeping"),
            ("IsSneaking", "q.is_sneaking"),
            ("IsSneezing", "q.is_sneezing"),
            ("IsSniffing", "q.is_sniffing"),
            ("IsSonicBoom", "q.is_sonic_boom"),
            ("IsSprinting", "q.is_sprinting"),
            ("IsStackable", "q.is_stackable"),
            ("IsStalking", "q.is_stalking"),
            ("IsStanding", "q.is_standing"),
            ("IsStunned", "q.is_stunned"),
            ("IsSwimming", "q.is_swimming"),
            ("IsTamed", "q.is_tamed"),
            ("IsTransforming", "q.is_transforming"),
            ("IsUsingItem", "q.is_using_item"),
            ("IsWallClimbing", "q.is_wall_climbing"),
            ("IsAttached", "q.is_attached"),
            ("IsSpectator", "q.is_spectator"),
            ("KeyFrameLerpTime", "q.key_frame_lerp_time"),
            ("LastHitByPlayer", "q.last_hit_by_player"),
            ("LieAmount", "q.lie_amount"),
            ("LifeSpan", "q.life_span"),
            ("LifeTime", "q.life_time"),
            ("MainHandItemMaxDuration", "q.main_hand_item_max_duration"),
            ("MainHandItemUseDuration", "q.main_hand_item_use_duration"),
            ("MarkVariant", "q.mark_variant"),
            ("MaxDurability", "q.max_durability"),
            ("MaxHealth", "q.max_health"),
            ("MaxTradeTier", "q.max_trade_tier"),
            ("ModelScale", "q.model_scale"),
            ("ModifiedDistanceMoved", "q.modified_distance_moved"),
            ("ModifiedMoveSpeed", "q.modified_move_speed"),
            ("ModifierSwingDuration", "q.modifier_swing_duration"),
            ("MoonBrightness", "q.moon_brightness"),
            ("MoonPhase", "q.moon_phase"),
            ("Noise", "q.noise"),
            ("OnFireTime", "q.on_fire_time"),
            ("OutOfControl", "q.out_of_control"),
            ("OverlayAlpha", "q.overlay_alpha"),
            ("OwnerIdentifier", "q.owner_identifier"),
            ("PlayerLevel", "q.player_level"),
            ("PreviousSquishValue", "q.previous_squish_value"),
            ("RemainingDurability", "q.remaining_durability"),
            ("RollCounter", "q.roll_counter"),
            ("ShakeAngle", "q.shake_angle"),
            ("ShakeTime", "q.shake_time"),
            ("ShieldBlockingBob", "q.shield_blocking_bob"),
            ("ShowBottom", "q.show_bottom"),
            ("SitAmount", "q.sit_amount"),
            ("SkinId", "q.skin_id"),
            ("SleepRotation", "q.sleep_rotation"),
            ("SneezeCounter", "q.sneeze_counter"),
            ("StandingScale", "q.standing_scale"),
            ("StructuralIntegrity", "q.structural_integrity"),
            ("SwellAmount", "q.swell_amount"),
            ("SwellingDir", "q.swelling_dir"),
            ("SwimAmount", "q.swim_amount"),
            ("TailAngle", "q.tail_angle"),
            ("TargetXRotation", "q.target_x_rotation"),
            ("TargetYRotation", "q.target_y_rotation"),
            ("TextureFrameIndex", "q.texture_frame_index"),
            ("TimeOfDay", "q.time_of_day"),
            (
                "TimeSinceLastVibrationDetection",
                "q.time_since_last_vibration_detection",
            ),
            ("TimeStamp", "q.time_stamp"),
            ("TimerFlag1", "q.timer_flag_1"),
            ("TimerFlag2", "q.timer_flag_2"),
            ("TimerFlag3", "q.timer_flag_3"),
            ("TotalEmitterCount", "q.total_emitter_count"),
            ("TotalParticleCount", "q.total_particle_count"),
            ("TradeTier", "q.trade_tier"),
            ("UnhappyCounter", "q.unhappy_counter"),
            ("Variant", "q.variant"),
            ("VerticalSpeed", "q.vertical_speed"),
            ("WalkDistance", "q.walk_distance"),
            ("WingFlapPosition", "q.wing_flap_position"),
            ("WingFlapSpeed", "q.wing_flap_speed"),
            ("YawSpeed", "q.yaw_speed"),
            ("HasPlayerRider", "q.has_player_rider"),
            ("RideBodyXRotation", "q.ride_body_x_rotation"),
            ("RideBodyYRotation", "q.ride_body_y_rotation"),
            ("RideHeadXRotation", "q.ride_head_x_rotation"),
            ("ClientMemoryTier", "q.client_memory_tier"),
            ("ServerMemoryTier", "q.server_memory_tier"),
            ("ClientMaxRenderDistance", "q.client_max_render_distance"),
            ("TouchOnlyAffectsHotbar", "q.touch_only_affects_hotbar"),
            ("StateTime", "q.state_time"),
            ("get_level_seed_based_fraction", "q.get_level_seed_based_fraction"),
            ("GetKineticItemDelay", "q.get_kinetic_item_delay"),
            ("GetKineticItemDamageDuration", "q.get_kinetic_item_damage_duration"),
            (
                "GetKineticItemKnockbackDuration",
                "q.get_kinetic_item_knockback_duration",
            ),
            ("GetKineticItemDismountDuration", "q.get_kinetic_item_dismount_duration"),
            ("KineticWeaponDelay", "q.kinetic_weapon_delay"),
            ("KineticWeaponDamageDuration", "q.kinetic_weapon_damage_duration"),
            ("KineticWeaponKnockbackDuration", "q.kinetic_weapon_knockback_duration"),
            ("KineticWeaponDismountDuration", "q.kinetic_weapon_dismount_duration"),
            ("TicksSinceLastKineticWeaponHit", "q.ticks_since_last_kinetic_weapon_hit"),
        ],
    )
    def test_query_output(self, method, expected):
        result = getattr(Query, method)()
        assert str(result) == expected
        assert isinstance(result, Molang)

    # --- methods with arguments ---

    def test_AboveTopSolid(self):
        assert str(Query.AboveTopSolid(10, 20)) == "q.above_top_solid(10, 20)"

    def test_All_raises_with_too_few_args(self):
        with pytest.raises(ValueError):
            Query.All(Molang("q.health"), Molang("q.max_health"))

    def test_All(self):
        result = Query.All(
            Molang("q.health"),
            Molang("q.max_health"),
            Molang("q.variant"),
            Molang("q.skin_id"),
        )
        assert str(result) == "q.all(q.health, q.max_health, q.variant, q.skin_id)"

    def test_AllTags(self):
        assert str(Query.AllTags("mob", "animal")) == "q.all_tags('mob', 'animal')"

    def test_Any(self):
        assert (
            str(Query.Any(Molang("q.variant"), Molang("q.skin_id")))
            == "q.any(q.variant, q.skin_id)"
        )

    def test_AnyTag(self):
        assert str(Query.AnyTag("mob")) == "q.any_tag('mob')"

    def test_ApproxEq(self):
        assert str(Query.ApproxEq(1, 2, 3)) == "q.approx_eq(1, 2, 3)"

    def test_ArmorColorSlot_clamps(self):
        assert str(Query.ArmorColorSlot(0, 0)) == "q.armor_color_slot(0, 0)"
        assert str(Query.ArmorColorSlot(5, 5)) == "q.armor_color_slot(3, 3)"

    def test_ArmorMaterialSlot(self):
        assert str(Query.ArmorMaterialSlot(1)) == "q.armor_material_slot(1)"

    def test_ArmorTextureSlot(self):
        assert str(Query.ArmorTextureSlot(2)) == "q.armor_texture_slot(2)"

    def test_AverageFrameTime_default(self):
        assert str(Query.AverageFrameTime()) == "q.average_frame_time(0)"

    def test_AverageFrameTime_clamped(self):
        assert str(Query.AverageFrameTime(50)) == "q.average_frame_time(30)"

    def test_BlockState_plain_string(self, mock_config):
        mock_config.NAMESPACE = "myns"
        assert str(Query.BlockState("open")) == "q.block_state('myns:open')"

    def test_BlockState_str_enum(self):
        class MyState(StrEnum):
            Open = "open"

        assert str(Query.BlockState(MyState.Open)) == "q.block_state('open')"

    def test_Property(self, mock_config):
        mock_config.NAMESPACE = "myns"
        assert str(Query.Property("stage")) == "q.property('myns:stage')"

    def test_HasProperty(self, mock_config):
        mock_config.NAMESPACE = "myns"
        assert str(Query.HasProperty("stage")) == "q.has_property('myns:stage')"

    def test_has_block_state(self, mock_config):
        mock_config.NAMESPACE = "myns"
        assert str(Query.has_block_state("open")) == "q.has_block_state('myns:open')"

    def test_BoneRotation_returns_Vec3Struct(self):
        result = Query.BoneRotation("rightarm")
        assert isinstance(result, _Vec3Struct)
        assert str(result) == "q.bone_rotation('rightarm')"

    def test_BoneOrigin_returns_Vec3Struct(self):
        result = Query.BoneOrigin()
        assert isinstance(result, _Vec3Struct)
        assert str(result) == "q.bone_origin"

    def test_BoneAabb_returns_AabbStruct(self):
        result = Query.BoneAabb()
        assert isinstance(result, _AabbStruct)
        assert str(result) == "q.bone_aabb"

    def test_BoneOrientationTrs_returns_TRSStruct(self):
        result = Query.BoneOrientationTrs("rightarm")
        assert isinstance(result, _TRSStruct)
        assert str(result) == "q.bone_orientation_trs('rightarm')"

    def test_BoneOrientationMatrix(self):
        assert (
            str(Query.BoneOrientationMatrix("leftarm"))
            == "q.bone_orientation_matrix('leftarm')"
        )

    def test_CameraDistanceRangeLerp(self):
        assert (
            str(Query.CameraDistanceRangeLerp(10, 20))
            == "q.camera_distance_range_lerp(10, 20)"
        )

    def test_CameraRotation_clamped(self):
        assert str(Query.CameraRotation(1)) == "q.camera_rotation(1)"
        assert str(Query.CameraRotation(5)) == "q.camera_rotation(1)"

    def test_Count(self):
        assert str(Query.Count(Molang("q.health"))) == "q.count(q.health)"

    def test_EquippedItemAllTags(self):
        assert (
            str(Query.EquippedItemAllTags(Slots.Mainhand, "sword"))
            == "q.equipped_item_all_tags('slot.weapon.mainhand', 'sword')"
        )

    def test_EquippedItemAnyTag(self):
        assert (
            str(Query.EquippedItemAnyTag(Slots.Offhand, "tool"))
            == "q.equipped_item_any_tag('slot.weapon.offhand', 'tool')"
        )

    def test_EquippedItemIsAttachable_clamped(self):
        assert (
            str(Query.EquippedItemIsAttachable()) == "q.equipped_item_is_attachable(0)"
        )
        assert (
            str(Query.EquippedItemIsAttachable(5)) == "q.equipped_item_is_attachable(1)"
        )

    def test_GetEquippedItemName_clamped(self):
        assert str(Query.GetEquippedItemName(0)) == "q.get_equipped_item_name(0, 0)"
        assert str(Query.GetEquippedItemName(5)) == "q.get_equipped_item_name(1, 0)"

    def test_HadComponentGroup(self):
        assert str(Query.HadComponentGroup("adult")) == "q.had_component_group('adult')"

    def test_HasAnyFamily(self):
        assert (
            str(Query.HasAnyFamily("mob", "animal"))
            == "q.has_any_family('mob', 'animal')"
        )

    def test_HasArmorSlot(self):
        assert (
            str(Query.HasArmorSlot(Slots.Head)) == "q.has_armor_slot('slot.armor.head')"
        )

    def test_HasBiomeTag(self):
        assert str(Query.HasBiomeTag("ocean")) == "q.has_biome_tag('ocean')"

    def test_HeadXRotation_default(self):
        assert str(Query.HeadXRotation()) == "q.head_x_rotation(0)"

    def test_HeadYRotation_default(self):
        assert str(Query.HeadYRotation()) == "q.head_y_rotation(0)"

    def test_Heightmap(self):
        assert str(Query.Heightmap(5, 10)) == "q.heightmap(5, 10)"

    def test_InRange(self):
        assert str(Query.InRange(5.0, 0.0, 10.0)) == "q.in_range(5.0, 0.0, 10.0)"

    def test_IsItemEquipped_clamped(self):
        assert str(Query.IsItemEquipped()) == "q.is_item_equipped(0)"
        assert str(Query.IsItemEquipped(9)) == "q.is_item_equipped(1)"

    def test_IsItemNameAny(self):
        result = Query.IsItemNameAny(Slots.Mainhand, 0, ["minecraft:sword"])
        assert (
            str(result)
            == "q.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:sword')"
        )

    def test_IsNameAny(self):
        assert str(Query.IsNameAny("Alice", "Bob")) == "q.is_name_any('Alice', 'Bob')"

    def test_IsOwnerIdentifierAny(self):
        assert (
            str(Query.IsOwnerIdentifierAny("minecraft:player"))
            == "q.is_owner_identifier_any('minecraft:player')"
        )

    def test_ItemInUseDuration(self):
        assert str(Query.ItemInUseDuration()) == "(q.item_in_use_duration / 200)"

    def test_ItemIsCharged_clamped(self):
        assert str(Query.ItemIsCharged()) == "q.item_is_charged(0)"

    def test_ItemMaxUseDuration(self):
        assert str(Query.ItemMaxUseDuration()) == "q.item_max_use_duration"

    def test_ItemRemainingUseDuration_default(self):
        assert (
            str(Query.ItemRemainingUseDuration()) == "q.item_remaining_use_duration(0)"
        )

    def test_ItemSlotToBoneName(self):
        assert (
            str(Query.ItemSlotToBoneName(Slots.Mainhand))
            == "q.item_slot_to_bone_name('slot.weapon.mainhand')"
        )

    def test_LastFrameTime_clamped(self):
        assert str(Query.LastFrameTime()) == "q.last_frame_time(0)"
        assert str(Query.LastFrameTime(100)) == "q.last_frame_time(30)"

    def test_LodIndex(self):
        assert str(Query.LodIndex(10, 20, 30)) == "q.lod_index(10, 20, 30)"

    def test_Log(self):
        assert str(Query.Log(Molang("q.health"))) == "q.log(q.health)"

    def test_MaximumFrameTime_clamped(self):
        assert str(Query.MaximumFrameTime()) == "q.maximum_frame_time(0)"
        assert str(Query.MaximumFrameTime(99)) == "q.maximum_frame_time(30)"

    def test_MinimumFrameTime_default(self):
        assert str(Query.MinimumFrameTime()) == "q.minimum_frame_time(0)"

    def test_MovementDirection(self):
        assert str(Query.MovementDirection(1)) == "q.movement_direction(1)"

    def test_Position_clamped(self):
        assert str(Query.Position(2)) == "q.position(2)"
        assert str(Query.Position(5)) == "q.position(2)"

    def test_PositionDelta(self):
        assert str(Query.PositionDelta(1)) == "q.position_delta(1)"

    def test_RotationToCamera_clamped(self):
        assert str(Query.RotationToCamera(0)) == "q.rotation_to_camera(0)"
        assert str(Query.RotationToCamera(9)) == "q.rotation_to_camera(1)"

    def test_Scoreboard(self):
        assert str(Query.Scoreboard("kills")) == "q.scoreboard('kills')"

    def test_Spellcolor_returns_ColorStruct(self):
        result = Query.Spellcolor()
        assert isinstance(result, _ColorStruct)
        assert str(result) == "q.spellcolor"

    def test_SurfaceParticleColor_returns_ColorStruct(self):
        assert isinstance(Query.SurfaceParticleColor(), _ColorStruct)

    def test_SurfaceParticleTextureCoordinate_returns_UVStruct(self):
        assert isinstance(Query.SurfaceParticleTextureCoordinate(), _UVStruct)

    def test_SurfaceParticleTextureSize_returns_UVStruct(self):
        assert isinstance(Query.SurfaceParticleTextureSize(), _UVStruct)

    def test_RideHeadYRotation_default(self):
        assert str(Query.RideHeadYRotation()) == "q.ride_head_y_rotation(0)"

    def test_RiderBodyXRotation_default(self):
        assert str(Query.RiderBodyXRotation()) == "q.rider_body_x_rotation(0)"

    def test_RiderBodyYRotation_default(self):
        assert str(Query.RiderBodyYRotation()) == "q.rider_body_y_rotation(0)"

    def test_RiderHeadXRotation_default(self):
        assert str(Query.RiderHeadXRotation()) == "q.rider_head_x_rotation(0)"

    def test_RiderHeadYRotation_default(self):
        assert str(Query.RiderHeadYRotation()) == "q.rider_head_y_rotation(0, 0)"

    def test_ArmorSlotDamage(self):
        assert (
            str(Query.ArmorSlotDamage(Slots.Head))
            == "q.armor_slot_damage('slot.armor.head', 0)"
        )

    def test_LastInputModeIsAny(self):
        assert (
            str(Query.LastInputModeIsAny(InputModes.Gamepad))
            == "q.last_input_mode_is_any('gamepad')"
        )

    def test_IsCooldownCategory(self):
        result = Query.IsCooldownCategory("attack", Slots.Mainhand)
        assert (
            str(result) == "q.is_cooldown_category('attack', 'slot.weapon.mainhand', 0)"
        )

    def test_CooldownTime(self):
        assert (
            str(Query.CooldownTime(Slots.Mainhand))
            == "q.cooldown_time('slot.weapon.mainhand', 0)"
        )

    def test_CooldownTimeRemaining_with_slot(self):
        assert (
            str(Query.CooldownTimeRemaining(Slots.Mainhand))
            == "q.cooldown_time_remaining('slot.weapon.mainhand')"
        )

    def test_CooldownTimeRemaining_with_name(self):
        assert (
            str(Query.CooldownTimeRemaining("attack"))
            == "q.cooldown_time_remaining('attack')"
        )

    def test_RelativeBlockHasAnyTags(self):
        assert (
            str(Query.RelativeBlockHasAnyTags(0, -1, 0, "stone"))
            == "q.relative_block_has_any_tags(0, -1, 0, 'stone')"
        )

    def test_RelativeBlockHasAllTags(self):
        assert (
            str(Query.RelativeBlockHasAllTags(1, 0, 0, "wood", "plank"))
            == "q.relative_block_has_all_tags(1, 0, 0, 'wood', 'plank')"
        )

    def test_BlockNeighborHasAnyTags(self):
        assert (
            str(Query.BlockNeighborHasAnyTags(0, 1, 0, "solid"))
            == "q.block_neighbor_has_any_tags(0, 1, 0, 'solid')"
        )

    def test_BlockNeighborHasAllTags(self):
        assert (
            str(Query.BlockNeighborHasAllTags(0, 0, 1, "stone", "solid"))
            == "q.block_neighbor_has_all_tags(0, 0, 1, 'stone', 'solid')"
        )

    def test_BlockHasAllTags(self):
        assert (
            str(Query.BlockHasAllTags(10, 64, -5, "dirt"))
            == "q.block_has_all_tags(10, 64, -5, 'dirt')"
        )

    def test_BlockHasAnyTags(self):
        assert (
            str(Query.BlockHasAnyTags(0, 0, 0, "lava", "fire"))
            == "q.block_has_any_tags(0, 0, 0, 'lava', 'fire')"
        )

    def test_EntityBiomeHasAllTags(self):
        assert (
            str(Query.EntityBiomeHasAllTags(("ocean", "deep")))
            == "q.entity_biome_has_all_tags('ocean', 'deep')"
        )

    def test_EntityBiomeHasAnyTags(self):
        assert (
            str(Query.EntityBiomeHasAnyTags(("forest",)))
            == "q.entity_biome_has_any_tags('forest')"
        )


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------


class TestContext:
    def test_is_query_subclass(self):
        assert issubclass(Context, Query)

    def test_handle(self):
        assert Context.handle == "context"

    def test_ItemSlot(self):
        assert str(Context.ItemSlot()) == "context.item_slot"

    def test_OwningEntity(self):
        assert str(Context.OwningEntity(None)) == "context.owning_entity"

    def test_OwningEntity_arrow(self):
        assert (
            str(Context.OwningEntity(Molang("q.health")))
            == "(context.owning_entity) -> (q.health)"
        )

    def test_Other(self):
        assert str(Context.Other(None)) == "context.other"

    def test_Other_arrow(self):
        assert (
            str(Context.Other(Molang("q.is_alive")))
            == "(context.other) -> (q.is_alive)"
        )


# ---------------------------------------------------------------------------
# Variable
# ---------------------------------------------------------------------------


class TestVariable:
    def test_is_molang_subclass(self):
        assert issubclass(Variable, Molang)

    def test_handle(self):
        assert Variable.handle == "v"

    def test_IsFirstPerson(self):
        assert str(Variable.IsFirstPerson()) == "v.is_first_person"

    def test_IsPaperdoll(self):
        assert str(Variable.IsPaperdoll()) == "v.is_paperdoll"

    def test_AttackTime(self):
        assert str(Variable.AttackTime()) == "v.attack_time"


# ---------------------------------------------------------------------------
# TempVar
# ---------------------------------------------------------------------------


class TestTempVar:
    def test_is_molang_subclass(self):
        assert issubclass(TempVar, Molang)

    def test_handle(self):
        assert TempVar.handle == "t"

    def test_dynamic_attribute(self):
        assert str(TempVar.my_counter) == "t.my_counter"

    def test_dynamic_attribute_cached(self):
        first = TempVar.some_value
        second = TempVar.some_value
        assert str(first) == str(second) == "t.some_value"

    def test_private_attribute_raises(self):
        with pytest.raises(AttributeError):
            _ = TempVar._private


# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------


class TestMath:
    def test_is_molang_subclass(self):
        assert issubclass(Math, Molang)

    @pytest.mark.parametrize(
        "method, args, expected",
        [
            ("abs", (Molang("q.health"),), "math.abs(q.health)"),
            ("acos", (Molang("q.health"),), "math.acos(q.health)"),
            ("asin", (Molang("q.health"),), "math.asin(q.health)"),
            ("atan", (Molang("q.health"),), "math.atan(q.health)"),
            ("atan2", (Molang("q.y"), Molang("q.x")), "math.atan2(q.y, q.x)"),
            ("ceil", (Molang("q.health"),), "math.ceil(q.health)"),
            ("clamp", (Molang("q.health"), 0, 20), "math.clamp(q.health, 0, 20)"),
            ("cos", (Molang("q.anim_time"),), "math.cos(q.anim_time)"),
            ("die_roll", (3, 1, 6), "math.die_roll(3, 1, 6)"),
            ("die_roll_integer", (2, 1, 4), "math.die_roll_integer(2, 1, 4)"),
            ("exp", (Molang("q.health"),), "math.exp(q.health)"),
            ("floor", (Molang("q.health"),), "math.floor(q.health)"),
            (
                "hermite_blend",
                (Molang("q.anim_time"),),
                "math.hermite_blend(q.anim_time)",
            ),
            ("ln", (Molang("q.health"),), "math.ln(q.health)"),
            ("max", (Molang("q.health"), 10), "math.max(q.health, 10)"),
            ("min", (Molang("q.health"), 5), "math.min(q.health, 5)"),
            ("min_angle", (Molang("q.anim_time"),), "math.min_angle(q.anim_time)"),
            ("mod", (Molang("q.health"), 10), "math.mod(q.health, 10)"),
            ("pi", (), "math.pi"),
            ("pow", (Molang("q.health"), 2), "math.pow(q.health, 2)"),
            ("random", (0, 1), "math.random(0, 1)"),
            ("random_integer", (1, 6), "math.random_integer(1, 6)"),
            ("round", (Molang("q.health"),), "math.round(q.health)"),
            ("sin", (Molang("q.anim_time"),), "math.sin(q.anim_time)"),
            ("sqrt", (Molang("q.health"),), "math.sqrt(q.health)"),
            ("trunc", (Molang("q.health"),), "math.trunc(q.health)"),
            (
                "inverse_lerp",
                (0, 100, Molang("q.health")),
                "math.inverse_lerp(0, 100, q.health)",
            ),
            (
                "ease_in_quad",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_quad(0, 1, q.anim_time)",
            ),
            (
                "ease_out_quad",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_quad(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_quad",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_quad(0, 1, q.anim_time)",
            ),
            (
                "ease_in_cubic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_cubic(0, 1, q.anim_time)",
            ),
            (
                "ease_out_cubic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_cubic(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_cubic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_cubic(0, 1, q.anim_time)",
            ),
            (
                "ease_in_quart",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_quart(0, 1, q.anim_time)",
            ),
            (
                "ease_out_quart",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_quart(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_quart",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_quart(0, 1, q.anim_time)",
            ),
            (
                "ease_in_quint",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_quint(0, 1, q.anim_time)",
            ),
            (
                "ease_out_quint",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_quint(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_quint",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_quint(0, 1, q.anim_time)",
            ),
            (
                "ease_in_sine",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_sine(0, 1, q.anim_time)",
            ),
            (
                "ease_out_sine",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_sine(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_sine",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_sine(0, 1, q.anim_time)",
            ),
            (
                "ease_in_expo",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_expo(0, 1, q.anim_time)",
            ),
            (
                "ease_out_expo",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_expo(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_expo",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_expo(0, 1, q.anim_time)",
            ),
            (
                "ease_in_circ",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_circ(0, 1, q.anim_time)",
            ),
            (
                "ease_out_circ",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_circ(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_circ",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_circ(0, 1, q.anim_time)",
            ),
            (
                "ease_in_bounce",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_bounce(0, 1, q.anim_time)",
            ),
            (
                "ease_out_bounce",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_bounce(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_bounce",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_bounce(0, 1, q.anim_time)",
            ),
            (
                "ease_in_back",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_back(0, 1, q.anim_time)",
            ),
            (
                "ease_out_back",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_back(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_back",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_back(0, 1, q.anim_time)",
            ),
            (
                "ease_in_elastic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_elastic(0, 1, q.anim_time)",
            ),
            (
                "ease_out_elastic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_out_elastic(0, 1, q.anim_time)",
            ),
            (
                "ease_in_out_elastic",
                (0, 1, Molang("q.anim_time")),
                "math.ease_in_out_elastic(0, 1, q.anim_time)",
            ),
        ],
    )
    def test_math_output(self, method, args, expected):
        result = getattr(Math, method)(*args)
        assert str(result) == expected
        assert isinstance(result, Molang)

    def test_lerp_clamps_float_factor(self):
        assert str(Math.lerp(0, 100, 1.5)) == "math.lerp(0, 100, 1)"

    def test_lerp_passes_molang_factor_unchanged(self):
        assert (
            str(Math.lerp(0, 100, Molang("q.anim_time")))
            == "math.lerp(0, 100, q.anim_time)"
        )

    def test_lerprotate_clamps_float_factor(self):
        assert str(Math.lerprotate(0, 360, -0.5)) == "math.lerprotate(0, 360, 0)"

    def test_lerprotate_passes_molang_factor_unchanged(self):
        assert (
            str(Math.lerprotate(0, 360, Molang("q.anim_time")))
            == "math.lerprotate(0, 360, q.anim_time)"
        )


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


def test_molang_conditions():
    result = molang_conditions(Molang("q.is_alive"), Molang("q.health"), Molang("0.0"))
    assert str(result) == "(q.is_alive ? q.health : 0.0)"
    assert isinstance(result, Molang)


def test_molang_conditions_string_args():
    assert (
        str(molang_conditions("q.is_alive", "1.0", "0.0")) == "(q.is_alive ? 1.0 : 0.0)"
    )


def test_arrow_operator():
    assert (
        arrow_operator("context.owning_entity", "q.health")
        == "(context.owning_entity) -> (q.health)"
    )


def test_arrow_operator_with_molang():
    assert (
        arrow_operator(Molang("context.other"), Molang("q.is_alive"))
        == "(context.other) -> (q.is_alive)"
    )
