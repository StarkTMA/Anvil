import shutil
import sys
from pathlib import Path

import click
from anvil.lib.config import CONFIG_FILE, Config, ConfigOption, ConfigSection
from anvil.lib.lib import OUTPUT, PREVIEW_COM_MOJANG, RELEASE_COM_MOJANG


def get_project_dev_pack_paths(config: Config) -> list[Path]:
    """Returns the current project's development pack directories."""
    preview = config.get_option(ConfigSection.BUILD, ConfigOption.PREVIEW)
    project_name = config.get_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME)

    local_export = (
        bool(config.get_option(ConfigSection.BUILD, ConfigOption.LOCAL_EXPORT))
        if config.has_option(ConfigSection.BUILD, ConfigOption.LOCAL_EXPORT)
        else (sys.platform != "win32")
    )

    if local_export or sys.platform != "win32":
        com_mojang = Path.cwd() / OUTPUT / "com.mojang"
    else:
        com_mojang = PREVIEW_COM_MOJANG if preview else RELEASE_COM_MOJANG

    return [
        com_mojang / "development_resource_packs" / f"RP_{project_name}",
        com_mojang / "development_behavior_packs" / f"BP_{project_name}",
    ]


@click.command(help="Clear the current project's development packs")
def clear() -> None:
    if not CONFIG_FILE.exists():
        click.echo(
            click.style(
                "No valid Anvil project found, to create a new project run: `anvil create --help`",
                fg="yellow",
            )
        )
        return None

    config = Config()

    pack_paths = [path for path in get_project_dev_pack_paths(config) if path.is_dir()]
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
