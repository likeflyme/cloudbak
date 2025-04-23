import time
from datetime import datetime

from app.models.sys import SysSession
from app.services.multi_fts_msg import msg_count_list_search, msg_search_by_user_name, cross_db_paginated_search
from db.sys_db import get_sys_db
from config.log_config import logger


def search():
    with get_sys_db() as db:
        match = '充电'
        sys_session = db.query(SysSession).filter_by(id=8).one()
        msgs = msg_count_list_search(match, sys_session)
        index = 0
        logger.info("contacts--------------------------------------")
        for msg in msgs:
            index = index + 1
            # logger.info(f'{index}: userName: {msg.userName}, count: {msg.count}, content: {msg.content}')
            logger.info(f'{index}: userName: {msg.userName}, count: {msg.count}')
        user_name = '19971051823@chatroom'
        db_name, start, msgs = cross_search(user_name, match, sys_session, 10, 0)
        cross_search(user_name, match, sys_session, 10, start, db_name)


def cross_search(user_name, match, sys_session, page_size, start, db_name=None):
    db_name, start, msgs = cross_db_paginated_search(user_name, match, sys_session, page_size, start, db_name)
    index = 0
    logger.info(f"msgs: page={0}, page_size={page_size}, start={start}------------------------------------------")
    for msg in msgs:
        index = index + 1
        logger.info(f'{index}: db_name: {msg.db_name}, msg: {msg.content}, type: {msg.type}, subType: {msg.subType}, sortSequence: {msg.sequence}')
    logger.info(f"db_name: {db_name}, start: {start}")
    return db_name, start, msgs


search()


# with get_sys_db() as db:
#     sys_session = db.query(SysSession).filter_by(id=8).one()
#     msgs = msg_search_by_user_name('2200692676@chatroom', '充电', sys_session)
#     for msg in msgs:
#         logger.info(msg)
