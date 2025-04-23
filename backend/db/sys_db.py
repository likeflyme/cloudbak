import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.app_config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

sys_db_path = os.path.join(settings.sys_dir, settings.sys_db_dir)
if not os.path.exists(sys_db_path):
    os.makedirs(sys_db_path)
sys_db_file_path = os.path.join(str(sys_db_path), settings.sys_db_file_name)
engine = create_engine(f"sqlite:///{sys_db_file_path}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    my_db = SessionLocal()
    try:
        yield my_db
    finally:
        my_db.close()


def get_sys_db():
    return SessionLocal()


def clear_all():
    session = SessionLocal()
    session.close()  # 关闭会话
    engine.dispose()
