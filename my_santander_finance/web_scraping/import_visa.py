"""
importa el .xls de la tarjeta de visa de santander Argentina a una base de datos sqlite
"""
import csv
import os
import shutil
import sqlite3
from datetime import datetime

import pandas as pd

from my_santander_finance.config.settings import settings
from my_santander_finance.logger import Logger
from my_santander_finance.util.func_dir import get_list_files
from my_santander_finance.util.func_excel import find_row_from_card_partial, find_rows

log = Logger().get_logger(__name__)


def create_card_dataframe(src_file, start_rows, filas, card_name):
    """
    crea un dataframe con los consumos de la tarjeta de credito
        src_file    Es el nombre del archivo a procesar
        start_rows  Es el numero inicial de fila (la primer fila despues del encabezado de la tabla)
        filas       Es la cantidad de filas totales
        card_name   Es el numero de tarjeta de credito
    """

    # leo el excel para generar el dataframe
    df1 = pd.read_excel(
        src_file,
        skiprows=start_rows + 1,
        nrows=filas,
        usecols=range(1, 7),
        converters={"Establecimiento": str, "Comprobante": str, "importe_pesos": float, "importe_dolares": float},
    )

    # seteo el nombre de las columnas, en un momento santander las cambió,
    # con lo cual es mejor dejarlo fijo
    # si cambia, manualmente tambien hay que modificar la definicion de la tabla sqlite
    df1.columns = [
        "fecha",
        "descripcion",
        "establecimiento",
        "comprobante",
        "importe_pesos",
        "importe_dolares",
    ]

    # elimino espacios adelante y atras en los headers, si existieran
    df1.columns = df1.columns.str.strip()

    # agrego una columna tarjeta(card), y una columna categoria, con valores por default
    # luego, otro procesamiento, realizara los tags dentro de 'categoria' en funcion del
    # campo descripcion
    df1["tarjeta"] = card_name
    df1["categoria"] = "unknown"

    return df1


def xls_to_csv(src_dir: str, src_ext: str, dst_dir: str, dst_ext: str):
    # obtengo la lista de arhivos (previamente descargados) a procesar
    files = get_list_files(dir=src_dir, ext=src_ext, prefix="visa")
    log.debug(f"Se econtraron {len(files)} archivos {src_ext} posibles para importar")

    # si la lista esta vacia finalizo con mensaje
    if len(files) == 0:
        log.debug(f"Ningun archivo {src_ext} pendiente de procesar")
        return

    # proceso cada archivo de la lista
    for f in files:
        # creo el path absoluto del archivo .xls a procesar
        src_file = src_dir + "\\" + f

        # genero el pandas dataframe
        df1 = pd.read_excel(src_file)

        # print(df1)
        # quit()

        # busco el str para saber donde empieza la tabla
        # str_to_find = "Últimos consumos"
        str_to_find = "Tarjeta VISA  XXXX"

        # primera tarjeta
        fila, card_name = find_row_from_card_partial(str_to_find, df1)
        # print(fila, card_name)
        # obtengo la cantidad de filas a poner en el dataframe
        filas = find_rows(fila, df1)
        # print(filas)
        df_a = create_card_dataframe(src_file, fila, filas, card_name)

        # segunda tarjeta
        fila, card_name = find_row_from_card_partial(str_to_find, df1, start=fila + 1)
        # print(fila, card_name)
        # obtengo la cantidad de filas a poner en el dataframe
        filas = find_rows(fila, df1)
        # print(filas)
        df_b = create_card_dataframe(src_file, fila, filas, card_name)

        # print(df_a)
        # print(df_b)
        # quit()

        # concatenar los dataframes
        frames = [df_a, df_b]
        df_final = pd.concat(frames)

        # guardo el archivo transformado
        index = f.index(".")
        file_name = dst_dir + "\\" + f[:index] + dst_ext
        # print(file_name)
        df_final.to_csv(file_name, index=False, sep=";", quotechar="'")

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

    conn = sqlite3.connect(sqlite_filepath)
    curs = conn.cursor()
    # curs.execute("CREATE TABLE document (col1 TEXT, col2 TEXT, col3 TEXT, col4 TEXT,col5 TEXT);")
    reader = csv.reader(open(cvs_filepath, "r"), delimiter=";")
    count = 0
    skip = 0
    first = 1
    for row in reader:
        if first == 1:
            first = 0
            continue

        # el campo 'fecha' lo convierto a 'yyyy-mm-dd' para mysql
        # aseguro el formato
        row[0] = datetime.strptime(row[0], "%d/%m/%Y")
        row[0] = row[0].strftime("%Y-%m-%d")

        # para los campos "real" (float), el valor por default 0.0
        # si es NULL o vacio
        if len(row[4]) == 0:
            row[4] = 0.0

        if len(row[5]) == 0:
            row[5] = 0.0

        to_db = [
            row[0].encode("utf-8"),
            row[1].encode("utf-8"),
            row[2].encode("utf-8"),
            row[3].encode("utf-8"),
            row[4],
            row[5],
            row[6].encode("utf-8"),
            row[7].encode("utf-8"),
        ]

        try:
            curs.execute("INSERT INTO visa VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
            count = count + 1
        except:  # noqa: E722
            skip = skip + 1

    conn.commit()
    conn.close()

    log.debug(f"Se proceso {cvs_filepath} , se agregaron {count} registros, y se omitieron {skip} registros.")


def import_csv_to_sqlite():
    # obtengo la lista de arhivos previamente descargados y transformados (xls->csv)
    files = get_list_files(dir=settings.CVS_TEMP_DIR, ext=".csv", prefix="visa")
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
        src_dir=settings.DOWNLOAD_VISA_DIR,
        src_ext=".xls",
        dst_dir=settings.CVS_TEMP_DIR,
        dst_ext=".csv",
    )
    import_csv_to_sqlite()
