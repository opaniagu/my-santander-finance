CREATE TABLE "amex_new" (
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
UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='amex_new';


INSERT INTO amex_new (fecha, descripcion, establecimiento, comprobante, importe_pesos, importe_dolares, tarjeta, categoria)
SELECT fecha, descripcion, establecimiento, comprobante, importe_pesos, importe_dolares, tarjeta, categoria
FROM amex
ORDER BY fecha DESC
;


DROP TABLE amex;

ALTER TABLE amex_new RENAME TO amex;


CREATE UNIQUE INDEX `index_3` ON amex (`fecha`, `descripcion`,`comprobante`);
