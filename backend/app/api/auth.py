from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.form.login_form import OAuth2PasswordCodeRequestForm
from app.dependencies.auth_dep import create_access_token, get_current_user, verify_password, get_current_sys_session
from app.enum.client_enum import ClientType, WindowsVersion
from app.enum.user_enum import UserState
from app.exception.auth_exception import LoginException
from app.exception.biz_exception import IllegalArgumentsException
from app.models.sys import SysUser, SysSession
from app.schemas.sys_schemas import Token, User, SysSessionSchemaWithHeadImg
from app.services.sys_conf_service import get_user_conf_with_db
from app.services.sys_session_service import session_info
from app.services.two_step_auth import get_qrcode_uri
from app.services.two_step_auth import verify_code
from config.auth_config import settings
from config.log_config import logger
from db.sys_db import get_db
from wx.client_factory import ClientFactory

router = APIRouter(
    prefix="/auth"
)


@router.post("/token")
def create_token(form_data: OAuth2PasswordCodeRequestForm = Depends(), session: Session = Depends(get_db)) -> Token:
    user = session.query(SysUser).filter(
        or_(SysUser.username == form_data.username, SysUser.email == form_data.username)
    ).first()
    if not user:
        raise LoginException("错误的用户名", key=form_data.username)
    if user.state != UserState.NORMAL:
        raise LoginException("该用户已被禁用", key=form_data.username)
    # 检查登录限次
    # count = count_within_hours(EventType.LOGIN_FAIL, form_data.username, 24)
    # sys_config = get_sys_conf_with_db(session)
    # if sys_config is not None and count >= sys_config.auth.login_error_count_day:
    #     raise LoginException("登录错误次数超过限制", key=form_data.username)
    # 开启两步验证需要验证验证码
    user_config = get_user_conf_with_db(user.id, session)
    if user_config.two_step_auth.two_step_auth_open:
        if form_data.captcha:
            if verify_code(form_data.captcha, user_config.two_step_auth.secret) is False:

                raise LoginException("验证码错误", key=form_data.username)
        else:
            raise HTTPException(status_code=461, detail="请输入验证码")
    if not verify_password(form_data.password, user.password):
        raise LoginException(detail="错误的用户名或密码", key=form_data.username)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
def read_curren_user(db: Session = Depends(get_db),
                     user: User = Depends(get_current_user),
                     session: SysSession = Depends(get_current_sys_session)):
    client = ClientFactory.get_client_by_id(session.id)
    sys_session = client.get_sys_session()
    extra = client.get_sys_session_extra()
    try:
        head_img = client.get_resource_manager().get_wx_owner_img()
    except Exception as e:
        logger.error(e)
        head_img = ''
    current_session = SysSessionSchemaWithHeadImg(
        **sys_session.__dict__,
        data_path=client.get_wx_dir(),
        client_type=extra.client_type if extra else ClientType.WINDOWS,
        client_version=extra.client_version if extra else WindowsVersion.V3,
        smallHeadImgUrl=head_img
    )
    current_session.wx_id = client.get_real_wx_id()
    return {
        "id": user.id,
        "username": user.username,
        "current_session_id": user.current_session_id,
        "current_session": current_session
    }


@router.get("/get-two-step-qrcode")
def two_step_qrcode(user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    获取两步验证QRCODE URI，没有则创建
    """
    user_conf = get_user_conf_with_db(user.id, db)
    if not user_conf.two_step_auth.two_step_auth_open:
        raise IllegalArgumentsException('未开启两步验证，请先开启两步验证并保存')

    return {
        "qr_code_uri": get_qrcode_uri(user.id, db)
    }
