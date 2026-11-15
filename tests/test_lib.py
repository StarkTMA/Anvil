import subprocess
from types import SimpleNamespace

import orjson
import requests

from anvil.lib.lib import AnvilValidator


def test_check_new_versions_npm_and_pip(monkeypatch):
    npm_json = orjson.dumps(
        {"@starktma/minecraft-utils": {"current": "1.5.41", "latest": "1.5.42"}}
    )
    pip_json = orjson.dumps(
        [{"name": "mcanvil", "version": "0.9.6.7", "latest_version": "0.9.9"}]
    )

    def run(cmd, **kwargs):
        if isinstance(cmd, str) and "npm" in cmd:
            return SimpleNamespace(returncode=1, stdout=npm_json)
        return SimpleNamespace(returncode=0, stdout=pip_json)

    def get(url, **kwargs):
        return SimpleNamespace(text='{"latest": {"version": "1.21.0"}}')

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(requests, "get", get)

    vanilla_ver, anvil_ver = AnvilValidator.check_new_versions()
    assert vanilla_ver == "1.21.0"
    assert anvil_ver is not None
