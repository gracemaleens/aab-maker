import os.path

from PySide6 import QtWidgets

from contract.home.home_controller_contract import HomeControllerContract
from utils import file_util
from view.collapsible_box import CollapsibleBox


class GooglePlayUploadKeyBox(CollapsibleBox):

    def __init__(self, controller: HomeControllerContract):
        super().__init__("Generate Google Play Upload Key")

        self._controller = controller

        self._init_view()
        self._generate_view()
        self._init_signal_slot()

    def _init_view(self):
        self.setCheckable(True)

    def _generate_view(self):
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(self._generate_encryption_public_key_path_layout())
        vertical_layout.addLayout(self._generate_output_path_layout())

        self.setLayout(vertical_layout)

    def _generate_encryption_public_key_path_layout(self) -> QtWidgets.QLayout:
        encryption_public_key_path_label = QtWidgets.QLabel("Encryption Public Key Path (.pem):")
        self._encryption_public_key_path_edit = QtWidgets.QLineEdit()
        self._encryption_public_key_path_edit.setPlaceholderText("Please choose a file for encryption public key")
        self._encryption_public_key_path_button = QtWidgets.QPushButton("Choose")

        encryption_public_key_path_layout = QtWidgets.QHBoxLayout()
        encryption_public_key_path_layout.addWidget(encryption_public_key_path_label)
        encryption_public_key_path_layout.addWidget(self._encryption_public_key_path_edit)
        encryption_public_key_path_layout.addWidget(self._encryption_public_key_path_button)

        return encryption_public_key_path_layout

    def _generate_output_path_layout(self) -> QtWidgets.QLayout:
        output_path_label = QtWidgets.QLabel("Output Path:")
        self._output_path_edit = QtWidgets.QLineEdit()
        self._output_path_edit.setPlaceholderText("Please choose a directory for output upload key")
        self._output_path_button = QtWidgets.QPushButton("Choose")

        output_path_layout = QtWidgets.QHBoxLayout()
        output_path_layout.addWidget(output_path_label)
        output_path_layout.addWidget(self._output_path_edit)
        output_path_layout.addWidget(self._output_path_button)

        return output_path_layout

    def _init_signal_slot(self):
        self.toggled.connect(self._on_toggled)
        self._encryption_public_key_path_edit.textChanged.connect(self._on_encryption_public_key_path_text_changed)
        self._encryption_public_key_path_button.clicked.connect(self._on_encryption_public_key_path_choose_clicked)
        self._output_path_edit.textChanged.connect(self._controller.update_encrypted_key_output_path)
        self._output_path_button.clicked.connect(self._on_output_path_choose_clicked)

    def _on_toggled(self, is_checked: bool):
        self._controller.update_is_generate_google_play_upload_key(is_checked)

        self.collapsed = not is_checked

    def _on_encryption_public_key_path_text_changed(self, path: str):
        self._controller.update_encryption_public_key_path(path)

        self._output_path_button.setEnabled(bool(path))

    def _on_encryption_public_key_path_choose_clicked(self):
        file_util.choose_file(
            file_filter='Public Key (*.pem)',
            on_result=lambda path: self._encryption_public_key_path_edit.setText(os.path.abspath(path))
        )

    def _on_output_path_choose_clicked(self):
        file_util.choose_folder(
            lambda path: self._output_path_edit.setText(
                self._controller.get_encrypted_key_output_path(os.path.abspath(path))
            )
        )

    def is_generate_google_play_upload_key_changed(self, is_generate_google_play_upload_key: bool):
        self.setChecked(is_generate_google_play_upload_key)

    def encryption_public_key_path_changed(self, encryption_public_key_path: str):
        self._encryption_public_key_path_edit.setText(encryption_public_key_path)

    def encrypted_key_output_path_changed(self, encrypted_key_output_path: str):
        self._output_path_edit.setText(encrypted_key_output_path)
        self._output_path_button.setEnabled(bool(encrypted_key_output_path))

    def encrypted_key_output_path_choose_enabled(self, is_enabled: bool):
        self._output_path_button.setEnabled(is_enabled)
