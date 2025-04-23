from app.models.sys import SysUser
from db.sys_db import get_sys_db
from config.log_config import logger
from sqlalchemy import text


def update_user_none_state():
    logger.info("用户状态兼容旧版本")
    with get_sys_db() as db:
        sql = text("UPDATE sys_user SET state = 1 WHERE state IS NULL")
        db.execute(sql)
        db.commit()
