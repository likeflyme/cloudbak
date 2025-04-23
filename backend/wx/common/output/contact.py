from typing import Optional

from pydantic import BaseModel

from wx.common.output.chat_room import ChatRoom


class Contact(BaseModel):
    username: str
    type: Optional[int] = None
    alias: Optional[str] = None
    remark: Optional[str] = None
    remark_quanpin: Optional[str] = None
    remark_quanpin_initial: Optional[str] = None
    nickname: Optional[str] = None
    nickname_quanpin: Optional[str] = None
    nickname_quanpin_initial: Optional[str] = None
    small_head_url: Optional[str] = None
    big_head_url: Optional[str] = None


class ContactSearchOut(BaseModel):
    contacts: list[Contact] = []
    chatrooms: list[ChatRoom] = []

