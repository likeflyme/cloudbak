from typing import Optional, List

from pydantic import BaseModel


class FtsMsgCount(BaseModel):
    username: str
    count: int
    content: Optional[str] = None
    db_name: Optional[str] = None


class FtsMsg(BaseModel):
    username: str
    sequence: int
    content: Optional[str] = None
    msg_id: Optional[str] = None
    type: int
    sub_type: Optional[int] = None
    db_name: Optional[str] = None
    sender: Optional[str] = None


class FtsMsgCountTop(BaseModel):
    total_count: int
    contact_list: List[FtsMsgCount]


class FtsMsgCross(BaseModel):
    start: int = 0
    start_db: str = None
    msgs: List[FtsMsg]
