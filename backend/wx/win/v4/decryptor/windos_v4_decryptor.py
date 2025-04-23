import hashlib
import hmac
import os.path
import re
import struct
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from app.models.sys import SysDecryptRecord
from config.log_config import get_context_logger
from db.sys_db import SessionLocal
from wx.interface.wx_interface import Decryptor, ClientInterface
from wx.win.v4.enums.v4_enums import V4DBEnum

IV_SIZE = 16
HMAC_SHA256_SIZE = 64
KEY_SIZE = 32
AES_BLOCK_SIZE = 16
ROUND_COUNT = 256000
PAGE_SIZE = 4096
SALT_SIZE = 16
SQLITE_HEADER = b"SQLite format 3"

patterns = [
    r'^biz.db$',
    r'^contact.db$',
    r'^contact_fts.db$',
    r'^fmessage_new.db$',
    r'^wa_contact_new.db$',
    r'^emoticon.db$',
    r'^favorite.db$',
    r'^favorite_fts.db$',
    r'^hardlink.db$',
    r'^head_image.db$',
    r'^ilinkvoip.db$',
    r'^biz_message_\d+.db$',
    r'^message_\d+.db$',
    r'^message_fts.db$',
    r'^message_resource.db$',
    r'^message_revoke.db$',
    r'^newtips.db$',
    r'^session.db$',
    r'^sns.db$',
    r'^teenager.db$',
    r'^tencentpay.db$',
    r'^wcfinder.db$',
    r'^websearch.db$'
]

compiled_patterns = [re.compile(pattern) for pattern in patterns]


class WindowsV4Decryptor(Decryptor):

    def __init__(self, client: ClientInterface):
        self.client = client

    def decrypt(self, deep: bool = False):
        logger = get_context_logger()
        logger.info("执行数据库解密任务，版本 win.v4")
        if deep:
            logger.info("全量解析，先删除 decoded_ 前缀的库文件")
            self.clear_decoded_files()
        with SessionLocal() as db:
            self.decode_msg(db)

    def clear_decoded_files(self):
        logger = get_context_logger()
        wx_dir = self.client.get_wx_dir()
        # Msg 路径
        msg_dir = os.path.join(wx_dir, 'db_storage')
        for dirpath, dirnames, filenames in os.walk(msg_dir):
            for filename in filenames:
                if filename.startswith('decoded_'):
                    file = os.path.join(dirpath, filename)
                    logger.info(f"删除文件：{file}")
                    os.remove(file)

    def decode_msg(self, db):
        logger = get_context_logger()
        wx_dir = self.client.get_wx_dir()
        # db 基础路径
        db_base_dir = os.path.join(wx_dir, V4DBEnum.DB_BASE_PATH)
        logger.info(f"db_base_dir: {db_base_dir}")
        sys_session = self.client.get_sys_session()
        # 遍历
        for dirpath, dirnames, filenames in os.walk(db_base_dir):
            for filename in filenames:
                for pattern in compiled_patterns:
                    if pattern.match(filename):
                        decoded_file_name = f"{V4DBEnum.DECODED_DB_PREFIX}{filename}"
                        db_file = os.path.join(dirpath, filename)
                        decoded_db_file = os.path.join(dirpath, decoded_file_name)
                        logger.info(f"db_file: {db_file}")
                        # 检查文件的修改时间与数据库中的修改时间
                        modification_time = os.path.getmtime(db_file)
                        record = db.query(SysDecryptRecord).filter_by(db_file=filename,
                                                                      session_id=sys_session.id).first()
                        # decoded_文件存在且时间戳相同，则跳过
                        if record is not None and record.file_last_ts == modification_time:
                            logger.info(f"file {filename} no modify")
                            if os.path.exists(decoded_db_file):
                                continue
                            else:
                                logger.info(f"file {decoded_file_name} not exists")
                        # 解密，解密的文件为原文件名加 decoded_ 前缀
                        is_success = decrypt_db_file_v4(db_file, sys_session.wx_key, decoded_db_file)
                        if is_success:
                            logger.info("decrypt success, record file modification_time")
                            if record is None:
                                record = SysDecryptRecord(db_file=filename, file_last_ts=modification_time,
                                                          session_id=sys_session.id)
                                db.add(record)
                                db.commit()
                            else:
                                record.file_last_ts = modification_time
                                db.commit()


def decrypt_db_file_v4(path: str, pkey: str, output_path: str):
    """
    Decrypts the SQLite database file and writes the result to the specified output file.
    """
    with open(path, 'rb') as f:
        buf = f.read()

    # If the file starts with SQLITE_HEADER, no decryption is needed
    if buf.startswith(SQLITE_HEADER):
        with open(output_path, 'wb') as out_file:
            out_file.write(buf)
        return

    decrypted_buf = bytearray()

    # Get the salt from the start of the file for key decryption
    salt = buf[:16]
    # XOR salt with 0x3a to get the mac_salt
    mac_salt = bytes(x ^ 0x3a for x in salt)

    # Decode the pkey from hex
    pass_key = bytes.fromhex(pkey)

    # PBKDF2 to derive the decryption key
    key = pbkdf2_hmac(pass_key, salt, ROUND_COUNT)

    # PBKDF2 to derive the mac_key
    mac_key = pbkdf2_hmac(key, mac_salt, 2)

    # Append the SQLite header to the decrypted buffer
    decrypted_buf.extend(SQLITE_HEADER)
    decrypted_buf.append(0x00)

    # Calculate reserve size for hash verification and padding
    reserve = IV_SIZE + HMAC_SHA256_SIZE
    reserve = (reserve + AES_BLOCK_SIZE - 1) // AES_BLOCK_SIZE * AES_BLOCK_SIZE

    total_page = len(buf) // PAGE_SIZE
    for cur_page in range(total_page):
        offset = SALT_SIZE if cur_page == 0 else 0
        start = cur_page * PAGE_SIZE
        end = start + PAGE_SIZE

        # Compute HMAC hash for verification
        hash_mac = compute_hmac(mac_key, buf[start + offset:end - reserve + IV_SIZE], cur_page + 1)

        # Check if hash matches
        hash_mac_start_offset = end - reserve + IV_SIZE
        hash_mac_end_offset = hash_mac_start_offset + len(hash_mac)
        if hash_mac != buf[hash_mac_start_offset:hash_mac_end_offset]:
            raise Exception("Hash verification failed")

        # Decrypt the content using AES-256-CBC
        iv = buf[end - reserve:end - reserve + IV_SIZE]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(buf[start + offset:end - reserve]) + decryptor.finalize()

        decrypted_buf.extend(decrypted_data)
        decrypted_buf.extend(buf[end - reserve:end])

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as out_file:
        out_file.write(bytes(decrypted_buf))
        return True


def pbkdf2_hmac(key, salt, iterations):
    """
    Derives a key using PBKDF2-HMAC.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations
    )
    return kdf.derive(key)


def compute_hmac(mac_key, data, page_number):
    """
    Computes the HMAC-SHA512 hash for the given data and page number.
    """
    mac = hmac.new(mac_key, digestmod=hashlib.sha512)  # Use hashlib.sha512 instead of cryptography's SHA512
    mac.update(data)
    mac.update(struct.pack("<I", page_number))  # Add the page number to the hash
    return mac.digest()
