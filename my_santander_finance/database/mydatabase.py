# Install Library

# -----------------------------------
#      Database Model
# -----------------------------------

from sqlalchemy import (  # Column,; ForeignKey,; Integer,; MetaData,; String,; Table,
    create_engine,
    text,
)

from my_santander_finance.tags.dict import tags

# Global Variables
SQLITE = "sqlite"
MYSQL = "mysql"
POSTGRESQL = "postgresql"

# Table Names
DEBIT = "debit"
VISA = "visa"
AMEX = "amex"


class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: r"sqlite:///{DB}",
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username="", password="", dbname=""):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            # print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    # def create_db_tables(self):
    #     metadata = MetaData()
    #     users = Table(
    #         USERS,
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("first_name", String),
    #         Column("last_name", String),
    #     )

    #     address = Table(
    #         ADDRESSES,
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("user_id", None, ForeignKey("users.id")),
    #         Column("email", String, nullable=False),
    #         Column("address", String),
    #     )

    #     try:
    #         metadata.create_all(self.db_engine)
    #         print("Tables created")
    #     except Exception as e:
    #         print("Error occurred during Table creation!")
    #         print(e)

    # Insert, Update, Delete
    def execute_query(self, query=""):
        if query == "":
            return

        with self.db_engine.connect() as connection:
            try:
                print(query)
                result = connection.execute(text(query))
                print(f"{result.rowcount} row was updated.")
                connection.commit()
                # connection.exec_driver_sql(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table="", query=""):
        query = query if query != "" else "SELECT * FROM '{}';".format(table)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(text(query))
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()

        print("\n")

    # Examples

    def unknown_query(self, table=""):
        query = "SELECT id, descripcion FROM {} WHERE categoria LIKE '%unknown%';".format(table)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(text(query))
            except Exception as e:
                print(e)
            else:
                for row in result:
                    # print(row[0])
                    # print(row)  # print(row[0], row[1], row[2])
                    res = [val for key, val in tags.items() if key in str(row[1])]
                    if not res:
                        print(str(row))
                        # print(res)
                    else:
                        query = "UPDATE {table} set categoria='{categoria}' WHERE id={id};".format(
                            table=table, categoria=res[0], id=row[0]
                        )
                        result = connection.execute(text(query))
                        # print(f"{result.rowcount} row was updated.")
                        connection.commit()

                result.close()

    # def sample_query(self):
    #     # Sample Query
    #     query = "SELECT first_name, last_name FROM {TBL_USR} WHERE " "last_name LIKE 'M%';".format(TBL_USR=USERS)
    #     self.print_all_data(query=query)

    #     # Sample Query Joining
    #     query = (
    #         "SELECT u.last_name as last_name, "
    #         "a.email as email, a.address as address "
    #         "FROM {TBL_USR} AS u "
    #         "LEFT JOIN {TBL_ADDR} as a "
    #         "WHERE u.id=a.user_id AND u.last_name LIKE 'M%';".format(TBL_USR=USERS, TBL_ADDR=ADDRESSES)
    #     )
    #     self.print_all_data(query=query)

    # def sample_delete(self):
    #     # Delete Data by Id
    #     query = "DELETE FROM {} WHERE id=3".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)

    #     # Delete All Data
    #     """
    #     query = "DELETE FROM {}".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)
    #     """

    # def sample_insert(self):
    #     # Insert Data
    #     query = "INSERT INTO {}(id, first_name, last_name) " "VALUES (3, 'Terrence','Jordan');".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)

    # def sample_update(self):
    #     # Update Data
    #     query = "UPDATE {} set first_name='XXXX' WHERE id={id}".format(USERS, id=3)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)

    def report(self, table="debit", month="01", year="2023"):

        col = "cuenta_sueldo"
        col_dolares = ""
        if table == "visa" or table == "amex":
            col = "importe_pesos"
            col_dolares = "sum(importe_dolares) as dolares,"

        query = """
        SELECT categoria, sum({col}) as pesos, {col_dolares}COUNT(id) AS cant FROM {table}
        WHERE
        strftime('%m', fecha) = '{month}'
        AND strftime('%Y', fecha) = '{year}'
        AND categoria NOT IN ('REINTEGRO', 'SUELDO', 'N/A', 'INVERSIONES')
        GROUP BY categoria
        ORDER BY categoria
        ;
        """.format(
            table=table, month=month, year=year, col=col, col_dolares=col_dolares
        )

        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(text(query))
            except Exception as e:
                print(e)
            else:
                for row in result:

                    if isinstance(row[0], bytes):
                        r0 = row[0].decode("utf-8")
                    else:
                        r0 = row[0]

                    if isinstance(row[1], bytes):
                        r1 = row[1].decode("utf-8")
                    else:
                        r1 = row[1]

                    if isinstance(row[2], bytes):
                        r2 = row[2].decode("utf-8")
                    else:
                        r2 = row[2]

                    # formatos para print
                    # http://programarcadegames.com/index.php?chapter=formatting&lang=en
                    if table == "debit":
                        print(f"{r0:<20};{r1:22.2f};{r2:22}")
                    else:
                        print(f"{r0:<22};{r1:22.2f};{r2:22.2f};{row[3]:22}")

                result.close()
        print("\n")
