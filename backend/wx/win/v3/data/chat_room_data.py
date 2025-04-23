from app.models.proto import cr_extra_buf_pb2
from config.log_config import logger
from wx.common.output.chat_room import ChatRoomInfo, ChatRoomMember
from wx.interface.wx_interface import ChatRoomManager
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.models.micro_msg import ChatRoom as ChatRoomModel
from wx.win.v3.models.micro_msg import Contact as ContactModel


class WindowsV3ChatRoomManager(ChatRoomManager):
    def __init__(self, db_manager: WindowsV3DB):
        self.db_manager = db_manager

    def chatroom_info(self, username: str) -> ChatRoomInfo:
        logger.info("执行 chatroom_info")
        members = []
        try:
            with self.db_manager.wx_db_micro_msg() as db:
                chat_room = db.query(ChatRoomModel).filter_by(ChatRoomName=username).one()
                if chat_room.RoomData:
                    room_data = cr_extra_buf_pb2.RoomData()
                    room_data.ParseFromString(chat_room.RoomData)
                    for u in room_data.users:
                        member = ChatRoomMember(username=u.id, remark=u.name)
                        if member.remark is None or member.remark == "":
                            logger.info(f"成员备注为空，username={member.username}，从Contact表查询昵称")
                            # 查询 Contact 表获取昵称
                            contact = db.query(ContactModel).filter_by(UserName=member.username).first()
                            logger.info(f"获取到 Contact {contact}")
                            if contact:
                                member.nickname = contact.NickName
                        members.append(member)
            return ChatRoomInfo(username=username, members=members, self_display_name=chat_room.SelfDisplayName)
        except Exception as e:
            logger.error(e)
            return ChatRoomInfo(username=username)

