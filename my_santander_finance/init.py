import os
import shutil
from os.path import join

import requests
import sqlalchemy

from my_santander_finance.chrome_version import get_chrome_version
from my_santander_finance.func_dir import create_dir
from my_santander_finance.settings import settings


def init_dir():
    create_dir(settings.LOCAL_DIR)
    create_dir(settings.DOWNLOAD_DIR)
    create_dir(settings.DOWNLOAD_CUENTA_DIR)
    create_dir(settings.DOWNLOAD_CUENTA_DIR + ".old")
    create_dir(settings.CVS_TEMP_DIR)
    create_dir(join(settings.LOCAL_DIR, "driver"))


def init_sqlite():
    # conectar a la base de datos
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(settings.LOCAL_DIR, settings.DATABASE_SQLITE)
    database_connection = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

    sql = """
            CREATE TABLE "debit" (
                "fecha" DATE NULL,
                "sucursal_origen" TEXT NULL,
                "descripcion" TEXT NULL,
                "referencia" BIGINT NULL,
                "cuenta_sueldo" REAL DEFAULT 0.0,
                "importe_cuenta_corriente_pesos" REAL DEFAULT 0.0,
                "saldo_pesos" REAL DEFAULT 0.0,
                "tarjeta" TEXT NULL,
                "categoria" TEXT NULL
        )
        ;
        """

    # print(sql)
    try:
        database_connection.execute(sql)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        # Silently ignore errors if table and index already exist
        if str(ex).find("already exists") != -1:
            pass
        else:
            print("####")
            print("Error sqlite")
            print(ex)
            error = str(ex.__dict__["orig"])
            print(error)
            print("####")

    sql = """
            CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
          """

    try:
        database_connection.execute(sql)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        # Silently ignore errors if table and index already exist
        if str(ex).find("already exists") != -1:
            pass
        else:
            print("####")
            print("Error sqlite")
            print(ex)
            error = str(ex.__dict__["orig"])
            print(error)
            print("####")


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
