def find_row_from_card(card_text, df):
    """
    busca el encabezado del nombre de la tarjeta
    a partir del cual comienzan los consumos
    ej.  'Tarjeta VISA  XXXX-YYYY'
    """
    fila = 0

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            # print(row, col, df.iat[row,col])
            if df.iat[row, col] == card_text:
                # row_start = row
                # print(row,col)
                fila = row + 1
                break
        else:
            continue  # only executed if the inner loop did NOT break
        break  # only executed if the inner loop DID break

    return fila


def find_rows(fila, df):
    """
    a partir de 'fila' busco el rpimer registro vacio,
    en ese caso supongo que es el fin de la tabla
    """
    # Fecha 	Descripcion	Establecimiento	Comprobante	Importe en pesos	Importe en dólares
    # obtengo el numero de filas
    i = 0
    for row in range(fila + 1, df.shape[0]):
        # print("'" + str(df.iat[row,1]) + "'", type(df.iat[row,1]))
        if str(df.iat[row, 1]) == "nan":
            # print("found nan")
            break
        else:
            i = i + 1
    # print(i)

    return i


def find_row_from_card_partial(card_text, df, start=0):
    """
    busca el encabezado del nombre de la tarjeta
    a partir del cual comienzan los consumos
    ej.  'Tarjeta VISA  XXXX'
    return:
        row, text of row
        example: 8, Tarjeta VISA  XXXX-YYYY
    """
    fila = 0
    txt = ""

    # shape es una tuple de cantidad de filas y columnas
    for row in range(start, df.shape[0]):
        for col in range(df.shape[1]):
            # print(row, col, df.iat[row,col])
            # if df.iat[row, col] == card_text:
            if isinstance(df.iat[row, col], str):
                if df.iat[row, col].startswith(card_text):
                    # row_start = row
                    # print(row,col)
                    fila = row + 1
                    txt = df.iat[row, col]
                    break
        else:
            continue  # only executed if the inner loop did NOT break
        break  # only executed if the inner loop DID break

    return fila, txt
