import os.path

from PySide6 import QtWidgets

from contract.home.home_controller_contract import HomeControllerContract
from utils import file_util
from utils.view_util import set_children_visible
from view.collapsible_box import CollapsibleBox


class SignatureConfigBox(CollapsibleBox):

    def __init__(self, controller: HomeControllerContract):
        super().__init__("Signature Config")

        self._controller = controller

        self._generate_view()
        self._init_signal_slot()

    def _generate_view(self):
        self._create_new_signature_checkbox = QtWidgets.QCheckBox("Create New Signature")
        self._signatures_config_path_layout = self._generate_signatures_config_path_layout()

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self._create_new_signature_checkbox)
        vertical_layout.addLayout(self._generate_key_store_path_layout())
        vertical_layout.addLayout(self._generate_key_store_password_layout())
        vertical_layout.addLayout(self._generate_key_alias_layout())
        vertical_layout.addLayout(self._generate_key_password_layout())
        vertical_layout.addLayout(self._signatures_config_path_layout)

        self.setLayout(vertical_layout)

    def _generate_key_store_path_layout(self) -> QtWidgets.QLayout:
        key_store_path_label = QtWidgets.QLabel("Key Store Path:")
        self._key_store_path_edit = QtWidgets.QLineEdit()
        self._key_store_path_edit.setPlaceholderText("Please choose a file for key store")
        self._key_store_path_button = QtWidgets.QPushButton("Choose")

        key_store_path_layout = QtWidgets.QHBoxLayout()
        key_store_path_layout.addWidget(key_store_path_label)
        key_store_path_layout.addWidget(self._key_store_path_edit)
        key_store_path_layout.addWidget(self._key_store_path_button)

        return key_store_path_layout

    def _generate_key_store_password_layout(self) -> QtWidgets.QLayout:
        key_store_password_label = QtWidgets.QLabel("Key Store Password:")
        self._key_store_password_edit = QtWidgets.QLineEdit()
        self._key_store_password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)
        self._key_store_password_edit.setPlaceholderText("Please input password for key store")

        key_store_password_layout = QtWidgets.QHBoxLayout()
        key_store_password_layout.addWidget(key_store_password_label)
        key_store_password_layout.addWidget(self._key_store_password_edit)

        return key_store_password_layout

    def _generate_key_alias_layout(self) -> QtWidgets.QLayout:
        key_alias_label = QtWidgets.QLabel("Key Alias:")
        self._key_alias_edit = QtWidgets.QLineEdit()
        self._key_alias_edit.setPlaceholderText("Please input alias for key")

        key_alias_layout = QtWidgets.QHBoxLayout()
        key_alias_layout.addWidget(key_alias_label)
        key_alias_layout.addWidget(self._key_alias_edit)

        return key_alias_layout

    def _generate_key_password_layout(self) -> QtWidgets.QLayout:
        key_password_label = QtWidgets.QLabel("Key Password:")
        self._key_password_edit = QtWidgets.QLineEdit()
        self._key_password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)
        self._key_password_edit.setPlaceholderText("Please input password for key")

        key_password_layout = QtWidgets.QHBoxLayout()
        key_password_layout.addWidget(key_password_label)
        key_password_layout.addWidget(self._key_password_edit)

        return key_password_layout

    def _generate_signatures_config_path_layout(self) -> QtWidgets.QLayout:
        signatures_config_path_label = QtWidgets.QLabel("Signatures Config Path:")
        self._signatures_config_path_edit = QtWidgets.QLineEdit()
        self._signatures_config_path_edit.setPlaceholderText("Please choose a file for signatures config")
        self._signatures_config_path_button = QtWidgets.QPushButton("Choose")

        signatures_config_path_layout = QtWidgets.QHBoxLayout()
        signatures_config_path_layout.addWidget(signatures_config_path_label)
        signatures_config_path_layout.addWidget(self._signatures_config_path_edit)
        signatures_config_path_layout.addWidget(self._signatures_config_path_button)

        return signatures_config_path_layout

    def _init_signal_slot(self):
        self._create_new_signature_checkbox.toggled.connect(self._controller.update_is_create_new_signature)
        self._key_store_path_edit.textChanged.connect(self._controller.update_key_store_path)
        self._key_store_path_button.clicked.connect(self._on_key_store_path_choose_clicked)
        self._key_store_password_edit.textChanged.connect(self._controller.update_key_store_password)
        self._key_alias_edit.textChanged.connect(self._controller.update_key_alias)
        self._key_password_edit.textChanged.connect(self._controller.update_key_password)
        self._signatures_config_path_edit.textChanged.connect(self._controller.update_signatures_config_path)
        self._signatures_config_path_button.clicked.connect(self._on_signatures_config_path_choose_clicked)

    def _on_key_store_path_choose_clicked(self):
        def choose_file():
            file_util.choose_file(
                file_filter='Key Store (*.jks *.keystore)',
                on_result=lambda path: self._key_store_path_edit.setText(os.path.abspath(path))
            )

        def choose_folder():
            def on_result(directory: str):
                path = self._controller.get_key_store_path(os.path.abspath(directory))
                self._key_store_path_edit.setText(path)

            file_util.choose_folder(on_result)

        self._controller.choose_key_store_path(choose_file, choose_folder)

    def _on_signatures_config_path_choose_clicked(self):
        file_util.choose_file(
            file_filter='Signatures Config (*.json)',
            on_result=lambda path: self._signatures_config_path_edit.setText(path)
        )

    def is_create_new_signature_changed(self, is_create_new_signature: bool):
        self._create_new_signature_checkbox.setChecked(is_create_new_signature)

        if is_create_new_signature:
            placeholder_text = 'Please choose a file for key store'
        else:
            placeholder_text = 'Please choose a directory for key store'
        self._key_store_path_edit.setPlaceholderText(placeholder_text)
        set_children_visible(self._signatures_config_path_layout, is_create_new_signature)

    def key_store_path_changed(self, key_store_path: str):
        self._key_store_path_edit.setText(key_store_path)

    def key_store_path_choose_enabled(self, is_enabled: bool):
        self._key_store_path_button.setEnabled(is_enabled)

    def key_store_password_changed(self, key_store_password: str):
        self._key_store_password_edit.setText(key_store_password)

    def key_alias_changed(self, key_alias: str):
        self._key_alias_edit.setText(key_alias)

    def key_password_changed(self, key_password: str):
        self._key_password_edit.setText(key_password)

    def signatures_config_path_changed(self, signatures_config_path: str):
        self._signatures_config_path_edit.setText(signatures_config_path)
