import json
import os
import shutil
from typing import Callable

from PySide6.QtCore import QThread, Signal

from model.maker_model import MakerModel
from persistence import local_persistence
from utils import cmd_util


class HomeWorker(QThread):
    log_info = Signal(str)
    log_error = Signal(str)

    def __init__(self, model: MakerModel, on_log_info: Callable[[str], None], on_log_error: Callable[[str], None]):
        super().__init__()

        self._model = model
        self.log_info.connect(on_log_info)
        self.log_error.connect(on_log_error)

    def run(self):
        try:
            self._generate_signature()
            self._generate_google_play_upload_key()
            self._build_aab()

            local_persistence.save('data.json', self._model.serialization())
        except Exception as e:
            self.log_error.emit(f'Action failed: {e}')

    def _generate_signature(self):
        if self._model.is_create_new_signature:
            self.log_info.emit('Generating signature...')

            if not self._model.key_store_path:
                self.log_error.emit('Please choose a keystore file')
                return

            if not self._model.key_store_password:
                self.log_error.emit('Please input password for keystore')
                return

            if not self._model.key_alias:
                self.log_error.emit('Please input alias for key')
                return

            if not self._model.key_password:
                self.log_error.emit('Please input password for key')
                return

            if not self._model.signatures_config_path:
                self.log_error.emit('Please choose a file for signatures config')
                return

            cmd = (
                'devkit gen-key '
                f'--keystore {self._model.key_store_path} '
                f'--ks-pass {self._model.key_store_password} '
                f'--alias {self._model.key_alias} '
                f'--key-pass {self._model.key_password} '
            )
            result = cmd_util.run(
                cmd,
                on_info=lambda message: self.log_info.emit(message),
                on_error=lambda message: self.log_error.emit(message)
            )
            if result == 0:
                self.log_info.emit(f'Signature generated successfully: {self._model.key_store_path}')

                self._save_signature_config()
                self._copy_signature_to_work_directory()

    def _save_signature_config(self):
        signature_config = {
            'keystore': self._model.key_store_path,
            'store_pass': self._model.key_store_password,
            'key_alias': self._model.key_alias,
            'key_pass': self._model.key_password
        }
        signature_name = os.path.basename(self._model.key_store_path).replace('.jks', '')
        signature_name = signature_name.replace('.keystore', '')

        signatures_config = self._read_signatures_config()
        signatures_config[signature_name] = signature_config

        self._write_signatures_config(signatures_config)

    def _read_signatures_config(self) -> dict:
        signatures_config_path = self._model.signatures_config_path
        if os.path.exists(signatures_config_path):
            with open(signatures_config_path, 'r') as file:
                return json.load(file)

        return {}

    def _write_signatures_config(self, signatures_config: dict):
        signatures_config_path = self._model.signatures_config_path
        with open(signatures_config_path, 'w') as file:
            json.dump(signatures_config, file, indent=4)

    def _copy_signature_to_work_directory(self):
        work_directory = os.path.dirname(self._model.apk_path)

        self.log_info.emit(f'Copying: {self._model.key_store_path} -> {work_directory}')

        shutil.copy2(self._model.key_store_path, work_directory)

    def _generate_google_play_upload_key(self):
        if self._model.is_generate_google_play_upload_key:
            self.log_info.emit('Generating Google Play upload key...')

            if not self._model.encryption_public_key_path:
                self.log_error.emit('Please choose a file for encryption public key')
                return

            if not os.path.exists(self._model.encryption_public_key_path):
                self.log_error.emit('Encryption public key file does not exist')
                return

            if not self._model.encrypted_key_output_path:
                self.log_error.emit('Please choose a directory for output upload key')
                return

            cmd = (
                'devkit export-pepk '
                f'--keystore {self._model.key_store_path} '
                f'--ks-pass {self._model.key_store_password} '
                f'--alias {self._model.key_alias} '
                f'--key-pass {self._model.key_password} '
                f'--encryption-public-key-path "{self._model.encryption_public_key_path}" '
                f'--output {self._model.encrypted_key_output_path}'
            )
            result = cmd_util.run(
                cmd,
                on_info=lambda message: self.log_info.emit(message),
                on_error=lambda message: self.log_error.emit(message)
            )
            if result == 0:
                self.log_info.emit(
                    f'Google Play upload key generated successfully: {self._model.encrypted_key_output_path}'
                )

    def _build_aab(self):
        self.log_info.emit('Building aab...')

        if not self._model.apk_path:
            self.log_error.emit('Please choose an apk file')
            return

        if not os.path.exists(self._model.apk_path):
            self.log_error.emit('Apk file does not exist')
            return

        if not self._model.is_create_new_signature and not os.path.exists(self._model.key_store_path):
            self.log_error.emit('Keystore file does not exist')
            return

        if not self._model.aab_output_path:
            self.log_error.emit('Please choose a directory for output aab')
            return

        cmd = (
            'packtool '
            f'--src {self._model.apk_path} '
            f'--out {self._model.aab_output_path} '
            'build-aab '
            f'--signature-name {self._model.key_alias} '
            f'--keystore {self._model.key_store_path} '
            f'--store-pass {self._model.key_store_password} '
            f'--key-alias {self._model.key_alias} '
            f'--key-pass {self._model.key_password} '
        )
        cmd_util.run(
            cmd,
            on_info=lambda message: self.log_info.emit(message),
            on_error=lambda message: self.log_error.emit(message)
        )
