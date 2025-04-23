from sqlalchemy import Column, Integer, String, BLOB, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from db.wx_db import Base


class HardLinkImageID(Base):
    __tablename__ = 'HardLinkImageID'
    DirID = Column(Integer, primary_key=True)
    Dir = Column(String)


class HardLinkImageAttribute(Base):
    __tablename__ = 'HardLinkImageAttribute'
    Md5Hash = Column(BLOB)
    DirID1 = Column(Integer, ForeignKey('HardLinkImageID.DirID'))
    DirID2 = Column(Integer, ForeignKey('HardLinkImageID.DirID'))
    MD5 = Column(BLOB)
    ModifyTime = Column(Integer)
    FileName = Column(String)
    Reserved1 = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(String)
    Reserved4 = Column(String)
    Reserved5 = Column(Integer)
    Reserved6 = Column(String)
    Reserved7 = Column(BLOB)

    __table_args__ = (
        PrimaryKeyConstraint('Md5Hash', 'DirID1', 'DirID2'),
    )

    dir1 = relationship("HardLinkImageID", foreign_keys=[DirID1])
    dir2 = relationship("HardLinkImageID", foreign_keys=[DirID2])

