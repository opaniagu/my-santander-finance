import os
import sys

from my_santander_finance.config.settings import settings
from my_santander_finance.database import mydatabase


def main(table, month, year):
    sqlite_filepath = os.path.join(settings.LOCAL_DIR, settings.DATABASE_SQLITE)
    dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname=sqlite_filepath)

    dbms.report(table, month, year)


# run the program
if __name__ == "__main__":

    # total arguments
    n = len(sys.argv)
    # print("Total arguments passed:", n)

    # check arguments
    source = ["debit", "visa", "amex"]
    if sys.argv[1] not in source:
        print("source must be [debit,visa,amex]")
        quit()

    mounths = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    if sys.argv[2] not in mounths:
        print("mounth must be [01...12]")
        quit()

    years = ["2022", "2023", "2024", "2025"]
    if sys.argv[3] not in years:
        print("year must be [2022...2025]")
        quit()

    main(sys.argv[1], sys.argv[2], sys.argv[3])
