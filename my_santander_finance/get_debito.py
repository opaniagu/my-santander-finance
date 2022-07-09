import datetime
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from my_santander_finance.func_files import tiny_file_rename
from my_santander_finance.settings import settings


def close_session(driver):
    """-- cerrar session --"""
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


def send_click_and_end(driver: webdriver, my_xpath: str):
    try:
        element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, my_xpath)))
        element.click()
    except TimeoutException as ex:
        print(ex.message)
        # logout
        close_session(driver=driver)


def configure_driver():
    options = Options()
    options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": settings.DOWNLOAD_CUENTA_DIR + "\\",  # IMPORTANT - ENDING SLASH V IMPORTANT
        "directory_upgrade": True,
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(executable_path=settings.CHROME_DRIVER_DIR)

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


def download_debit(driver: webdriver):
    # -- ingreso a 'Cuentas ' --
    my_xpath = (
        '//*[@id="main-view"]/home/div/div/div[2]/div[1]/div/account-card/md-card/md-card-content/div[2]/div/button[1]'
    )
    send_click_and_end(driver, my_xpath)
    sleep(3)
    # -- end ingreso a 'Cuentas ' --

    # -- start set 60 dias de movimientos--
    # click en buscar movimientos (barra) para fijar 60 dias
    my_xpath = '//*[@id="grilla"]/cuentas-inicio-movimientos/div[2]/obp-selector/div/div/div/a'
    send_click_and_end(driver, my_xpath)
    sleep(3)
    # click en el boton buscar
    my_xpath = '//*[@id="grilla"]/cuentas-inicio-movimientos/div[2]/obp-selector/div/ng-transclude/cuentas-buscador/form/div[2]/obp-boton'  # noqa: E501
    send_click_and_end(driver, my_xpath)
    sleep(3)
    # -- end set 60 dias --

    # click en href 'descargar'
    try:
        element_h = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "descargar")))
        element_h.click()
        sleep(3)
        new_file_name = datetime.now().strftime("debit_%Y-%m-%d_%H#%M#%S.xls")
        tiny_file_rename(new_file_name, settings.DOWNLOAD_CUENTA_DIR)
    except:  # noqa: E722
        pass


# ----------------------------------------------------
if __name__ == "__main__":
    options, service = configure_driver()
    driver = webdriver.Chrome(service=service, options=options)
    login(driver=driver)
    download_debit(driver)
    close_session(driver=driver)
