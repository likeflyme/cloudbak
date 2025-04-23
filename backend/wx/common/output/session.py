from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    username: str
    type: Optional[int] = None
    summary: Optional[str] = None
    modify_timestamp: Optional[int] = None


class CheckResult(BaseModel):
    success: bool
    msg: Optional[str] = None
