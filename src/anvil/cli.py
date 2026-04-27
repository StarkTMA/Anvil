import click
from click_aliases import ClickAliasedGroup

from .cli_commands.clear_cmd import clear
from .cli_commands.create_cmd import init
from .cli_commands.loopback_cmd import loopback
from .cli_commands.process_sounds import sound
from .cli_commands.profile_cmd import profile
from .cli_commands.run_cmd import build


@click.group(cls=ClickAliasedGroup)
def cli() -> None:
    """
    Main command line interface function.

    Returns:
        None
    """


cli.add_command(init, aliases=["create"])
cli.add_command(build, aliases=["run"])
cli.add_command(clear, aliases=["clean"])
cli.add_command(profile, aliases=["prof"])
cli.add_command(sound, aliases=["sounds"])
cli.add_command(loopback, aliases=["lb"])
