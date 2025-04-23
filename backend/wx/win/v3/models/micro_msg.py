from sqlalchemy import Column, Integer, String, LargeBinary, BLOB
from sqlalchemy.orm import relationship

from db.wx_db import Base


class Session(Base):
    __tablename__ = 'Session'
    __table_args__ = {'extend_existing': True}

    strUsrName = Column(String, primary_key=True)
    nOrder = Column(Integer)
    nUnReadCount = Column(Integer)
    parentRef = Column(String)
    Reserved0 = Column(Integer)
    Reserved1 = Column(String)
    strNickName = Column(String)
    nStatus = Column(Integer)
    nIsSend = Column(Integer)
    strContent = Column(String)
    nMsgType = Column(Integer)
    nMsgLocalID = Column(Integer)
    nMsgStatus = Column(Integer)
    nTime = Column(Integer)
    editContent = Column(String)
    othersAtMe = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(String)
    Reserved4 = Column(Integer)
    Reserved5 = Column(String)
    bytesXml = Column(LargeBinary)


class Contact(Base):
    __tablename__ = 'Contact'
    __table_args__ = {'extend_existing': True}

    UserName = Column(String, primary_key=True)
    Alias = Column(String)
    EncryptUserName = Column(String)
    DelFlag = Column(Integer)
    Type = Column(Integer)
    VerifyFlag = Column(Integer)
    Reserved1 = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(String)
    Reserved4 = Column(String)
    Remark = Column(String)
    NickName = Column(String)
    LabelIDList = Column(String)
    DomainList = Column(String)
    ChatRoomType = Column(Integer)
    PYInitial = Column(String)
    QuanPin = Column(String)
    RemarkPYInitial = Column(String)
    RemarkQuanPin = Column(String)
    BigHeadImgUrl = Column(String)
    SmallHeadImgUrl = Column(String)
    HeadImgMd5 = Column(String)
    ChatRoomNotify = Column(Integer)
    Reserved5 = Column(Integer)
    Reserved6 = Column(String)
    Reserved7 = Column(String)
    ExtraBuf = Column(LargeBinary)
    Reserved8 = Column(Integer)
    Reserved9 = Column(Integer)
    Reserved10 = Column(String)

    # 外键关系
    head_img_url = relationship('ContactHeadImgUrl',
                                primaryjoin="Contact.UserName == foreign(ContactHeadImgUrl.usrName)",
                                uselist=False,
                                overlaps="contact")


class ChatRoom(Base):
    __tablename__ = 'ChatRoom'
    __table_args__ = {'extend_existing': True}

    ChatRoomName = Column(String, primary_key=True)
    UserNameList = Column(String)
    DisplayNameList = Column(String)
    ChatRoomFlag = Column(Integer)
    Owner = Column(Integer)
    IsShowName = Column(Integer)
    SelfDisplayName = Column(String)
    Reserved1 = Column(Integer)
    Reserved2 = Column(String)
    Reserved3 = Column(Integer)
    Reserved4 = Column(String)
    Reserved5 = Column(Integer)
    Reserved6 = Column(String)
    RoomData = Column(LargeBinary)
    Reserved7 = Column(Integer)
    Reserved8 = Column(String)


class ContactHeadImgUrl(Base):
    __tablename__ = 'ContactHeadImgUrl'
    __table_args__ = {'extend_existing': True}

    usrName = Column(String, primary_key=True)
    smallHeadImgUrl = Column(String)
    bigHeadImgUrl = Column(String)
    headImgMd5 = Column(String)
    reverse0 = Column(Integer)
    reverse1 = Column(String)

    contact = relationship('Contact',
                           primaryjoin="foreign(ContactHeadImgUrl.usrName) == Contact.UserName",
                           overlaps="head_img_url")

