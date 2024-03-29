import os
import shutil
from os.path import join

import requests
import sqlalchemy

from my_santander_finance.config.settings import settings
from my_santander_finance.logger import Logger
from my_santander_finance.util.func_chrome import get_chrome_version
from my_santander_finance.util.func_dir import create_dir

log = Logger().get_logger(__name__)


def init_dir():
    create_dir(settings.LOCAL_DIR)
    create_dir(settings.DOWNLOAD_DIR)
    create_dir(settings.CVS_TEMP_DIR)
    create_dir(join(settings.LOCAL_DIR, "driver"))

    # debit
    create_dir(settings.DOWNLOAD_CUENTA_DIR)
    create_dir(settings.DOWNLOAD_CUENTA_DIR + ".old")

    # visa
    create_dir(settings.DOWNLOAD_VISA_DIR)
    create_dir(settings.DOWNLOAD_VISA_DIR + ".old")

    # amex
    create_dir(settings.DOWNLOAD_AMEX_DIR)
    create_dir(settings.DOWNLOAD_AMEX_DIR + ".old")


def sqlite_exec_sql(sql: str):
    # conectar a la base de datos
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(settings.LOCAL_DIR, settings.DATABASE_SQLITE)
    log.debug(f"sqlite uri '{SQLALCHEMY_DATABASE_URI}'")
    database_connection = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

    # ejecutar la consulta sql
    try:
        conn = database_connection.connect()
        conn.execute(sql)
        # database_connection.execute(sql)

    except sqlalchemy.exc.SQLAlchemyError as ex:
        # Silently ignore errors if table and index already exist
        if str(ex).find("already exists") != -1:
            log.debug("sql skiped...resource already exist")
        else:
            # error = str(ex.__dict__["orig"])
            # log.debug(error)
            log.debug(ex)


def init_sqlite():
    # debito
    sql = """
            CREATE TABLE "debit" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "fecha" DATE NULL,
                "sucursal_origen" TEXT NULL,
                "descripcion" TEXT NULL,
                "referencia" BIGINT NULL,
                "cuenta_sueldo" REAL DEFAULT 0.0,
                "importe_cuenta_corriente_pesos" REAL DEFAULT 0.0,
                "saldo_pesos" REAL DEFAULT 0.0,
                "tarjeta" TEXT NULL,
                "categoria" TEXT NULL,
                "nota" TEXT NULL
        )
        ;
        """
    sqlite_exec_sql(sql)

    sql = """
            CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
          """
    sqlite_exec_sql(sql)

    # visa
    sql = """
            CREATE TABLE "visa" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "fecha" DATE NULL,
                "descripcion" TEXT NULL,
                "establecimiento" TEXT NULL,
                "comprobante" TEXT NULL,
                "importe_pesos" REAL DEFAULT 0.0,
                "importe_dolares" REAL DEFAULT 0.0,
                "tarjeta" TEXT NULL,
                "categoria" TEXT NULL,
                "nota" TEXT NULL
        )
        ;
        """
    sqlite_exec_sql(sql)

    sql = """
            CREATE UNIQUE INDEX `index_2` ON visa (`fecha`, `descripcion`,`comprobante`);
          """
    sqlite_exec_sql(sql)

    # amex
    sql = """
            CREATE TABLE "amex" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "fecha" DATE NULL,
                "descripcion" TEXT NULL,
                "establecimiento" TEXT NULL,
                "comprobante" TEXT NULL,
                "importe_pesos" REAL DEFAULT 0.0,
                "importe_dolares" REAL DEFAULT 0.0,
                "tarjeta" TEXT NULL,
                "categoria" TEXT NULL,
                "nota" TEXT NULL
        )
        ;
        """
    sqlite_exec_sql(sql)

    sql = """
            CREATE UNIQUE INDEX `index_3` ON amex (`fecha`, `descripcion`,`comprobante`);
          """
    sqlite_exec_sql(sql)


def create_env_example():
    env_file_path = join(settings.LOCAL_DIR, ".env.example")
    if os.path.exists(env_file_path) is False:
        with open(env_file_path, "w") as f:
            f.write("DNI=12345678\n")
            f.write("CLAVE=clave\n")
            f.write("USUARIO=usuario\n")


def download_chromedriver():
    """only supported windows OS, chrome"""
    if os.path.exists(settings.CHROME_DRIVER_EXE) is False:
        chrome_version = get_chrome_version()[:3]
        if chrome_version == "103":
            url = "https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_win32.zip"
        elif chrome_version == "104":
            url = "https://chromedriver.storage.googleapis.com/104.0.5112.29/chromedriver_win32.zip"
        elif chrome_version == "109":
            url = "https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_win32.zip"
        elif chrome_version == "110":
            url = "https://chromedriver.storage.googleapis.com/110.0.5481.30/chromedriver_win32.zip"
        else:
            print(f"Can not found chromedriver version {chrome_version}")
            return

        # try to download
        r = requests.get(url, allow_redirects=True)
        open(settings.CHROME_DRIVER_ZIP, "wb").write(r.content)
        shutil.unpack_archive(settings.CHROME_DRIVER_ZIP, settings.CHROME_DRIVER_DIR)


# ----------------------------------
if __name__ == "__main__":
    init_dir()
    create_env_example()
    init_sqlite()
    download_chromedriver()
