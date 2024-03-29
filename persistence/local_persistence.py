import os

from PySide6.QtCore import QStandardPaths


def save(filename: str, content: str):
    with open(os.path.join(_get_base_directory(), filename), 'w', encoding='utf-8') as file:
        file.write(content)


def read(filename: str) -> str:
    path = os.path.join(_get_base_directory(), filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ''


def _get_base_directory():
    base_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    return base_directory
