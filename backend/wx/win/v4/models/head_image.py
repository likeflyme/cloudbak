from sqlalchemy import Column, Integer, String, LargeBinary

from wx.win.v4.db.windows_v4_db import Base


class HeadImageModel(Base):
    __tablename__ = 'head_image'

    username = Column(Integer, primary_key=True)
    md5 = Column(String)
    image_buffer = Column(LargeBinary)
    update_time = Column(Integer)
