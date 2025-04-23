from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.helper.machine import Machine


class SystemInfo(BaseModel):
    # 安装时间
    install: datetime = Field(default_factory=datetime.now)
    # 客户端唯一ID
    client_id: str = Machine.get_machine_code()
    # 授权码
    license: Optional[str] = None

