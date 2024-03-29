import json
import os.path
import re
from typing import Callable

from contract.home.home_controller_contract import HomeControllerContract
from contract.home.home_view_contract import HomeViewContract
from controller.home_worker import HomeWorker
from logger import Logger
from model.maker_model import MakerModel
from persistence import local_persistence


class BaseHomeController(HomeControllerContract):

    def __init__(self, view: HomeViewContract):
        super().__init__()

        self._view: HomeViewContract = view
        self._model: MakerModel = MakerModel()

        self._worker: HomeWorker | None = None


class HomeController(BaseHomeController):
    APP_NAME_REGEX = r"(?P<APP_NAME>[a-zA-Z0-9]+)_\d+.\d+(.\d+)?_\d+\w*(?=.apk)"

    SIGNATURE_FILE_BASE_PATH = 'D:\\Codes\\Signings'
    SIGNATURE_CONFIG_FILENAME = 'signatures_config.json'
    DEFAULT_KEY_STORE_PASSWORD = '123456'
    DEFAULT_KEY_PASSWORD = '123456'

    def init(self):
        try:
            self._model = MakerModel.deserialization(local_persistence.read('data.json'))
        except json.JSONDecodeError:
            pass

        self._view.apk_path_changed(self._model.apk_path)
        self._view.is_create_new_signature_changed(self._model.is_create_new_signature)
        self._view.key_store_path_changed(self._model.key_store_path)
        self._view.key_store_password_changed(self._model.key_store_password)
        self._view.key_alias_changed(self._model.key_alias)
        self._view.key_password_changed(self._model.key_password)
        self._view.signatures_config_path_changed(self._model.signatures_config_path)
        self._view.is_generate_google_play_upload_key_changed(self._model.is_generate_google_play_upload_key)
        self._view.encryption_public_key_path_changed(self._model.encryption_public_key_path)
        self._view.encrypted_key_output_path_changed(self._model.encrypted_key_output_path)
        self._view.aab_output_path_changed(self._model.aab_output_path)

        Logger.init(self._view.output_log)

    def update_apk_path(self, apk_path: str):
        self._model.apk_path = apk_path

        if apk_path:
            try:
                app_name_with_separator = self._transform_name_with_separator(self._get_app_name())

                # 更新签名文件配置
                self._view.is_create_new_signature_changed(True)

                key_store_path = os.path.join(self.SIGNATURE_FILE_BASE_PATH, f'{app_name_with_separator}.jks')
                self._view.key_store_path_changed(key_store_path)

                if self._model.is_create_new_signature:
                    self._view.key_store_path_choose_enabled(True)

                self._view.key_store_password_changed(self.DEFAULT_KEY_STORE_PASSWORD)

                self._view.key_alias_changed(app_name_with_separator)

                self._view.key_password_changed(self.DEFAULT_KEY_PASSWORD)

                signatures_config_path = os.path.join(self.SIGNATURE_FILE_BASE_PATH, self.SIGNATURE_CONFIG_FILENAME)
                self._view.signatures_config_path_changed(signatures_config_path)

                # 重置 Google Play 上传密钥配置
                self._view.encryption_public_key_path_changed('')
                self._view.encrypted_key_output_path_changed('')

                # 更新 Aab 输出路径
                aab_output_path = os.path.join(os.path.dirname(apk_path), self._get_aab_output_filename())
                self._view.aab_output_path_changed(aab_output_path)

                self._view.aab_output_path_choose_enabled(True)
            except Exception as e:
                Logger.error(f'Error occurred while updating apk path: {e}')
        else:
            if self._model.is_create_new_signature:
                self._view.key_store_path_choose_enabled(False)

            self._view.aab_output_path_choose_enabled(False)

    def _get_app_name(self):
        return re.search(self.APP_NAME_REGEX, self._model.apk_path).group('APP_NAME')

    @staticmethod
    def _transform_name_with_separator(app_name):
        app_name = app_name.replace(' ', '')
        transformed_app_name = ''
        for i in range(len(app_name)):
            current_char = app_name[i]
            if current_char.isupper():
                transformed_app_name += ('-' if i != 0 else '') + current_char.lower()
            else:
                transformed_app_name += current_char

        return transformed_app_name

    def update_is_create_new_signature(self, is_create_new_signature: bool):
        self._model.is_create_new_signature = is_create_new_signature

        self._view.is_create_new_signature_changed(is_create_new_signature)

        if not is_create_new_signature:
            self._view.key_store_path_choose_enabled(True)
        else:
            self._view.key_store_path_choose_enabled(bool(self._model.apk_path))

    def update_key_store_path(self, key_store_path: str):
        if self._model.key_store_path != key_store_path:
            self._model.key_store_path = key_store_path

            extension_name = os.path.splitext(key_store_path)[1]
            filename = os.path.basename(key_store_path).replace(extension_name, '')
            self._view.key_alias_changed(filename)

    def get_key_store_path(self, key_store_directory: str) -> str:
        try:
            return os.path.join(key_store_directory, self._get_key_store_filename())
        except Exception as e:
            Logger.error(f'Error occurred while getting key store path: {e}')

    def _get_key_store_filename(self):
        return f'{self._transform_name_with_separator(self._get_app_name())}.jks'

    def choose_key_store_path(self, choose_file: Callable[[], None], choose_folder: Callable[[], None]):
        choose_folder() if self._model.is_create_new_signature else choose_file()

    def update_key_store_password(self, key_store_password: str):
        self._model.key_store_password = key_store_password

    def update_key_alias(self, key_alias: str):
        self._model.key_alias = key_alias

    def update_key_password(self, key_password: str):
        self._model.key_password = key_password

    def update_signatures_config_path(self, signatures_config_path: str):
        self._model.signatures_config_path = signatures_config_path

    def update_is_generate_google_play_upload_key(self, is_generate_google_play_upload_key: bool):
        self._model.is_generate_google_play_upload_key = is_generate_google_play_upload_key

    def update_encryption_public_key_path(self, encryption_public_key_path: str):
        if self._model.encryption_public_key_path != encryption_public_key_path:
            self._model.encryption_public_key_path = encryption_public_key_path

            output_path = os.path.join(
                os.path.dirname(encryption_public_key_path),
                self._get_encrypted_key_output_filename()
            )
            self._view.encrypted_key_output_path_changed(output_path)

        self._view.encrypted_key_output_path_choose_enabled(bool(encryption_public_key_path))

    def update_encrypted_key_output_path(self, encrypted_key_output_path: str):
        self._model.encrypted_key_output_path = encrypted_key_output_path

    def get_encrypted_key_output_path(self, encrypted_key_output_directory: str) -> str:
        return os.path.join(encrypted_key_output_directory, self._get_encrypted_key_output_filename())

    def _get_encrypted_key_output_filename(self) -> str:
        encryption_public_key_filename = os.path.basename(self._model.encryption_public_key_path)
        encrypted_key_output_filename = encryption_public_key_filename.replace('.pem', '-encrypted.zip')
        encrypted_key_output_filename = self._transform_name_with_separator(encrypted_key_output_filename)

        return encrypted_key_output_filename

    def update_aab_output_path(self, aab_output_path: str):
        self._model.aab_output_path = aab_output_path

    def get_aab_output_path(self, aab_output_directory: str) -> str:
        return os.path.join(aab_output_directory, self._get_aab_output_filename())

    def _get_aab_output_filename(self) -> str:
        return str(os.path.basename(self._model.apk_path).replace('.apk', '.aab'))

    def run(self):
        if self._worker and self._worker.isRunning():
            Logger.warn('Action is running, please wait...')
            return

        self._worker = HomeWorker(self._model, self._view.output_log, self._view.output_log)
        self._worker.start()
