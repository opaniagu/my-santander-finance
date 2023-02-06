"""
importa el .xls de la tarjeta de debito de santander Argentina a una base de datos sqlite
"""
import csv
import datetime
import os
import shutil
import sqlite3

import pandas as pd

from my_santander_finance.config.settings import settings
from my_santander_finance.logger import Logger
from my_santander_finance.util.func_dir import get_list_files
from my_santander_finance.util.func_excel import (
    find_row_from_card,
    find_row_from_card_partial,
    find_rows,
)

log = Logger().get_logger(__name__)


def xls_to_csv(src_dir: str, src_ext: str, dst_dir: str, dst_ext: str):
    # obtengo la lista de arhivos (previamente descargados) a procesar
    log.debug(f"source dir: {src_dir}")
    log.debug(f"source ext: {src_ext}")

    files = get_list_files(dir=src_dir, ext=src_ext)
    log.debug(f"Se econtraron {len(files)} archivos {src_ext} posibles para importar")

    # si la lista esta vacia finalizo con mensaje
    if len(files) == 0:
        log.debug(f"Ningun archivo {src_ext} pendiente de procesar")
        return

    # proceso cada archivo de la lista
    for f in files:
        # creo el path absoluto del archivo .xls a procesar
        src_file = src_dir + "\\" + f

        log.debug(f"processing file: {src_file}")

        # genero el pandas dataframe
        df1 = pd.read_excel(src_file)

        # busco el numero de cuenta
        str_to_find = "Cuenta única"
        pos, cuenta = find_row_from_card_partial(str_to_find, df1)
        log.debug(cuenta)

        # busco el str para saber donde empieza la tabla
        str_to_find = "Últimos movimientos"
        fila = find_row_from_card(str_to_find, df1)

        # obtengo la cantidad de filas a poner en el dataframe
        filas = find_rows(fila, df1)

        # re-leo el excel para generar el dataframe correcto
        df1 = pd.read_excel(src_file, skiprows=fila + 2, nrows=filas - 1, usecols=range(1, 8))

        # seteo el nombre de las columnas, en un momento santander las cambió,
        # con lo cual es mejor dejarlo fijo
        # si cambia, manualmente tambien hay que modificar la definicion de la tabla sqlite

        qc = len(df1.columns)
        log.debug(f"quantity of columns: {qc}")

        if qc == 5:
            df1.columns = ["fecha", "sucursal_origen", "descripcion", "referencia", "cuenta_sueldo"]
            # add cols
            df1["importe_cuenta_corriente_pesos"] = 0
            df1["saldo_pesos"] = 0

        else:
            df1.columns = [
                "fecha",
                "sucursal_origen",
                "descripcion",
                "referencia",
                "cuenta_sueldo",
                "importe_cuenta_corriente_pesos",
                "saldo_pesos",
            ]

        # elimino espacios adelante y atras en los headers, si existieran
        df1.columns = df1.columns.str.strip()

        # agrego una columna tarjeta(card), y una columna categoria, con valores por default
        # luego, otro procesamiento, realizara los tags dentro de 'categoria' en funcion del
        # campo descripcion
        df1["tarjeta"] = cuenta[13:]
        df1["categoria"] = "unknown"

        # convierto la columna Fecha que esta en str a date con el formato correcto
        df1["fecha"] = df1["fecha"].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y").date())

        # convierto la columna 'Cuenta sueldo' de str a double
        if isinstance(df1["cuenta_sueldo"], str) is True:
            df1["cuenta_sueldo"] = df1["cuenta_sueldo"].apply(lambda x: (x.replace(".", "")))
            df1["cuenta_sueldo"] = df1["cuenta_sueldo"].apply(lambda x: float(x.replace(",", ".")))

        # convierto la columna 'Saldo pesos' de str a double
        if isinstance(df1["saldo_pesos"], str) is True:
            df1["saldo_pesos"] = df1["saldo_pesos"].str.replace(".", "", regex=True)
            df1["saldo_pesos"] = df1["saldo_pesos"].str.replace(",", ".", regex=True)

        # guardo el archivo transformado
        index = f.index(".")
        file_name = dst_dir + "\\" + f[:index] + dst_ext
        df1.to_csv(file_name, index=False, sep=";", quotechar="'")

        # el archivo ya procesado lo muevo al directorio .old
        # absolute path
        src_path = src_file
        dst_path = src_dir + ".old" + "\\" + f
        try:
            shutil.move(src_path, dst_path)
        except FileNotFoundError:
            log.debug(f"File Not Found {src_path}")
        except Exception as ex:
            print(ex)


