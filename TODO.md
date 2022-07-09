# TODO

### Todo

- [ ] Agregar soporte de log (loguru)
- [ ] Agregar modo "debug" (log)
- [ ] En el caso de no encontrar el driver chromedriver.exe, consultar si quiere realizar el download
- [ ] Mejorar la documentacion
- [ ] Agregar compatibilidad con linux
- [ ] Agregar que los archivos y directorios del "usuario" se guarden en el home del usuario (en linux)
- [ ] Agregar tests

### In Progress

### Done ✓

- [x] Realizar validaciones de que existan las variables de entorno o el archivo .env con los datos necesarios para el login en la web de Santander

- [x] Renombrar los archivos que se mueven a download\debit.old con esta mascara: debit_yyyy-mm-dd_hh#mm#ss.xls

- [x] Agregar soporte a lint ( flake8, isort, black, pre-commit )

- [x] Agregar que los archivos y directorios del "usuario" se guarden en el home del usuario (en windows)
- [x] Crear si no existe un archivo de ejemplo .env.example en el home local
- [x] Cambiar el nombre de la app a "sanfi"

        pyproject.toml
        ```
        [tool.poetry.scripts]
        sanfi = "my_santander_finance.app:main"
        ```
