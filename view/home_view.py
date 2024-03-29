import os.path

from PySide6 import QtWidgets, QtCore

from contract.home.home_view_contract import HomeViewContract
from controller.home_controller import HomeController, BaseHomeController
from utils import file_util
from view.google_play_upload_key_box import GooglePlayUploadKeyBox
from view.output_box import OutputBox
from view.signature_config_box import SignatureConfigBox


class BaseHomeView(HomeViewContract):
    def __init__(self, controller: BaseHomeController):
        self._controller = controller


class HomeView(BaseHomeView, QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        BaseHomeView.__init__(self, HomeController(self))

        self._generate_view()
        self._init_signal_slot()
        self._controller.init()

    def _generate_view(self):
        self._signature_config_box = SignatureConfigBox(self._controller)
        self._google_play_upload_key_box = GooglePlayUploadKeyBox(self._controller)
        self._output_box = OutputBox()

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        vertical_layout.addLayout(self._generate_apk_path_layout())
        vertical_layout.addWidget(self._signature_config_box)
        vertical_layout.addWidget(self._google_play_upload_key_box)
        vertical_layout.addLayout(self._generate_aab_output_path_layout())
        vertical_layout.addLayout(self._generate_bottom_action_layout())
        vertical_layout.addWidget(self._output_box)

        self.setLayout(vertical_layout)

    def _generate_apk_path_layout(self) -> QtWidgets.QLayout:
        apk_path_label = QtWidgets.QLabel("Apk Path:")
        self._apk_path_edit = QtWidgets.QLineEdit()
        self._apk_path_edit.setPlaceholderText("Please choose a apk file")
        self._apk_path_button = QtWidgets.QPushButton("Choose")

        apk_path_layout = QtWidgets.QHBoxLayout()
        apk_path_layout.addWidget(apk_path_label)
        apk_path_layout.addWidget(self._apk_path_edit)
        apk_path_layout.addWidget(self._apk_path_button)

        return apk_path_layout

    def _generate_aab_output_path_layout(self) -> QtWidgets.QLayout:
        aab_output_path_label = QtWidgets.QLabel("Aab Output Path:")
        self._aab_output_path_edit = QtWidgets.QLineEdit()
        self._aab_output_path_edit.setPlaceholderText("Please choose a directory for output aab file")
        self._aab_output_path_button = QtWidgets.QPushButton("Choose")

        aab_output_path_layout = QtWidgets.QHBoxLayout()
        aab_output_path_layout.addWidget(aab_output_path_label)
        aab_output_path_layout.addWidget(self._aab_output_path_edit)
        aab_output_path_layout.addWidget(self._aab_output_path_button)

        return aab_output_path_layout

    def _generate_bottom_action_layout(self) -> QtWidgets.QLayout:
        self._run_button = QtWidgets.QPushButton("Run")

        bottom_action_layout = QtWidgets.QHBoxLayout()
        bottom_action_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        bottom_action_layout.addWidget(self._run_button)

        return bottom_action_layout

    def _init_signal_slot(self):
        self._apk_path_edit.textChanged.connect(self._controller.update_apk_path)
        self._apk_path_button.clicked.connect(self._on_apk_path_choose_clicked)
        self._aab_output_path_edit.textChanged.connect(self._controller.update_aab_output_path)
        self._aab_output_path_button.clicked.connect(self._on_aab_output_path_choose_clicked)
        self._run_button.clicked.connect(self._controller.run)

    def _on_apk_path_choose_clicked(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("APK (*.apk)")
        dialog.fileSelected.connect(lambda path: self._apk_path_edit.setText(os.path.abspath(path)))
        dialog.exec()

    def _on_aab_output_path_choose_clicked(self):
        file_util.choose_folder(
            lambda path: self._aab_output_path_edit.setText(self._controller.get_aab_output_path(os.path.abspath(path)))
        )

    def apk_path_changed(self, apk_path: str):
        self._apk_path_edit.setText(apk_path)

    def is_create_new_signature_changed(self, is_create_new_signature: bool):
        self._signature_config_box.is_create_new_signature_changed(is_create_new_signature)

    def key_store_path_changed(self, key_store_path: str):
        self._signature_config_box.key_store_path_changed(key_store_path)

    def key_store_path_choose_enabled(self, is_enabled: bool):
        self._signature_config_box.key_store_path_choose_enabled(is_enabled)

    def key_store_password_changed(self, key_store_password: str):
        self._signature_config_box.key_store_password_changed(key_store_password)

    def key_alias_changed(self, key_alias: str):
        self._signature_config_box.key_alias_changed(key_alias)

    def key_password_changed(self, key_password: str):
        self._signature_config_box.key_password_changed(key_password)

    def signatures_config_path_changed(self, signatures_config_path: str):
        self._signature_config_box.signatures_config_path_changed(signatures_config_path)

    def is_generate_google_play_upload_key_changed(self, is_generate_google_play_upload_key: bool):
        self._google_play_upload_key_box.is_generate_google_play_upload_key_changed(is_generate_google_play_upload_key)

    def encryption_public_key_path_changed(self, encryption_public_key_path: str):
        self._google_play_upload_key_box.encryption_public_key_path_changed(encryption_public_key_path)

    def encrypted_key_output_path_changed(self, encrypted_key_output_path: str):
        self._google_play_upload_key_box.encrypted_key_output_path_changed(encrypted_key_output_path)

    def encrypted_key_output_path_choose_enabled(self, is_enabled: bool):
        self._google_play_upload_key_box.encrypted_key_output_path_choose_enabled(is_enabled)

    def aab_output_path_changed(self, aab_output_path: str):
        self._aab_output_path_edit.setText(aab_output_path)

    def aab_output_path_choose_enabled(self, is_enabled: bool):
        self._aab_output_path_button.setEnabled(is_enabled)

    def output_log(self, message: str):
        self._output_box.on_output_log(message)
