import os
from abc import ABC

from app.models.sys import SysSession, SysSessionExtra
from wx.common.output.session import CheckResult
from wx.interface.wx_interface import ClientInterface, Decryptor, DBManager, ContactManager, SessionManager, \
    MessageManager, FTSManager, ChatRoomManager, ResourceManager

from config.app_config import settings as app_settings
from wx.win.v3.data.chat_room_data import WindowsV3ChatRoomManager
from wx.win.v3.data.contact_data import ContactManagerWindowsV3
from wx.win.v3.data.fts_data import FTSManagerWindowsV3
from wx.win.v3.data.message_data import MessageManagerWindowsV3
from wx.win.v3.data.resource_data import WindowsV3ResourceManager
from wx.win.v3.data.session_data import SessionManagerWindowsV3
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from config.log_config import logger
from wx.win.v3.db.windows_v3_db_order import WindowsV3DBOrder
from wx.win.v3.db.windows_v3_db_taker_id import WindowsV3TakerId
from wx.win.v3.decryptor.windows_v3_decryptor import WindowsV3Decryptor, check_file_list


class WindowsClientV3(ClientInterface, ABC):

    def __init__(self, sys_session: SysSession, sys_session_extra: SysSessionExtra):
        logger.info("Initializing WindowsClientV3")
        self.name = "WindowsClientV3"
        self.sys_session = sys_session
        self.sys_session_extra = sys_session_extra
        self.session_dir = str(os.path.join(app_settings.sys_dir, app_settings.sessions_dir, str(self.sys_session.id)))
        self.wx_dir = os.path.join(self.session_dir, sys_session.wx_id)
        self.db_manager = WindowsV3DB(self)
        self.db_order = WindowsV3DBOrder(self.db_manager)
        self.decryptor = WindowsV3Decryptor(self)
        self.taker_id_manager = WindowsV3TakerId(self.db_manager)
        self.contact_manager = ContactManagerWindowsV3(self.db_manager)
        self.session_manager = SessionManagerWindowsV3(self.db_manager)
        self.message_manager = MessageManagerWindowsV3(self)
        self.fts_manager = FTSManagerWindowsV3(self.db_manager, self.db_order, self)
        self.chat_room_manager = WindowsV3ChatRoomManager(self.db_manager)
        self.resource_manager = WindowsV3ResourceManager(self)

    def get_real_wx_id(self):
        return self.get_sys_session().wx_id

    def get_sys_session(self) -> SysSession:
        return self.sys_session

    def get_sys_session_extra(self) -> SysSessionExtra:
        return self.sys_session_extra

    def get_db_manager(self) -> DBManager:
        return self.db_manager

    def get_decryptor(self) -> Decryptor:
        return self.decryptor

    def get_session_dir(self) -> str:
        return self.session_dir

    def get_wx_dir(self) -> str:
        return self.wx_dir

    def clear(self):
        logger.info(f"{self.name} execute clear method")
        self.db_manager.clear()
        self.db_order.clear()
        self.taker_id_manager.clear()
        self.fts_manager.clear()
        self.contact_manager.clear()

    def decrypt_db(self):
        logger.info(f"{self.name} decrypt db method")
        self.db_manager.clear()
        self.decryptor.decrypt()

    def get_db_order_manager(self):
        return self.db_order

    def get_taker_id_manager(self):
        return self.taker_id_manager

    def sys_session_check(self) -> CheckResult:
        # 检查微信文件夹是否存在
        logger.info("检查微信文件夹是否存在")
        wx_dir = self.get_wx_dir()
        if not os.path.exists(wx_dir):
            return CheckResult(success=False, msg=f"微信目录 {wx_dir} 未创建，请手动创建或在 PC 客户端点击同步。")
        # 检查库文件是否存在
        logger.info("检查必要的已解析的库文件是否存在")
        for db_name in check_file_list:
            file_path = os.path.join(wx_dir, db_name)
            if not os.path.exists(file_path):
                return CheckResult(success=False, msg=f"未发现已解析的库文件 {file_path}，请检查微信源文件是否上传并解析成功。")
        return CheckResult(success=True)

    def get_contact_manager(self) -> ContactManager:
        return self.contact_manager

    def get_session_manager(self) -> SessionManager:
        return self.session_manager

    def get_message_manager(self) -> MessageManager:
        return self.message_manager

    def get_fts_manager(self) -> FTSManager:
        return self.fts_manager

    def get_chat_room_manager(self) -> ChatRoomManager:
        return self.chat_room_manager

    def get_resource_manager(self) -> ResourceManager:
        return self.resource_manager
