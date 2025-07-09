import logging
from datetime import datetime

import click

from anvil import __version__


class Logger:
    """A class used to log messages to the console and to a log file."""

    @staticmethod
    def Red(text: str):
        return click.style(text, "red")

    @staticmethod
    def Yellow(text: str):
        return click.style(text, "yellow")

    @staticmethod
    def Green(text: str):
        return click.style(text, "green")

    @staticmethod
    def Cyan(text: str):
        return click.style(text, "cyan")

    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="anvil.log",
            filemode="w",
        )
        self.logger = logging.getLogger()

    # Console header
    def header(self):
        click.clear()
        click.echo(
            "\n".join(
                [
                    f"{self.Cyan('Anvil')} - by StarkTMA.",
                    f"Version {self.Cyan(__version__)}.",
                    f"Copyright © {datetime.now().year} {self.Red('StarkTMA')}.",
                    "All rights reserved.",
                    "",
                    "",
                ]
            )
        )

    # ------------------------------------------------------------------------
    # Addon Objects
    # ------------------------------------------------------------------------
    # Info
    def new_anvil_build(self, new):
        m = f"A newer anvil build were found: [{new}]."
        self.logger.info(m)
        click.echo(m)

    # Info
    def anvil_up_to_date(self):
        m = "Anvil is up to date"
        self.logger.info(m)
        click.echo(m)

    # Info
    def packaging_zip(self):
        m = "Packaging submission .zip"
        self.logger.info(m)
        click.echo(self.Cyan(m))

    # Info
    def packaging_mcaddon(self):
        m = "Packaging .mcaddon"
        self.logger.info(m)

    # Info
    def packaging_mcworld(self):
        m = "Packaging .mcworld"
        self.logger.info(m)

    # Info
    def file_exist_info(self, filename):
        m = f"{filename} does not exist. It is optional but might have been left out unintentionally."
        self.logger.info(m)
        click.echo(self.Cyan("[INFO]: " + m))

    # Info
    def project_missing_config(self):
        m = f"The project require missing configuration. Please fill in the following options:"
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # Info
    def config_added_option(self, section: str, option: str):
        m = f"{option} was added to {section}"
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # Info
    def config_option_changeable(self, *options: str):
        m = f"The options {options} can be changed from the config file at any time, recompilation will be required."
        self.logger.info(m)
        click.echo(self.Cyan("[Info]: " + m))

    # General
    def check_update(self):
        m = f"Checking for package updates..."
        self.logger.info(m)

    # Error
    def object_export_error(self, name: str, error: Exception):
        m = f"Error exporting {name}: {error}"
        self.logger.error(m)
        raise error
