import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.exception.auth_exception import LoginException
from app.middleware.request_id_middleware import add_request_id
from app.services.sys_conf_service import initial_sys_info
from app.services.user_service import update_user_none_state
from routes import api
from fastapi_pagination import add_pagination

from app.exception.handler_exception import global_exception_handler, login_exception_handler
from db.sys_db import engine, Base
# 加载表模型，确保创建表
from app.models import sys
from config.app_config import settings
from app.sheduler import load_jobs

from db.wx_db import clear_all as wx_db_clear_all
from db.sys_db import clear_all as sys_db_clear_all
from config.log_config import logger
from contextlib import asynccontextmanager
from app.sheduler import shutdown as scheduler_shutdown
from wx.client_factory import ClientFactory


def create_app() -> FastAPI:
    # 加载配置文件环境变量
    load_dotenv()
    # 上传大文件缓存目录
    tempfile.tempdir = os.path.join(settings.sys_dir, settings.tmp_dir)
    if not os.path.exists(tempfile.tempdir):
        os.makedirs(tempfile.tempdir)

    # 创建数据库与所有系统表
    Base.metadata.create_all(bind=engine)

    # 启动并注册生命周期函数 lifespan
    app = FastAPI(lifespan=lifespan)

    head_path = os.path.join(settings.sys_dir, settings.head_dir)
    # 检查目录是否已经存在
    if not os.path.exists(head_path):
        os.makedirs(head_path)
    # 配置静态文件映射
    app.mount(settings.head_mapping, StaticFiles(directory=str(head_path)), name="images")

    # 中间件
    app.middleware('http')(add_request_id)
    # 路由
    app.include_router(api.router)
    # 分页
    add_pagination(app)

    # 通用异常处理
    app.add_exception_handler(Exception, global_exception_handler)
    # 登录异常处理
    app.add_exception_handler(LoginException, login_exception_handler)

    # 创建定时任务
    load_jobs()

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    生命周期函数
    启动事件放在 yield 之前，关闭事件放在 yield 之后
    :param app:
    :return:
    """
    try:
        startup()
        yield
        shutdown()
    except Exception as e:
        logger.error(e)


def startup():
    """
    启动事件
    :return:
    """
    logger.info("Start")
    # 初始化系统配置信息，当前主要为系统唯一ID用户授权系统
    initial_sys_info()
    # 用户状态兼容
    update_user_none_state()


def shutdown():
    """
    关闭事件
    :return:
    """
    try:
        logger.info("Shutting down...")
        ClientFactory.clear()
        logger.info("DB Connections All Closed")
    except Exception as e:
        logger.warning("Close DB Connection Error")
        logger.error(e)
    try:
        logger.info('Shutting down scheduler')
        scheduler_shutdown()
        logger.info('Shutting down scheduler success')
    except Exception as e:
        logger.warning('scheduler shutdown error')
        logger.error(e)

