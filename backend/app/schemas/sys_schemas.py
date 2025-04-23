import time
from datetime import datetime
from typing import Union, List, Optional

from pydantic import BaseModel

from app.conf.sys_conf import SystemConfig
from app.enum.client_enum import ClientType, WindowsVersion
from app.helper.licence import License
from app.schemas.sys_conf_schemas import SysConfigOut


class TokenData(BaseModel):
    username: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserSession(BaseModel):
    id: int
    name: str | None = None
    desc: str | None = None
    wx_id: str | None = None
    wx_name: str | None = None
    wx_acct_name: str | None = None
    wx_key: str | None = None
    wx_mobile: str | None = None
    wx_email: str | None = None
    create_time: int = time.time()
    update_time: int = time.time()
    owner_id: int


class SysSessionOut(BaseModel):
    id: int
    name: str | None = None
    desc: str | None = None
    wx_id: str | None = None
    wx_name: str | None = None
    wx_acct_name: str | None = None
    wx_mobile: str | None = None
    wx_email: str | None = None
    wx_dir: str | None = None
    owner_id: int
    analyze_state: int
    create_time: int
    update_time: int

    class Config:
        from_attributes = True


class SysSessionSchema(BaseModel):
    id: int
    name: str | None = None
    desc: str | None = None
    wx_id: str | None = None
    wx_name: str | None = None
    wx_acct_name: str | None = None
    wx_mobile: str | None = None
    wx_email: str | None = None
    wx_dir: str | None = None
    # 客户端类型
    client_type: str = ClientType.WINDOWS
    # 客户端版本
    client_version: str = WindowsVersion.V3
    # 添加时版本号
    add_version: Optional[str] = None
    create_time: int | None = None
    update_time: int | None = None
    owner_id: int

    class Config:
        from_attributes = True


class SysSessionSchemaWithId(SysSessionSchema):
    id: int


class SysSessionSchemaWithHeadImg(SysSessionSchema):
    smallHeadImgUrl: str | None = None
    bigHeadImgUrl: str | None = None
    wx_key: str | None = None
    data_path: str | None = None


class User(BaseModel):
    id: int
    username: str
    nickname: Union[str, None] = None
    current_session_id: Union[int, None] = None
    state: Union[int, None] = None
    create_time: Union[int, None] = None
    update_time: Union[int, None] = None
    current_session: Optional[SysSessionSchemaWithHeadImg] = None
    configs: List[Union[SysConfigOut, None]] = None


class UserInDB(User):
    hashed_password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Union[str, None] = None
    nickname: Union[str, None] = None
    state: Union[int, None] = None
    create_time: float
    update_time: float

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class SysSessionIn(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    wx_id: Optional[str] = None
    wx_name: Optional[str] = None
    wx_acct_name: Optional[str] = None
    wx_key: Optional[str] = None
    wx_mobile: Optional[str] = None
    wx_dir: Optional[str] = None
    client_type: str = ClientType.WINDOWS
    client_version: str = WindowsVersion.V3
    add_version: Optional[str] = None

    class Config:
        from_attributes = True


class SysSessionUpdate(BaseModel):
    name: Optional[str] = None
    desc: str | None = None
    wx_key: Optional[str] = None
    wx_id: Optional[str] = None
    wx_name: Optional[str] = None
    wx_acct_name: Optional[str] = None
    wx_dir: Optional[str] = None
    wx_mobile: Optional[str] = None
    update_time: Optional[int] = None

    class Config:
        from_attributes = True


class CreateSysSessionSchema(BaseModel):
    name: str
    wx_key: str
    wx_id: str
    wx_name: str
    wx_acct_name: str
    wx_mobile: str | None = None


class SysTaskOut(BaseModel):
    id: int
    name: str
    state: int
    detail: str | None = None
    create_time: float
    update_time: float
    owner_id: int


class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str


class SysInfoOut(BaseModel):
    # 安装时间
    install: datetime
    # 客户端唯一ID
    client_id: str
    # 授权码
    license: Optional[str] = None
    # 授权信息
    license_info: Optional[License] = None
    # 系统配置
    sys_conf: Optional[SystemConfig] = None
    # 系统版本号
    sys_version: Optional[str] = 'unkown'
