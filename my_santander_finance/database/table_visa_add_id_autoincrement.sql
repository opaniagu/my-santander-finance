CREATE TABLE "visa_new" (
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
);

/* reset auto increment*/
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='visa_new';


INSERT INTO visa_new (fecha, descripcion, establecimiento, comprobante, importe_pesos, importe_dolares, tarjeta, categoria)
SELECT fecha, descripcion, establecimiento, comprobante, importe_pesos, importe_dolares, tarjeta, categoria
FROM visa
ORDER BY fecha DESC
;


DROP TABLE visa;

ALTER TABLE visa_new RENAME TO visa;

CREATE UNIQUE INDEX `index_2` ON visa (`fecha`, `descripcion`,`comprobante`);
