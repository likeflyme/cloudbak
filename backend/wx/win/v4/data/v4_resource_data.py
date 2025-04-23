import os.path

from sqlalchemy import select, func

from config.log_config import logger
from wx.interface.wx_interface import ResourceManager, ClientInterface
from wx.win.v4.enums.v4_enums import V4DBEnum
from wx.win.v4.models.hardlink import Dir2IdModel, VideoHardlinkInfoModel
from wx.win.v4.models.head_image import HeadImageModel


class WindowsV4ResourceManager(ResourceManager):

    def __init__(self, client: ClientInterface):
        self.client = client

    def windows_v3_image_from_full_md5(self, full_md5: str, prev: str = 'Thumb'):
        pass

    def get_decode_media_path(self) -> str:
        pass

    def get_media_path(self, username: str, win_v3_msg_svr_id: str) -> str | None:
        pass

    def get_wx_owner_img(self) -> str:
        wx_id = self.client.get_sys_session().wx_id
        logger.info(f"获取头像 {wx_id}")
        relative_path = os.path.join(wx_id, V4DBEnum.HEAD_IMAGE_FOLDER, f"{wx_id}.jpg")
        image_path = os.path.join(self.client.get_wx_dir(), V4DBEnum.HEAD_IMAGE_FOLDER, f"{wx_id}.jpg")
        logger.info(f"头像路径")
        if os.path.exists(image_path):
            logger.info("存在，返回")
            return relative_path
        logger.info("不存在，生成")
        sm = self.client.get_db_manager().wx_db(V4DBEnum.HEAD_IMAGE_DB_PATH)
        with sm() as db:
            real_wx_id = self.client.get_real_wx_id()
            head = db.query(HeadImageModel).filter_by(username=real_wx_id).first()
            if head:
                logger.info("head_image库中存在数据")
                folder = os.path.join(self.client.get_wx_dir(), V4DBEnum.HEAD_IMAGE_FOLDER)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                try:
                    logger.info(f"写入头像 {image_path}")
                    with open(image_path, 'wb') as f:
                        f.write(head.image_buffer)
                    return relative_path
                except Exception as e:
                    logger.error('保存头像错误', e)
        logger.info("head_image库中不存在数据")
        return None

    def get_video_poster(self, md5: str) -> str | None:
        sm = self.client.get_db_manager().wx_db(V4DBEnum.HARDLINK_DB_PATH)
        dir2id_subquery = (
            select(
                func.row_number().over(order_by=None).label("row_num"),
                Dir2IdModel.username
            ).subquery("b")
        )
        stmt = (
            select(VideoHardlinkInfoModel, dir2id_subquery)
            .join(dir2id_subquery, VideoHardlinkInfoModel.dir1 == dir2id_subquery.c.row_num, isouter=True)
            .where(VideoHardlinkInfoModel.md5.is_(md5))
        )
        with sm() as db:
            row = db.execute(stmt).first()
            if not row:
                return None
            logger.info(f"hardlink data: {row}")
            hardlink = row[0]
            # row_num = row[1]
            dir_name = row[2]
            name, ext = hardlink.file_name.rsplit('.', 1)
            return f"{self.client.get_wx_dir()}/msg/video/{dir_name}/{name}_thumb.jpg"

    def get_video(self, md5: str) -> str | None:
        sm = self.client.get_db_manager().wx_db(V4DBEnum.HARDLINK_DB_PATH)
        dir2id_subquery = (
            select(
                func.row_number().over(order_by=None).label("row_num"),
                Dir2IdModel.username
            ).subquery("b")
        )
        stmt = (
            select(VideoHardlinkInfoModel, dir2id_subquery)
            .join(dir2id_subquery, VideoHardlinkInfoModel.dir1 == dir2id_subquery.c.row_num, isouter=True)
            .where(VideoHardlinkInfoModel.md5.is_(md5))
        )
        with sm() as db:
            row = db.execute(stmt).first()
            if not row:
                return None
            logger.info(f"hardlink data: {row}")
            hardlink = row[0]
            # row_num = row[1]
            dir_name = row[2]
            return f"{self.client.get_wx_dir()}/msg/video/{dir_name}/{hardlink.file_name}"

    def get_member_head(self, username: str) -> bytearray:
        pass
