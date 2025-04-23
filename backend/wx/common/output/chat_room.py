from typing import Optional, List

from pydantic import BaseModel


class ChatRoom(BaseModel):
    username: str
    owner: Optional[str] = None
    user_name_list: Optional[str] = None
    display_name_list: Optional[str] = None
    self_display_name: Optional[str] = None


class ChatRoomMember(BaseModel):
    username: str
    nickname: Optional[str] = None
    remark: Optional[str] = None
    display_name: Optional[str] = None
    small_head_img: Optional[str] = None


class ChatRoomInfo(BaseModel):
    username: str
    # 成员
    members: List[ChatRoomMember] = None
    # 公告
    announcement: Optional[str] = None
    owner: Optional[str] = None
    self_display_name: Optional[str] = None

