import os.path

from app.models.sys import SysSession
from config.app_config import settings as app_setting
from config.wx_config import settings as wx_settings


def get_session_base_dir() -> str:
    return str(os.path.join(app_setting.sys_dir, app_setting.sessions_dir))


def get_session_dir(session_id) -> str:
    return os.path.join(get_session_base_dir(), str(session_id))


def get_wx_dir(sys_session: SysSession) -> str:
    return os.path.join(get_session_dir(sys_session.id), sys_session.wx_id)


def get_wx_dir_directly(session_id: int, wx_dir: str) -> str:
    return os.path.join(get_session_dir(str(session_id)), wx_dir)


def get_head_base_dir() -> str:
    return str(os.path.join(app_setting.sys_dir, app_setting.head_dir))


def get_head_session_dir(sys_session: SysSession) -> str:
    return os.path.join(get_head_base_dir(), str(sys_session.id))


def get_db_multi_msg_path(sys_session: SysSession) -> str:
    return os.path.join(get_wx_dir(sys_session), wx_settings.db_multi_msg)


def get_db_micro_msg_path(sys_session: SysSession) -> str:
    return os.path.join(get_wx_dir(sys_session), wx_settings.db_micro_msg)


def get_db_misc_path(sys_session: SysSession) -> str:
    return os.path.join(get_wx_dir(sys_session), wx_settings.db_misc)


def get_db_hard_link_image_path(sys_session: SysSession) -> str:
    return os.path.join(get_wx_dir(sys_session), wx_settings.db_hard_link_image)


def get_decoded_media_path(sys_session: SysSession) -> str:
    return os.path.join(get_wx_dir(sys_session), wx_settings.decoded_media_path)
