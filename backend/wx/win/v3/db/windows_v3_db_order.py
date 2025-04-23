import array

from config.log_config import get_context_logger
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.models.multi.msg import Msg


class WindowsV3DBOrder:
    def __init__(self, db_manager: WindowsV3DB):
        self.db_manager = db_manager
        # 保存MGS文件名列表，从大到小排序
        self.msg_name_sort = []
        # 保存MediaMSG文件名列表，从大到小排序
        self.media_msg_sort = []
        # 保存FTSMSG文件名列表，从大到小排序
        self.fts_msg_sort = []

    def clear(self):
        self.msg_name_sort.clear()
        self.media_msg_sort.clear()
        self.fts_msg_sort.clear()

    def msg_db_array(self):
        logger = get_context_logger()
        if len(self.msg_name_sort) > 0:
            logger.info(f"获取到MSG缓存的库排序: {self.msg_name_sort}")
            return self.msg_name_sort
        # 直接查询的数据是从小到大排序，需要反向排序
        sorted_array = self.db_manager.multi_msg_db_array()
        sorted_array.sort(reverse=True)
        key_value_array = []
        for db_name in sorted_array:
            logger.info(f"查询库 {db_name}")
            sm = self.db_manager.wx_db_msg_by_name(db_name)
            if sm is None:
                logger.warning(f"警告：库 {db_name} 对应的 session_local 不存在")
                continue
            with sm() as db:
                msg = db.query(Msg).order_by(Msg.localId.desc()).first()
                if msg is None:
                    logger.warning(f"警告：库 {db_name} 中没有找到消息记录，跳过。")
                    continue
                key_value_array.append({
                    "name": db_name,
                    "create_time": msg.CreateTime
                })
        # 排序
        key_value_array.sort(key=lambda x: x["create_time"], reverse=True)
        self.msg_name_sort = [x["name"] for x in key_value_array]
        logger.info(f"生成Multi/MSG库排序缓存：{self.msg_name_sort}")
        return self.msg_name_sort

    def media_msg_db_array(self):
        """
        Multi/MediaMSG.db 排序列表
        """
        logger = get_context_logger()
        if len(self.media_msg_sort) > 0:
            logger.info(f"获取到MediaMSG缓存的库排序: {self.media_msg_sort}")
            return self.media_msg_sort
        # 直接查询的数据是从小到大排序，需要反向排序
        sorted_array = self.db_manager.media_msg_db_array()
        sorted_array.sort(reverse=True)
        self.media_msg_sort = sorted_array
        logger.info(f"生成MediaMSG库排序缓存：{self.media_msg_sort}")
        return sorted_array

    def fts_msg_db_array(self):
        """
        Multi/FTSMSG.db 排序列表
        """
        logger = get_context_logger()
        sorted_array = self.fts_msg_sort
        if sorted_array:
            logger.info(f"获取到FTSMSG缓存的库排序: {sorted_array}")
            return sorted_array
        # 直接查询的数据是从小到大排序，需要反向排序
        sorted_array = self.db_manager.fts_msg_db_array()
        sorted_array.sort(reverse=True)
        self.fts_msg_sort = sorted_array
        logger.info(f"生成FTSMSG库排序缓存：{self.fts_msg_sort}")
        return sorted_array
