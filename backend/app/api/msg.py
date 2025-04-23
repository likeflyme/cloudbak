from collections import defaultdict
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.dependencies.auth_dep import get_session_manager, \
    get_message_manager, get_contact_manager, get_chat_room_manager
from app.exception.biz_exception import BizException
from config.log_config import logger
from wx.common.filters.contact_filter import ContactFilterObj
from wx.common.filters.msg_filter import SingleMsgFilterObj, MsgFilterObj
from wx.common.filters.session_filter import SessionFilterObj
from wx.common.output.chat_room import ChatRoomInfo
from wx.common.output.contact import ContactSearchOut, Contact
from wx.common.output.message import Msg, MsgSearchOut
from wx.common.output.session import Session as SessionOut
from wx.interface.wx_interface import SessionManager, MessageManager, ContactManager, ChatRoomManager

session_local_dict = defaultdict(lambda: None)

router = APIRouter(
    prefix="/msg"
)


@router.get("/session", response_model=Optional[SessionOut])
def red_session(username: str, session_manager: SessionManager = Depends(get_session_manager)):
    if session_manager is None:
        return None
    return session_manager.session(username)


@router.post("/sessions", response_model=List[SessionOut])
def red_sessions(filter_obj: SessionFilterObj, session_manager: SessionManager = Depends(get_session_manager)):
    """ 查询会话分页列表 """
    if session_manager is None:
        return []
    return session_manager.sessions_page(filter_obj)


@router.get("/msg_by_svr_id", response_model=Optional[Msg])
def red_msg_by_svr_id(username: str, v3_msg_svr_id: int, message_manager: MessageManager = Depends(get_message_manager)):
    if message_manager is None:
        return None
    return message_manager.message(SingleMsgFilterObj(username=username, v3_msg_svr_id=v3_msg_svr_id))


@router.get("/single-msg", response_model=Optional[Msg])
def single_msg(username: str, v3_msg_svr_id: int, message_manager: MessageManager = Depends(get_message_manager)):
    if message_manager is None:
        return None
    return message_manager.message(SingleMsgFilterObj(username=username, v3_msg_svr_id=v3_msg_svr_id))


@router.post("/msgs", response_model=MsgSearchOut)
def red_msgs(filter_obj: MsgFilterObj, message_manager: MessageManager = Depends(get_message_manager)):
    if message_manager is None:
        return MsgSearchOut(start=0, messages=[])
    return message_manager.messages_filter_page(filter_obj)


@router.get("/contact", response_model=List[Contact])
def red_contact(contact_manager: ContactManager = Depends(get_contact_manager)):
    logger.info("获取联系人列表")
    if contact_manager is None:
        return []
    return contact_manager.base_contacts()


@router.get("/contact-search", response_model=ContactSearchOut)
async def contact_search(search: str, contact_manager: ContactManager = Depends(get_contact_manager)):
    if contact_manager is None:
        raise BizException("该微信版本暂不支持联系人搜索")
    return contact_manager.contacts_search(ContactFilterObj(search=search))


@router.post("/contact-page", response_model=List[Contact])
def contact_page(filter_obj: ContactFilterObj, contact_manager: ContactManager = Depends(get_contact_manager)):
    logger.info(f"获取联系人列表, {filter_obj}")
    if contact_manager is None:
        return []
    return contact_manager.contacts(filter_obj)


@router.get("/chatroom-info", response_model=ChatRoomInfo)
async def get_chatroom_info(username: str, chat_room_manager: ChatRoomManager = Depends(get_chat_room_manager)):
    if chat_room_manager is None:
        return ChatRoomInfo(username=username)
    return chat_room_manager.chatroom_info(username)
