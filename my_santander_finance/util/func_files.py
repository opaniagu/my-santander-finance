"""
https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading
"""
import os
import time
from datetime import datetime

from my_santander_finance.config.settings import settings


def tiny_file_rename(newname, folder_of_download, time_to_wait=60):

    print(newname)
    print(folder_of_download)
    # quit()

    time_counter = 0
    try:
        filename = max(
            [f for f in os.listdir(folder_of_download)],
            key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)),
        )
    except ValueError:
        # if dir is empty....
        print("tiny_file_rename:: dir is empty?")
        return

    print(f"tiny_file_rename - filename:: {filename}")
    # quit()

    while ".part" in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception("Waited too long for file to download")
    # quit()

    filename = max(
        [f for f in os.listdir(folder_of_download)],
        key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)),
    )

    print(filename)
    print(os.path.join(folder_of_download, filename))
    print(os.path.join(folder_of_download, newname))
    # quit()

    try:
        os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))
    # For permission related errors
    except PermissionError:
        print("Operation not permitted.")
    # For other errors
    except OSError as error:
        print(error)


if __name__ == "__main__":
    # new_file_name = datetime.now().strftime("debit_%Y-%m-%d_%H#%M#%S.xls")
    # tiny_file_rename(new_file_name, settings.DOWNLOAD_CUENTA_DIR)

    new_file_name = datetime.now().strftime("amex_%Y-%m-%d_%H#%M#%S.xls")
    tiny_file_rename(new_file_name, settings.DOWNLOAD_AMEX_DIR)
