# Lint
Se insalarán 4 herramientas:
    - flake8
    - black
    - isort
    - pre-commit

# flake8

## install
```bash
poetry add flake8
```
## using from shell
```bash
poetry run flake8 my_santander_finance/
```

## configure

Add a file .flake8 with the following:

```bash
$cat .flake8
[flake8]
max-line-length = 120
```

## flake8 Python in Visual Studio Code
https://code.visualstudio.com/docs/python/linting

```bash
$cat .vscode/settings.json
{
    "makefile.extensionOutputFolder": "./.vscode",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
    },
    "python.formatting.blackArgs": [
        "--line-length",
        "120"
    ],
}
```

# black

## install
```bash
poetry add black
```

## black Python in Visual Studio Code
https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0

_con la configuracion descripta en este link, al guardar, se auto-formatea el archivo_


```bash
$cat .vscode/settings.json
{
    "makefile.extensionOutputFolder": "./.vscode",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
    },
    "python.formatting.blackArgs": [
        "--line-length",
        "120"
    ],
}
```

## black Python in poetry

```bash
$cat pyproject.toml
[tool.black]
line-length = 120
```

## using from shell
```bash
poetry run black -S -l 120 --target-version py38 my_santander_finance/
```

# isort

## install
```bash
poetry add isort
```

## using from shell
```bash
poetry run isort my_santander_finance/
```

# pre-commit
https://pre-commit.com/

## install
```bash
poetry add pre-commit
```

## configuracion
```bash
$cat .pre-commit-config.yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.0.1
  hooks:
  - id: check-yaml
  - id: end-of-file-fixer

- repo: local
  hooks:
  - id: lint
    name: Lint
    entry: make lint
    types: [python]
    language: system
```

- run pre-commit install to set up the git hook scripts
poetry run pre-commit install

- now pre-commit will run automatically on git commit!

- (optional) Run against all the files
it's usually a good idea to run the hooks against all of the files when adding new hooks (usually pre-commit will only run on the changed files during git hooks)

```bash
$poetry run pre-commit run --all-files
```

# Makefile

```bash
$cat Makefile
...
lint: 
	poetry run isort my_santander_finance/
	poetry run black -S -l 120 --target-version py38 my_santander_finance/
	poetry run flake8 my_santander_finance/
```
