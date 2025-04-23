import os
import re
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.helper.directory_helper import get_wx_dir
from app.models.sys import SysSession
from sqlalchemy.ext.declarative import declarative_base
from config.log_config import logger, get_context_logger
from config.wx_config import settings as wx_settings

Base = declarative_base()

# 保存 session local
session_local_dict = defaultdict(lambda: None)
# 保存 engine
engine_dict = defaultdict(lambda: None)


def clear_wx_db_cache():
    session_local_dict.clear()
    engine_dict.clear()


def clear_session_db_cache(session_dir):
    c_logger = get_context_logger()
    c_logger.info(f"清除微信db连接缓存: {session_dir}")
    try:
        keys_to_delete = []  # 需要删除的 keys
        for key in engine_dict.keys():
            abs_file_path = os.path.abspath(key)
            abs_base_dir = os.path.abspath(session_dir)
            if abs_file_path.startswith(abs_base_dir):
                engine = engine_dict[key]
                if engine:
                    # 关闭所有连接
                    c_logger.info(f"engin关闭所有连接：{key}")
                    engine.dispose()
                # 放入待删除列表
                keys_to_delete.append(key)
        # 删除缓存字典中的数据
        for key in keys_to_delete:
            del engine_dict[key]
            del session_local_dict[key]
            c_logger.info(f"已删除缓存中的连接和会话：{key}")
    except Exception as e:
        c_logger.info("关闭连接异常")
        c_logger.error(e)


def clear_all():
    for db_path, session_local in session_local_dict.items():
        if session_local is not None:
            session = session_local()
            session.close()  # 关闭会话
            engine = engine_dict[db_path]
            if engine:
                engine.dispose()  # 关闭引擎
                del engine_dict[db_path]
    # 清空 session_local_dict
    session_local_dict.clear()


def get_session_local(db_path):
    """
    获取对应数据库文件的 session local
    :param db_path: 数据库路径
    :return: SessionLocal
    """
    if session_local_dict[db_path] is None:
        engine = get_engin(db_path)
        session_local_dict[db_path] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_local_dict[db_path]


def get_engin(db_path):
    engine = engine_dict[db_path]
    if engine is None:
        engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600
        )
        engine_dict[db_path] = engine
    return engine


def msg_db_count(sys_session: SysSession) -> int:
    path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi)

    pattern = re.compile(r'^decoded_MSG\d+\.db$')
    # 计数器
    count = 0

    # 遍历目录中的文件
    for filename in os.listdir(path):
        if pattern.match(filename):
            count += 1
    return count


def multi_msg_db_array(sys_session: SysSession) -> list:
    path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi)
    pattern = re.compile(r'^decoded_MSG\d+\.db$')
    db_array = []
    # 遍历目录中的文件
    for filename in os.listdir(path):
        if pattern.match(filename):
            db_array.append(filename)
    return db_array


def media_msg_db_array(sys_session: SysSession) -> list:
    path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi)
    pattern = re.compile(r'^decoded_MediaMSG\d+\.db$')
    db_array = []
    # 遍历目录中的文件
    for filename in os.listdir(path):
        if pattern.match(filename):
            db_array.append(filename)
    return db_array


def fts_msg_db_array(sys_session: SysSession) -> list:
    path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi)
    pattern = re.compile(r'^decoded_FTSMSG\d+\.db$')
    db_array = []
    # 遍历目录中的文件
    for filename in os.listdir(path):
        if pattern.match(filename):
            db_array.append(filename)
    return db_array


def wx_db_msg(c: int, sys_session: SysSession):
    db_path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi_msg + str(c) + '.db')
    logger.info(f"{db_path}")
    if not os.path.exists(db_path):
        logger.info("库文件不存在")
        return None
    return get_session_local(db_path)


def wx_db_msg_by_name(db_name: str, sys_session: SysSession):
    wx_dir = get_wx_dir(sys_session)
    db_path = os.path.join(wx_dir, wx_settings.db_multi, db_name)
    logger.info(f"{db_path}")
    if not os.path.exists(db_path):
        logger.info("库文件不存在")
        return None
    return get_session_local(db_path)


def wx_db_media_msg(c: int, sys_session):
    db_path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi_media_msg + str(c) + '.db')
    logger.info(f"{db_path}")
    if not os.path.exists(db_path):
        return None
    return get_session_local(db_path)


def wx_db_media_msg_by_filename(filename: str, sys_session):
    db_path = os.path.join(get_wx_dir(sys_session), wx_settings.db_multi, filename)
    logger.info(f"{db_path}")
    if not os.path.exists(db_path):
        return None
    return get_session_local(db_path)


def wx_db_msg0(curren_session: SysSession):
    """
    获取 multi/MSG0.db 数据库 session
    :param wxid: 用户当前微信id
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), wx_settings.db_multi_msg)
    SessionLocal = get_session_local(db_path)
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def wx_db_micro_msg(curren_session: SysSession):
    """
    获取 MicroMsg.db 数据库 session
    :param wxid: 用户当前微信id
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), wx_settings.db_micro_msg)
    logger.info("DB: %s", db_path)
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="库文件不存在:" + db_path
        )
    SessionLocal = get_session_local(db_path)
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def wx_db_hard_link_image(curren_session: SysSession):
    """
    获取 HardLinkImage.db 数据库 session
    :param wxid: 用户当前微信id
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), wx_settings.db_hard_link_image)
    logger.info("DB: %s", db_path)
    SessionLocal = get_session_local(db_path)
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def wx_db_public_msg(curren_session: SysSession):
    """
    获取 PublicMsg.db 数据库 session
    :param wxid: 用户当前微信id
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), wx_settings.db_public_msg)
    logger.info("DB: %s", db_path)
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="库文件不存在:" + db_path
        )
    SessionLocal = get_session_local(db_path)
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def wx_db_openim_msg(curren_session: SysSession):
    """
    获取 OpenIMMsg.db 数据库 session
    :param wxid: 用户当前微信id
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), wx_settings.db_openim_msg)
    logger.info("DB: %s", db_path)
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="库文件不存在:" + db_path
        )
    SessionLocal = get_session_local(db_path)
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def wx_db_for_conf(db_url: str, curren_session: SysSession):
    """
    获取微信数据库 session
    :param db_url: wx_settings 中的配置地址
    :curren_session: 用户 session
    :return: 数据库 session
    """
    db_path = os.path.join(get_wx_dir(curren_session), db_url)
    logger.info("DB: %s", db_path)
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="库文件不存在:" + db_path
        )
    return get_session_local(db_path)


def wx_db_engin_for_conf(db_url: str, curren_session: SysSession):
    db_path = os.path.join(get_wx_dir(curren_session), db_url)
    logger.info("DB: %s", db_path)
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="库文件不存在:" + db_path
        )
    return get_engin(db_path)
