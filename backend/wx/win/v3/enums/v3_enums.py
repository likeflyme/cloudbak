from enum import StrEnum


class V3DBEnum(StrEnum):
    DB_MULTI = 'Msg/Multi'
    DB_MULTI_MSG = 'Msg/Multi/decoded_MSG'
    DB_MULTI_MEDIA_MSG = 'Msg/Multi/decoded_MediaMSG'
    DB_MICRO_MSG = 'Msg/decoded_MicroMsg.db'
    DB_MISC = 'Msg/decoded_Misc.db'
    DB_HARD_LINK_IMAGE = 'Msg/decoded_HardLinkImage.db'
    DB_PUBLIC_MSG = 'Msg/decoded_PublicMsg.db'
    DB_OPENIM_MSG = 'Msg/decoded_OpenIMMsg.db'
    DB_OPENIM_CONTACT = 'Msg/decoded_OpenIMContact.db'
    DB_OPENIM_MEDIA = 'Msg/decoded_OpenIMMedia.db'
    # 解析后的数据库文件前缀
    DECODED_DB_PREFIX = 'decoded_'
    # 存放MEDIA解密数据
    DECODED_MEDIA_PATH = 'decoded_Media'
