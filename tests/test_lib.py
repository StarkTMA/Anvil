import json
import pytest
from unittest.mock import patch, MagicMock
from anvil.lib.lib import AnvilValidator


def test_check_new_versions_npm_and_pip():
    with patch("subprocess.run") as mock_run, patch("requests.get") as mock_get:
        mock_get.return_value.text = '{"latest": {"version": "1.21.0"}}'

        npm_json = json.dumps({
            "@starktma/minecraft-utils": {
                "current": "1.5.41",
                "latest": "1.5.42"
            }
        })
        pip_json = json.dumps([
            {
                "name": "mcanvil",
                "version": "0.9.6.7",
                "latest_version": "0.9.9"
            }
        ])

        def side_effect(cmd, **kwargs):
            mock_res = MagicMock()
            if isinstance(cmd, str) and "npm" in cmd:
                mock_res.returncode = 1
                mock_res.stdout = npm_json
            else:
                mock_res.returncode = 0
                mock_res.stdout = pip_json
            return mock_res

        mock_run.side_effect = side_effect

        vanilla_ver, anvil_ver = AnvilValidator.check_new_versions()
        assert vanilla_ver == "1.21.0"
        assert anvil_ver is not None
