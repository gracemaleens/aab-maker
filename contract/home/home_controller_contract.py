from typing import Callable


class HomeControllerContract:

    def init(self):
        pass

    def update_apk_path(self, apk_path: str):
        pass

    def update_is_create_new_signature(self, is_create_new_signature: bool):
        pass

    def update_key_store_path(self, key_store_path: str):
        pass

    def get_key_store_path(self, key_store_directory: str) -> str:
        pass

    def choose_key_store_path(self, choose_file: Callable[[], None], choose_folder: Callable[[], None]):
        pass

    def update_key_store_password(self, key_store_password: str):
        pass

    def update_key_alias(self, key_alias: str):
        pass

    def update_key_password(self, key_password: str):
        pass

    def update_signatures_config_path(self, signatures_config_path: str):
        pass

    def update_is_generate_google_play_upload_key(self, is_generate_google_play_upload_key: bool):
        pass

    def update_encryption_public_key_path(self, encryption_public_key_path: str):
        pass

    def update_encrypted_key_output_path(self, encrypted_key_output_path: str):
        pass

    def get_encrypted_key_output_path(self, encrypted_key_output_directory: str) -> str:
        pass

    def update_aab_output_path(self, aab_output_path: str):
        pass

    def get_aab_output_path(self, aab_output_directory: str) -> str:
        pass

    def run(self):
        pass
