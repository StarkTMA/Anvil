"""Tests for anvil/lib/format_versions.py: the files that follow the Minecraft build."""

import pytest


def _package(**sections):
    data = {
        "package": {
            "namespace": "test",
            "project_name": "test_proj",
            "company": "TestCo",
            "display_name": "Test Project",
            "project_description": "desc",
            "behavior_description": "bp",
            "resource_description": "rp",
        }
    }
    data.update(sections)
    return data


def test_experimental_needs_preview():
    from anvil.lib.config import AnvilConfig

    with pytest.raises(ValueError, match="features.experimental needs build.preview"):
        AnvilConfig.from_dict(_package(features={"experimental": True}))
    assert AnvilConfig.from_dict(
        _package(features={"experimental": True}, build={"preview": True})
    )._EXPERIMENTAL


@pytest.mark.parametrize(
    ("preview", "experimental", "expected"),
    [
        (False, False, "1.26.60"),
        (True, False, "1.26.60"),
        (False, True, "1.26.60"),
        (True, True, "1.26.70"),
    ],
)
def test_build_version(monkeypatch, preview, experimental, expected):
    from anvil.lib.config import CONFIG
    from anvil.lib.format_versions import (
        MANIFEST_BUILD,
        MANIFEST_BUILD_PREVIEW,
        build_version,
    )

    assert (MANIFEST_BUILD, MANIFEST_BUILD_PREVIEW) == ("1.26.60", "1.26.70")
    monkeypatch.setattr(CONFIG, "_PREVIEW", preview, raising=False)
    monkeypatch.setattr(CONFIG, "_EXPERIMENTAL", experimental, raising=False)
    assert build_version() == expected
