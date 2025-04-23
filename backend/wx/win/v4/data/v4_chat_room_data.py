import subprocess

from sqlalchemy import select

from config.log_config import logger
from wx.common.output.chat_room import ChatRoomInfo, ChatRoomMember
from wx.interface.wx_interface import ChatRoomManager
from wx.win.v4.db.windows_v4_db import WindowsV4DB
from wx.win.v4.enums.v4_enums import V4DBEnum
from wx.win.v4.models.contact import ChatRoomModelV4, ChatRoomMemberModelV4, ContactModelV4


class WindowsV4ChatRoomManager(ChatRoomManager):
    def __init__(self, db_manager: WindowsV4DB):
        self.db_manager = db_manager

    def chatroom_info(self, username: str) -> ChatRoomInfo:
        sm = self.db_manager.wx_db(V4DBEnum.CONTACT_DB_PATH)
        stmt = (
            select(ChatRoomModelV4, ChatRoomMemberModelV4, ContactModelV4)
            .join(ChatRoomMemberModelV4, ChatRoomMemberModelV4.room_id == ChatRoomModelV4.id, isouter=True)
            .join(ContactModelV4, ContactModelV4.id == ChatRoomMemberModelV4.member_id, isouter=True)
            .where(ChatRoomModelV4.username.is_(username))
        )
        logger.info(f"sql: {stmt}")
        logger.info(f"params: {username}")
        with sm() as db:
            results = db.execute(stmt).fetchall()
            return ChatRoomInfo(
                username=username,
                members=[
                    ChatRoomMember(
                        username=row[2].username,
                        nickname=row[2].nick_name,
                        remark=row[2].remark,
                        small_head_img=row[2].small_head_url
                    ) for row in results
                ]
            )
