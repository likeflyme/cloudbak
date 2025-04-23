from typing import Optional

from pydantic import BaseModel

from app.enum.msg_enum import FilterMode


class MsgFilterObj(BaseModel):
    username: str
    page: int = 1
    size: int = 20
    start: Optional[int] = None
    start_db: Optional[str] = None
    filter_day: Optional[str] = None
    filter_file: Optional[bool] = False
    filter_text: Optional[str] = None
    filter_media: Optional[bool] = False
    filter_id: Optional[int] = None
    filter_sequence: Optional[int] = None
    filter_mode: Optional[FilterMode] = FilterMode.DESC


class SingleMsgFilterObj(BaseModel):
    username: Optional[str] = None
    local_id: Optional[int] = None
    sequence: Optional[int] = None
    db_name: Optional[str] = None
    server_sequence: Optional[int] = None
    v3_msg_svr_id: Optional[int] = None
