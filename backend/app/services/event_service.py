from datetime import datetime, timedelta

from sqlalchemy import func, and_

from app.enum.event_enum import EventType
from app.models.sys import SysEvent
from db.sys_db import get_sys_db


def record_event(event: EventType, key: str, detail: str):
    with get_sys_db() as db:
        event = SysEvent(event_type=event, event_key=key, event_detail=detail)
        db.add(event)
        db.commit()


def count_within_hours(event: EventType, key: str, hours: int):
    """
    获取一定时间内的事件次数
    """
    now = datetime.now()
    # 减去 24 小时
    time_24_hours_ago = now - timedelta(hours=hours)
    with get_sys_db() as db:
        count = db.query(func.count(SysEvent.id)).filter(
            and_(
                SysEvent.event_type == event,
                SysEvent.event_key == key,
                SysEvent.create_time >= time_24_hours_ago,  # 使用 DateTime 对象直接比较
            )
        ).scalar()
        return count
