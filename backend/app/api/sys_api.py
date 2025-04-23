import os

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.form.license_request import LicenseRequest
from app.dependencies.auth_dep import get_current_user
from app.enum.sys_conf_enum import SysConfEnum
from app.exception.biz_exception import BizException
from app.helper.licence import LicenseManager, License
from app.models.sys import SysUser
from app.schemas.sys_schemas import SysInfoOut
from app.services.sys_conf_service import get_sys_info_with_db, save_config, save_config_with_db, get_sys_conf
from db.sys_db import get_db
from config.app_config import settings as app_settings
from datetime import timedelta
from config.log_config import logger

router = APIRouter(
    prefix="/sys"
)


@router.get("/sys-info", response_model=SysInfoOut)
def get_sys_info(db: Session = Depends(get_db), login_user: SysUser = Depends(get_current_user)):
    sys_info = get_sys_info_with_db(db)
    sys_info_out = SysInfoOut(
        install=sys_info.install,
        client_id=sys_info.client_id,
        license=sys_info.license
    )
    if sys_info.license:
        license_info = LicenseManager(app_settings.license_version, app_settings.license_aes_key).parse_license(sys_info.license)
        sys_info_out.license_info = license_info
    else:
        # 设置免费授权过期日
        # 安装日期+30天
        # 创建一个 timedelta 对象表示 30 天
        delta = timedelta(days=app_settings.free_max_day)

        # 将 30 天加到当前时间
        expiry_date_time = sys_info.install + delta
        license_info = License(expiry_date=expiry_date_time.strftime('%Y-%m-%d'))
        sys_info_out.license_info = license_info
    # 系统配置
    sys_info_out.sys_conf = get_sys_conf()
    # 系统版本
    system_version = os.getenv("SYSTEM_VERSION", "unkown")
    sys_info_out.sys_version = system_version
    return sys_info_out


@router.post("/save-license", response_model=License)
def save_license(request: LicenseRequest,
                 db: Session = Depends(get_db),
                 login_user: SysUser = Depends(get_current_user)):
    try:
        license_info = LicenseManager(app_settings.license_version, app_settings.license_aes_key).parse_license(request.license_text)
        sys_info = get_sys_info_with_db(db)
        logger.info(f"系统client_id: {sys_info.client_id}")
        logger.info(f"授权client_id: {license_info.client_id}")
        if sys_info.client_id != license_info.client_id:
            raise BizException('无效授权码：unmatched')
        # 保存授权码到 sys_info
        sys_info.license = request.license_text
        save_config_with_db(db, SysConfEnum.SYS_INFO, sys_info)
        # 返回授权数据
        return license_info
    except ValueError as e:
        raise BizException('无效授权码')

