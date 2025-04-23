from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.conf.session_conf import SessionConfig
from app.conf.sys_conf import SystemConfig
from app.conf.sys_info import SystemInfo
from app.conf.user_conf import UserConfig
from app.enum.sys_conf_enum import SysConfEnum
from app.models.sys import SysConfig, SysSession
from db.sys_db import SessionLocal
from config.log_config import logger


def get_sys_conf():
    with SessionLocal() as db:
        return get_sys_conf_with_db(db)


def get_sys_conf_with_db(db: Session):
    conf = db.query(SysConfig).filter_by(conf_key=SysConfEnum.SYS_CONF).first()
    if conf:
        return SystemConfig.model_validate_json(conf.conf_value)
    return SystemConfig()


def get_user_conf(user_id: int):
    with SessionLocal() as db:
        return get_user_conf_with_db(user_id, db)


def get_user_conf_with_db(user_id: int, db: Session):
    conf = db.query(SysConfig).filter_by(user_id=user_id, conf_key=SysConfEnum.USER_CONF).first()
    if conf:
        return UserConfig.model_validate_json(conf.conf_value)
    return UserConfig()


def get_session_conf(sys_session: SysSession):
    with SessionLocal() as db:
        return get_session_conf_with_db(sys_session, db)


def get_session_conf_with_db(sys_session: SysSession, db: Session):
    conf = db.query(SysConfig).filter_by(user_id=sys_session.owner_id,
                                         session_id=sys_session.id,
                                         conf_key=SysConfEnum.SESSION_CONF).first()
    if conf:
        return SessionConfig.model_validate_json(conf.conf_value)
    return SessionConfig()


def initial_sys_info():
    with SessionLocal() as db:
        sys_info = db.query(SysConfig).filter_by(conf_key=SysConfEnum.SYS_INFO).first()
        if sys_info is None:
            logger.info("初始化系统信息配置")
            sys_info = SystemInfo()
            sys_config = SysConfig(conf_key=SysConfEnum.SYS_INFO, conf_value=sys_info.model_dump_json())
            db.add(sys_config)
            db.commit()


def get_sys_info():
    with SessionLocal() as db:
        return get_sys_info_with_db(db)


def get_sys_info_with_db(db):
    sys_info = db.query(SysConfig).filter_by(conf_key=SysConfEnum.SYS_INFO).one()
    return SystemInfo.model_validate_json(sys_info.conf_value)


def save_config(config_tp: SysConfEnum, config: BaseModel):
    """
    保存配置
    """
    with SessionLocal() as db:
        save_config_with_db(db, config_tp, config)


def save_config_with_db(db, config_tp: SysConfEnum, config: BaseModel):
    """
    保存配置
    """
    json_str = config.model_dump_json()
    stmt = update(SysConfig).where(SysConfig.conf_key == config_tp).values(conf_value=json_str)
    db.execute(stmt)
    db.commit()


# if __name__ == "__main__":
#     json_str = '{"install":"2025-02-11T17:04:43.400604","client_id":"3BBFE81C-E857-11EF-A8C8-001A7DDA7111","license":null}'
#     sys_info = SystemInfo.model_validate_json(json_str)
#     print(sys_info.client_id)
#     print(sys_info.install)
#     print(sys_info.license)
