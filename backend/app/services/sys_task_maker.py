import time
import os

from db.sys_db import SessionLocal
from app.models.sys import SysTask
from config.log_config import analyze_logger, set_context_logger, clear_logger
from config.app_config import settings

task_running = 2  # 任务执行中
task_success = 0  # 任务执行完成
task_fail = 1  # 任务执行失败


class TaskObj:
    def __init__(self, owner_id, name, func, *args):
        self.owner_id = owner_id
        self.name = name
        self.func = func
        self.args = args


class TaskExecutionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"TaskExecutionError: {self.message}"


def task_execute(obj: TaskObj):
    start_time = time.time()
    log_dir = os.path.join(settings.sys_dir, settings.log_dir, settings.log_task_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # log_file_name = int(time.time() * 1000)
    log_file_name = f"{int(time.time() * 1000)}-{obj.name}.log"
    log_file_path = os.path.join(str(log_dir), str(log_file_name))
    logger = analyze_logger(str(log_file_name), log_file_path)
    # 设置上下文 logger
    set_context_logger(logger)
    logger.info(f'执行任务：{obj.name}')
    db = SessionLocal()
    relative_path = os.path.join(settings.log_dir, settings.log_task_dir, str(log_file_name))
    task = SysTask(name=obj.name, owner_id=obj.owner_id, state=task_running, detail=str(relative_path), create_time=start_time, update_time=start_time)
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        # 调用函数
        try:
            logger.info(f"args: {obj.args}")
            obj.func(*obj.args)
            task.state = task_success
        except TaskExecutionError as e:
            task.state = task_fail
            task.detail = e.message
            logger.error(e.message)
        except Exception as e:
            task.state = task_fail
            logger.error("任务执行异常")
            logger.error(e)
    except Exception as e:
        logger.info("任务数据提交异常")
        logger.error(e)
    finally:
        # 更新时间
        task.update_time = time.time()
        db.commit()
        db.close()
        # 计算执行时间，单位为秒
        execution_time = time.time() - start_time
        logger.info(f'任务执行完成，花费时间: {execution_time}s')
        # 销毁 logger
        clear_logger(str(log_file_name))
