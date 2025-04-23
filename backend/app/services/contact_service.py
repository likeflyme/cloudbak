from app.schemas import schemas
from wx.win.v3.models.micro_msg import Contact, ContactHeadImgUrl
from app.schemas.schemas import Session


def select_contact(micro_db: Session, wxId: str) -> schemas.ContactWithHeadImg:
    contact = micro_db.query(Contact).filter_by(UserName=wxId).first()
    if contact:
        data = schemas.ContactWithHeadImg(**contact.__dict__)
        if contact.head_img_url:
            data.smallHeadImgUrl = contact.head_img_url.smallHeadImgUrl
            data.bigHeadImgUrl = contact.head_img_url.bigHeadImgUrl
        return data
    img = micro_db.query(ContactHeadImgUrl).filter_by(usrName=wxId).first()
    if img:
        if img.contact:
            data = schemas.ContactWithHeadImg(**img.contact.__dict__)
            data.smallHeadImgUrl = img.smallHeadImgUrl
            data.bigHeadImgUrl = img.bigHeadImgUrl
        else:
            data = schemas.ContactWithHeadImg(**img.__dict__)
        return data
