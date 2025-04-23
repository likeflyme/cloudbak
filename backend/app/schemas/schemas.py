from typing import Optional, Dict, List

from pydantic import BaseModel


class MsgBase(BaseModel):
    localId: int
    TalkerId: int
    MsgSvrIDStr: Optional[str] = None
    MsgSvrID: Optional[int] = None
    Type: int
    SubType: Optional[int] = None
    IsSender: int
    CreateTime: int
    Sequence: int
    StatusEx: int
    Status: int
    MsgServerSeq: Optional[int] = None
    MsgSequence: Optional[int] = None
    StrTalker: Optional[str] = None
    StrContent: Optional[str] = None
    DisplayContent: Optional[str] = None


class Msg(MsgBase):

    class Config:
        from_attributes = True


class MsgWithSender(MsgBase):
    sender: Optional[str] = None
    WxId: Optional[str] = None
    Thumb: Optional[str] = None
    Image: Optional[str] = None
    compress_content: Optional[Dict] = None

    class Config:
        from_attributes = True


class MsgWithExtra(MsgBase):
    WxId: Optional[str] = None
    Thumb: Optional[str] = None
    Image: Optional[str] = None
    compress_content: Optional[Dict] = None
    DbNo: Optional[int] = None
    smallHeadImgUrl: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None
    Remark: Optional[str] = None
    NickName: Optional[str] = None

    class Config:
        from_attributes = True


class ChatMsg(BaseModel):
    dbNo: int
    start: int
    msgs: List[MsgWithExtra]


class ChatMsgUseDbName(BaseModel):
    start: int
    start_db: Optional[str]
    msgs: List[MsgWithSender] = []


class SessionBaseOut(BaseModel):
    username: str
    strUsrName: str
    strNickName: str
    Remark: Optional[str] = None
    strContent: Optional[str] = None
    nTime: Optional[int] = None
    smallHeadImgUrl: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None
    headImgMd5: Optional[str] = None

    class Config:
        from_attributes = True


class ContactHeadImgUrlOut(BaseModel):
    usrName: str
    smallHeadImgUrl: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None
    headImgMd5: Optional[str] = None

    class Config:
        from_attributes = True


class Session(BaseModel):
    strUsrName: str
    nOrder: Optional[int] = None
    nUnReadCount: Optional[int] = None
    parentRef: Optional[str] = None
    Reserved0: Optional[int] = None
    Reserved1: Optional[str] = None
    strNickName: Optional[str] = None
    nStatus: Optional[int] = None
    nIsSend: Optional[int] = None
    strContent: Optional[str] = None
    nMsgType: Optional[int] = None
    nMsgLocalID: Optional[int] = None
    nMsgStatus: Optional[int] = None
    nTime: Optional[int] = None
    editContent: Optional[str] = None
    othersAtMe: Optional[int] = None
    Reserved2: Optional[int] = None
    Reserved3: Optional[str] = None
    Reserved4: Optional[int] = None
    Reserved5: Optional[str] = None


class MsgDetail(MsgBase):
    Reserved0: Optional[int] = None
    Reserved1: Optional[int] = None
    Reserved2: Optional[int] = None
    Reserved3: Optional[int] = None
    Reserved4: Optional[int] = None
    Reserved5: Optional[int] = None
    Reserved6: Optional[int] = None
    CompressContent: Optional[str] = None
    BytesExtra: Optional[str] = None
    BytesTrans: Optional[str] = None


class ContactBase(BaseModel):
    UserName: Optional[str] = None
    Alias: Optional[str] = None
    EncryptUserName: Optional[str] = None
    Remark: Optional[str] = None
    NickName: Optional[str] = None
    PYInitial: Optional[str] = None
    QuanPin: Optional[str] = None
    RemarkPYInitial: Optional[str] = None
    ChatRoomName: Optional[str] = None


class ContactWithHeadImg(ContactBase):
    smallHeadImgUrl: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None
    headImgMd5: Optional[str] = None


class Contact(BaseModel):
    UserName: Optional[str] = None
    Alias: Optional[str] = None
    EncryptUserName: Optional[str] = None
    DelFlag: Optional[int] = None
    Type: Optional[int] = None
    VerifyFlag: Optional[int] = None
    Reserved1: Optional[int] = None
    Reserved2: Optional[int] = None
    Reserved3: Optional[str] = None
    Reserved4: Optional[str] = None
    Remark: Optional[str] = None
    NickName: Optional[str] = None
    LabelIDList: Optional[str] = None
    DomainList: Optional[str] = None
    ChatRoomType: Optional[int] = None
    PYInitial: Optional[str] = None
    QuanPin: Optional[str] = None
    RemarkPYInitial: Optional[str] = None
    RemarkQuanPin: Optional[str] = None
    BigHeadImgUrl: Optional[str] = None
    SmallHeadImgUrl: Optional[str] = None
    HeadImgMd5: Optional[str] = None
    ChatRoomNotify: Optional[int] = None
    Reserved5: Optional[int] = None
    Reserved6: Optional[str] = None
    Reserved7: Optional[str] = None
    Reserved8: Optional[int] = None
    Reserved9: Optional[int] = None
    Reserved10: Optional[str] = None
    Reserved11: Optional[str] = None
