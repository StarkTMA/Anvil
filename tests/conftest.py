from dataclasses import replace

import pytest

from anvil.lib import config

TEST_PROJECT = {
    "package": {
        "namespace": "test",
        "project_name": "test",
        "company": "test",
        "display_name": "Test",
        "project_description": "Test",
        "behavior_description": "Test",
        "resource_description": "Test",
    }
}


def project_settings(**values) -> config.AnvilConfig:
    """The settings of a minimal project, with `values` changed."""
    return replace(config.AnvilConfig.from_dict(TEST_PROJECT), **values)


config.use(project_settings())


@pytest.fixture(autouse=True)
def project_config():
    """Gives each test fresh settings of a minimal project."""
    with config.override(project_settings()):
        yield
