# sqlite3

A continuacion se muestran los comandos basicos de sqlite3.

## abrir la base de datos

```cmd
sqlite3 santander.sqlite

SQLite version 3.38.4 2022-05-04 15:45:55
Enter ".help" for usage hints.
sqlite>
```

## mostrar todas las tablas

```cmd
sqlite> .tables
debit
sqlite>
```

## mostrar la tabla 'debit'
```cmd
sqlite> .schema  debit
CREATE TABLE IF NOT EXISTS "debit" (
                "fecha" DATE NULL,
                "sucursal_origen" TEXT NULL,
                "descripcion" TEXT NULL,
                "referencia" BIGINT NULL,
                "cuenta_sueldo" REAL DEFAULT 0.0,
                "importe_cuenta_corriente_pesos" REAL DEFAULT 0.0,
                "saldo_pesos" REAL DEFAULT 0.0,
                "tarjeta" TEXT NULL,
                "categoria" TEXT NULL
        );
CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
```

## mostrar el contenido de la  tabla 'debit'
```cmd
sqlite> select * from debit;
```

## salir

```cmd
sqlite> .quit
```

## contar la cantidad de registros en la tabla 'debit'

```cmd
sqlite> select count(*) from debit;
90
```
