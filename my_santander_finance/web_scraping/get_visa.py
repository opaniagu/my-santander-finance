from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from my_santander_finance.config.settings import settings
from my_santander_finance.logger import Logger
from my_santander_finance.util.func_files import tiny_file_rename
from my_santander_finance.web_scraping.import_visa import (
    import_csv_to_sqlite,
    xls_to_csv,
)
from my_santander_finance.web_scraping.santander_scraping import (
    close_session,
    configure_driver,
    login,
    send_click_and_end,
)

log = Logger().get_logger(__name__)


def download(driver: webdriver):
    # -- ingreso a 'Cuentas ' --
    my_xpath = '//*[@id="main-view"]/home/div/div/div[2]/div[1]/div/div/credit-card[1]/md-card/md-card-content'
    send_click_and_end(driver, my_xpath)
    sleep(3)
    log.debug("clicked credit card visa")
    # -- end ingreso a 'Cuentas ' --

    # click en href 'descargar'
    try:
        element_h = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "descargar")))
        element_h.click()
        sleep(3)
        log.debug("credit card visa report downloaded")
        new_file_name = datetime.now().strftime("visa_%Y-%m-%d_%H#%M#%S.xls")
        tiny_file_rename(new_file_name, settings.DOWNLOAD_VISA_DIR)
        log.debug(f"Renamed file to {settings.DOWNLOAD_VISA_DIR}\\{new_file_name}")
    except Exception as ex:
        log.debug("download:: Exception")
        log.debug(ex)


def get_visa(flag_download: bool):
    if flag_download is True:
        options, service = configure_driver(settings.DOWNLOAD_VISA_DIR, True)
        driver = webdriver.Chrome(service=service, options=options)
        login(driver=driver)
        download(driver)
        close_session(driver=driver)
    xls_to_csv(
        src_dir=settings.DOWNLOAD_VISA_DIR,
        src_ext=".xls",
        dst_dir=settings.CVS_TEMP_DIR,
        dst_ext=".csv",
    )
    import_csv_to_sqlite()


# ----------------------------------------------------
if __name__ == "__main__":
    get_visa()
