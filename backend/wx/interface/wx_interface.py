from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import sessionmaker

from app.enum.resource_enum import ResourceType
from app.models.sys import SysSession, SysSessionExtra
from wx.common.enum.contact_type import ContactType
from wx.common.filters.contact_filter import ContactFilterObj
from wx.common.filters.fts_filter import FtsFilterObj
from wx.common.filters.msg_filter import MsgFilterObj, SingleMsgFilterObj
from wx.common.filters.session_filter import SessionFilterObj
from wx.common.output.chat_room import ChatRoomInfo
from wx.common.output.contact import Contact, ContactSearchOut
from wx.common.output.fts import FtsMsgCountTop, FtsMsgCount, FtsMsgCross
from wx.common.output.message import MsgSearchOut, Msg
from wx.common.output.session import Session, CheckResult


class DBManager(ABC):
    @abstractmethod
    def clear(self):
        """清除连接"""
        pass


class Decryptor(ABC):
    @abstractmethod
    def decrypt(self, deep: bool = False):
        """数据库解析"""
        pass


class ContactManager(ABC):
    """
    联系人管理器
    """
    @abstractmethod
    def contacts(self, filter_obj: ContactFilterObj = None) -> List[Contact]:
        pass

    @abstractmethod
    def contacts_search(self, filter_obj: ContactFilterObj) -> ContactSearchOut:
        pass

    @abstractmethod
    def contact_type(self, username: str) -> ContactType:
        pass

    @abstractmethod
    def base_contacts(self) -> List[Contact]:
        """
        基础联系人查询，不含陌生人
        """
        pass


class SessionManager(ABC):
    """
    会话管理器
    """
    @abstractmethod
    def sessions_page(self, filter_obj: SessionFilterObj) -> List[Session]:
        """会话分页查询"""
        pass

    def session(self, username: str) -> Session:
        pass


class ChatRoomManager(ABC):

    @abstractmethod
    def chatroom_info(self, username: str) -> ChatRoomInfo:
        pass


class MessageManager(ABC):
    """
    消息管理器
    """
    @abstractmethod
    def messages_filter_page(self, filter_obj: MsgFilterObj) -> MsgSearchOut:
        """聊天内消息搜索分页"""
        pass

    @abstractmethod
    def message(self, filter_obj: SingleMsgFilterObj) -> Msg | None:
        """单个聊天查询"""
        pass


class FTSManager(ABC):
    """
    全文索引管理器
    """
    @abstractmethod
    def fts_search(self, text: str) -> List[FtsMsgCount]:
        """全文搜索会话列表"""
        pass

    @abstractmethod
    def fts_messages(self, filter_obj: FtsFilterObj) -> FtsMsgCross:
        """全文搜索会话中的消息分页数据"""
        pass


class ResourceManager(ABC):

    @abstractmethod
    def windows_v3_image_from_full_md5(self, full_md5: str, prev: str = 'Thumb') -> str:
        pass

    @abstractmethod
    def get_decode_media_path(self) -> str:
        pass

    @abstractmethod
    def get_media_path(self, username: str, win_v3_msg_svr_id: str) -> str | None:
        pass

    @abstractmethod
    def get_wx_owner_img(self) -> str:
        """
        获取微信拥有者头像
        """
        pass

    @abstractmethod
    def get_video_poster(self, md5: str) -> str | None:
        """
        根据 md5 获取 video 封面图路径
        """
        pass

    @abstractmethod
    def get_video(self, md5: str) -> str | None:
        """
        根据 md5 获取 video 路径
        """
        pass

    @abstractmethod
    def get_member_head(self, username: str) -> bytearray | None:
        """
        获取群成员用户头像
        """
        pass


class ClientInterface(ABC):

    @abstractmethod
    def get_sys_session(self) -> SysSession:
        pass

    @abstractmethod
    def get_sys_session_extra(self) -> SysSessionExtra:
        pass

    @abstractmethod
    def get_db_manager(self) -> DBManager:
        pass

    @abstractmethod
    def get_decryptor(self) -> Decryptor:
        pass

    @abstractmethod
    def get_session_dir(self):
        pass

    @abstractmethod
    def get_wx_dir(self):
        pass

    @abstractmethod
    def get_real_wx_id(self):
        pass

    @abstractmethod
    def clear(self):
        """清理数据"""
        pass

    @abstractmethod
    def decrypt_db(self):
        """执行一次数据解析"""
        pass

    @abstractmethod
    def sys_session_check(self) -> CheckResult:
        """执行数据检查"""
        pass

    @abstractmethod
    def get_db_order_manager(self):
        pass

    @abstractmethod
    def get_taker_id_manager(self):
        pass

    @abstractmethod
    def get_contact_manager(self) -> ContactManager:
        pass

    @abstractmethod
    def get_session_manager(self) -> SessionManager:
        pass

    @abstractmethod
    def get_message_manager(self) -> MessageManager:
        pass

    @abstractmethod
    def get_fts_manager(self) -> FTSManager:
        pass

    @abstractmethod
    def get_chat_room_manager(self) -> ChatRoomManager:
        pass

    @abstractmethod
    def get_resource_manager(self) -> ResourceManager:
        pass

