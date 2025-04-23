from app.api.msg import red_msgs_by_sequence
from app.enum.msg_enum import FilterMode
from app.models.sys import SysSession
from db.sys_db import get_sys_db
from config.log_config import logger


def search(strUsrName: str, sequence: int, start: int = 0, db_name: str = None):
    with get_sys_db() as db:
        sys_session = db.query(SysSession).filter_by(id=8).one()
        return red_msgs_by_sequence(strUsrName, sequence, FilterMode.DESC, start, db_name, 20, sys_session)


def scroll_search_print(strUsrName: str, sequence: int, start: int = 0, db_name: str = None):
    chat_msg = search(strUsrName, sequence, start, db_name)

    for msg in chat_msg.msgs:
        logger.info(f"type: {msg.Type}, subType: {msg.SubType}, strContent: {msg.StrContent}")
    logger.info(f"start: {chat_msg.start}, start_db: {chat_msg.start_db}")
    return chat_msg


strUsrName = '19971051823@chatroom'
sequence = 1705022963000
start = 0
db_name = None

chat_msg = scroll_search_print(strUsrName, sequence, start, db_name)

start = chat_msg.start
db_name = chat_msg.start_db
logger.info("new search: ================================")
logger.info(f"start={start}, db_name={db_name}")
scroll_search_print(strUsrName, sequence, start, db_name)






