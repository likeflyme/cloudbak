from typing import Optional, Dict, List

from pydantic import BaseModel


class WindowsV3Properties(BaseModel):
    localId: int
    TalkerId: Optional[int] = None
    MsgSvrID: Optional[int] = None
    MsgSvrIDStr: Optional[str] = None
    Type: Optional[int] = None
    SubType: Optional[int] = None
    IsSender: Optional[int] = None
    CreateTime: Optional[int] = None
    Sequence: Optional[int] = None
    StatusEx: Optional[int] = None
    FlagEx: Optional[int] = None
    Status: Optional[int] = None
    MsgServerSeq: Optional[int] = None
    MsgSequence: Optional[int] = None
    StrTalker: Optional[str] = None
    StrContent: Optional[str] = None
    DisplayContent: Optional[str] = None
    Reserved0: Optional[int] = None
    Reserved1: Optional[int] = None
    Reserved2: Optional[int] = None
    Reserved3: Optional[int] = None
    Reserved4: Optional[str] = None
    Reserved5: Optional[str] = None
    Reserved6: Optional[str] = None
    compress_content: Optional[Dict] = None
    bytes_extra: Optional[Dict] = None
    bytes_trans: Optional[Dict] = None
    thumb: Optional[str] = None
    source: Optional[str] = None
    sender: Optional[str] = None


class WindowsV4Properties(BaseModel):
    local_id: int
    server_id: int
    local_type: int
    sort_seq: int
    seal_sender_id: Optional[int] = None
    create_time: Optional[int] = None
    status: Optional[int] = None
    upload_status: Optional[int] = None
    download_status: Optional[int] = None
    server_seq: Optional[int] = None
    origin_source: Optional[int] = None
    source_data: Optional[Dict] = None
    message_content_data: Optional[str] = None
    compress_content_data: Optional[str] = None
    packed_info_data_data: Optional[str] = None
    WCDB_CT_message_content: Optional[int] = None
    WCDB_CT_source: Optional[int] = None
    sender: Optional[str] = None


class Msg(BaseModel):
    windows_v3_properties: Optional[WindowsV3Properties] = None
    windows_v4_properties: Optional[WindowsV4Properties] = None


class MsgSearchOut(BaseModel):
    start: int
    start_db: Optional[str] = None
    messages: List[Msg]
