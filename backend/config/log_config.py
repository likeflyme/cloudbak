import logging
import os.path
import time
import uuid
import contextvars
from logging import Logger, LogRecord, getLogger
from typing import Optional
from config.app_config import settings
from logging.handlers import TimedRotatingFileHandler


context_logger = contextvars.ContextVar('context_logger', default=None)


class CustomContextFilter(logging.Filter):
    def __init__(self, initial_request_id: Optional[str] = None):
        super().__init__()
        self.request_id = initial_request_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id
        return True


class RequestFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        record.request_id = getattr(record, 'request_id', '')  # Safe retrieval of request_id
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        """重写 formatTime 方法，使日志时间精确到毫秒"""
        ct = self.converter(record.created)  # 获取本地时间
        t = time.strftime("%Y-%m-%d %H:%M:%S", ct)  # 格式化时间（秒级）
        ms = f"{int(record.msecs):03d}"  # 获取毫秒部分，格式化为三位数
        return f"{t}.{ms}"  # 返回最终时间格式（精确到毫秒）


# 创建一个自定义的 ContextFilter，并设置初始的 request_id
context_filter = CustomContextFilter(None)


def set_log_id():
    # 生成一个唯一的 request_id
    request_id = str(uuid.uuid4())

    # 更新 ContextFilter 中的 request_id
    context_filter.request_id = request_id


def logger():
    # 创建一个日志记录器
    app_logger = logging.getLogger('fastapi_app')
    app_logger.setLevel(logging.INFO)

    # 添加 ContextFilter 到全局 Logger
    app_logger.addFilter(context_filter)

    formatter = RequestFormatter(fmt='%(asctime)s - %(request_id)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 创建一个 handler 将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    log_dir = os.path.join(settings.sys_dir, settings.log_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_name = settings.log_file_name
    log_file_path = os.path.join(str(log_dir), log_file_name)
    # 创建一个文件处理器，并设置编码为 UTF-8
    # 使用 TimedRotatingFileHandler 按日期分割日志文件
    file_handler = TimedRotatingFileHandler(
        str(log_file_path), when='midnight', interval=1, backupCount=7, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)
    return app_logger


def analyze_logger(logger_name: str, path: str):
    """
    数据解析用的日志记录器
    :return:
    """
    a_logger = logging.getLogger(logger_name)
    a_logger.setLevel(logging.INFO)

    # 添加 ContextFilter 到全局 Logger
    a_logger.addFilter(context_filter)

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 创建一个 handler 将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    a_logger.addHandler(console_handler)
    # 创建一个文件处理器，并设置编码为 UTF-8
    file_handler = logging.FileHandler(path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    a_logger.addHandler(file_handler)
    return a_logger


logger = logger()


def set_context_logger(c_logger):
    """
    设置上下文 logger
    """
    context_logger.set(c_logger)


def get_context_logger() -> Logger:
    """
    获取上下文 logger，没有上下文 logger 则返回默认 logger
    """
    c_logger = context_logger.get()
    if c_logger is None:
        return logger
    return c_logger


def clear_logger(logger_name: str):
    """
    删除 loging 中的 logger
    :param logger_name:
    :return:
    """
    if logger_name in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict[logger_name]
