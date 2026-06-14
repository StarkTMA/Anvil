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
    "--noarch",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip archive steps (zip, mcaddon, etc.).",
)
@click.option(
    "--nocompile",
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
@click.option(
    "--workflow",
    is_flag=True,
    default=False,
    show_default=True,
    help="Update the project's GitHub workflow file with the latest build command.",
)
@click.option(
    "--minify",
    is_flag=True,
    default=False,
    show_default=True,
    help="Minify the project's JSON and JavaScript files.",
)
@click.option(
    "--clean",
    is_flag=True,
    default=False,
    show_default=True,
    help="Compile a clean new build (Clears previous build artifacts).",
)
def build(
    js_only: bool,
    nocompile: bool,
    noarch: bool,
    mcaddon: bool,
    mcworld: bool,
    zip: bool,
    tech_notes: bool,
    workflow: bool,
    minify: bool,
    clean: bool,
) -> None:
    if not os.path.exists("anvilconfig.json"):
        click.echo(
            click.style(
                "No valid Anvil project found, to create a new project run: `anvil create --help`",
                fg="yellow",
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
    if nocompile:
        command.append("--nocompile")
    if noarch:
        command.append("--noarch")
    if mcaddon:
        command.append("--mcaddon")
    if mcworld:
        command.append("--mcworld")
    if zip:
        command.append("--zip")
    if tech_notes:
        command.append("--tech-notes")
    if workflow:
        command.append("--workflow")
    if minify:
        command.append("--minify")
    if clean:
        command.append("--clean")

    process_subcommand(
        " ".join(command),
        "Unable to run the anvil project.",
    )
