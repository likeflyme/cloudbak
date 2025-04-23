from typing import Optional, List

from pydantic import BaseModel


class BaseContact(BaseModel):
    Alias: Optional[str] = None
    Remark: Optional[str] = None
    NickName: Optional[str] = None
    smallHeadImgUrl: Optional[str] = None
    bigHeadImgUrl: Optional[str] = None


class FtsMsgCount(BaseModel):
    userName: str
    count: int
    content: Optional[str] = None
    db_name: Optional[str] = None


class FtsMsg(BaseModel):
    userName: str
    sequence: int
    content: Optional[str] = None
    msgId: int
    type: int
    subType: int
    tableType: Optional[int] = None
    db_name: Optional[str] = None
    sender: Optional[str] = None


class FtsMsgCountTop(BaseModel):
    totalCount: int
    contactList: List[FtsMsgCount]


class FtsMsgCross(BaseModel):
    start: int = 0
    start_db: str = None
    msgs: List[FtsMsg] = []
