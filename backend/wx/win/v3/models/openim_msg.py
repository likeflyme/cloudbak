from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class Msg(Base):
    __tablename__ = "ChatCRMsg"
    __table_args__ = {'extend_existing': True}

    localId = Column(Integer, primary_key=True)
    talkerId = Column(Integer)
    MsgSvrID = Column(Integer)
    type = Column(Integer)
    sequence = Column(Integer)
    StatusEx = Column(Integer)
    FlagEx = Column(Integer)
    IsSender = Column(Integer)
    Status = Column(Integer)
    CreateTime = Column(Integer)
    strTalker = Column(String)
    StrContent = Column(String)
    Reserved0 = Column(Integer)
    Reserved1 = Column(Integer)
    BytesExtra = Column(LargeBinary)
    BytesTrans = Column(LargeBinary)
    Reserved2 = Column(Integer)
    Reserved3 = Column(Integer)
    Reserved4 = Column(Integer)


class Name2ID(Base):
    __tablename__ = "Name2ID"
    __table_args__ = {'extend_existing': True}

    UsrName = Column(String, primary_key=True)

