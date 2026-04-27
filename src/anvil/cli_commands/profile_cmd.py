import os

import click

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.lib import process_subcommand


@click.command(help="Profile the current Anvil project")
def profile() -> None:
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
    process_subcommand(
        f"py-spy record -o output\\anvil_trace.json --format speedscope -- python {entry_point}",
        "Unable to profile the anvil project.",
    )
