import click
from selenium import webdriver

from my_santander_finance.get_debito import (
    close_session,
    configure_driver,
    download_debit,
    login,
)
from my_santander_finance.import_debito import import_csv_to_sqlite, xls_to_csv
from my_santander_finance.init import init_dir, init_sqlite
from my_santander_finance.settings import settings


@click.command()
@click.option(
    "--download",
    "-d",
    default=False,
    is_flag=True,
    help="Download el reporte de consumo de la cuenta",
)
def main(download):

    if download is False:
        print("#################################################################################")  # noqa: E501
        print("Si desea realizar un un download de consumo de la cuenta, incluye -d o --download")  # noqa: E501
        print("#################################################################################")  # noqa: E501
        print("\n")

    # creo directorios y tablas en la base de datos
    init_dir()
    init_sqlite()

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
