import ctypes
import hashlib
import hmac
import os
import re
from pathlib import Path

from Crypto.Cipher import AES

from app.models.sys import SysDecryptRecord
from db.sys_db import SessionLocal
from wx.interface.wx_interface import Decryptor, ClientInterface

from config.log_config import get_context_logger


SQLITE_FILE_HEADER = bytes('SQLite format 3', encoding='ASCII') + bytes(1)
IV_SIZE = 16
HMAC_SHA1_SIZE = 20
KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000

patterns = [
    r'^MicroMsg.db$',
    r'^Misc.db$',
    r'^PublicMsg.db$',
    r'^HardLinkImage.db$',
    r'^MediaMSG\d+.db$',
    r'^MSG\d+.db$',
    r'^OpenIMContact.db$',
    r'^OpenIMMedia.db$',
    r'^OpenIMMsg.db$',
    r'^OpenIMResource.db$',
    r'^FTSContact.db$',
    r'^FTSFavorite.db$',
    r'^FTSMsg.db$',
    r'^FTSMSG\d+.db$',
]

check_file_list = [
    'Msg/decoded_MicroMsg.db',
    'Msg/decoded_Misc.db',
    'Msg/decoded_PublicMsg.db',
    'Msg/decoded_HardLinkImage.db',
    'Msg/decoded_OpenIMContact.db',
    'Msg/decoded_OpenIMMedia.db',
    'Msg/decoded_OpenIMMsg.db',
    'Msg/decoded_OpenIMResource.db',
    'Msg/decoded_FTSContact.db',
    'Msg/decoded_FTSFavorite.db',
]

compiled_patterns = [re.compile(pattern) for pattern in patterns]


def decode_one(input_file, password):
    """
    解码数据库文件，优化为流式处理以支持大文件
    :param input_file: 输入文件路径
    :param password: 解密密码
    :return: 解密是否成功
    """
    logger = get_context_logger()
    logger.info('decryption file: %s', input_file)
    input_file = Path(input_file)
    output_file = input_file.parent / f'decoded_{input_file.name}'

    try:
        with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            # 读取头部16字节salt
            salt = f_in.read(16)
            if len(salt) != 16:
                logger.info('file too small, invalid format')
                return False

            # 生成key和mac_key
            key = hashlib.pbkdf2_hmac('sha1', password, salt, DEFAULT_ITER, KEY_SIZE)
            mac_salt = bytes([x ^ 58 for x in salt])
            mac_key = hashlib.pbkdf2_hmac('sha1', key, mac_salt, 2, KEY_SIZE)

            # 读取第一个页面并验证
            first = f_in.read(DEFAULT_PAGESIZE - 16)  # 减去salt的16字节
            if len(first) != DEFAULT_PAGESIZE - 16:
                logger.info('first page incomplete')
                return False

            hash_mac = hmac.new(mac_key, digestmod='sha1')
            hash_mac.update(first[:-32])  # 不包括最后32字节的HMAC和IV
            hash_mac.update(bytes(ctypes.c_int(1)))
            if hash_mac.digest() != first[-32:-12]:
                logger.info('password error or file corrupted')
                return False

            logger.info('decryption success, processing file')

            # 写入SQLite文件头
            f_out.write(SQLITE_FILE_HEADER)

            # 解密并写入第一个页面
            iv = first[-48:-32]  # 提取IV
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(first[:-48])  # 解密主体部分
            f_out.write(decrypted)
            f_out.write(first[-48:])  # 写入未加密的尾部（IV + HMAC）

            # 流式处理剩余页面
            while True:
                chunk = f_in.read(DEFAULT_PAGESIZE)
                if not chunk:
                    break
                if len(chunk) < DEFAULT_PAGESIZE:
                    logger.info('last chunk incomplete, padding or truncating as needed')
                    # 如果最后一个块不足页面大小，直接写入（通常不需要填充）
                    f_out.write(chunk)
                    break

                iv = chunk[-48:-32]  # 提取IV
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = cipher.decrypt(chunk[:-48])  # 解密主体部分
                f_out.write(decrypted)
                f_out.write(chunk[-48:])  # 写入未加密的尾部

        return True

    except Exception as e:
        logger.error(f'decryption failed: {str(e)}')
        return False


class WindowsV3Decryptor(Decryptor):
    """
    windows 客户端 v3 版本数据库解密
    """
    def __init__(self, client: ClientInterface):
        self.client = client

    def decrypt(self, deep: bool = False):
        logger = get_context_logger()
        logger.info("执行数据库解密任务，版本 win.v3")
        if deep:
            logger.info("全量解析，先删除 decoded_ 前缀的库文件")
            self.clear_decoded_files()
        with SessionLocal() as db:
            self.decode_msg(db)

    def clear_decoded_files(self):
        logger = get_context_logger()
        wx_dir = self.client.get_wx_dir()
        # Msg 路径
        msg_dir = os.path.join(wx_dir, 'Msg')
        for dirpath, dirnames, filenames in os.walk(msg_dir):
            for filename in filenames:
                if filename.startswith('decoded_'):
                    file = os.path.join(dirpath, filename)
                    logger.info(f"删除文件：{file}")
                    os.remove(file)

    def decode_msg(self, db):
        logger = get_context_logger()
        wx_dir = self.client.get_wx_dir()
        sys_session = self.client.get_sys_session()
        # 2. 数据库解密
        logger.info("数据库解密")
        # 生成password
        password = bytes.fromhex(sys_session.wx_key.replace(' ', ''))
        logger.info(f"password: {password}")
        # Msg 路径
        msg_dir = os.path.join(wx_dir, 'Msg')
        logger.info(f"msg_dir: {msg_dir}")
        # 遍历
        for dirpath, dirnames, filenames in os.walk(msg_dir):
            for filename in filenames:
                logger.info(f"filename: {filename}")
                for pattern in compiled_patterns:
                    if pattern.match(filename):
                        logger.info("match, do decrypt")
                        db_file = os.path.join(dirpath, filename)
                        # 检查文件的修改时间与数据库中的修改时间
                        modification_time = os.path.getmtime(db_file)
                        record = db.query(SysDecryptRecord).filter_by(db_file=filename,
                                                                      session_id=sys_session.id).first()
                        # decoded_文件存在且时间戳相同，则跳过
                        if record is not None and record.file_last_ts == modification_time:
                            logger.info(f"file {filename} no modify")
                            decoded_file = os.path.join(dirpath, f"decoded_{filename}")
                            if os.path.exists(decoded_file):
                                continue
                            else:
                                logger.info(f"file decoded_{filename} not exists")
                        # 解密，解密的文件为原文件名加 decoded_ 前缀
                        is_success = decode_one(db_file, password)
                        if is_success:
                            logger.info("record file modification_time")
                            if record is None:
                                record = SysDecryptRecord(db_file=filename, file_last_ts=modification_time,
                                                          session_id=sys_session.id)
                                db.add(record)
                                db.commit()
                            else:
                                record.file_last_ts = modification_time
                                db.commit()

