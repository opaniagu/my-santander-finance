from pathlib import Path

ROOT_DIR = Path(__file__).parent
# ROOT_DIR = Path(__file__).parent.parent

# HOME_DIR is an object of class:
#   - PosixPath: if you're running on Linux or macOS
#   - WindowsPath: if you're running on Windows
# You can print it directly (including inside formatted f-strings)
# but if you want to perform string operations on it, you must first convert it to a string:
# https://csatlas.com/python-os-user-home-directory/
HOME_DIR = str(Path.home())
