from sqlalchemy import Column, String, Integer

from wx.win.v4.db.windows_v4_db import Base


class SessionModelV4(Base):
    __tablename__ = 'SessionTable'

    username = Column(String, primary_key=True)
    type = Column(Integer)
    unread_count = Column(Integer)
    unread_first_msg_srv_id = Column(Integer)
    is_hidden = Column(Integer)
    summary = Column(String)
    draft = Column(String)
    status = Column(Integer)
    last_timestamp = Column(Integer)
    sort_timestamp = Column(Integer)
    last_clear_unread_timestamp = Column(Integer)
    last_msg_locald_id = Column(Integer)
    last_msg_type = Column(Integer)
    last_msg_sub_type = Column(Integer)
    last_msg_sender = Column(String)
    last_sender_display_name = Column(String)
    last_msg_ext_type = Column(Integer)
