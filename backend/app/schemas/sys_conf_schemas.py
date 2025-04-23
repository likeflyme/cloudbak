from pydantic import BaseModel


class JobIn(BaseModel):
    open: bool
    sys_session_id: int | None = None
    cron: str | None = None


class SysConfigOut(BaseModel):
    conf_key: str
    conf_value: str = None
    user_id: int = None
    session_id: int = None


class SysConfigUpdate(BaseModel):
    conf_key: str
    conf_value: str
