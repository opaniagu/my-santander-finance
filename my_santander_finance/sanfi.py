import logging

import click
from selenium import webdriver

from my_santander_finance.get_debito import (
    close_session,
    configure_driver,
    download_debit,
    login,
)
from my_santander_finance.import_debito import import_csv_to_sqlite, xls_to_csv
from my_santander_finance.init import (
    create_env_example,
    download_chromedriver,
    init_dir,
    init_sqlite,
)
from my_santander_finance.logger import Logger
from my_santander_finance.settings import settings

# Starts logger for file
log = Logger().get_logger(__name__)
# This sets the root logger level to be info.
logging.root.setLevel(logging.INFO)


@click.command()
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Activate debug mode",
)
@click.option(
    "--download",
    "-d",
    default=False,
    is_flag=True,
    help="Download el reporte de consumo de la cuenta",
)
def main(debug, download):

    # Now I'm going to set debug mode to be true - Function that changes root level logging.
    # This could be from anything.
    # This could be from a user initiating --debug or its own function etc. Up to you.
    if debug is True:
        Logger().set_debug_mode(True)

    if download is False:
        # print("#################################################################################")  # noqa: E501
        # print("Si desea realizar un download de consumo de la cuenta, incluya -d o --download")  # noqa: E501
        # print("#################################################################################")  # noqa: E501
        # print("\n")
        log.debug("Add -d or --download to get consumption")

    # creo directorios y tablas en la base de datos
    init_dir()
    create_env_example()
    init_sqlite()
    download_chromedriver()

    # download el reporte de la tarjeta de debito
    if download:
        options, service = configure_driver()
        driver = webdriver.Chrome(service=service, options=options)
        login(driver=driver)
        download_debit(driver)
        close_session(driver=driver)

    # to sqlite
    xls_to_csv(
        src_dir=settings.DOWNLOAD_CUENTA_DIR,
        src_ext=".xls",
        dst_dir=settings.CVS_TEMP_DIR,
        dst_ext=".csv",
    )
    import_csv_to_sqlite()


# -----------------------------------------
if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
