import os
from abc import ABC

from app.models.sys import SysSession, SysSessionExtra
from config.app_config import settings as app_settings
from config.log_config import logger
from wx.common.output.session import CheckResult
from wx.interface.wx_interface import ClientInterface, DBManager, ContactManager, SessionManager, MessageManager, \
    FTSManager, ChatRoomManager, ResourceManager, Decryptor
from wx.win.v4.data.v4_chat_room_data import WindowsV4ChatRoomManager
from wx.win.v4.data.v4_contact_data import ContactManagerWindowsV4
from wx.win.v4.data.v4_message_data import MessageManagerWindowsV4
from wx.win.v4.data.v4_resource_data import WindowsV4ResourceManager
from wx.win.v4.data.v4_session_data import SessionManagerWindowsV4
from wx.win.v4.db.windows_v4_db import WindowsV4DB
from wx.win.v4.decryptor.windos_v4_decryptor import WindowsV4Decryptor


class WindowsClientV4(ClientInterface, ABC):

    def __init__(self, sys_session: SysSession, sys_session_extra: SysSessionExtra):
        self.sys_session = sys_session
        self.sys_session_extra = sys_session_extra
        self.session_dir = str(os.path.join(app_settings.sys_dir, app_settings.sessions_dir, str(sys_session.id)))
        self.wx_dir = os.path.join(self.session_dir, sys_session.wx_id)
        self.decryptor = WindowsV4Decryptor(self)
        self.contact_manager = ContactManagerWindowsV4(self)
        self.db_manager = WindowsV4DB(self)
        self.session_manager = SessionManagerWindowsV4(self)
        self.resource_manager = WindowsV4ResourceManager(self)
        self.message_manager = MessageManagerWindowsV4(self)
        self.chat_room_manager = WindowsV4ChatRoomManager(self.db_manager)

    def get_real_wx_id(self):
        wx_id = self.get_sys_session().wx_id
        real_wx_id = wx_id.rsplit('_', 1)[0]
        logger.info(f"微信4 id{wx_id}，真实id {real_wx_id}")
        return real_wx_id

    def get_sys_session(self) -> SysSession:
        return self.sys_session

    def get_sys_session_extra(self) -> SysSessionExtra:
        return self.sys_session_extra

    def get_db_manager(self) -> DBManager:
        return self.db_manager

    def get_db_decryptor(self) -> WindowsV4Decryptor:
        return self.decryptor

    def get_session_dir(self) -> str:
        return self.session_dir

    def get_wx_dir(self) -> str:
        return self.wx_dir

    def clear(self):
        self.db_manager.clear()
        self.message_manager.clear()
        self.contact_manager.clear()

    def decrypt_db(self):
        self.get_db_decryptor().decrypt()

    def sys_session_check(self) -> CheckResult:
        # 检查微信文件夹是否存在
        logger.info("检查微信文件夹是否存在")
        wx_dir = self.get_wx_dir()
        if not os.path.exists(wx_dir):
            return CheckResult(success=False, msg=f"微信目录 {wx_dir} 未创建，请手动创建或在 PC 客户端点击同步。")
        return CheckResult(success=True)

    def get_db_order_manager(self):
        pass

    def get_contact_manager(self) -> ContactManager:
        return self.contact_manager

    def get_session_manager(self) -> SessionManager:
        return self.session_manager

    def get_message_manager(self) -> MessageManager:
        return self.message_manager

    def get_fts_manager(self) -> FTSManager:
        pass

    def get_chat_room_manager(self) -> ChatRoomManager:
        return self.chat_room_manager

    def get_resource_manager(self) -> ResourceManager:
        return self.resource_manager

    def get_decryptor(self) -> Decryptor:
        return self.decryptor

    def get_taker_id_manager(self):
        pass

