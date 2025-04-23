import os
import re
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette import status

from config.log_config import logger, get_context_logger
from wx.interface.wx_interface import ClientInterface, DBManager
from wx.win.v4.enums.v4_enums import V4DBEnum

Base = declarative_base()


class WindowsV4DB(DBManager):

    def __init__(self, client: ClientInterface):
        self.client = client
        # 保存 session local
        self.session_local_dict = defaultdict(lambda: None)
        # 保存 engine
        self.engine_dict = defaultdict(lambda: None)

    def clear(self):
        c_logger = get_context_logger()
        c_logger.info(f"清除微信4 db 连接缓存")
        for db_path, engine in self.engine_dict.items():
            engine.dispose()
        self.session_local_dict.clear()
        self.engine_dict.clear()

    def get_engin(self, db_path) -> Engine:
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

    def get_session_local(self, db_path) -> sessionmaker:
        """
        获取对应数据库文件的 session local
        :param db_path: 数据库路径
        :return: SessionLocal
        """
        sm = self.session_local_dict[db_path]
        if sm is None:
            engine = self.get_engin(db_path)
            sm = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            self.session_local_dict[db_path] = sm
        return sm

    def wx_db(self, relative_db_path: str) -> sessionmaker:
        db_path = os.path.join(self.client.get_wx_dir(), V4DBEnum.DB_BASE_PATH, relative_db_path)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        return self.get_session_local(db_path)

    def wx_db_engine(self, relative_db_path: str) -> Engine:
        db_path = os.path.join(self.client.get_wx_dir(), V4DBEnum.DB_BASE_PATH, relative_db_path)
        logger.info("DB: %s", db_path)
        if not os.path.exists(db_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="库文件不存在:" + db_path
            )
        return self.get_engin(db_path)

    def messages_db_name_array(self):
        message_path = os.path.join(self.client.get_wx_dir(), V4DBEnum.DB_BASE_PATH, V4DBEnum.MESSAGE_DB_FOLDER)
        pattern = re.compile(r'^decoded_message_\d+\.db$')
        db_array = []
        # 遍历目录中的文件
        for filename in os.listdir(message_path):
            if pattern.match(filename):
                db_array.append(filename)
        return db_array

