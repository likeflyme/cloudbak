from sqlalchemy import Column, String, Integer, LargeBinary

from wx.win.v4.db.windows_v4_db import Base


class VideoHardlinkInfoModel(Base):
    __tablename__ = 'video_hardlink_info_v3'

    md5_hash = Column(Integer, primary_key=True)
    md5 = Column(String)
    type = Column(Integer)
    file_name = Column(String)
    file_size = Column(Integer)
    modify_time = Column(Integer)
    dir1 = Column(Integer)
    dir2 = Column(Integer)
    _rowid_ = Column(Integer)
    extra_buffer = Column(LargeBinary)


class Dir2IdModel(Base):
    __tablename__ = "dir2id"

    username = Column(String, primary_key=True)
