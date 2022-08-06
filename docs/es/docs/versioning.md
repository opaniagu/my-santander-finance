# Versioning

Para el versionado utilizo la herramienta [bump2version](https://github.com/c4urself/bump2version)

## Instalación

```console
poetry add bumpversion
```

Al utilizar 'poetry', y generar un nuevo proyecto se crea un archivo '__init__.py', con el siguiente contenido:

```console
$ cat __init__.py
__version__ = '0.1.0'
```

Si no existe, se tiene que crear:

```console
$ echo '__version__ = "0.1.0"'> __init__.py
```

Crear el archivo de configuracion de bump2version, con el siguienet contenido:

```console
$ cat .bumpversion.cfg
[bumpversion]
current_version = 0.1.0
commit = True
tag = True

[bumpversion:file:my_santander_finance/__init__.py]
search = __version__ = "{current_version}"
replace = __version__ = "{new_version}"

[flake8]
exclude = docs
max-line-length = 88
docstring-convention = numpy
ignore = D1, W503

[isort]
profile = black
```
# Ejecución

show version
```console
$ poetry version
```

change version (only change pyproject.toml)
```console
$ poetry version minor
```

change version .bumpversion.cfg and my_santander_finance/__init__.py
_git repo must be clear_
```console
$ poetry run make bumpversion-minor
```

update (clear) git repository
```console
$ git add .
$ git commit -m "<message>"
$ git push
```
