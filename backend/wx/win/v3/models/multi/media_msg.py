from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class Media(Base):
    __tablename__ = "Media"
    __table_args__ = {'extend_existing': True}

    Key = Column(String, primary_key=True)
    Reserved0 = Column(Integer)
    Buf = Column(LargeBinary)
    Reserved1 = Column(Integer)
    Reserved2 = Column(String)


