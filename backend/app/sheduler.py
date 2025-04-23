import json
from collections import defaultdict

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.conf.session_conf import SessionConfig
from app.enum.sys_conf_enum import SysConfEnum
from app.models.sys import SysConfig, SysSession
from db.sys_db import SessionLocal
from app.services.analyze import analyze

from app.services.sys_task_maker import TaskObj, task_execute
from config.log_config import logger

scheduler = BackgroundScheduler()

scheduler.start()
logger.info('start background scheduler')

# analyze-user_id-session_id -> Job
job_mapping = defaultdict(lambda: None)

JOB_STABLE_ANALYZE = 'analyze_stable'
JOB_ONCE_ANALYZE = 'analyze_once'

JOB_TP_SESSION = 'session_conf'
JOB_TP_USER = 'user_conf'
JOB_TP_SYS = 'sys_conf'


def load_jobs():

    with SessionLocal() as session:
        configs = session.query(SysConfig).filter_by(conf_key=SysConfEnum.SESSION_CONF).all()
        for config in configs:
            if config.conf_value:
                sys_session = session.query(SysSession).filter_by(id=config.session_id).first()
                if not sys_session:
                    logger.warn(f'no sys_session id is: {config.session_id}')
                    continue
                try:
                    session_conf = SessionConfig.model_validate_json(config.conf_value)
                except Exception as e:
                    logger.warn('load session config error: {}'.format(e))
                    continue
                single = session_conf.analyze
                if single and single.analyze_open:
                    if single.analyze_cron:
                        key = f"{JOB_STABLE_ANALYZE}-{config.user_id}-{sys_session.id}"
                        add_job(key, f"定时数据解析-{sys_session.name}", single.analyze_cron, config.user_id, analyze,
                                [sys_session.id])


def reload_all_jobs():
    """
    停止并删除所有现有的 jobs，然后重新加载从数据库获取的 jobs。
    :return: None
    """
    logger.info('Stopping and removing all jobs')

    # 停止所有 job
    for key in list(job_mapping.keys()):
        remove_job(key)  # 移除每个 job

    # 停止调度器
    # scheduler.shutdown()

    # 重新加载所有 job
    load_jobs()


def add_job(key, job_name, job_cron, user_id, func, args):
    """
    添加job
    :param key: 用于删除
    :param job_name: 展示给用户的名字
    :param job_cron: cron 表达式
    :param user_id: 属于哪个用户
    :param func: 函数名
    :param args: 函数参数
    :return:
    """
    logger.info(f'add {key}, cron is {job_cron}, user: {user_id}')
    if job_mapping[key]:
        logger.warning('job is exist')
        return
    task_obj = TaskObj(user_id, job_name, func, *args)
    job = scheduler.add_job(task_execute, trigger=CronTrigger.from_crontab(job_cron), id=key, args=[task_obj])
    job_mapping[key] = job


def remove_job(key):
    """
    删除job
    :param key:
    :return:
    """
    logger.info(f'remove a job named {key}')
    job = job_mapping[key]
    if not job:
        logger.warning('job not exist')
        return False
    scheduler.remove_job(key)
    del job_mapping[key]


def job_key(job_type, user_id, sys_session_id):
    return f"{job_type}-{user_id}-{sys_session_id}"


def shutdown():
    scheduler.shutdown()
