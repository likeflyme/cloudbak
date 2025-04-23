import os
from typing import List

from fastapi import Depends, APIRouter, HTTPException, status, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.auth_dep import get_current_user, pwd_context, get_current_sys_session
from app.enum.client_enum import ClientType, WindowsVersion
from app.enum.user_enum import UserState
from app.exception.biz_exception import BizException
from app.helper.directory_helper import get_wx_dir
from app.models.sys import SysUser, SysSession, SysSessionExtra
from app.schemas.sys_schemas import SysSessionSchemaWithId, SysSessionIn, UserCreate, \
    SysSessionSchemaWithHeadImg, SysSessionUpdate, PasswordUpdateRequest, UserOut
from app.services.clear_session import clear_session
from app.services.decode_wx_db import check_file_list
from app.services.sys_session_service import session_info
from app.services.sys_task_maker import TaskObj, task_execute
from config.auth_config import settings as auth_settings
from config.log_config import logger
from db.sys_db import get_db
from wx.client_factory import ClientFactory

router = APIRouter(
    prefix="/user"
)


@router.get("/check-install")
def check_install(db: Session = Depends(get_db)):
    count = db.query(SysUser).count()
    return {"count": count}


@router.post("/create-user")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 用户总数控制
    max_user_count = auth_settings.max_user_count
    if max_user_count != -1:
        total_count = db.query(SysUser).count()
        if total_count >= max_user_count:
            raise BizException(f"用户数量超过限制（{max_user_count}）")
    user_count = db.query(SysUser).filter_by(username=user_in.username).count()
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已使用",
        )
    email_count = db.query(SysUser).filter_by(email=user_in.email).count()
    if email_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被使用",
        )
    user = SysUser(**user_in.model_dump())
    user.password = pwd_context.hash(user_in.password)
    user.state = UserState.NORMAL
    db.add(user)
    db.commit()


