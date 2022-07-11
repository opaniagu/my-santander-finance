from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from my_santander_finance.config.settings import settings
from my_santander_finance.logger import Logger

log = Logger().get_logger(__name__)


def close_session(driver):
    """-- cerrar session --"""
    log.debug("trying close session Santander...")
    # click boton salir
    my_xpath = '//*[@id="topbar"]/div[1]/div/div[3]/a[5]'
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, my_xpath)))
    element.click()
    # aca aparece el modal: No | Si
    # click boton Si
    my_xpath = " /html/body/div[2]/md-dialog/topbar-logout-dialog/div/md-dialog-actions/div[2]/obp-boton/button"
    element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, my_xpath)))
    element.click()
    # end
    driver.close()
    log.debug("Session Santander...clossed")


def send_click_and_end(driver: webdriver, my_xpath: str):
    try:
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, my_xpath)))
        element.click()
    except TimeoutException as ex:
        log.debug(ex.message)
        # logout
        close_session(driver=driver)


def configure_driver(download_directory: str, chrome_start_maximized: bool = False):
    options = Options()
    if chrome_start_maximized is True:
        options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_directory + "\\",  # IMPORTANT - ENDING SLASH V IMPORTANT
        "directory_upgrade": True,
    }
    options.add_experimental_option("prefs", prefs)
    service = Service(executable_path=settings.CHROME_DRIVER_EXE)
    return options, service


def login(driver: webdriver):
    # -- start login --
    input_0 = settings.DNI
    input_1 = settings.CLAVE
    input_2 = settings.USUARIO

    driver.get(settings.SANTANDER_LOGIN_URL)
    driver.maximize_window()

    element = driver.find_element(By.ID, "input_0")
    element.send_keys(input_0)

    element = driver.find_element(By.ID, "input_1")
    element.send_keys(input_1)

    element = driver.find_element(By.ID, "input_2")
    element.send_keys(input_2)

    sleep(1)

    element.send_keys(Keys.RETURN)

    # -- end login --
