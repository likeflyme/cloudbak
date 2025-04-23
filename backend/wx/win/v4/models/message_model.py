import hashlib
from typing import Any, Type

from sqlalchemy import Column, Integer, String, LargeBinary

from config.log_config import logger
from wx.win.v4.db.windows_v4_db import Base


class DynamicModel:
    message_models = {}

    @classmethod
    def get_dynamic_message_model(cls, username: str) -> Type[Base] | Any:
        name_hash = DynamicModel.md5_username(username)
        logger.info(cls.message_models.keys())
        if name_hash in cls.message_models.keys():
            return cls.message_models[name_hash]

        table_name = f"Msg_{name_hash}"
        class_name = f"DynamicTable_{table_name}"  # 生成唯一的类名

        logger.info(f"创建动态类，table_name={table_name} for username={username}")

        # 动态创建类
        DynamicTable = type(class_name, (Base,), {
            "__tablename__": table_name,
            "local_id": Column(Integer, primary_key=True),
            "server_id": Column(Integer),
            "local_type": Column(Integer),
            "sort_seq": Column(Integer),
            "real_sender_id": Column(Integer),
            "create_time": Column(Integer),
            "status": Column(Integer),
            "upload_status": Column(Integer),
            "download_status": Column(Integer),
            "origin_source": Column(Integer),
            "source": Column(String),
            "message_content": Column(String),
            "compress_content": Column(String),
            "packed_info_data": Column(LargeBinary),
            "WCDB_CT_message_content": Column(Integer),
            "WCDB_CT_source": Column(Integer),
        })

        # 缓存表
        cls.message_models[name_hash] = DynamicTable
        return DynamicTable

    @classmethod
    def md5_username(cls, username: str):
        """
        用户名转md5字符串用于获取表名后缀
        """
        # 创建 MD5 对象
        md5 = hashlib.md5()
        # 更新输入字符串，记得编码成字节
        md5.update(username.encode('utf-8'))
        # 获取哈希值并返回
        return md5.hexdigest()


class Name2Id(Base):
    __tablename__ = "Name2Id"

    user_name = Column(String, primary_key=True)
