"""Tests for anvil/lib/lib.py utilities not yet covered by test_lib.py."""
import os
import zipfile

import pytest

from anvil.lib.lib import (
    AnvilFormatter,
    AnvilValidator,
    AnvilArchive,
    AnvilIO,
    clamp,
    frange,
    salt_from_str,
)
from anvil.api.core.types import RGB, RGBA, RGB255, RGBA255, HexRGB, HexRGBA


# ---------------------------------------------------------------------------
# clamp
# ---------------------------------------------------------------------------

class TestClamp:
    def test_below_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_above_max(self):
        assert clamp(15, 0, 10) == 10

    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_at_min(self):
        assert clamp(0, 0, 10) == 0

    def test_at_max(self):
        assert clamp(10, 0, 10) == 10

    def test_float(self):
        assert clamp(1.5, 0.0, 1.0) == 1.0


# ---------------------------------------------------------------------------
# frange
# ---------------------------------------------------------------------------

class TestFrange:
    def test_two_values(self):
        result = frange(0, 10, 2)
        assert len(result) == 2
        assert result[0] == 0
        assert result[1] == 10.0

    def test_three_values(self):
        result = frange(0, 10, 3)
        assert len(result) == 3
        assert result[0] == 0
        assert result[2] == 10.0

    def test_midpoint(self):
        result = frange(0, 10, 3)
        assert result[1] == 5.0


# ---------------------------------------------------------------------------
# salt_from_str
# ---------------------------------------------------------------------------

class TestSaltFromStr:
    def test_deterministic(self):
        assert salt_from_str("hello") == salt_from_str("hello")

    def test_different_strings(self):
        assert salt_from_str("hello") != salt_from_str("world")

    def test_returns_int(self):
        assert isinstance(salt_from_str("test"), int)

    def test_empty_string(self):
        assert salt_from_str("") == 0

    def test_range(self):
        assert 0 <= salt_from_str("anything") < 1_000_000


# ---------------------------------------------------------------------------
# AnvilFormatter.min_max_dict / min_max_list
# ---------------------------------------------------------------------------

class TestAnvilFormatterMinMax:
    def test_min_max_dict_normal(self):
        result = AnvilFormatter.min_max_dict([2, 8], "test")
        assert result == {"min": 2, "max": 8}

    def test_min_max_dict_auto_swap(self):
        result = AnvilFormatter.min_max_dict([8, 2], "test")
        assert result == {"min": 2, "max": 8}

    def test_min_max_dict_clamp_min(self):
        result = AnvilFormatter.min_max_dict([-5, 5], "test", clamp_min=0)
        assert result["min"] == 0

    def test_min_max_dict_clamp_max(self):
        result = AnvilFormatter.min_max_dict([0, 20], "test", clamp_max=10)
        assert result["max"] == 10

    def test_min_max_dict_invalid_not_pair(self):
        with pytest.raises(ValueError):
            AnvilFormatter.min_max_dict([1, 2, 3], "test")

    def test_min_max_dict_invalid_type(self):
        with pytest.raises(ValueError):
            AnvilFormatter.min_max_dict(["a", "b"], "test")

    def test_min_max_list_normal(self):
        result = AnvilFormatter.min_max_list([3, 7], "test")
        assert result == [3, 7]

    def test_min_max_list_auto_swap(self):
        result = AnvilFormatter.min_max_list([7, 3], "test")
        assert result == [3, 7]

    def test_range_min_max_dict_scalar(self):
        result = AnvilFormatter.range_min_max_dict(5, "test")
        assert result == {"range_min": 5, "range_max": 5}

    def test_range_min_max_dict_tuple(self):
        result = AnvilFormatter.range_min_max_dict((1, 9), "test")
        assert result == {"range_min": 1, "range_max": 9}


# ---------------------------------------------------------------------------
# AnvilFormatter.convert_color
# ---------------------------------------------------------------------------

class TestConvertColor:
    def test_hex_to_rgb(self):
        result = AnvilFormatter.convert_color("#FF0000", RGB)
        assert result == pytest.approx((1.0, 0.0, 0.0))

    def test_hex_to_rgba(self):
        result = AnvilFormatter.convert_color("#FF0000FF", RGBA)
        assert result == pytest.approx((1.0, 0.0, 0.0, 1.0))

    def test_hex_shorthand_rgb(self):
        result = AnvilFormatter.convert_color("#F00", RGB)
        assert result == pytest.approx((1.0, 0.0, 0.0))

    def test_hex_shorthand_rgba(self):
        result = AnvilFormatter.convert_color("#F00F", RGBA)
        assert result == pytest.approx((1.0, 0.0, 0.0, 1.0))

    def test_rgb_float_to_hex_rgb(self):
        result = AnvilFormatter.convert_color((1.0, 0.0, 0.0), HexRGB)
        assert result == "#ff0000"

    def test_rgb_float_to_hex_rgba(self):
        result = AnvilFormatter.convert_color((1.0, 0.0, 0.0), HexRGBA)
        assert result == "#ff0000ff"

    def test_rgb255_to_rgb(self):
        result = AnvilFormatter.convert_color((255, 0, 0), RGB)
        assert result == pytest.approx((1.0, 0.0, 0.0))

    def test_rgb_to_rgba_adds_alpha(self):
        result = AnvilFormatter.convert_color((0.5, 0.5, 0.5), RGBA)
        assert len(result) == 4
        assert result[3] == pytest.approx(1.0)

    def test_hex_missing_hash(self):
        with pytest.raises(ValueError, match="must start with"):
            AnvilFormatter.convert_color("FF0000", RGB)

    def test_hex_wrong_length(self):
        with pytest.raises(ValueError):
            AnvilFormatter.convert_color("#12", RGB)
        with pytest.raises(ValueError):
            AnvilFormatter.convert_color("#FF00F", RGB)

    def test_tuple_wrong_length(self):
        with pytest.raises(ValueError):
            AnvilFormatter.convert_color((1.0, 0.0), RGB)

    def test_unsupported_type(self):
        with pytest.raises(TypeError):
            AnvilFormatter.convert_color(12345, RGB)

    def test_hex_no_target_normalises(self):
        result = AnvilFormatter.convert_color("#F00")
        assert result == "#ff0000"

    def test_tuple_no_target_rgb255(self):
        result = AnvilFormatter.convert_color((128, 0, 0))
        assert isinstance(result, tuple)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# AnvilValidator.is_color_value
