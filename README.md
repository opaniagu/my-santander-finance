# App para Automatizacion (web scrapping) de Banco Santander

Aplicacion para la gestion de cuentas del banco Santander de Argentina, permite:

* [x] obtener el resumen de la cuenta(download) de los ultimos 60 dias
* [x] transformarlos y cargarlos en una base de datos (sqlite)
* [ ] clasificar y etiquetar los consumos
* [ ] generar reportes

## Instalacion

_se requiere tener instalado python_

Instalar utilizando pip, desde la consola(cmd.exe):

```bash
  pip install my-santander-finance
```

## Actualizacion

Actualizar utilizando pip

```bash
  pip install --upgrade my-santander-finance
```

Luego verificar version
```bash
  sanfi --version
```


## Configuracion

La aplicacion crea un directorio en el 'home' del usuario con el nombre '.sanfi', por ejemplo en Windows seria en:

c:\Users\Oscar\.sanfi\

Para poder realizar el web scrapping de la pagina de Santander Argentina, es necesario definir tres(3) variables de entorno, ya sea como variables de entorno propiamente dichas o bien en un archivo en el raiz del directorio de la app llamado .env, por ejemplo:

c:\Users\Oscar\.sanfi\.env

### Environment Variables

Las tres(3) variables de entorno son:

`DNI`

`CLAVE`

`USUARIO`

_Estos datos, son los requeridos para el login en la web de Santander._ 

Para mas informacion de como trabajar con las variables de entorno hacer click en este link [variables de entorno](docs/es/environment_variables.md)

## Utilizacion

Desde la consola, ejecutar para obtener la ayuda:
```bash
sanfi --help
```

En el caso de querer realizar el download de los consumos:
```bash
sanfi --download
```
La informacion se guarda en una base de datos sqlite (santander.sqlite). Se puede consultar el formato de las tablas en [sqlite](my_santander_finance/sqlite.sql)

Para trabajar directamente con la base de datos sqlite, utilizo la siguiente herramienta grafica free para Windows [HeidiSQL](https://www.heidisql.com/)

Obviamente, tambien es posible utlizar al consola proporcionada por sqlite desde la linea de comandos:

```bash
sqlite3 --help
```
Para mas informacion, click en [sqlite3](docs/es/sqlite3.md)

## Crontab

Para mas informacion, click en [crontab](docs/es/crontab.md)

## Feedback

Contactarme a opaniagu@gmail.com

## Authors

- [@opaniagu](https://www.github.com/opaniagu)


## License

[MIT](https://choosealicense.com/licenses/mit/)
