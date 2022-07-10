import os
from os import listdir

from my_santander_finance.logger import Logger
from my_santander_finance.settings import settings

log = Logger().get_logger(__name__)


def get_list_files(dir: str, ext: str):
    lst = []
    for file in listdir(dir):
        if file.endswith(ext):
            lst.append(file)
    return lst


def create_dir(directory):
    log.debug(f"try creating directory: {directory}...")
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)  # succeeds even if directory exists.
        except FileExistsError:
            # directory already exists
            pass
    else:
        log.debug(f"directory: {directory}...already exist. Skiped")


# --------------------------------------------------------------------------
if __name__ == "__main__":
    print(get_list_files(settings.DOWNLOAD_CUENTA_DIR))
