import time
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Index
from sqlalchemy.orm import relationship

from app.enum.client_enum import ClientType, WindowsVersion
from app.enum.event_enum import EventType
from db.sys_db import Base

session_analyze_end = 0
session_analyze_running = 1
session_analyze_pending = 2
session_analyze_fail = 3


class SysUser(Base):
    __tablename__ = "sys_user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    nickname = Column(String)
    email = Column(String)
    current_session_id = Column(Integer, default=None)
    state = Column(Integer)
    create_time = Column(Integer, default=time.time())
    update_time = Column(Integer, default=time.time())

    sessions = relationship("SysSession", back_populates="owner")


class SysSession(Base):
    __tablename__ = "sys_session"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    desc = Column(String)
    wx_id = Column(String, default=None)
    wx_name = Column(String, default=None)
    wx_acct_name = Column(String, default=None)
    wx_key = Column(String, default=None)
    wx_mobile = Column(String, default=None)
    wx_email = Column(String, default=None)
    wx_dir = Column(String, default=None)
    create_time = Column(Integer, default=lambda: int(time.time()))
    update_time = Column(Integer, default=lambda: int(time.time()))
    owner_id = Column(Integer, ForeignKey("sys_user.id"))
    analyze_state = Column(Integer, default=session_analyze_end)

    owner = relationship("SysUser", back_populates="sessions")


class SysSessionExtra(Base):
    __tablename__ = "sys_session_extra"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 客户端类型
    client_type = Column(String, default=ClientType.WINDOWS)
    # 客户端版本
    client_version = Column(String, default=WindowsVersion.V3)
    # 添加时版本号
    add_version = Column(String)
    sys_session_id = Column(Integer, ForeignKey("sys_session.id"))
    reversed0 = Column(Integer)
    reversed1 = Column(Integer)
    reversed2 = Column(String)
    reversed3 = Column(String)


class SysTask(Base):
    __tablename__ = "sys_task"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    state = Column(Integer, default=2)
    detail = Column(String, default=None)
    create_time = Column(Integer, default=time.time())
    update_time = Column(Integer, default=time.time())
    owner_id = Column(Integer, ForeignKey("sys_user.id"), default=None)


class SysConfig(Base):
    __tablename__ = 'sys_config'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    conf_key = Column(String)
    conf_value = Column(String)
    user_id = Column(Integer, ForeignKey("sys_user.id"))
    session_id = Column(Integer, ForeignKey("sys_session.id"))
    create_time = Column(Integer, default=time.time())
    update_time = Column(Integer, default=time.time())
    reversed0 = Column(Integer)
    reversed1 = Column(Integer)
    reversed2 = Column(String)
    reversed3 = Column(String)


class SysDecryptRecord(Base):
    __tablename__ = 'sys_decrypt_record'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    db_file = Column(String)
    file_last_ts = Column(Integer)
    session_id = Column(Integer, ForeignKey("sys_session.id"))
    create_time = Column(Integer, default=time.time())
    update_time = Column(Integer, default=time.time())
    reversed0 = Column(Integer)
    reversed1 = Column(Integer)
    reversed2 = Column(String)
    reversed3 = Column(String)


class SysEvent(Base):
    __tablename__ = 'sys_event'
    __table_args__ = (
        Index('ix_event_type_key', 'event_type', 'event_key'),
        Index('ix_create_time', 'create_time'),
        {'extend_existing': True},
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(Enum(EventType), nullable=False)
    event_key = Column(String)
    event_detail = Column(String)
    user_id = Column(Integer, ForeignKey("sys_user.id"))
    session_id = Column(Integer, ForeignKey("sys_session.id"))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    reversed0 = Column(Integer)
    reversed1 = Column(Integer)
    reversed2 = Column(String)
    reversed3 = Column(String)

