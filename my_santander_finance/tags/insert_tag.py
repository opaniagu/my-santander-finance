import os

from my_santander_finance.config.settings import settings
from my_santander_finance.database import mydatabase


def main():

    sqlite_filepath = os.path.join(settings.LOCAL_DIR, settings.DATABASE_SQLITE)
    dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname=sqlite_filepath)
    # dbms.print_all_data(mydatabase.VISA)
    dbms.unknown_query(table="visa")
    dbms.unknown_query(table="amex")
    dbms.unknown_query(table="debit")


# run the program
if __name__ == "__main__":
    main()
