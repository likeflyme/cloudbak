from typing import Optional

from pydantic import BaseModel


class ChatRoom(BaseModel):
    ChatRoomName: str
    UserNameList: Optional[str] = None
    DisplayNameList: Optional[str] = None
    ChatRoomFlag: Optional[int] = None
    Owner: Optional[int] = None
    IsShowName: Optional[int] = None
    SelfDisplayName: Optional[str] = None
    Reserved1: Optional[int] = None
    Reserved2: Optional[str] = None
    Reserved3: Optional[int] = None
    Reserved4: Optional[str] = None
    Reserved5: Optional[int] = None
    Reserved6: Optional[str] = None
    Reserved7: Optional[int] = None
    Reserved8: Optional[str] = None

    Remark: Optional[str] = None
    NickName: Optional[str] = None

    ContactList: Optional[list] = None

    ChatRoomMembers: Optional[list] = None

    