import os

from sqlalchemy import select
from sqlalchemy.orm import aliased

from config.log_config import logger
from wx.common.enum.contact_type import ContactType
from wx.interface.wx_interface import ResourceManager, ClientInterface
from wx.win.v3.enums.v3_enums import V3DBEnum
from wx.win.v3.models.hard_link_image import HardLinkImageID, HardLinkImageAttribute
from wx.win.v3.models.micro_msg import ContactHeadImgUrl
from wx.win.v3.models.misc import ContactHeadImg
from wx.win.v3.models.multi.media_msg import Media
from wx.win.v3.models.openim_media import Media as OpenIMMedia
from wx.win.v3.util.media_util import MediaUtils


class WindowsV3ResourceManager(ResourceManager):

    def __init__(self, client: ClientInterface):
        self.client = client

    def windows_v3_image_from_full_md5(self, full_md5: str, prev: str = 'Thumb'):
        HardLinkImageID2 = aliased(HardLinkImageID)

        # 构建查询
        query = (
            select(
                HardLinkImageAttribute.Md5Hash,
                HardLinkImageAttribute.MD5,
                HardLinkImageAttribute.FileName,
                HardLinkImageID.Dir.label("dirName1"),
                HardLinkImageID2.Dir.label("dirName2"),
            )
            .join(HardLinkImageID, HardLinkImageAttribute.DirID1 == HardLinkImageID.DirID)
            .join(HardLinkImageID2, HardLinkImageAttribute.DirID2 == HardLinkImageID2.DirID)
            .where(HardLinkImageAttribute.FileName.like(f"%{full_md5}%"))
        )

        session_maker = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_HARD_LINK_IMAGE)
        with session_maker() as image_db:
            # 执行查询，最多只有一个结果
            row = image_db.execute(query).first()
            if row is None:
                return None
            # 处理查询结果
            relative_path = f'FileStorage/MsgAttach/{row.dirName1}/{prev}/{row.dirName2}/{row.FileName}'
            logger.info(f'path: {relative_path}')

        wx_dir = self.client.get_wx_dir()

        file_path = os.path.join(wx_dir, relative_path)
        return file_path

    def get_decode_media_path(self) -> str:
        return os.path.join(self.client.get_wx_dir(), V3DBEnum.DECODED_MEDIA_PATH).__str__()

    def get_media_path(self, username: str, win_v3_msg_svr_id: str) -> str | None:
        media_folder = os.path.join(self.client.get_wx_dir(), V3DBEnum.DECODED_MEDIA_PATH).__str__()
        mp3_name = os.path.join(media_folder, f"{win_v3_msg_svr_id}.mp3")
        logger.info(f"mp3: {mp3_name}")
        if os.path.exists(mp3_name):
            logger.info("存在，直接返回该数据")
            return mp3_name
        logger.info("不存在，临时生成")
        # 需要判断是否是openim消息
        ctp = self.client.get_contact_manager().contact_type(username)
        if ctp == ContactType.OPENIM:
            # openim 查询OpenIMContact
            sm = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_OPENIM_MEDIA)
            with sm() as db:
                media = db.query(OpenIMMedia).filter_by(Reserved0=win_v3_msg_svr_id).first()
                logger.info(f"{media}")
                if media and media.Buf:
                    logger.info("查询到 media，准备生成 mp3 文件")
                    try:
                        mp3_name = MediaUtils.decode_media(media_folder, win_v3_msg_svr_id, media.Buf)
                        return mp3_name
                    except Exception as e:
                        logger.error(e)
                        return None
        db_array = self.client.get_db_order_manager().media_msg_db_array()
        for filename in db_array:
            session_local = self.client.get_db_manager().wx_db_media_msg_by_filename(filename)
            with session_local() as media_db:
                media = media_db.query(Media).filter_by(Reserved0=win_v3_msg_svr_id).first()
                logger.info(f"{media}")
                if media and media.Buf:
                    logger.info("查询到 media，准备生成 mp3 文件")
                    mp3_name = MediaUtils.decode_media(media_folder, win_v3_msg_svr_id, media.Buf)
                    logger.info(f"生成成功，{mp3_name}")
                    return mp3_name

    def get_wx_owner_img(self) -> str:
        # 存在微信库文件则查询微信用户头像信息
        try:
            sm = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_MICRO_MSG)
            with sm() as micro_db:
                head_img = micro_db.query(ContactHeadImgUrl).filter_by(usrName=self.client.get_sys_session().wx_id).first()
                if head_img:
                    return head_img.smallHeadImgUrl
        except Exception as e:
            logger.error(e)
        return ''

    def get_video_poster(self, md5: str) -> str | None:
        pass

    def get_video(self, md5: str) -> str | None:
        pass

    def get_member_head(self, username: str) -> bytearray | None:
        sm = self.client.get_db_manager().wx_db_for_conf(V3DBEnum.DB_MISC)
        logger.info(f"查询成员头像：{username}")
        with sm() as db:
            head_img = db.query(ContactHeadImg).filter_by(usrName=username).first()
            if head_img:
                logger.info(f"查询结果 {head_img.usrName}")
                return head_img.smallHeadBuf
            else:
                logger.warn(f"未查询到成员头像：{username}")
        return None
