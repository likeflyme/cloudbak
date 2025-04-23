import os

from pydantic_settings import BaseSettings
from config.app_config import settings as app_settings


class Settings(BaseSettings):
    home: str = 'wx/'
    msg_path: str = 'Msg/'
    head_path: str = 'SysHead/'
    multi_msg_db: str = 'Multi/decoded_MSG0.db'
    micro_msg_db: str = 'decoded_MicroMsg.db'
    misc_db: str = 'decoded_Misc.db'
    hard_link_image_db: str = 'decoded_HardLinkImage.db'
    file_storage_path: str = 'FileStorage/'
    msg_attach_path: str = 'MsgAttach/'

    class Config:
        env_prefix = 'DATA_'
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'allow'


settings = Settings()


def home():
    return os.path.join(app_settings.sys_dir, settings.home)
