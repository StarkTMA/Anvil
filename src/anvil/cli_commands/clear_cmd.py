import os
import shutil
import click

from anvil.lib.config import Config, ConfigOption, ConfigSection, ConfigOption
from anvil.lib.lib import PREVIEW_COM_MOJANG, RELEASE_COM_MOJANG


def get_project_dev_pack_paths(config: Config) -> list[str]:
    """Returns the current project's development pack directories."""
    preview = config.get_option(ConfigSection.ANVIL, ConfigOption.PREVIEW)
    project_name = config.get_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME)
    com_mojang = PREVIEW_COM_MOJANG if preview else RELEASE_COM_MOJANG

    return [
        os.path.join(com_mojang, "development_resource_packs", f"RP_{project_name}"),
        os.path.join(com_mojang, "development_behavior_packs", f"BP_{project_name}"),
    ]


@click.command(help="Clear the current project's development packs")
def clear() -> None:
    if not os.path.exists("anvilconfig.json"):
        click.echo(
            click.style(
                "No valid Anvil project found, to create a new project run: `anvil create --help`",
                fg="orange",
            )
        )
        return None

    config = Config()

    pack_paths = [
        path for path in get_project_dev_pack_paths(config) if os.path.isdir(path)
    ]
    if not pack_paths:
        click.echo(
            click.style(
                "\r[INFO]: No project development packs found to clear.",
                fg="yellow",
            )
        )
        return
    click.echo("The following project development packs were found:")
    for pack_path in pack_paths:
        click.echo(f" - {pack_path}")
    if not click.confirm("Delete these development packs", default=False):
        click.echo(
            click.style(
                "\r[INFO]: Clear operation cancelled.",
                fg="yellow",
            )
        )
        return
    for pack_path in pack_paths:
        shutil.rmtree(pack_path)
    click.echo(
        click.style(
            f"\r[INFO]: Cleared {len(pack_paths)} project development pack(s).",
            fg="green",
        )
    )
