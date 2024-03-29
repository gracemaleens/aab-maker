from enum import Enum
from typing import Callable

from PySide6 import QtWidgets


class DialogType(Enum):
    WARN = 1
    ERROR = 2


def show_dialog(
        dialog_type: DialogType,
        message: str,
        title: str = None,
        on_ok: Callable[[], None] = None,
        on_cancel: Callable[[], None] = None
):
    dialog = QtWidgets.QMessageBox()
    if dialog_type == DialogType.WARN:
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    elif dialog_type == DialogType.ERROR:
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    if title:
        dialog.setWindowTitle(title)
    standard_buttons = QtWidgets.QMessageBox.StandardButton.Ok
    if on_ok:
        dialog.button(QtWidgets.QMessageBox.StandardButton.Ok).clicked.connect(on_ok)
    if on_cancel:
        standard_buttons |= QtWidgets.QMessageBox.StandardButton.Cancel

        dialog.button(QtWidgets.QMessageBox.StandardButton.Cancel).clicked.connect(on_cancel)
    dialog.setStandardButtons(standard_buttons)
    dialog.setText(message)
    dialog.exec()