@router.put("/set-current-session-id", response_model=SysSessionSchemaWithHeadImg)
def update_current_session(sys_session_id: int, user: SysUser = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    client = ClientFactory.get_client_by_id(sys_session_id)
    sys_session = client.get_sys_session()
    extra = client.get_sys_session_extra()

    db_user = db.query(SysUser).filter_by(id=user.id).first()
    db_user.current_session_id = sys_session_id
    db.commit()
    # 缓存中的数据
    user.current_session_id = sys_session_id
    try:
        head_img = client.get_resource_manager().get_wx_owner_img()
    except Exception as e:
        logger.error(e)
        head_img = ''
    session_detail = SysSessionSchemaWithHeadImg(
        **sys_session.__dict__,
        data_path=client.get_wx_dir(),
        client_type=extra.client_type if extra else ClientType.WINDOWS,
        client_version=extra.client_version if extra else WindowsVersion.V3,
        smallHeadImgUrl=head_img
    )
    session_detail.wx_id = client.get_real_wx_id()
    return session_detail


@router.get("/sys-sessions", response_model=List[SysSessionSchemaWithHeadImg])
def session_list(user: SysUser = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    sys_sessions = db.query(SysSession).filter_by(owner_id=user.id).all()
    array = []
    for sys_session in sys_sessions:
        array.append(session_info(sys_session))
    return array


@router.post("/sys-session", response_model=SysSessionSchemaWithId)
def create_session(
        sys_session_in: SysSessionIn,
        user: SysUser = Depends(get_current_user),
        db: Session = Depends(get_db)):
    logger.info("sys_session创建")
    logger.info(sys_session_in)

    sys_session = SysSession(
        name=sys_session_in.name,
        desc=sys_session_in.desc,
        wx_id=sys_session_in.wx_id,
        wx_name=sys_session_in.wx_name,
        wx_acct_name=sys_session_in.wx_acct_name,
        wx_key=sys_session_in.wx_key,
        wx_mobile=sys_session_in.wx_mobile,
        wx_dir=sys_session_in.wx_dir
    )
    sys_session.owner = user
    db.add(sys_session)
    db.commit()
    db.refresh(sys_session)

    extra = SysSessionExtra(
        client_type=sys_session_in.client_type,
        client_version=sys_session_in.client_version,
        sys_session_id=sys_session.id
    )
    db.add(extra)

    db.commit()
    db.refresh(sys_session)
    # 没有设置用户 session，则设置新添加的 session 为用户当前 session
    db_user = db.query(SysUser).filter_by(id=user.id).first()
    if not db_user.current_session_id:
        db_user.current_session_id = sys_session.id
        user.current_session_id = sys_session.id
        db.commit()
    # 创建对应目录
    wx_dir = get_wx_dir(sys_session)
    if not os.path.exists(wx_dir):
        os.makedirs(wx_dir)
    return SysSessionSchemaWithId(**sys_session.__dict__,
                                  client_type=sys_session_in.client_type,
                                  client_version=sys_session_in.client_version)


@router.delete("/sys-session/{sys_session_id}")
def delete_session(sys_session_id: int,
                    background_tasks: BackgroundTasks,
                   user: SysUser = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    sys_session = db.query(SysSession).filter_by(id=sys_session_id).first()
    db.delete(sys_session)
    db.commit()

    sys_user = db.query(SysUser).filter_by(id=user.id).first()
    if sys_user is not None and sys_user.current_session_id == sys_session.id:
        first_session = db.query(SysSession).first()
        if first_session is not None:
            sys_user.current_session_id = first_session.id
            db.commit()
    # 异步执行清除硬盘数据
    task_obj = TaskObj(sys_user.id, "清除session数据", clear_session, sys_session.id)
    background_tasks.add_task(task_execute, task_obj)


@router.put("/sys-session", response_model=SysSessionSchemaWithHeadImg)
def update_session(
        sys_session_update: SysSessionUpdate,
        user: SysUser = Depends(get_current_user),
        db: Session = Depends(get_db),
        sys_session: SysSession = Depends(get_current_sys_session)):
    logger.info("sys_session修改")
    logger.info(sys_session_update)
    db_session = db.query(SysSession).filter_by(id=sys_session.id).one()
    db_session.name = sys_session_update.name
    db_session.desc = sys_session_update.desc
    db_session.wx_name = sys_session_update.wx_name
    db_session.wx_acct_name = sys_session_update.wx_acct_name
    db_session.wx_key = sys_session_update.wx_key
    db_session.wx_dir = sys_session_update.wx_dir
    db_session.wx_mobile = sys_session_update.wx_mobile
    db.commit()
    # 修改的会话为当前会话，重新设置缓存中的当前会话
    ClientFactory.refresh_client_by_id(sys_session.id)
    return update_current_session(sys_session.id, user, db)


@router.put("/update-password")
def update_password(password_form: PasswordUpdateRequest,
                    user: SysUser = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if not pwd_context.verify(password_form.old_password.strip(), user.password):
        raise BizException("当前密码不正确")
    user.password = pwd_context.hash(password_form.new_password.strip())
    db.commit()


@router.get("/users", response_model=List[UserOut])
def users(user: SysUser = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(SysUser).where(SysUser.id.not_in([1])).order_by(SysUser.id.desc())
    return db.execute(stmt).scalars().all()


@router.put("/ban/{user_id}")
def users(user_id: int,
          user: SysUser = Depends(get_current_user),
          db: Session = Depends(get_db)):
    update_user = db.query(SysUser).filter_by(id=user_id).one()
    update_user.state = UserState.INVALID
    db.commit()


@router.put("/active/{user_id}")
def users(user_id: int,
          user: SysUser = Depends(get_current_user),
          db: Session = Depends(get_db)):
    update_user = db.query(SysUser).filter_by(id=user_id).one()
    update_user.state = UserState.NORMAL
    db.commit()


@router.put("/reset-password/{user_id}")
def reset_password(user_id: int,
                   user: SysUser = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """
    重置密码
    """
    if user.id != 1:
        raise BizException("权限不足")
    update_user = db.query(SysUser).filter_by(id=user_id).first()
    if update_user is None:
        raise BizException("用户不存在")
    password = pwd_context.hash(auth_settings.reset_password)
    user.password = password
    db.commit()


@router.get("/session-check/{session_id}")
def session_check(session_id: int,
                  user: SysUser = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    logger.info("sys_session 检查")
    sys_session = db.query(SysSession).filter_by(id=session_id, owner_id=user.id).first()
    if sys_session is None:
        raise BizException(f"用户不存在的会话")
    client = ClientFactory.get_client_by_id(session_id)
    if client is None:
        raise BizException(f"不支持的版本")
    result = client.sys_session_check()
    if result.success is False:
        raise BizException(f"会话检查失败：{result.msg}")

