import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.dependencies.auth_dep import get_current_user, get_current_sys_session
from app.models.sys import SysTask, SysUser, SysConfig, SysSession
from app.schemas.sys_conf_schemas import JobIn
from app.sheduler import JOB_STABLE_ANALYZE, remove_job, add_job
from config.app_config import settings
from db.sys_db import get_db
from app.services.analyze import analyze
from app.services.sys_task_maker import TaskObj, task_execute

from app.schemas.sys_schemas import SysTaskOut
from app.sheduler import job_key
from config.log_config import logger

router = APIRouter(
    prefix="/task"
)


@router.get("/", response_model=List[SysTaskOut])
async def upload_zip(
        size: int = 20,
        page: int = 1,
        db: Session = Depends(get_db),
        user: SysUser = Depends(get_current_user)):
    return db.query(SysTask).filter_by(owner_id=user.id).order_by(SysTask.id.desc()).offset((page - 1) * size).limit(size).all()


@router.get("/log")
async def get_video(task_id: int, db: Session = Depends(get_db)):
    task = db.query(SysTask).filter_by(id=task_id).one()

    if task.detail:
        log_path = os.path.join(settings.sys_dir, task.detail)
        if os.path.exists(log_path):
            return FileResponse(str(log_path), media_type="text/plain")
    raise HTTPException(status_code=404, detail="File not found")


@router.post("/single-decrypt/{sys_session_id}/{deep}")
def single_decrypt(sys_session_id: int,
                   background_tasks: BackgroundTasks,
                   deep: bool = False,
                   sys_user: SysUser = Depends(get_current_user)):
    """
    只执行一次解析任务
    :param sys_session_id:
    :param background_tasks:
    :param deep 是否全量解析
    :param sys_user:
    :return:
    """
    logger.info(f"method param deep: {deep}")
    task_obj = TaskObj(sys_user.id, "数据解析", analyze, sys_session_id, deep)
    background_tasks.add_task(task_execute, task_obj)


@router.post("/update-analyze-job")
def update_analyze_job(job_in: JobIn,
                       sys_user: SysUser = Depends(get_current_user),
                       sys_session: SysSession = Depends(get_current_sys_session)):
    """
    修改解析任务
    :param job_in: 任务数据
    :param sys_user:
    :param sys_session:
    :return:
    """
    key = job_key(JOB_STABLE_ANALYZE, sys_user.id, job_in.sys_session_id)
    remove_job(key)
    if job_in.open:
        add_job(key, f"定时数据解析-{sys_session.name}", job_in.cron, sys_user.id, analyze, job_in.sys_session_id)
