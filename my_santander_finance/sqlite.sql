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
);

CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
