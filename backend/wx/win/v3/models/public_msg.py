from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class Msg(Base):
    __tablename__ = "PublicMsg"
    __table_args__ = {'extend_existing': True}

    localId = Column(Integer, primary_key=True)
    TalkerId = Column(Integer)
    MsgSvrID = Column(Integer)
    Type = Column(Integer)
    SubType = Column(Integer)
    IsSender = Column(Integer)
    CreateTime = Column(Integer)
    Sequence = Column(Integer)
    StatusEx = Column(Integer)
    FlagEx = Column(Integer)
    Status = Column(Integer)
    MsgServerSeq = Column(Integer)
    MsgSequence = Column(Integer)
    StrTalker = Column(String)
    StrContent = Column(String)
    DisplayContent = Column(String)
    Reserved0 = Column(Integer)
    Reserved1 = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(Integer)
    Reserved4 = Column(Integer)
    Reserved5 = Column(Integer)
    Reserved6 = Column(Integer)
    CompressContent = Column(LargeBinary)
    BytesExtra = Column(LargeBinary)
    BytesTrans = Column(LargeBinary)


class PublicNameToID(Base):
    __tablename__ = "PublicNameToID"
    __table_args__ = {'extend_existing': True}

    UsrName = Column(String, primary_key=True)

