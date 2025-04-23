from ..models.sys import SysUser
from db.sys_db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


def get_user_by_username(username: str, session: Session = Depends(get_db)):
    return session.query(SysUser).filter_by(username=username).first()
