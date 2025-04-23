from sqlalchemy import Column, Integer, String, LargeBinary

from db.wx_db import Base


class Config(Base):
    __tablename__ = "Config"
    __table_args__ = {'extend_existing': True}

    Key = Column(String, primary_key=True)
    Reserved0 = Column(Integer)
    Buf = Column(LargeBinary)
    Reserved1 = Column(Integer)
    Reserved2 = Column(String)


class FavItems(Base):
    __tablename__ = "FavItems"
    __table_args__ = {'extend_existing': True}

    FavLocalID = Column(Integer, primary_key=True)
    SvrFavId = Column(Integer)
    Type = Column(Integer)
    ServerSeq = Column(Integer)
    LocalStatus = Column(Integer)
    Flag = Column(Integer)
    FromUser = Column(String)
    RealChatName = Column(String)
    SourceId = Column(String)
    LocalSeq = Column(Integer)
    SearchKey = Column(String)
    UpdateTime = Column(Integer)
    Status = Column(Integer)
    SourceType = Column(Integer)
    Reserved0 = Column(Integer)
    Reserved1 = Column(Integer)
    Reserved2 = Column(Integer)
    Reserved3 = Column(Integer)
    Reserved4 = Column(String)
    Reserved5 = Column(String)
    Reserved6 = Column(String)
    XmlBuf = Column(String)


class FavDataItem(Base):
    __tablename__ = "FavDataItem"
    __table_args__ = {'extend_existing': True}

    RecId = Column(Integer, primary_key=True)
    FavLocalID = Column(Integer)
    Type = Column(Integer)
    DataId = Column(String)
    HtmlId = Column(String)
    Datasourceid = Column(String)
    Datastatus = Column(Integer)
    Datafmt = Column(String)
    Datatitle = Column(String)
    Datadesc = Column(String)
    Thumbfullmd5 = Column(String)
    Thumbhead256md5 = Column(String)
    Thumbfullsize = Column(Integer)
    fullmd5 = Column(String)
    head256md5 = Column(String)
    fullsize = Column(Integer)
    cdn_thumburl = Column(String)
    cdn_thumbkey = Column(String)
    thumb_width = Column(Integer)
    thumb_height = Column(Integer)
    cdn_dataurl = Column(String)
    cdn_datakey = Column(String)
    cdn_encryver = Column(Integer)
    duration = Column(String)
    stream_weburl = Column(String)
    stream_dataurl = Column(String)
    stream_lowbandurl = Column(String)
    sourcethumbpath = Column(String)
    sourcedatapath = Column(String)
    stream_videoid = Column(String)
    Rerserved1 = Column(Integer)
    Rerserved2 = Column(Integer)
    Rerserved3 = Column(Integer)
    Rerserved4 = Column(String)
    Rerserved5 = Column(String)
    Rerserved6 = Column(String)
    Rerserved7 = Column(LargeBinary)
