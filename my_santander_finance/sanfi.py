import logging
import sys

import click

from my_santander_finance.__init__ import __version__
from my_santander_finance.init import (
    create_env_example,
    download_chromedriver,
    init_dir,
    init_sqlite,
)
from my_santander_finance.logger import Logger
from my_santander_finance.web_scraping.get_debito import get_debito
from my_santander_finance.web_scraping.get_visa import get_visa

# Starts logger for file
log = Logger().get_logger(__name__)
# This sets the root logger level to be info.
logging.root.setLevel(logging.INFO)


def show_version():
    # log.info(f"sanfi version {__version__}")
    print(__version__)


@click.command()
@click.option(
    "--version",
    default=False,
    is_flag=True,
    help="Show version",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Activate debug mode",
)
@click.option(
    "--debit",
    default=False,
    is_flag=True,
    help="Procesa el reporte de consumo de la cuenta unica(debito)",
)
@click.option(
    "--visa",
    default=False,
    is_flag=True,
    help="Procesa el reporte de consumo de la tarjeta Visa",
)
@click.option(
    "--download",
    default=False,
    is_flag=True,
    help="Download el reporte de la cuenta o tarjeta de credito del banco",
)
def main(version, debug, debit, visa, download):

    if version is True:
        show_version()
        sys.exit()

    # Now I'm going to set debug mode to be true - Function that changes root level logging.
    # This could be from anything.
    # This could be from a user initiating --debug or its own function etc. Up to you.
    if debug is True:
        Logger().set_debug_mode(True)

    if debit is False:
        log.debug("Add --debit to get consumption of your account")

    if visa is False:
        log.debug("Add --visa to get consumption of your Visa credit card")

    # creo directorios y tablas en la base de datos
    init_dir()
    create_env_example()
    init_sqlite()
    download_chromedriver()

    # download el reporte de la tarjeta de debito
    if debit:
        get_debito(download)

    # download el reporte de la tarjeta de credito Visa
    if visa:
        get_visa(download)


# -----------------------------------------
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
