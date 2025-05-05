import os
import shutil
import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends, HTTPException 
from sqlalchemy.orm import Session

from app.dependencies.auth_dep import get_current_user
from app.helper.directory_helper import get_session_dir, get_wx_dir_directly
from app.models.sys import SysSession
from app.schemas.sys_schemas import User, SysSessionOut
from app.services.analyze import analyze
from app.services.sys_task_maker import TaskObj, task_execute
from config.log_config import logger
from db.sys_db import get_db

router = APIRouter(
    prefix="/wx"
)


def save_file_chunk(file_path: str, file_chunk: UploadFile):
    with open(file_path, "ab") as f:
        shutil.copyfileobj(file_chunk.file, f)


@router.post("/upload-single/")
async def upload_zip(
        file: UploadFile = File(...),
        file_path: Optional[str] = Form(...),
        sys_session_id: Optional[int] = Form(...),
        wx_id: Optional[str] = Form(...)):
    file_path = file_path.replace("\\", "/").lstrip("/")
    logger.info("文件路径：" + str(file_path))
    # 获取用户保存目录
    wx_dir = get_wx_dir_directly(sys_session_id, wx_id)
    # 拼接保存路径
    save_path = os.path.join(wx_dir, file_path)

    # 检查路径是否穿透到 wx_dir 之外
    try:
        abs_save_path = Path(save_path).resolve(strict=False)
        abs_wx_dir = Path(wx_dir).resolve(strict=True)
        if not str(abs_save_path).startswith(str(abs_wx_dir)):
            logger.error("路径非法：尝试穿透目录")
            raise HTTPException(status_code=400, detail="非法文件路径")
    except Exception as e:
        logger.error(f"路径校验失败：{e}")
        raise HTTPException(status_code=400, detail="路径校验失败")

    # 创建目录（如果不存在）
    directory = Path(save_path).parent
    directory.mkdir(parents=True, exist_ok=True)

    logger.info("保存路径：" + save_path)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)


@router.post("/upload-zip/")
async def upload_zip(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        sys_session_id: Optional[int] = Form(...),
        db: Session = Depends(get_db)
):
    logger.info("sys_session_id 为: " + str(sys_session_id))
    session_dir = get_session_dir(sys_session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    file_location = os.path.join(session_dir, file.filename)
    save_file_chunk(file_location, file)

    # 获取上传文件的大小
    uploaded_file_size = os.path.getsize(file_location)

    # 判断文件上传完成
    if uploaded_file_size == file.file._file.seek(0, os.SEEK_END):
        logger.info("文件上传完成，大小为" + str(uploaded_file_size))
        sys_session = db.query(SysSession).filter_by(id=sys_session_id).first()
        task_obj = TaskObj(sys_session.owner_id, "数据库解析任务", analyze, sys_session_id)
        background_tasks.add_task(task_execute, task_obj)
        return {"detail": "File uploaded successfully."}
    else:
        logger.info("文件正在上传")
        return {"detail": "Upload incomplete."}


@router.post("/do-decrypt/{sys_session_id}", response_model=SysSessionOut)
def client_decrypt(sys_session_id: int,
               background_tasks: BackgroundTasks,
               update_time: int = int(time.time()),
               sys_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    """
    客户端同步完数据后调用，设置上次同步时间，提交异步解析任务
    :param sys_session_id:
    :param background_tasks:
    :param update_time:
    :param sys_user:
    :param db:
    :return:
    """
    logger.info("客户端提交的时间戳：%d", update_time)
    sys_session = db.query(SysSession).filter_by(id=sys_session_id).first()
    sys_session.update_time = update_time
    db.commit()
    db.refresh(sys_session)
    # 异步执行解析
    task_obj = TaskObj(sys_user.id, f"数据解析-{sys_session.name}", analyze, sys_session_id)
    background_tasks.add_task(task_execute, task_obj)
    return sys_session
