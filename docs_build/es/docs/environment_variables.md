# Variables de Entorno

Para el caso especial del login a santander, es necesario ingresar las siguientes variables que deberian estar configuradas como variales de entorno:
* DNI
* CLAVE
* USUARIO

Las variables de entorno en Win10, se pueden setear desde el Panel de Control,
o bien desde la linea de comandos (cmd.exe)

Para hacerlo desde la linea de comandos, abrir una terminal y ejecutar por ejemplo:

```bash
setx DNI "12345678"
```
Para  comprobar el valor

```bash
echo %DNI%
```
```bash
set DNI
```
```bash
set | find "DNI"
```

Se tiene que tener en cuenta, que para que se vean los cambios,
se tiene que cerrar y abrir una nueva terminal

Tambien es compatible con [dotenv](https://pypi.org/project/python-dotenv/), es decir creando un archivo de texto '.env' en el home  de la app, con la definicion de las variables.

El formato es muy simple:

```dosini
# esto es un comentario
CLAVE=valor
```

por convencion se utiliza como nombres de clave en mayusculas.

A contiuacion se muestra un ejemplo del archivo necesario en el caso de utilizar un .env:

```dosini
# .env.example
DNI=12345678
CLAVE=clave
USUARIO=usuario
```
