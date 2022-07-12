# TODO

### Todo

* [ ] config/settings.py: variables de entorno con prefix 'SANFI_', de esta manera, aseguramos que no colisione con otra app.
* [ ] clasificar y etiquetar los consumos
* [ ] generar reportes
* [ ] Refactor csv_to_sqlite() para que utilice sqlalchemy (en vez de sqlite3 lib)
* [ ] Agregar tests (pytest)
* [ ] Linux: Agregar compatibilidad con linux, en general
* [ ] Linux: Agregar compatibilidad con linux en chromedriver_download()
* [ ] Linux: Agregar que los archivos y directorios del "usuario" se guarden en el home del usuario (en linux)
* [ ] Agregar consumos de amex
* [ ] Publicar en netlify (sin el modulo de webscraping, para no comprometer las contraseñas)

### In Progress

* [ ] Mejorar la documentacion

### Done ✓

* [x] Realizar validaciones de que existan las variables de entorno o el archivo .env con los datos necesarios para el login en la web de Santander

* [x] Renombrar los archivos que se mueven a download\debit.old con esta mascara: debit_yyyy-mm-dd_hh#mm#ss.xls

* [x] Agregar soporte a lint ( flake8, isort, black, pre-commit )

* [x] Agregar que los archivos y directorios del "usuario" se guarden en el home del usuario (en windows)

* [x] Crear si no existe un archivo de ejemplo .env.example en el home local

* [x] Cambiar el nombre de la app a "sanfi"

        pyproject.toml
        ```
        [tool.poetry.scripts]
        sanfi = "my_santander_finance.app:main"
        ```
* [x] En el caso de no encontrar el driver chromedriver.exe, realizar el download (soporte version 103 y 104 Windows)

* [x] Agregar soporte de log

* [x] Agregar modo "debug" (log)

* [x] Ejecutar desde el crontab de Windows
  
* [x] Agregar argumento --version, para mostrar la version de la app

* [x] Agregar consumos de visa
