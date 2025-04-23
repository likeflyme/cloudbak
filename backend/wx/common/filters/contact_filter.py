from typing import Optional

from pydantic import BaseModel

from wx.common.enum.contact_type import ContactType


class ContactFilterObj(BaseModel):
    search: Optional[str] = None
    page: int = 1
    size: int = 20
    contact_type: Optional[ContactType] = ContactType.NORMAL
