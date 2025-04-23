from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class OpenIMContact(Base):
    __tablename__ = 'OpenIMContact'
    __table_args__ = {'extend_existing': True}

    UserName = Column(String, primary_key=True)
    NickName = Column(String)
    Type = Column(Integer)
    Remark = Column(String)
    BigHeadImgUrl = Column(String)
    SmallHeadImgUrl = Column(String)
    Source = Column(Integer)
    NickNamePYInit = Column(String)
    NickNameQuanPin = Column(String)
    RemarkPYInit = Column(String)
    RemarkQuanPin = Column(String)
    CustomInfoDetail = Column(String)
    CustomInfoDetailVisible = Column(Integer)
    AntiSpamTicket = Column(String)
    AppId = Column(String)
    Sex = Column(Integer)
    DescWordingId = Column(String)
    Reserved1 = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(Integer)
    Reserved4 = Column(Integer)
    Reserved5 = Column(String)
    Reserved6 = Column(String)
    Reserved7 = Column(String)
    Reserved8 = Column(String)
    ExtraBuf = Column(LargeBinary)
