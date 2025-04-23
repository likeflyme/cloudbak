from typing import Optional

from pydantic import BaseModel


class FtsFilterObj(BaseModel):
    username: str
    text: str
    page: int = 1
    size: int = 20
    start: Optional[int] = None
    start_db: Optional[str] = None
