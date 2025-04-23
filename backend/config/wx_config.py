from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_multi: str = 'Msg/Multi'
    db_multi_msg: str = 'Msg/Multi/decoded_MSG'
    db_multi_media_msg: str = 'Msg/Multi/decoded_MediaMSG'
    db_micro_msg: str = 'Msg/decoded_MicroMsg.db'
    db_misc: str = 'Msg/decoded_Misc.db'
    db_hard_link_image: str = 'Msg/decoded_HardLinkImage.db'
    db_public_msg: str = 'Msg/decoded_PublicMsg.db'
    db_openim_msg: str = 'Msg/decoded_OpenIMMsg.db'
    db_openim_contact: str = 'Msg/decoded_OpenIMContact.db'
    db_openim_media: str = 'Msg/decoded_OpenIMMedia.db'
    max_msg: int = 10
    decoded_media_path: str = 'decoded_Media/'

    class Config:
        env_prefix = 'WX_'
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'allow'


settings = Settings()
