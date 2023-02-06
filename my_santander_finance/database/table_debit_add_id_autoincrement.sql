CREATE TABLE "debit_new" (
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
);

/* reset auto increment*/
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='debit_new';


INSERT INTO debit_new (fecha, sucursal_origen, descripcion, referencia, cuenta_sueldo, importe_cuenta_corriente_pesos, saldo_pesos, tarjeta, categoria )
SELECT fecha, sucursal_origen, descripcion, referencia, cuenta_sueldo, importe_cuenta_corriente_pesos, saldo_pesos, tarjeta, categoria
FROM debit
ORDER BY fecha DESC
;


DROP TABLE debit;

ALTER TABLE debit_new RENAME TO debit;


CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
