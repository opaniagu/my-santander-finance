# App para Automatizacion (web scrapping) de Banco Santander

Aplicacion para la gestion de cuentas del banco Santander de Argentina, permite:

- [x] obtener el resumen de la cuenta realizando un download del archivo con los registros de los ultimos 60 dias

- [x] transformarlos y cargarlos en una base de datos sqlite

- [] etiquetar los consumos para luego generar reportes


## Environment Variables

Para ejecutar este proyecto se necesitan las siguientes variables de entorno, pudiendo ser definidas en un archivo .env:

`DNI`

`CLAVE`

`USUARIO`

_Estos datos, son los requeridos para el login en la web de Santander._ 


## Instalacion

Instalar utilizando pip

```bash
  pip install my-santander-finance
```

## Utilizacion

```bash
  app
```



## Feedback

Contactarme a opaniagu@gmail.com

## Authors

- [@opaniagu](https://www.github.com/opaniagu)


## License

[MIT](https://choosealicense.com/licenses/mit/)