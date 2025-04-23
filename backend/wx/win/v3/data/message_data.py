import os.path
from datetime import datetime, timedelta

from sqlalchemy import select, and_, or_, func, literal_column

from app.enum.msg_enum import FilterMode
from config.log_config import logger
from wx.common.enum.contact_type import ContactType
from wx.common.filters.msg_filter import MsgFilterObj, SingleMsgFilterObj
from wx.common.output.message import MsgSearchOut, Msg, WindowsV3Properties
from wx.common.util.contact_utils import ContactUtils
from wx.interface.wx_interface import MessageManager, ClientInterface
from wx.win.v3.enums.v3_enums import V3DBEnum
from wx.win.v3.models.multi.msg import Msg as MsgModel, Name2ID
from wx.win.v3.models.openim_msg import Name2ID as OpenIMName2ID
from wx.win.v3.models.openim_msg import Msg as OpenIMMsgModel
from wx.win.v3.models.public_msg import Msg as PublicMsgModel, PublicNameToID
from wx.win.v3.util.msg_utils import MsgUtils


class MessageManagerWindowsV3(MessageManager):

    def __init__(self, client: ClientInterface):
        self.client = client

    def messages_filter_page(self, filter_obj: MsgFilterObj) -> MsgSearchOut:
        """
        通用消息分页查询
        """
        contact_type = ContactUtils.contact_type(filter_obj.username)
        if contact_type == ContactType.OPENIM:
            return self.message_filter_for_openim(filter_obj)
        elif contact_type == ContactType.GH:
            return self.message_filter_for_gh(filter_obj)
        else:
            return self.message_filter(filter_obj)

    def message_filter_for_openim(self, filter_obj: MsgFilterObj) -> MsgSearchOut:
        talker_id_subq = (
            select(literal_column("rowid").label("TalkerId"))
            .select_from(OpenIMName2ID)
            .where(OpenIMName2ID.UsrName == filter_obj.username)
            .limit(1)
            .scalar_subquery()
        )
        stmt = (
            select(OpenIMMsgModel)
            .where(OpenIMMsgModel.talkerId == talker_id_subq)
            .order_by(OpenIMMsgModel.sequence.desc())
            .offset((filter_obj.page - 1) * filter_obj.size + filter_obj.start).limit(filter_obj.size)
        )
        logger.info(f"query sql: {stmt}")
        session_maker = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_OPENIM_MSG)
        with session_maker() as openimmsg_db:
            msgs = openimmsg_db.execute(stmt).scalars().all()
        results = []
        for m in msgs:
            # openim_msg.Msg 转 msg.Msg
            normal_msg = MsgModel(localId=m.localId, TalkerId=m.talkerId, MsgSvrID=m.MsgSvrID, Type=m.type,
                                 IsSender=m.IsSender, CreateTime=m.CreateTime, Sequence=m.sequence,
                                 StatusEx=m.StatusEx,
                                 FlagEx=m.FlagEx, Status=m.Status, StrTalker=m.strTalker, StrContent=m.StrContent,
                                 BytesExtra=m.BytesExtra, BytesTrans=m.BytesTrans)

            msg = self.parse_msg(normal_msg)
            results.append(msg)
        return MsgSearchOut(start=0, messages=results)

    def message_filter_for_gh(self, filter_obj: MsgFilterObj) -> MsgSearchOut:

        talker_id_subq = (
            select(literal_column("rowid").label("TalkerId"))
            .select_from(PublicNameToID)
            .where(PublicNameToID.UsrName == filter_obj.username)
            .limit(1)
            .scalar_subquery()
        )

        # 第二步：查询消息
        stmt = (
            select(PublicMsgModel)
            .where(PublicMsgModel.TalkerId == talker_id_subq)
            .order_by(PublicMsgModel.Sequence.desc())
            .offset((filter_obj.page - 1) * filter_obj.size + filter_obj.start)
            .limit(filter_obj.size)
        )
        logger.info(f"query sql: {stmt}")
        session_maker = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_PUBLIC_MSG)
        with session_maker() as pb_db:
            msgs = pb_db.execute(stmt).scalars().all()
            results = []
            for m in msgs:
                msg = self.parse_msg(m)
                results.append(msg)
            return MsgSearchOut(start=0, messages=results)

    def message_filter(self, filter_obj: MsgFilterObj) -> MsgSearchOut:
        db_array = self.client.get_db_order_manager().msg_db_array()  # 降序排序的数组，对应的查询模式为由近到远，filterModel = 0
        if filter_obj.filter_mode == FilterMode.ASC:
            # 由远到近的排序模式，使用 sorted 函数避免改变原数组结构
            db_array = sorted(db_array, key=str.lower)
        logger.info(f"排序模式为：{filter_obj.filter_mode}")
        logger.info(f"库排序为：{db_array}")
        left = filter_obj.size  # 待查询数据剩余数量
        offset = filter_obj.start
        if offset is None:
            offset = 0
        db_start = False  # 查询是否开始标志，用于跳过不需要查询的库
        current_db_name = filter_obj.start_db  # 当前库
        msgs = []
        for db_name in db_array:
            logger.info(f"需要查询的数据量为：{left}")
            if left == 0:
                current_db_name = db_name
                break
            if not db_start:
                if filter_obj.start_db is None or filter_obj.start_db == '':
                    db_start = True
                elif filter_obj.start_db == db_name:
                    db_start = True
            if not db_start:
                logger.info(f"跳过库：{db_name}")
                continue
            current_db_name = db_name
            logger.info(f"查询库：{db_name}")
            limit = left
            logger.info(f"offset:{offset}, limit: {limit}")
            talker_id_subq = (
                select(literal_column("rowid").label("TalkerId"))
                .select_from(Name2ID)
                .where(Name2ID.UsrName == filter_obj.username)
                .limit(1)
                .scalar_subquery()
            )
            stmt = (
                select(MsgModel)
                .where(MsgModel.TalkerId == talker_id_subq)
                .offset(offset)
                .limit(limit)
            )
            # 根据查询模式确定排序方向
            if filter_obj.filter_mode == FilterMode.DESC:
                stmt = stmt.order_by(MsgModel.Sequence.desc())
            else:
                stmt = stmt.order_by(MsgModel.Sequence.asc())
            # 组装查询条件
            # 序列号分割
            if filter_obj.filter_sequence:
                if filter_obj.filter_mode == FilterMode.DESC:
                    stmt = stmt.where(MsgModel.Sequence <= filter_obj.filter_sequence)
                else:
                    stmt = stmt.where(MsgModel.Sequence > filter_obj.filter_sequence)
            # 日期
            if filter_obj.filter_day:
                # 将 yyyyMMdd 转换为 datetime 对象
                date = datetime.strptime(filter_obj.filter_day, "%Y%m%d")
                # 当天开始时间
                start_of_day = datetime(date.year, date.month, date.day)
                # 当天结束时间（23:59:59）
                end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)

                # 转换为时间戳（秒级）
                end_timestamp = int(end_of_day.timestamp())
                logger.info(f"时间戳: {end_timestamp}")
                if filter_obj.filter_mode == FilterMode.DESC:
                    stmt = stmt.where(MsgModel.CreateTime <= end_timestamp)
                else:
                    stmt = stmt.where(MsgModel.CreateTime > end_timestamp)
            # 图片视频
            if filter_obj.filter_media:
                stmt = stmt.where(or_(
                    and_(MsgModel.Type == '3', MsgModel.SubType == '0'),
                    and_(MsgModel.Type == '43', MsgModel.SubType == '0')
                ))
            # 文字
            if filter_obj.filter_text:
                stmt = stmt.where(MsgModel.StrContent.contains(filter_obj.filter_text))
            # 文件
            if filter_obj.filter_file:
                stmt = stmt.where(and_(MsgModel.Type == '49', MsgModel.SubType == '6'))
            session_local = self.client.get_db_manager().wx_db_msg_by_name(current_db_name)
            if session_local is None:
                continue
            with session_local() as db:
                logger.info(f"query sql: {stmt}")
                results = db.execute(stmt).scalars().all()
                for m in results:
                    msg = self.parse_msg(m)
                    msgs.append(msg)
                data_count = len(results)
                logger.info(f"预期 {limit}, 实际 {data_count}")
                filter_obj.start = offset + limit
                offset = 0
                if data_count >= limit:
                    logger.info("查询到足够数据，结束")
                    break
                left = left - data_count
                logger.info(f"未查询到足够数据，剩余查询数量：{left}，跨库查询")
        logger.info(f"current_db_name: {current_db_name}")
        return MsgSearchOut(start=filter_obj.start, start_db=current_db_name, messages=msgs)

    def parse_msg(self, db_msg) -> Msg:
        windows_v3_properties = WindowsV3Properties(**db_msg.__dict__)
        windows_v3_properties.MsgSvrIDStr = str(db_msg.MsgSvrID)

        sender, thumb, source = MsgUtils.parse_sender_thumb_source(db_msg)
        # 发送者微信号
        if sender is None:
            sender = self.client.get_sys_session().wx_id
        windows_v3_properties.sender = sender
        windows_v3_properties.thumb = thumb
        windows_v3_properties.source = source

        if db_msg.CompressContent:
            compress_content = MsgUtils.parse_compress_content(db_msg.CompressContent)
            windows_v3_properties.compress_content = compress_content

        return Msg(windows_v3_properties=windows_v3_properties)

    def message(self, filter_obj: SingleMsgFilterObj) -> Msg | None:
        """
        单条消息查询
        """
        db_array = self.client.get_db_order_manager().msg_db_array()
        for db_name in db_array:
            session_local = self.client.get_db_manager().wx_db_msg_by_name(db_name)
            with session_local() as db:
                db_msg = db.query(MsgModel).filter_by(MsgSvrID=filter_obj.v3_msg_svr_id).first()
                logger.info(f"db_msg = {db_msg}")
                if db_msg:
                    return self.parse_msg(db_msg)
        # openim 库中查询
        openimdb = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_OPENIM_MSG)
        with openimdb() as db:
            m = db.query(OpenIMMsgModel).filter_by(MsgSvrID=filter_obj.v3_msg_svr_id).first()
            # openim_msg.Msg 转 msg.Msg
            msg = MsgModel(localId=m.localId, TalkerId=m.talkerId, MsgSvrID=m.MsgSvrID, Type=m.type,
                             IsSender=m.IsSender, CreateTime=m.CreateTime, Sequence=m.sequence, StatusEx=m.StatusEx,
                             FlagEx=m.FlagEx, Status=m.Status, StrTalker=m.strTalker, StrContent=m.StrContent,
                             BytesExtra=m.BytesExtra, BytesTrans=m.BytesTrans)
            logger.info(f"msg = {msg}")
            return self.parse_msg(msg)

