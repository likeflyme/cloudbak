from collections import defaultdict
from typing import List

from sqlalchemy import select, or_

from config.log_config import logger
from wx.common.enum.contact_type import ContactType
from wx.common.filters.contact_filter import ContactFilterObj
from wx.common.output.chat_room import ChatRoom
from wx.win.v3.enums.v3_enums import V3DBEnum
from wx.win.v3.models import micro_msg
from wx.win.v3.models.micro_msg import Contact as ContactModel, ContactHeadImgUrl
from wx.common.output.contact import Contact, ContactSearchOut
from wx.interface.wx_interface import ContactManager
from wx.win.v3.db.windows_v3_db import WindowsV3DB
from wx.win.v3.models.openim_contact import OpenIMContact
from wx.win.v3.models.public_msg import PublicNameToID as Name2IDGH


class ContactManagerWindowsV3(ContactManager):

    def __init__(self, db_manager: WindowsV3DB):
        self.db_manager = db_manager
        self.contact_type_dict = defaultdict(lambda: None)

    def clear(self):
        self.contact_type_dict.clear()

    def contacts(self, filter_obj: ContactFilterObj = None) -> List[Contact]:
        stmt = (
            select(ContactModel, ContactHeadImgUrl)
            .join(
                ContactHeadImgUrl,
                ContactHeadImgUrl.usrName == ContactModel.UserName,
                isouter=True
            ).order_by(ContactModel.NickName.asc())
        )
        if filter_obj is not None:
            logger.info("add limit offset")
            stmt = stmt.limit(filter_obj.size).offset((filter_obj.page - 1) * filter_obj.size)
            if filter_obj.contact_type is not None:
                if filter_obj.contact_type == ContactType.CHATROOM:
                    stmt = stmt.where(ContactModel.Type.is_("2"), ContactModel.NickName.isnot(''))
                else:
                    stmt = stmt.where(ContactModel.Type.not_in([2, 4]))
            if filter_obj.search is not None and filter_obj.search != '':
                stmt = stmt.where(or_(
                    ContactModel.NickName.like(f"%{filter_obj.search}%"),
                    ContactModel.Remark.like(f"%{filter_obj.search}%")
                ))
        logger.info(f"query: {stmt}")
        with self.db_manager.wx_db_micro_msg() as db:
            results = db.execute(stmt).fetchall()
            contacts = [
                Contact(
                    username=contact.UserName,
                    alias=contact.Alias,
                    remark=contact.Remark,
                    remark_quanpin=contact.RemarkQuanPin,
                    remark_quanpin_initial=contact.RemarkPYInitial,
                    nickname=contact.NickName,
                    nickname_quanpin=contact.QuanPin,
                    nickname_quanpin_initial=contact.PYInitial,
                    small_head_url=img.smallHeadImgUrl if img else None,
                    # big_head_url=img.bigHeadImgUrl
                )
                for contact, img in results
            ]
        if filter_obj is None:
            openim_session_maker = self.db_manager.wx_db_for_conf(V3DBEnum.DB_OPENIM_CONTACT)
            with openim_session_maker() as openim_db:
                # 查询openIM联系人
                results = openim_db.query(OpenIMContact).all()
                for contact in results:
                    contacts.append(Contact(
                        username=contact.UserName,
                        remark=contact.Remark,
                        nickname=contact.NickName,
                        small_head_url=contact.SmallHeadImgUrl,
                        # bigHeadImgUrl=contact.BigHeadImgUrl)
                    ))
        return contacts

    def contacts_search(self, filter_obj: ContactFilterObj) -> ContactSearchOut:
        search = filter_obj.search
        base_stmt = (
            select(ContactModel)
            .where(or_(
                ContactModel.NickName.like(f"%{search}%"),
                ContactModel.Remark.like(f"%{search}%")
            ))
            .where(ContactModel.Type.not_in([2, 4]))
        )

        contact_stmt = base_stmt.where(ContactModel.UserName.notlike("%@chatroom"))

        chatroom_stmt = base_stmt.where(ContactModel.UserName.like("%@chatroom"))

        with self.db_manager.wx_db_micro_msg() as db:
            contact_result = db.execute(contact_stmt).scalars().all()
            logger.info(f"query: {contact_stmt}")
            chatroom_result = db.execute(chatroom_stmt).scalars().all()
            return ContactSearchOut(
                contacts=[
                    Contact(
                        username=contact.UserName,
                    )
                    for contact in contact_result
                ],
                chatrooms=[
                    ChatRoom(
                        username=contact.UserName,
                    )
                    for contact in chatroom_result
                ]
            )

    def contact_type(self, username: str) -> ContactType:
        if username in self.contact_type_dict:
            return self.contact_type_dict[username]

        session_maker = self.db_manager.wx_db_for_conf(V3DBEnum.DB_PUBLIC_MSG)
        with session_maker() as pb_db:
            name = pb_db.query(Name2IDGH).filter_by(UsrName=username).first()
            if name is not None:
                self.contact_type_dict[username] = ContactType.GH
                return ContactType.GH

        session_maker = self.db_manager.wx_db_for_conf(V3DBEnum.DB_OPENIM_CONTACT)
        with session_maker() as im_db:
            name = im_db.query(OpenIMContact).filter_by(UserName=username).first()
            if name is not None:
                self.contact_type_dict[username] = ContactType.OPENIM
                return ContactType.OPENIM

        self.contact_type_dict[username] = ContactType.NORMAL
        return ContactType.NORMAL

    def base_contacts(self) -> List[Contact]:
        stmt = (
            select(ContactModel, ContactHeadImgUrl)
            .join(
                ContactHeadImgUrl,
                ContactHeadImgUrl.usrName == ContactModel.UserName,
                isouter=True
            )
            .where(ContactModel.Type.is_not(4))  # 4为陌生人
            .order_by(ContactModel.NickName.asc())
        )
        with self.db_manager.wx_db_micro_msg() as db:
            results = db.execute(stmt).fetchall()
            contacts = [
                Contact(
                    username=contact.UserName,
                    alias=contact.Alias,
                    remark=contact.Remark,
                    remark_quanpin=contact.RemarkQuanPin,
                    remark_quanpin_initial=contact.RemarkPYInitial,
                    nickname=contact.NickName,
                    nickname_quanpin=contact.QuanPin,
                    nickname_quanpin_initial=contact.PYInitial,
                    small_head_url=img.smallHeadImgUrl if img else None,
                    # big_head_url=img.bigHeadImgUrl
                )
                for contact, img in results
            ]

        openim_session_maker = self.db_manager.wx_db_for_conf(V3DBEnum.DB_OPENIM_CONTACT)
        with openim_session_maker() as openim_db:
            # 查询openIM联系人
            results = openim_db.query(OpenIMContact).all()
            for contact in results:
                contacts.append(Contact(
                    username=contact.UserName,
                    remark=contact.Remark,
                    nickname=contact.NickName,
                    small_head_url=contact.SmallHeadImgUrl
                ))

        return contacts
