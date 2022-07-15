# Changelog

## [Unreleased]

## [0.3.1] - 2022-07-15
### Added
- Fixed typo on import_debito.py


## [0.3.0] - 2022-07-11
### Added
- Add visa credit card web scraping
- Refactor source code

## [0.2.7] - 2022-07-10
### Added
- Add crontab documentation
- Add argument --version
- Fixed on import_debit.py sqlite file path.

## [0.2.6] - 2022-07-10
### Added
- Changed 'app.py' to 'sanfi.py'
- Fixed minor bugs in sanfi.py
- Add log
- Add debug mode
- Add some docs/es files


## [0.2.5] - 2022-07-09
### Added
- Add support automatic download chromedriver on windows (version 103 and 104)

## [0.2.4] - 2022-07-09
### Added
- Add support to home directory on windows
- Add .env.example
- Change app name to "sanfi" (poetry build process - pyproject.toml)


## [0.2.3] - 2022-07-08
### Added
- Add support to lint


## [0.2.2] - 2022-07-08
### Added
- Rename downloaded files to debit_yyyy-mm-dd_hh#mm#ss.xls mask.


## [0.2.1] - 2022-07-07
### Added
- Validate (empty) env or .env variables, before start to login to bank url.


## [0.2.0] - 2022-07-07
### Added
- Start using "changelog" format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
- Start using "version" based on [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
- Add control version using bump
- Add Makefile
- Add docs folder with language support (en, es)

### Fixed
- Fix Settings CHROME_DRIVER_DIR to find "chromedriver.exe" based on ROOT_DIR


### Changed
- Start using 'en' (English) as default language comment code
