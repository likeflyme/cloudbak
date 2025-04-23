import os

from app.helper.directory_helper import get_wx_dir
from db.sys_db import get_sys_db
from wx.win.v3.models.micro_msg import ContactHeadImgUrl
from app.models.sys import SysSession, SysSessionExtra
from app.schemas.sys_schemas import SysSessionSchemaWithHeadImg
from config.wx_config import settings as wx_settings
from config.log_config import logger
from db.wx_db import get_session_local


def session_info(sys_session: SysSession) -> SysSessionSchemaWithHeadImg:
    data_path = get_wx_dir(sys_session)
    # db_path = os.path.join(data_path, wx_settings.db_micro_msg)
    # logger.info("DB: %s", db_path)
    data = SysSessionSchemaWithHeadImg(**sys_session.__dict__)
    # 数据目录
    data.data_path = data_path
    # if not os.path.exists(db_path):
    #     return data
    # 存在微信库文件则查询微信用户头像信息
    # SessionLocal = get_session_local(db_path)
    # with SessionLocal() as micro_db:
    #     head_img = micro_db.query(ContactHeadImgUrl).filter_by(usrName=sys_session.wx_id).first()
    #     if head_img:
    #         data.smallHeadImgUrl = head_img.smallHeadImgUrl
    #         data.bigHeadImgUrl = head_img.bigHeadImgUrl
    with get_sys_db() as db:
        session_extra = db.query(SysSessionExtra).filter_by(sys_session_id=sys_session.id).first()
        if session_extra:
            data.client_type = session_extra.client_type
            data.client_version = session_extra.client_version
            data.add_version = session_extra.add_version
    return data
