from typing import List

from sqlalchemy import select

from wx.common.filters.session_filter import SessionFilterObj
from wx.common.output.session import Session
from wx.interface.wx_interface import SessionManager, ClientInterface
from wx.win.v4.db.windows_v4_db import WindowsV4DB
from wx.win.v4.enums.v4_enums import V4DBEnum
from wx.win.v4.models.session_model import SessionModelV4


class SessionManagerWindowsV4(SessionManager):

    def __init__(self, client: ClientInterface):
        self.client = client

    def sessions_page(self, filter_obj: SessionFilterObj) -> List[Session]:
        stmt = (
            select(SessionModelV4)
            .where(SessionModelV4.username.notlike("@%"))
            .where(SessionModelV4.username.notlike("gh_%"))
            .order_by(SessionModelV4.sort_timestamp.desc())
            .offset((filter_obj.page - 1) * filter_obj.size)
            .limit(filter_obj.size)
        )
        sm = self.client.get_db_manager().wx_db(V4DBEnum.SESSION_DB_PATH)
        with sm() as db:
            results = db.execute(stmt).scalars().fetchall()
            return [
                Session(
                    username=session.username,
                    type=session.type,
                    summary=session.summary,
                    modify_timestamp=session.last_timestamp
                )
                for session in results
            ]

    def session(self, username: str) -> Session:
        pass
