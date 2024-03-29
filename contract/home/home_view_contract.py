class HomeViewContract:

    def apk_path_changed(self, apk_path: str):
        pass

    def is_create_new_signature_changed(self, is_create_new_signature: bool):
        pass

    def key_store_path_changed(self, key_store_path: str):
        pass

    def key_store_path_choose_enabled(self, is_enabled: bool):
        pass

    def key_store_password_changed(self, key_store_password: str):
        pass

    def key_alias_changed(self, key_alias: str):
        pass

    def key_password_changed(self, key_password: str):
        pass

    def signatures_config_path_changed(self, signatures_config_path: str):
        pass

    def is_generate_google_play_upload_key_changed(self, is_generate_google_play_upload_key: bool):
        pass

    def encryption_public_key_path_changed(self, encryption_public_key_path: str):
        pass

    def encrypted_key_output_path_changed(self, encrypted_key_output_path: str):
        pass

    def encrypted_key_output_path_choose_enabled(self, is_enabled: bool):
        pass

    def aab_output_path_changed(self, aab_output_path: str):
        pass

    def aab_output_path_choose_enabled(self, is_enabled: bool):
        pass

    def output_log(self, message: str):
        pass
