from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class ContactHeadImg(Base):
    __tablename__ = "ContactHeadImg1"
    __table_args__ = {'extend_existing': True}

    usrName = Column(String, primary_key=True)
    createTime = Column(Integer)
    smallHeadBuf = Column(LargeBinary)
    m_headImgMD5 = Column(String)


