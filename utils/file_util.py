from typing import Callable

from PySide6 import QtWidgets


def choose_file(on_result: Callable[[str], None], file_filter: str = None):
    dialog = QtWidgets.QFileDialog()
    dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
    if file_filter:
        dialog.setNameFilter(file_filter)
    dialog.fileSelected.connect(lambda path: on_result(path) if path else None)
    dialog.exec()


def choose_folder(on_result: Callable[[str], None]):
    folder_path = QtWidgets.QFileDialog.getExistingDirectory()
    if folder_path:
        on_result(folder_path)
