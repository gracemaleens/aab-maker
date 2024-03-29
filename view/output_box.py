from PySide6 import QtWidgets
from PySide6.QtCore import Signal


class OutputBox(QtWidgets.QGroupBox):

    def __init__(self):
        super().__init__("Output")

        self._generate_view()
        self._init_signal_slot()

    def _generate_view(self):
        self._output_text_browser = QtWidgets.QTextBrowser()
        self._clear_button = QtWidgets.QPushButton("Clear")
        self._clear_button.setFixedWidth(50)

        box_layout = QtWidgets.QVBoxLayout()
        box_layout.addWidget(self._output_text_browser)
        box_layout.addWidget(self._clear_button)

        self.setLayout(box_layout)

    def _init_signal_slot(self):
        self._clear_button.clicked.connect(self._output_text_browser.clear)

    def on_output_log(self, message: str):
        self._output_text_browser.append(message)
