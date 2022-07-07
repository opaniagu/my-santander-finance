"""
Gestion de la configuracion.

Para el caso especial del login a santander, lee la configuracion desde las variables de entorno:
    - DNI
    - CLAVE
    - USUARIO

Las variables de entorno en Win10, se pueden setear desde el Panel de Control,
o bien desde la linea de comandos (cmd.exe)

Para hacerlo desde la linea de comandos, abrir una terminal:

c:\>setx DNI "12345678"

Se tiene que tener en cuenta, que para que se vean lso cambios, 
se tiene que cerrar y abrir una nueva terminal

c:\>set DNI
DNI=12345678

o

c:\>set | find "DNI"
DNI=12345678

Tambien es compatible con dotenv (.env) 

"""
import os
from os.path import join

from pydantic import BaseSettings

from my_santander_finance.definitions import ROOT_DIR

class Settings(BaseSettings):
    # general
    SANTANDER_LOGIN_URL     = "https://www2.personas.santander.com.ar/obp-webapp/angular/#!/login"
    CHROME_DRIVER_DIR       = join(ROOT_DIR, "driver\\chromedriver.exe")
    DOWNLOAD_DIR            = join(ROOT_DIR, 'download\\')
    DOWNLOAD_CUENTA_DIR     = DOWNLOAD_DIR + "debit"
    CVS_TEMP_DIR            = join(ROOT_DIR, "temp")
    
    # base de datos
    DATABASE_SQLITE         = "santander.sqlite"
    
    # datos para acceso a santander
    DNI: str
    CLAVE: str
    USUARIO: str


# debug
# print(Settings().dict())

settings = Settings()
