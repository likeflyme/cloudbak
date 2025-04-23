import pyotp
from sqlalchemy.orm import Session

from app.models.sys import SysUser
from app.services.sys_conf_service import get_user_conf_with_db
from config.app_config import settings


def get_qrcode_uri(user_id: int, db: Session):
    user = db.query(SysUser).filter_by(id=user_id).one()
    user_conf = get_user_conf_with_db(user.id, db)
    totp = pyotp.TOTP(user_conf.two_step_auth.secret)
    return totp.provisioning_uri(name=user.username, issuer_name=settings.app_name)


def verify_code(code: str, secret: str):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
