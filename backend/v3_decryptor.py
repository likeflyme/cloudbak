import traceback

from app.models.sys import SysSession
from config.log_config import logger
from db.sys_db import get_sys_db
from wx.client_factory import ClientFactory
from wx.common.filters.contact_filter import ContactFilterObj
from wx.common.filters.msg_filter import MsgFilterObj, SingleMsgFilterObj
from wx.common.filters.session_filter import SessionFilterObj

if __name__ == '__main__':
    logger.info("test decrypt")
    logger.info("test decrypt")
    try:
        with get_sys_db() as db:
            sys_session = db.query(SysSession).filter_by(id=8).one()
            client = ClientFactory.get_client(sys_session)
            logger.info(f'client is {client}')
            decryptor = client.get_decryptor()
            logger.info(f'decryptor is {decryptor}')
            # decryptor.decrypt()
            contact_manager = client.get_contact_manager()
            logger.info(f'contact_manager is {contact_manager}')
            # contacts = contact_manager.contacts()
            # logger.info("===========================")
            # for contact in contacts:
            #     logger.info(contact)
            contact_filter = ContactFilterObj(search="莉莉")
            contacts = contact_manager.contacts(contact_filter)
            logger.info(f"{len(contacts)}")

            # session_manager = client.get_session_manager()
            # logger.info(f'session_manager is {session_manager}')
            # logger.info("================================")
            # sfo = SessionFilterObj()
            # session_list = session_manager.sessions_page(sfo)
            # for session in session_list:
            #     logger.info(session)

            # logger.info("==================")
            # logger.info(f"第一个会话：{session_list[0]}")
            # message_manager = client.get_message_manager()
            # mfo = MsgFilterObj(username=session_list[0].username)
            # mso = message_manager.messages_filter_page(mfo)
            # logger.info(f"mso = {mso}")
            # for message in mso.messages:
            #     logger.info(message)

            # logger.info("=================")
            # fts_manager = client.get_fts_manager()
            # fts_search_list = fts_manager.fts_search("充电")
            # for fts_msg in fts_search_list:
            #     logger.info(fts_msg)

            # logger.info("======================")
            # logger.info("chatroominfo")
            # chat_room_manager = client.get_chat_room_manager()
            # chat_room_info = chat_room_manager.chatroom_info("39146279886@chatroom")
            # logger.info(chat_room_info.members)

            # logger.info("========================")
            # message_manager = client.get_message_manager()
            # msg = message_manager.message(SingleMsgFilterObj(v3_msg_svr_id=3022847233994031072))
            # logger.info(f"msg is {msg}")
    except Exception as e:
        logger.info("execute error")
        logger.error(e)
        traceback.print_exc()