# ---------------------------------------------------------------------------

class TestIsColorValue:
    def test_rgb_float(self):
        assert AnvilValidator.is_color_value((0.5, 0.5, 0.5)) is True

    def test_rgba_float(self):
        assert AnvilValidator.is_color_value((0.5, 0.5, 0.5, 1.0)) is True

    def test_rgb255(self):
        assert AnvilValidator.is_color_value((128, 64, 32)) is True

    def test_hex_string(self):
        assert AnvilValidator.is_color_value("#FF0000") is True

    def test_hex_short(self):
        assert AnvilValidator.is_color_value("#F00") is True

    def test_plain_string(self):
        assert AnvilValidator.is_color_value("my_texture") is False

    def test_none(self):
        assert AnvilValidator.is_color_value(None) is False

    def test_wrong_tuple_length(self):
        assert AnvilValidator.is_color_value((0.5,)) is False


# ---------------------------------------------------------------------------
# AnvilValidator.validate_namespace_project_name
# ---------------------------------------------------------------------------

class TestValidateNamespace:
    def test_valid(self):
        AnvilValidator.validate_namespace_project_name("stark", "my_project")

    def test_reserved_minecraft(self):
        with pytest.raises(ValueError, match="reserved"):
            AnvilValidator.validate_namespace_project_name("minecraft", "test")

    def test_namespace_too_long(self):
        with pytest.raises(ValueError, match="8 characters"):
            AnvilValidator.validate_namespace_project_name("verylongnamespace", "test")

    def test_project_name_too_long(self):
        with pytest.raises(ValueError, match="16 characters"):
            AnvilValidator.validate_namespace_project_name("stark", "a_very_long_project_name_here")

    def test_addon_valid_suffix(self):
        # project_name="my_project" -> initials="MP" -> namespace must end with "_mp"
        AnvilValidator.validate_namespace_project_name("stark_mp", "my_project", is_addon=True)

    def test_addon_wrong_suffix(self):
        with pytest.raises(ValueError, match="unique"):
            AnvilValidator.validate_namespace_project_name("stark", "my_project", is_addon=True)


# ---------------------------------------------------------------------------
# AnvilArchive.from_mapping
# ---------------------------------------------------------------------------

class TestAnvilArchive:
    def test_creates_zip(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "hello.txt").write_text("hello")

        zip_path = str(tmp_path / "out.zip")
        AnvilArchive.from_mapping(zip_path, {str(src): "content"})

        assert os.path.exists(zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert any("hello.txt" in n for n in names)

    def test_excludes_js_map(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "main.js").write_text("code")
        (src / "main.js.map").write_text("sourcemap")

        zip_path = str(tmp_path / "out.zip")
        AnvilArchive.from_mapping(zip_path, {str(src): "scripts"})

        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        map_names = [n for n in names if n.endswith(".map")]
        assert len(map_names) == 0

    def test_single_file(self, tmp_path):
        src_file = tmp_path / "data.json"
        src_file.write_text('{"key": "value"}')

        zip_path = str(tmp_path / "out.zip")
        AnvilArchive.from_mapping(zip_path, {str(src_file): "root"})

        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert any("data.json" in n for n in names)

    def test_nested_directory(self, tmp_path):
        src = tmp_path / "src"
        nested = src / "sub"
        nested.mkdir(parents=True)
        (nested / "file.txt").write_text("nested")

        zip_path = str(tmp_path / "out.zip")
        AnvilArchive.from_mapping(zip_path, {str(src): "root"})

        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
        assert any("file.txt" in n for n in names)


# ---------------------------------------------------------------------------
# AnvilIO._normalize_json_like
# ---------------------------------------------------------------------------

class TestAnvilIONormalizeJsonLike:
    def test_prunes_empty_dict(self):
        result = AnvilIO._normalize_json_like({"a": {}, "b": "keep"})
        assert "a" not in result
        assert result["b"] == "keep"

    def test_prunes_none(self):
        result = AnvilIO._normalize_json_like({"a": None, "b": 1})
        assert "a" not in result

    def test_prunes_empty_list(self):
        result = AnvilIO._normalize_json_like({"a": [], "b": 2})
        assert "a" not in result

    def test_keeps_colon_key(self):
        result = AnvilIO._normalize_json_like({"minecraft:key": {}})
        assert "minecraft:key" in result

    def test_normalizes_nested(self):
        result = AnvilIO._normalize_json_like({"outer": {"inner": None, "val": 42}})
        assert "inner" not in result["outer"]
        assert result["outer"]["val"] == 42

    def test_bool_false_kept(self):
        result = AnvilIO._normalize_json_like({"flag": False})
        assert result["flag"] is False

    def test_zero_kept(self):
        result = AnvilIO._normalize_json_like({"count": 0})
        assert result["count"] == 0

    def test_tuple_to_list(self):
        result = AnvilIO._normalize_json_like((1, 2, 3))
        assert result == [1, 2, 3]

    def test_backslash_to_forward_slash(self):
        result = AnvilIO._normalize_json_like("path\\to\\file")
        assert result == "path/to/file"
