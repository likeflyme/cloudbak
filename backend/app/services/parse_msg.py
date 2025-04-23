import os
import re
import lz4.block as lb
import xmltodict
from lz4.block import LZ4BlockError

from app.helper.directory_helper import get_session_dir
from wx.win.v3.models.multi.msg import Msg
from app.models.proto import msg_bytes_extra_pb2
from app.models.sys import SysSession
from app.schemas.schemas import MsgWithExtra
from app.services.file_handler import dat_to_img
from config.log_config import logger


def clean_xml_data(xml_str):
    # 删除非XML字符
    xml_str = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF]', '', xml_str)
    # 删除空的CDATA节点
    xml_str = re.sub(r'<!\[CDATA\[\]\]>', '', xml_str)
    # 将所有的 & 符号替换为 &amp;
    # xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_str)
    return xml_str


def deep_clean_xml_data(xml_str):
    """
    进一步格式化xml
    """
    xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_str)
    return xml_str


def parse(msg: Msg, session_id: int, db_no: int):
    nmsg = MsgWithExtra(**msg.__dict__)
    nmsg.MsgSvrIDStr = str(msg.MsgSvrID)
    nmsg.DbNo = db_no
    if msg.BytesExtra:
        proto = msg_bytes_extra_pb2.BytesExtra()
        proto.ParseFromString(msg.BytesExtra)
        for f3 in proto.f3:
            # 群聊消息发送者wxid
            if f3.s1 == 1:
                nmsg.WxId = f3.s2
            # 图片缩略图
            if f3.s1 == 3:
                # nmsg.Thumb = dat_to_img(session_id, f3.s2)
                if f3.s2:
                    img_path = f3.s2.replace("\\", "/")
                    nmsg.Thumb = img_path
            # 图片原图
            if f3.s1 == 4:
                # nmsg.Image = dat_to_img(session_id, f3.s2)
                if f3.s2:
                    img_path = f3.s2.replace("\\", "/")
                    file_path = os.path.join(get_session_dir(session_id), img_path)
                    if os.path.exists(file_path):
                        nmsg.Image = img_path
    if hasattr(msg, 'CompressContent') and msg.CompressContent:
        try:
            unzipStr = lb.decompress(msg.CompressContent, uncompressed_size=0x10004)
            xml_data = unzipStr.decode('utf-8')
        except LZ4BlockError as e:
            # 如果解压失败，尝试增加缓冲区大小
            logger.warning(f"Decompression failed with error: {e}. Retrying with larger uncompressed_size.")
            unzipStr = lb.decompress(msg.CompressContent, uncompressed_size=0x7D000)  # 增加缓冲区大小，500KB
            xml_data = unzipStr.decode('utf-8')
        try:
            xml_data = clean_xml_data(xml_data)
            # xml_data = extract_msg_content(xml_data)
            compress_content_dict = xmltodict.parse(xml_data)
            nmsg.compress_content = compress_content_dict
        except Exception as ex:
            logger.warning(f"parse compress_content failed with error: {ex}")
            # 进一步格式化（信息可能有所失真）
            xml_data = deep_clean_xml_data(xml_data)
            try:
                compress_content_dict = xmltodict.parse(xml_data)
                nmsg.compress_content = compress_content_dict
            except Exception as ex:
                logger.warning(f"parse compress_content failed with error: {ex}")
                logger.info(f"xml_data is : {xml_data}")
    return nmsg


def parse_sender_thumb_source(msg: Msg, sys_session: SysSession):
    """
    解析消息的发送者
    群聊消息发送者存放在 BytesExtra 中，需要解析
    如果为非群聊
      IsSender=0，则为聊天对手
      IsSender=1，则为当前会话微信
    """
    sender = None
    thumb = None
    source = None
    wxId = None
    if msg.BytesExtra:
        proto = msg_bytes_extra_pb2.BytesExtra()
        proto.ParseFromString(msg.BytesExtra)
        for f3 in proto.f3:
            # 群聊消息发送者wxid
            if f3.s1 == 1:
                wxId = f3.s2
            # 图片缩略图
            if f3.s1 == 3:
                if f3.s2:
                    path = f3.s2.replace("\\", "/")
                    thumb = path
            # 图片原图
            if f3.s1 == 4:
                if f3.s2:
                    relative_path = f3.s2.replace("\\", "/")
                    file_path = os.path.join(get_session_dir(sys_session.id), relative_path)
                    if os.path.exists(file_path):
                        source = file_path
    if msg.StrTalker.endswith("@chatroom"):
        sender = wxId
    elif msg.IsSender == 0:
        sender = msg.StrTalker
    else:
        sender = sys_session.wx_id
    return sender, thumb, source


def parse_compress_content(compress_content: bytes):
    try:
        unzipStr = lb.decompress(compress_content, uncompressed_size=0x10004)
        xml_data = unzipStr.decode('utf-8')
    except LZ4BlockError as e:
        # 如果解压失败，尝试增加缓冲区大小
        logger.warning(f"Decompression failed with error: {e}. Retrying with larger uncompressed_size.")
        unzipStr = lb.decompress(compress_content, uncompressed_size=0x7D000)  # 增加缓冲区大小，500KB
        xml_data = unzipStr.decode('utf-8')
    try:
        xml_data = clean_xml_data(xml_data)
        # xml_data = extract_msg_content(xml_data)
        compress_content_dict = xmltodict.parse(xml_data)
        return compress_content_dict
    except Exception as ex:
        logger.warning(f"parse compress_content failed with error: {ex}")
        logger.info(f"xml_data is : {xml_data}")
    return None


def extract_msg_content(xml_data):
    """
    只提取 <msg></msg>标签中的内容，如果没匹配到，则原样返回
    """
    # 匹配 <msg></msg> 标签及其中的内容
    match = re.search(r'<msg>.*?</msg>', xml_data, re.DOTALL)  # re.DOTALL 使得 '.' 可以匹配换行符
    if match:
        return match.group(0)  # 返回匹配的部分
    return xml_data

