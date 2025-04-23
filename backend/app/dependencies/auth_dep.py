from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.sys import SysUser, SysSession, SysSessionExtra
from app.schemas.sys_schemas import UserInDB
from config.auth_config import settings
from db.sys_db import get_db
from config.cache_config import cache_half_hour
from config.log_config import logger
from passlib.handlers import bcrypt

from wx.client_factory import ClientFactory
from wx.interface.wx_interface import ClientInterface, SessionManager, MessageManager, ContactManager, ChatRoomManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 尝试从缓存中获取
    # cached_user = cache_half_hour.get(token)
    # if cached_user is not None:
    #     logger.info("返回缓存中存在的用户")
    #     return cached_user
    # logger.info("缓存中不存在用户信息，数据库查询该用户")
    try:

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        logger.info("username is " + username)
        if username is None:
            logger.info("jwt 凭证中用户名不存在")
            raise credentials_exception
    except JWTError as e:
        logger.error('jwt error', e)
        raise credentials_exception
    user = db.query(SysUser).filter_by(username=username).first()
    if user is None:
        logger.info("数据库中用户不存在")
        raise credentials_exception
    cache_half_hour[token] = user
    logger.info("缓存用户")
    return user


def get_current_sys_session(db: Session = Depends(get_db), user: SysUser = Depends(get_current_user)):
    return db.query(SysSession).filter_by(id=user.current_session_id).first()


def get_current_wx_id(sys_session: SysSession = Depends(get_current_sys_session)):
    return sys_session.wx_id


def get_wx_client(db: Session = Depends(get_db), sys_session: SysSession = Depends(get_current_sys_session)) -> ClientInterface | None:
    if sys_session:
        extra = db.query(SysSessionExtra).filter_by(sys_session_id=sys_session.id).first()
        return ClientFactory.get_client(sys_session, extra)
    return None


def get_session_manager(client: ClientInterface = Depends(get_wx_client)) -> SessionManager | None:
    if client is None:
        return None
    return client.get_session_manager()


def get_message_manager(client: ClientInterface = Depends(get_wx_client)) -> MessageManager | None:
    if client is None:
        return None
    return client.get_message_manager()


def get_contact_manager(client: ClientInterface = Depends(get_wx_client)) -> ContactManager | None:
    if client is None:
        return None
    return client.get_contact_manager()


def get_chat_room_manager(client: ClientInterface = Depends(get_wx_client)) -> ChatRoomManager | None:
    if client is None:
        return None
    return client.get_chat_room_manager()

