r"""
Gestion de la configuracion.

Para el caso especial del login a santander, lee la configuracion desde las variables de entorno:
    - DNI
    - CLAVE
    - USUARIO

Las variables de entorno en Win10, se pueden setear desde el Panel de Control,
o bien desde la linea de comandos (cmd.exe)

Para hacerlo desde la linea de comandos, abrir una terminal:

c:\>setx DNI "12345678"

Para  comprobar el valor

echo %DNI%

Se tiene que tener en cuenta, que para que se vean los cambios,
se tiene que cerrar y abrir una nueva terminal

c:\>set DNI
DNI=12345678

o

c:\>set | find "DNI"
DNI=12345678

Tambien es compatible con dotenv (.env)

"""
from os.path import join

from pydantic import BaseSettings, Field, ValidationError

from my_santander_finance.definitions import HOME_DIR

# global, TODO! fix
GLOBAL_APP_NAME = "sanfi"
GLOBAL_LOCAL_DIR = join(HOME_DIR, "." + GLOBAL_APP_NAME)
GLOBAL_ENV_FILE = join(GLOBAL_LOCAL_DIR, ".env")


class Settings(BaseSettings):
    # general
    APP_NAME = GLOBAL_APP_NAME
    LOCAL_DIR = GLOBAL_LOCAL_DIR
    SANTANDER_LOGIN_URL = "https://www2.personas.santander.com.ar/obp-webapp/angular/#!/login"
    DOWNLOAD_DIR = join(LOCAL_DIR, "download\\")
    DOWNLOAD_CUENTA_DIR = DOWNLOAD_DIR + "debit"
    CVS_TEMP_DIR = join(LOCAL_DIR, "temp")

    # chromedriver
    CHROME_DRIVER_DIR = join(LOCAL_DIR, "driver")
    CHROME_DRIVER_EXE = join(LOCAL_DIR, "driver\\chromedriver.exe")
    CHROME_DRIVER_ZIP = join(LOCAL_DIR, "driver\\chromedriver.zip")

    # base de datos
    DATABASE_SQLITE = "santander.sqlite"

    # datos para acceso a santander (requeridos)
    DNI: str = Field(...)
    CLAVE: str = Field(...)
    USUARIO: str = Field(...)

    class Config:
        env_file = GLOBAL_ENV_FILE


# debug
# print(Settings().dict())

try:
    settings = Settings()
except ValidationError as e:
    print(e)
    quit()
