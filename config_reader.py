from pydantic import BaseSettings, SecretStr


class Setting(BaseSettings):
    bot_token: SecretStr
    admin_id: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Setting()
