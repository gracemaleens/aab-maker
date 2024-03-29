import os
import sys

from PySide6 import QtWidgets

from view.home_view import HomeView


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aab Maker")
        self.setCentralWidget(HomeView())


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    with open(os.path.join(os.path.dirname(__file__), 'qss/common_style.qss'), 'r') as file_obj:
        app.setStyleSheet(file_obj.read())

    window = MainWindow()
    window.resize(800, 800)
    window.show()

    sys.exit(app.exec())
