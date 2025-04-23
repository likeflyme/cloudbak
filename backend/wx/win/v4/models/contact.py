from sqlalchemy import Column, String, Integer, LargeBinary

from wx.win.v4.db.windows_v4_db import Base


class ContactModelV4(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    local_type = Column(Integer)
    alias = Column(String)
    encrypt_username = Column(String)
    flag = Column(Integer)
    delete_flag = Column(Integer)
    verify_flag = Column(Integer)
    remark = Column(String)
    remark_quan_pin = Column(String)
    remark_pin_yin_initial = Column(String)
    nick_name = Column(String)
    pin_yin_initial = Column(String)
    quan_pin = Column(String)
    big_head_url = Column(String)
    small_head_url = Column(String)
    head_img_md5 = Column(String)
    chat_room_notify = Column(Integer)
    is_in_chat_room = Column(Integer)
    description = Column(String)
    extra_buffer = Column(LargeBinary)
    chat_room_type = Column(Integer)


class ChatRoomModelV4(Base):
    __tablename__ = 'chat_room'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    owner = Column(String)
    ext_buffer = Column(LargeBinary)


class ChatRoomMemberModelV4(Base):
    __tablename__ = 'chatroom_member'
    room_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, primary_key=True)

