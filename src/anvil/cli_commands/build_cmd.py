import os
import sys

import click

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.lib import process_subcommand


@click.command(help="Build an Anvil project")
@click.option(
    "--js-only",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip archive steps (zip, mcaddon, etc.).",
)
@click.option(
    "--no-arch",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip archive steps (zip, mcaddon, etc.).",
)
@click.option(
    "--mcaddon",
    is_flag=True,
    default=False,
    show_default=True,
    help="Build the project as a Minecraft Addon.",
)
@click.option(
    "--mcworld",
    is_flag=True,
    default=False,
    show_default=True,
    help="Build the project as a Minecraft World.",
)
@click.option(
    "--zip",
    is_flag=True,
    default=False,
    show_default=True,
    help="Build the project as a zip file.",
)
@click.option(
    "--tech-notes",
    is_flag=True,
    default=False,
    show_default=True,
    help="Generate technical notes for the project.",
)
def build(
    js_only: bool,
    no_arch: bool,
    mcaddon: bool,
    mcworld: bool,
    zip: bool,
    tech_notes: bool,
) -> None:
    if not os.path.exists("anvilconfig.json"):
        click.echo(
            click.style(
                "No valid Anvil project found, to create a new project run: `anvil create --help`",
                fg="orange",
            )
        )
        return None

    config = Config()
    entry_point = config.get_option(ConfigSection.ANVIL, ConfigOption.ENTRY_POINT)
    if not entry_point:
        click.echo(
            click.style(
                "\r[INFO]: No entry point found in the Anvil project configuration.",
                fg="yellow",
            )
        )
        return

    command = [f'"{sys.executable}" "{entry_point}"']
    if js_only:
        command.append("--js-only")
    if no_arch:
        command.append("--no-arch")
    if mcaddon:
        command.append("--mcaddon")
    if mcworld:
        command.append("--mcworld")
    if zip:
        command.append("--zip")
    if tech_notes:
        command.append("--tech-notes")

    process_subcommand(
        " ".join(command),
        "Unable to run the anvil project.",
    )
