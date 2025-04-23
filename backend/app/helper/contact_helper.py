from collections import defaultdict

from app.models.sys import SysSession

from db.wx_db import wx_db_for_conf
from wx.win.v3.models import public_msg, openim_msg, openim_contact
from config.wx_config import settings as wx_settings

# key: session_id + type
session_name_dict = defaultdict(lambda: None)

contact_normal = 0
contact_gh = 1
contact_openim = 2


def contact_type(strUsrName: str, sys_session: SysSession):
    """
    判断用户查询消息用户类型
    该方法会缓存微信id对应的类型
    :param strUsrName: 消息用户名
    :param sys_session: 用户会话
    :return:
        0-Multi, 正常 Multi 目录的消息
        1-publicMsg, 公众号等公共服务
        2-OpenIMMsg, 企业用户
    """
    normal_key = get_key_type(contact_normal, strUsrName, sys_session)
    gh_key = get_key_type(contact_gh, strUsrName, sys_session)
    openim_key = get_key_type(contact_openim, strUsrName, sys_session)
    # 先判断一次
    if normal_key in session_name_dict:
        return contact_normal
    if gh_key in session_name_dict:
        return contact_gh
    if openim_key in session_name_dict:
        return contact_openim
    # 都不存在
    # 先判断是否在 PublicMsg 中，再判断是否在 OpenIMContact 中
    if is_in_public_msg(strUsrName, sys_session):
        session_name_dict[gh_key] = True
        return contact_gh
    if is_in_openim_msg(strUsrName, sys_session):
        session_name_dict[contact_openim] = True
        return contact_openim

    session_name_dict[normal_key] = True
    return contact_normal


def clear():
    return None


def get_key_type(contact_type: int, strUsrName: str, sys_session: SysSession):
    return f"{sys_session}-{contact_type}-{strUsrName}"


def is_in_public_msg(strUsrName: str, sys_session: SysSession):
    pb_db = wx_db_for_conf(wx_settings.db_public_msg, sys_session)()
    try:
        name = pb_db.query(public_msg.Name2ID).filter_by(UsrName=strUsrName).first()
        return name is not None
    finally:
        pb_db.close()


def is_in_openim_msg(strUsrName: str, sys_session: SysSession):
    contact_db = wx_db_for_conf(wx_settings.db_openim_contact, sys_session)()
    try:
        name = contact_db.query(openim_contact.OpenIMContact).filter_by(UserName=strUsrName).first()
        return name is not None
    finally:
        contact_db.close()
