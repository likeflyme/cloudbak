from app.models.sys import SysSession, SysSessionExtra
from wx.interface.wx_interface import ClientInterface


class AbstractClientInterface(ClientInterface):
    """
    抽象客户端，实现一些通用功能
    """
    def __init__(self, sys_session: SysSession, sys_session_extra: SysSessionExtra):
        self.sys_session = sys_session
        self.sys_session_extra = sys_session_extra