def csv_to_sqlite(cvs_filepath: str, sqlite_filepath: str):
    # NO utilizar "to_sql", tiene el problema que al insert si aparece un duplicado
    # no continua mas y no hay manera de hacerlo
    # por eso descarto utilizar to_sql

    # log.debug(f"{cvs_filepath}")
    # exit()

    conn = sqlite3.connect(sqlite_filepath)
    curs = conn.cursor()
    # curs.execute("CREATE TABLE document (col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT,col5 TEXT);")
    reader = csv.reader(open(cvs_filepath, "r"), delimiter=";")
    count = 0
    skip = 0
    first = 1
    for row in reader:

        # print(row)

        if first == 1:
            first = 0
            continue

        # para los campos "real" (float), el valor por default 0.0
        # si es NULL o vacio
        if len(row[4]) == 0:
            row[4] = 0.0

        if len(row[5]) == 0:
            row[5] = 0.0

        if len(row[6]) == 0:
            row[6] = 0.0

        if isinstance(row[4], str):
            sueldo = row[4].replace(".", "")
            sueldo = sueldo.replace(",", ".")
        else:
            sueldo = row[4]

        if isinstance(row[5], str):
            corriente = row[5].replace(".", "")
            corriente = corriente.replace(",", ".")
        else:
            corriente = row[5]

        if isinstance(row[6], str):
            saldo = row[6].replace(".", "")
            saldo = saldo.replace(",", ".")
        else:
            saldo = row[6]

        to_db = [
            row[0].encode("utf-8"),
            row[1].encode("utf-8"),
            row[2].encode("utf-8"),
            row[3].encode("utf-8"),
            sueldo,  # cuenta sueldo
            corriente,
            saldo,
            row[7].encode("utf-8"),
            row[8].encode("utf-8"),
        ]

        try:

            curs.execute(
                "INSERT INTO debit(fecha, sucursal_origen, descripcion, referencia, cuenta_sueldo, importe_cuenta_corriente_pesos, saldo_pesos, tarjeta, categoria ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",  # noqa: E501
                to_db,
            )
            count = count + 1
        except:  # noqa: E722
            skip = skip + 1

    conn.commit()
    conn.close()

    log.debug(f"Se proceso {cvs_filepath} , se agregaron {count} registros, y se omitieron {skip} registros.")


def import_csv_to_sqlite():
    # obtengo la lista de arhivos previamente descargados y transformados (xls->csv)
    files = get_list_files(dir=settings.CVS_TEMP_DIR, ext=".csv")
    log.debug(f"Se econtraron {len(files)} archivos .csv posibles para importar")

    # si la lista esta vacia finalizo con mensaje
    if len(files) == 0:
        log.debug("Ningun archivo .csv pendiente de procesar")
        return

    # proceso cada archivo de la lista
    for f in files:
        # creo el path absoluto del archivo .csv a procesar
        src_file = settings.CVS_TEMP_DIR + "\\" + f
        sqlite_filepath = os.path.join(settings.LOCAL_DIR, settings.DATABASE_SQLITE)
        log.debug(f"sqlite absolute path to connect: {sqlite_filepath}")
        csv_to_sqlite(cvs_filepath=src_file, sqlite_filepath=sqlite_filepath)

        if os.path.exists(src_file):
            os.remove(src_file)


# ------------------------------------------------
if __name__ == "__main__":
    xls_to_csv(
        src_dir=settings.DOWNLOAD_CUENTA_DIR,
        src_ext=".xls",
        dst_dir=settings.CVS_TEMP_DIR,
        dst_ext=".csv",
    )
    import_csv_to_sqlite()
