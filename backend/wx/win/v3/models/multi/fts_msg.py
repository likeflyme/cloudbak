from sqlalchemy import Column, Integer, String

from db.wx_db import Base


class FTSChatMsg2_content(Base):
    __tablename__ = "FTSChatMsg2_content"

    docid = Column(Integer, primary_key=True)
    c0content = Column(String)
    c1entityId = Column(Integer)


class FTSChatMsg2_MetaData(Base):
    __tablename__ = "FTSChatMsg2_MetaData"

    docid = Column(Integer, primary_key=True)
    msgId = Column(Integer)
    entityId = Column(Integer)
    type = Column(Integer)
    subType = Column(Integer)
    tableType = Column(Integer)
    sortSequence = Column(Integer)


class NameToId(Base):
    __tablename__ = "NameToId"

    userName = Column(String, primary_key=True)
