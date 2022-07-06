import sqlalchemy

from my_santander_finance.settings import settings
from my_santander_finance.func_dir import create_dir

def init_dir():
    create_dir(settings.DOWNLOAD_DIR)
    create_dir(settings.DOWNLOAD_CUENTA_DIR)
    create_dir(settings.DOWNLOAD_CUENTA_DIR + '.old')
    create_dir(settings.CVS_TEMP_DIR)



def init_sqlite():
    # conectar a la base de datos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + settings.DATABASE_SQLITE
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
        if str(ex).find('already exists') != -1:
                pass
        else:
            print('####')
            print('Error sqlite')
            print(ex)
            error = str(ex.__dict__['orig'])
            print(error)
            print('####')
    
    sql = """
            CREATE UNIQUE INDEX `index_1` ON debit (`fecha`, `descripcion`,`cuenta_sueldo`);
          """

    try:
        database_connection.execute(sql)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        # Silently ignore errors if table and index already exist
        if str(ex).find('already exists') != -1:
                pass
        else:
            print('####')
            print('Error sqlite')
            print(ex)
            error = str(ex.__dict__['orig'])
            print(error)
            print('####')

if __name__ == "__main__":
   init_dir()
   init_sqlite()

