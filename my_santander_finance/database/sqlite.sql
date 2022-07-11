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

CREATE TABLE "visa" (
	"fecha" DATE NULL,
	"descripcion" TEXT NULL,
	"establecimiento" TEXT NULL,
	"comprobante" TEXT NULL,
	"importe_pesos" REAL NULL,
	"importe_dolares" REAL NULL,
	"tarjeta" TEXT NULL,
	"categoria" TEXT NULL
);
CREATE UNIQUE INDEX "index_2" ("fecha", "descripcion", "comprobante");
