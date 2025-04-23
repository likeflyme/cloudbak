from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.conf.session_conf import SessionConfig
from app.conf.sys_conf import SystemConfig
from app.conf.user_conf import UserConfig
from app.dependencies.auth_dep import get_current_user, get_current_sys_session
from app.enum.sys_conf_enum import SysConfEnum
from app.models.sys import SysUser, SysConfig, SysSession
from app.schemas.sys_conf_schemas import SysConfigUpdate
from app.services.sys_conf_service import get_sys_conf, get_session_conf, get_user_conf, save_config
from app.sheduler import reload_all_jobs
from config.log_config import logger
from db.sys_db import get_db

router = APIRouter(
    prefix="/conf"
)


@router.post("/update-conf")
def update_conf(conf: SysConfigUpdate,
                sys_user: SysUser = Depends(get_current_user),
                sys_session: SysSession = Depends(get_current_sys_session),
                db: Session = Depends(get_db)):
    """
    修改配置
    配置分三个级别：sys_conf 系统级别配置，user_conf 用户级别配置，session_conf 会话级别配置
    用户为配置则设置默认配置
    :param conf:
    :param sys_user:
    :param sys_session:
    :param db:
    :return:
    """
    stmt = select(SysConfig).where(SysConfig.conf_key == conf.conf_key)
    if conf.conf_key == SysConfEnum.USER_CONF:
        stmt = stmt.where(SysConfig.user_id == sys_user.id)
    elif conf.conf_key == SysConfEnum.SESSION_CONF:
        stmt = stmt.where(SysConfig.session_id == sys_session.id).where(SysConfig.user_id == sys_user.id)
    result = db.execute(stmt).first()
    if result and len(result) == 1:
        conf_instance = result[0]
        conf_instance.conf_value = conf.conf_value
        db.commit()
    else:
        logger.info("初始化配置")
        conf = SysConfig(**conf.__dict__)
        if conf.conf_key == SysConfEnum.USER_CONF:
            conf.user_id = sys_user.id
        elif conf.conf_key == SysConfEnum.SESSION_CONF:
            conf.user_id = sys_user.id
            conf.session_id = sys_session.id
        db.add(conf)
        db.commit()

    if conf.conf_key == SysConfEnum.SESSION_CONF:
        reload_all_jobs()


@router.get("/load-sys-conf", response_model=SystemConfig)
def load_conf(sys_user: SysUser = Depends(get_current_user)):
    return get_sys_conf()


@router.get("/load-user-conf", response_model=UserConfig)
def load_conf(sys_user: SysUser = Depends(get_current_user)):
    return get_user_conf(sys_user.id)


@router.get("/load-session-conf", response_model=SessionConfig)
def load_session_conf(sys_user: SysUser = Depends(get_current_user),
                      sys_session: SysSession = Depends(get_current_sys_session)):
    return get_session_conf(sys_session)

