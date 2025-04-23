from collections import defaultdict

from config.log_config import get_context_logger
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.models.multi.msg import Name2ID


class WindowsV3TakerId:
    def __init__(self, db_manager: WindowsV3DB):
        self.db_manager = db_manager
        # 保存库名对应的用户id
        self.talker_id_by_name_cache = defaultdict(lambda: None)

    def clear(self):
        self.talker_id_by_name_cache.clear()

    def get_talker_id_by_db_name(self, db_name: int, wx_id: str):
        taker_cache = self.talker_id_by_name_cache[db_name]
        if taker_cache is None:
            self.init_talker(db_name)
            return self.talker_id_by_name_cache[db_name][wx_id]
        return taker_cache[wx_id]

    def init_talker(self, db_name):
        logger = get_context_logger()
        logger.info(f"初始化takerId, db_name = {db_name}")
        wx_dict = defaultdict(lambda: None)
        wx_session_local = self.db_manager.wx_db_msg_by_name(db_name)
        with wx_session_local() as wx_db:
            talkers = wx_db.query(Name2ID).all()
            for index, talker in enumerate(talkers):
                wx_dict[talker.UsrName] = index + 1
        self.talker_id_by_name_cache[db_name] = wx_dict
