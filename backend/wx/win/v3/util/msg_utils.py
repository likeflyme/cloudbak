import re
import lz4.block as lb
import xmltodict
from lz4.block import LZ4BlockError

from app.models.proto import msg_bytes_extra_pb2
from config.log_config import logger
from wx.win.v3.models.multi.msg import Msg as MsgModel


class MsgUtils(object):

    @staticmethod
    def parse_sender_thumb_source(msg: MsgModel):
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
                        source = f3.s2.replace("\\", "/")
        if msg.StrTalker.endswith("@chatroom"):
            sender = wxId
        elif msg.IsSender == 0:
            sender = msg.StrTalker
        return sender, thumb, source

    @staticmethod
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
            xml_data = MsgUtils.clean_xml_data(xml_data)
            # xml_data = extract_msg_content(xml_data)
            compress_content_dict = xmltodict.parse(xml_data)
            return compress_content_dict
        except Exception as ex:
            logger.warning(f"parse compress_content failed with error: {ex}")
            logger.info(f"xml_data is : {xml_data}")
        return None

    @staticmethod
    def clean_xml_data(xml_str):
        # 删除非XML字符
        xml_str = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF]', '', xml_str)
        # 删除空的CDATA节点
        xml_str = re.sub(r'<!\[CDATA\[\]\]>', '', xml_str)
        # 将所有的 & 符号替换为 &amp;
        # xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_str)
        return xml_str

    @staticmethod
    def deep_clean_xml_data(xml_str):
        """
        进一步格式化xml
        """
        xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_str)
        return xml_str
