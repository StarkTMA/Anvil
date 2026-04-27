import click
from anvil.lib.lib import process_subcommand


@click.command(help="Enable loopback for Minecraft UWP")
def loopback() -> None:
    process_subcommand(
        'CheckNetIsolation LoopbackExempt -a -n="Microsoft.MinecraftUWP_8wekyb3d8bbwe";',
        "Unable to enable loopback for Minecraft.",
    )
    process_subcommand(
        "start http://localhost:7003/",
        "Unable to start the loopback test page.",
    )
