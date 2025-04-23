import os
import re
from collections import defaultdict
from contextlib import contextmanager

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from config.log_config import get_context_logger, logger
from wx.interface.wx_interface import ClientInterface, DBManager
from wx.win.v3.enums.v3_enums import V3DBEnum


class WindowsV3DB(DBManager):

    def __init__(self, client: ClientInterface):
        self.client = client
        # 保存 session local
        self.session_local_dict = defaultdict(lambda: None)
        # 保存 engine
        self.engine_dict = defaultdict(lambda: None)

    def clear(self):
        c_logger = get_context_logger()
        c_logger.info(f"清除微信3 db 连接缓存")
        # for db_path, session_factory in self.session_local_dict.items():
        #     c_logger.info(f"关闭session：{db_path}")
        #     try:
        #         session = session_factory()
        #         session.close()  # 显式关闭会话
        #     except Exception as e:
        #         c_logger.warning(f"关闭 session 失败: {e}")
        for db_path, engine in self.engine_dict.items():
            c_logger.info(f"关闭连接： {db_path}")
            try:
                engine.dispose(close=True)
            except Exception as e:
                c_logger.warning(f"关闭 engine 失败: {e}")
        self.session_local_dict.clear()
        self.engine_dict.clear()

    def clear_all(self):
        pass

    def get_session_local(self, db_path):
        """
        获取对应数据库文件的 session local
        :param db_path: 数据库路径
        :return: SessionLocal
        """
        if self.session_local_dict[db_path] is None:
            engine = self.get_engin(db_path)
            self.session_local_dict[db_path] = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        return self.session_local_dict[db_path]

    def get_engin(self, db_path):
        engine = self.engine_dict[db_path]
        if engine is None:
            engine = create_engine(
                f"sqlite:///{db_path}",
                connect_args={"check_same_thread": False},
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600
            )
            self.engine_dict[db_path] = engine
        return engine

    @contextmanager
    def session_scope(self, db_path):
        sm = self.get_session_local(db_path)
        session = sm()
        try:
            yield session
        finally:
            session.close()

    def msg_db_count(self) -> int:
        path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI)

        pattern = re.compile(r'^decoded_MSG\d+\.db$')
        # 计数器
        count = 0

        # 遍历目录中的文件
        for filename in os.listdir(path):
            if pattern.match(filename):
                count += 1
        return count

    def multi_msg_db_array(self) -> list:
        path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI)
        pattern = re.compile(r'^decoded_MSG\d+\.db$')
        db_array = []
        # 遍历目录中的文件
        for filename in os.listdir(path):
            if pattern.match(filename):
                db_array.append(filename)
        return db_array

    def media_msg_db_array(self) -> list:
        path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI)
        pattern = re.compile(r'^decoded_MediaMSG\d+\.db$')
        db_array = []
        # 遍历目录中的文件
        for filename in os.listdir(path):
            if pattern.match(filename):
                db_array.append(filename)
        return db_array

    def fts_msg_db_array(self) -> list:
        path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI)
        pattern = re.compile(r'^decoded_FTSMSG\d+\.db$')
        db_array = []
        # 遍历目录中的文件
        for filename in os.listdir(path):
            if pattern.match(filename):
                db_array.append(filename)
        return db_array

    def wx_db_msg(self, c: int):
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI_MSG + str(c) + '.db')
        logger.info(f"{db_path}")
        if not os.path.exists(db_path):
            logger.info("库文件不存在")
            return None
        return self.get_session_local(db_path)

    def wx_db_msg_by_name(self, db_name: str):
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI, db_name)
        logger.info(f"{db_path}")
        if not os.path.exists(db_path):
            logger.info("库文件不存在")
            return None
        return self.get_session_local(db_path)

    def wx_db_media_msg(self, c: int):
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI_MEDIA_MSG + str(c) + '.db')
        logger.info(f"{db_path}")
        if not os.path.exists(db_path):
            return None
        return self.get_session_local(db_path)

    def wx_db_media_msg_by_filename(self, filename: str):
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI, filename)
        logger.info(f"{db_path}")
        if not os.path.exists(db_path):
            return None
        return self.get_session_local(db_path)

    def wx_db_msg0(self, ):
        """
        获取 multi/MSG0.db 数据库 session
        :param wxid: 用户当前微信id
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MULTI_MSG)
        SessionLocal = self.get_session_local(db_path)
        my_db = SessionLocal()
        try:
            yield my_db
        finally:
            my_db.close()

    @contextmanager
    def wx_db_micro_msg(self):
        """
        获取 MicroMsg.db 数据库 session
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_MICRO_MSG)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        sm = self.get_session_local(db_path)
        session = sm()
        try:
            yield session
        finally:
            session.close()

    def wx_db_hard_link_image(self):
        """
        获取 HardLinkImage.db 数据库 session
        :param wxid: 用户当前微信id
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_HARD_LINK_IMAGE)
        logger.info("DB: %s", db_path)
        SessionLocal = self.get_session_local(db_path)
        my_db = SessionLocal()
        try:
            yield my_db
        finally:
            my_db.close()

    def wx_db_public_msg(self):
        """
        获取 PublicMsg.db 数据库 session
        :param wxid: 用户当前微信id
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_PUBLIC_MSG)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        SessionLocal = self.get_session_local(db_path)
        my_db = SessionLocal()
        try:
            yield my_db
        finally:
            my_db.close()

    def wx_db_openim_msg(self):
        """
        获取 OpenIMMsg.db 数据库 session
        :param wxid: 用户当前微信id
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), V3DBEnum.DB_OPENIM_MSG)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        SessionLocal = self.get_session_local(db_path)
        my_db = SessionLocal()
        try:
            yield my_db
        finally:
            my_db.close()

    def wx_db_for_conf(self, db_url):
        """
        获取微信数据库 session
        :param db_url: wx_settings 中的配置地址
        :return: 数据库 session
        """
        db_path = os.path.join(self.client.get_wx_dir(), db_url)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        return self.get_session_local(db_path)

    def wx_db_engin_for_conf(self, db_url: str):
        db_path = os.path.join(self.client.get_wx_dir(), db_url)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        return self.get_engin(db_path)
