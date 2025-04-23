from typing import Optional

from pydantic import BaseModel


class SessionFilterObj(BaseModel):
    page: int = 1
    size: int = 20
    normal: Optional[bool] = True
    gh: Optional[bool] = True
    openim: Optional[bool] = True
    chatroom: Optional[bool] = True
    filehelper: Optional[bool] = True
    other: Optional[bool] = True
