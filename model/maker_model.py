import json


class MakerModel:

    def __init__(self):
        self._apk_path: str | None = None
        self._is_create_new_signature: bool = True
        self._key_store_path: str | None = None
        self._key_store_password: str | None = None
        self._key_alias: str | None = None
        self._key_password: str | None = None
        self._signatures_config_path: str | None = None
        self._is_generate_google_play_upload_key: bool = True
        self._encryption_public_key_path: str | None = None
        self._encrypted_key_output_path: str | None = None
        self._aab_output_path: str | None = None

    def serialization(self):
        return json.dumps({
            'apk_path': self._apk_path,
            'is_create_new_signature': self._is_create_new_signature,
            'key_store_path': self._key_store_path,
            'key_store_password': self._key_store_password,
            'key_alias': self._key_alias,
            'key_password': self._key_password,
            'signatures_config_path': self._signatures_config_path,
            'is_generate_google_play_upload_key': self._is_generate_google_play_upload_key,
            'encryption_public_key_path': self._encryption_public_key_path,
            'encrypted_key_output_path': self._encrypted_key_output_path,
            'aab_output_path': self._aab_output_path
        }, indent=4, ensure_ascii=False)

    @staticmethod
    def deserialization(json_data: str):
        data = json.loads(json_data)
        model = MakerModel()
        model.apk_path = data['apk_path']
        model.is_create_new_signature = data['is_create_new_signature']
        model.key_store_path = data['key_store_path']
        model.key_store_password = data['key_store_password']
        model.key_alias = data['key_alias']
        model.key_password = data['key_password']
        model.signatures_config_path = data['signatures_config_path']
        model.is_generate_google_play_upload_key = data['is_generate_google_play_upload_key']
        model.encryption_public_key_path = data['encryption_public_key_path']
        model.encrypted_key_output_path = data['encrypted_key_output_path']
        model.aab_output_path = data['aab_output_path']

        return model

    @property
    def apk_path(self) -> str | None:
        return self._apk_path

    @apk_path.setter
    def apk_path(self, value: str | None):
        self._apk_path = value

    @property
    def is_create_new_signature(self) -> bool:
        return self._is_create_new_signature

    @is_create_new_signature.setter
    def is_create_new_signature(self, value: bool):
        self._is_create_new_signature = value

    @property
    def key_store_path(self) -> str | None:
        return self._key_store_path

    @key_store_path.setter
    def key_store_path(self, value: str | None):
        self._key_store_path = value

    @property
    def key_store_password(self) -> str | None:
        return self._key_store_password

    @key_store_password.setter
    def key_store_password(self, value: str | None):
        self._key_store_password = value

    @property
    def key_alias(self) -> str | None:
        return self._key_alias

    @key_alias.setter
    def key_alias(self, value: str | None):
        self._key_alias = value

    @property
    def key_password(self) -> str | None:
        return self._key_password

    @key_password.setter
    def key_password(self, value: str | None):
        self._key_password = value

    @property
    def signatures_config_path(self) -> str | None:
        return self._signatures_config_path

    @signatures_config_path.setter
    def signatures_config_path(self, value: str | None):
        self._signatures_config_path = value

    @property
    def is_generate_google_play_upload_key(self) -> bool:
        return self._is_generate_google_play_upload_key

    @is_generate_google_play_upload_key.setter
    def is_generate_google_play_upload_key(self, value: bool):
        self._is_generate_google_play_upload_key = value

    @property
    def encryption_public_key_path(self) -> str | None:
        return self._encryption_public_key_path

    @encryption_public_key_path.setter
    def encryption_public_key_path(self, value: str | None):
        self._encryption_public_key_path = value

    @property
    def encrypted_key_output_path(self) -> str | None:
        return self._encrypted_key_output_path

    @encrypted_key_output_path.setter
    def encrypted_key_output_path(self, value: str | None):
        self._encrypted_key_output_path = value

    @property
    def aab_output_path(self) -> str | None:
        return self._aab_output_path

    @aab_output_path.setter
    def aab_output_path(self, value: str | None):
        self._aab_output_path = value

