from collections import defaultdict
from typing import List

from wx.common.filters.fts_filter import FtsFilterObj
from wx.common.output.fts import FtsMsgCount, FtsMsgCross
from wx.interface.wx_interface import FTSManager, ClientInterface
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.db.windows_v3_db_order import WindowsV3DBOrder


def merge_msgs(msgs: List[FtsMsgCount]) -> List[FtsMsgCount]:
    return []


class FTSManagerWindowsV3(FTSManager):

    def __init__(self, db_manager: WindowsV3DB, db_order: WindowsV3DBOrder, client: ClientInterface):
        self.db_manager = db_manager
        self.db_order = db_order
        self.client = client
        self.fts_cache = defaultdict(lambda: None)

    def clear(self):
        self.fts_cache.clear()

    def fts_search(self, text: str) -> List[FtsMsgCount]:
        return []

    def fts_messages(self, filter_obj: FtsFilterObj) -> FtsMsgCross:
        return FtsMsgCross()
