from typing import List

from sqlalchemy import select

from wx.common.filters.session_filter import SessionFilterObj
from wx.common.output.session import Session
from wx.interface.wx_interface import SessionManager
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.models.micro_msg import Session as SessionModel


class SessionManagerWindowsV3(SessionManager):

    def __init__(self, db_manager: WindowsV3DB):
        self.db_manager = db_manager

    def sessions_page(self, filter_obj: SessionFilterObj) -> List[Session]:
        stmt = (
            select(SessionModel)
            .where(SessionModel.strUsrName.notlike("@%"))
            .where(SessionModel.strUsrName.notlike("%@openim"))
            .where(SessionModel.strUsrName.notlike("gh_%"))
            .order_by(SessionModel.nOrder.desc())
            .offset((filter_obj.page - 1) * filter_obj.size)
            .limit(filter_obj.size)
        )
        if not filter_obj.gh:
            stmt.where(SessionModel.strUsrName.notlike("gh_%"))
        if not filter_obj.openim:
            stmt.where(SessionModel.strUsrName.notlike("%@openim"))
        if not filter_obj.chatroom:
            stmt.where(SessionModel.strUsrName.notlike("%@chatroom"))
        if not filter_obj.filehelper:
            stmt.where(SessionModel.strUsrName.notlike("%@filehelper"))
        with self.db_manager.wx_db_micro_msg() as db:
            results = db.execute(stmt).scalars().all()
            return [
                Session(
                    username=db_session.strUsrName,
                    summary=db_session.strContent,
                    modify_timestamp=db_session.nTime
                )
                for db_session in results
            ]
