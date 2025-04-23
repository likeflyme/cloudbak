from app.models.sys import SysSession, SysSessionExtra
from config.log_config import logger
from db.sys_db import get_sys_db
from wx.interface.wx_interface import ClientInterface
from wx.win.v3.windows_client_v3 import WindowsClientV3
from wx.win.v4.windows_client_v4 import WindowsClientV4

session_client_cache = {}
client_map = {
    "win.v3": WindowsClientV3,
    "win.v4": WindowsClientV4
}
default_client_type_version = "win.v3"


class ClientFactory:

    @staticmethod
    def clear():
        for session_id, client in client_map:
            client.clear()

    @staticmethod
    def get_client(sys_session: SysSession, sys_session_extra: SysSessionExtra = None) -> ClientInterface:
        logger.info("get_client")
        logger.info(f"sys_session: {sys_session}")
        logger.info(f"sys_session_extra: {sys_session_extra}")
        # 映射client_id到实现类
        logger.info(f"session_client_cache keys: {session_client_cache.keys()}")
        if sys_session.id in session_client_cache:
            return session_client_cache[sys_session.id]
        if sys_session_extra:
            client_type_version = f"{sys_session_extra.client_type}.{sys_session_extra.client_version}"
        else:
            # 默认为 win.v3
            client_type_version = default_client_type_version
            logger.info(f"默认版本：{default_client_type_version}")
        logger.info(f"type_version: {client_type_version}")
        # 根据id获取对应的实现类
        if client_type_version not in client_map:
            logger.info(f"不支持的客户端版本：{client_type_version}")
            raise ValueError(f"不支持的客户端版本: {client_type_version}")
        session_client = client_map[client_type_version](sys_session, sys_session_extra)
        session_client_cache[sys_session.id] = session_client
        return session_client

    @staticmethod
    def get_client_by_id(sys_session_id: int) -> ClientInterface:
        """根据传入的client_id选择对应的实现类"""
        logger.info("get_client_by_id")
        with get_sys_db() as db:
            sys_session = db.query(SysSession).filter_by(id=sys_session_id).one()
            sys_session_extra = db.query(SysSessionExtra).filter_by(sys_session_id=sys_session_id).first()
            return ClientFactory.get_client(sys_session, sys_session_extra)

    @staticmethod
    def refresh_client_by_id(sys_session_id: int) -> ClientInterface:
        if sys_session_id in session_client_cache:
            del session_client_cache[sys_session_id]
        return ClientFactory.get_client_by_id(sys_session_id)