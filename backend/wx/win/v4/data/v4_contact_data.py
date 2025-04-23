from collections import defaultdict
from typing import List

from sqlalchemy import select, or_

from wx.common.enum.contact_type import ContactType
from wx.common.filters.contact_filter import ContactFilterObj
from wx.common.output.contact import Contact, ContactSearchOut

from wx.interface.wx_interface import ContactManager, ClientInterface
from wx.win.v4.db.windows_v4_db import WindowsV4DB
from wx.win.v4.enums.v4_enums import V4DBEnum
from wx.win.v4.models.contact import ContactModelV4
from config.log_config import logger


class ContactManagerWindowsV4(ContactManager):

    def __init__(self, client: ClientInterface):
        self.client = client
        self.contact_type_dict = defaultdict(lambda: None)

    def clear(self):
        self.contact_type_dict.clear()

    def contacts(self, filter_obj: ContactFilterObj = None) -> List[Contact]:
        stmt = (select(ContactModelV4).order_by(ContactModelV4.nick_name.asc()))
        if filter_obj is not None:
            stmt = stmt.limit(filter_obj.size).offset((filter_obj.page - 1)*filter_obj.size)
            if filter_obj.contact_type:
                if filter_obj.contact_type == ContactType.CHATROOM:
                    stmt = stmt.where(ContactModelV4.local_type.is_(2))
                else:
                    stmt = stmt.where(ContactModelV4.local_type.is_(1))
            if filter_obj.search and filter_obj.search != "":
                stmt = stmt.where(
                    or_(ContactModelV4.nick_name.like(f"%{filter_obj.search}%"), ContactModelV4.remark.like(f"%{filter_obj.search}%"))
                )
        sm = self.client.get_db_manager().wx_db(V4DBEnum.CONTACT_DB_PATH)
        with sm() as db:
            results = db.execute(stmt).scalars().fetchall()
            return [
                Contact(
                    username=contact.username,
                    alias=contact.alias,
                    remark=contact.remark,
                    remark_quanpin=contact.remark_quan_pin,
                    nickname=contact.nick_name,
                    nickname_quanpin=contact.quan_pin,
                    nickname_quanpin_initial=contact.pin_yin_initial,
                    small_head_url=contact.small_head_url
                )
                for contact in results
            ]

    def contacts_search(self, filter_obj: ContactFilterObj = ContactFilterObj) -> ContactSearchOut:
        stmt = (select(ContactModelV4).order_by(ContactModelV4.nick_name.asc()))
        stmt = stmt.limit(filter_obj.size).offset((filter_obj.page - 1) * filter_obj.size)
        if filter_obj.contact_type:
            if filter_obj.contact_type == ContactType.CHATROOM:
                stmt = stmt.where(ContactModelV4.local_type.is_(2))
            else:
                stmt = stmt.where(ContactModelV4.local_type.is_(1))
        if filter_obj.search and filter_obj.search != "":
            stmt = stmt.where(
                or_(ContactModelV4.nick_name.like(f"%{filter_obj.search}%"),
                    ContactModelV4.remark.like(f"%{filter_obj.search}%"))
            )
        sm = self.client.get_db_manager().wx_db(V4DBEnum.CONTACT_DB_PATH)
        with sm() as db:
            results = db.execute(stmt).scalars().fetchall()
            return [
                Contact(
                    username=contact.username,
                    alias=contact.alias,
                    remark=contact.remark,
                    remark_quanpin=contact.remark_quan_pin,
                    nickname=contact.nick_name,
                    nickname_quanpin=contact.quan_pin,
                    nickname_quanpin_initial=contact.pin_yin_initial,
                    small_head_url=contact.small_head_url
                )
                for contact in results
            ]

    def contact_type(self, username: str) -> ContactType:
        pass

    def base_contacts(self) -> List[Contact]:
        stmt = (
            select(
                ContactModelV4.username,
                ContactModelV4.alias,
                ContactModelV4.remark,
                ContactModelV4.remark_quan_pin,
                ContactModelV4.nick_name,
                ContactModelV4.quan_pin,
                ContactModelV4.pin_yin_initial,
                ContactModelV4.small_head_url
            )
            .where(ContactModelV4.local_type.is_not(3))  # 3 为陌生人
            .order_by(ContactModelV4.nick_name.asc())
        )
        logger.info(f"sql: {stmt}")
        sm = self.client.get_db_manager().wx_db(V4DBEnum.CONTACT_DB_PATH)
        with sm() as db:
            results = db.execute(stmt).fetchall()
            contacts = []
            for contact in results:
                try:
                    contacts.append(
                        Contact(
                            username=contact.username,
                            alias=contact.alias,
                            remark=contact.remark,
                            remark_quanpin=contact.remark_quan_pin,
                            nickname=contact.nick_name,
                            nickname_quanpin=contact.quan_pin,
                            nickname_quanpin_initial=contact.pin_yin_initial,
                            small_head_url=contact.small_head_url.encode("latin1").decode("utf-8", "ignore")
                        )
                    )
                except UnicodeDecodeError:
                    logger.warning(f"Skipping contact {contact.username} due to encoding issue")
            return contacts
