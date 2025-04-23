from enum import StrEnum


class V4DBEnum(StrEnum):
    DB_BASE_PATH = 'db_storage'
    # 解析后的数据库文件前缀
    DECODED_DB_PREFIX = 'decoded_'
    # 存放MEDIA解密数据
    DECODED_MEDIA_PATH = 'decoded_Media'
    CONTACT_DB_PATH = 'contact/decoded_contact.db'
    SESSION_DB_PATH = 'session/decoded_session.db'
    HEAD_IMAGE_DB_PATH = 'head_image/decoded_head_image.db'
    MESSAGE_DB_FOLDER = 'message'
    HARDLINK_DB_PATH = 'hardlink/decoded_hardlink.db'

    # 头像存放路径
    HEAD_IMAGE_FOLDER = 'head_image'
