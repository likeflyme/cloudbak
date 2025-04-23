# a = 0x1136
# b = 0xFFD8
# hex_a = a.to_bytes(2, byteorder='big')
# hex_b = b.to_bytes(2, byteorder='big')
# print(hex_a)
# print(hex_b)
# hex_c = bytes([b1 ^ b2 for b1, b2 in zip(hex_a, hex_b)])
# print(hex_c)
# print(bytes.fromhex('EEEE'))
# 图片格式的前两个字节固定特征码
import os
import io

from app.helper.directory_helper import get_wx_dir
from app.models.sys import SysSession
from config.log_config import logger

tp = {
    "jpg": 0xFFD8,
    "gif": 0x4749,
    "png": 0x8950,
}


def decrypt_images(sys_session: SysSession):
    wx_dir = get_wx_dir(sys_session)
    msg_attach_dir = os.path.join(wx_dir, 'FileStorage/MsgAttach/')
    logger.info('图片文件根路径: %s', msg_attach_dir)
    decrypt_files_in_directory(msg_attach_dir)


def decrypt_files_in_directory(directory):
    """
    解密微信目录中的所有图片：jpg,gif,png
    :param directory:
    :return:
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".dat"):
                encrypted_file_path = os.path.join(root, file)
                try:
                    decrypt_file(encrypted_file_path)
                except Exception as e:
                    logger.error(f"Failed to decrypt {encrypted_file_path}", e)


def xor_byte_arrays(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def match_bytes(a1, a2):
    for key, value in tp.items():
        xor1 = a1 ^ (value >> 8)
        xor2 = a2 ^ (value & 0xFF)
        if xor1 == xor2:
            return xor1, key
    return None


def decrypt_file(encrypted_file_path):
    logger.info('decrypt file: %s', encrypted_file_path)
    # 读取文件的前两个字节
    with open(encrypted_file_path, "rb") as f:
        first_byte = f.read(1)
        second_byte = f.read(1)

        if len(first_byte) < 1 or len(second_byte) < 1:
            logger.warn("File is too small to contain two bytes for matching.")
            return None

        a1 = first_byte[0]
        a2 = second_byte[0]

    # 使用前两个字节进行匹配
    result = match_bytes(a1, a2)

    if result is None:
        logger.warn("No matching key found for the given bytes.")
        return None

    key, image_type = result

    # 生成解密后的文件路径
    decrypted_file_path = os.path.splitext(encrypted_file_path)[0] + "." + image_type

    # 使用 key 对整个文件进行异或运算并写入新的文件
    with open(encrypted_file_path, "rb") as encrypted_file:
        with open(decrypted_file_path, "wb") as decrypted_file:
            while byte := encrypted_file.read(1):
                decrypted_file.write(bytes([byte[0] ^ key]))

    logger.debug('Decrypted file saved as: %s', decrypted_file_path)
    return decrypted_file_path


def decrypt_by_file_type(encrypted_file_path: str, image_type: str):
    logger.info('decrypt file: %s', encrypted_file_path)

    tp_bt = tp[image_type]
    if not tp_bt:
        return None

    with open(encrypted_file_path, "rb") as f:
        first_byte = f.read(1)
        second_byte = f.read(1)

        if len(first_byte) < 1 or len(second_byte) < 1:
            logger.warn("File is too small to contain two bytes for matching.")
            return None

        a1 = first_byte[0]

    # 使用前两个字节进行匹配
    key = a1 ^ (tp_bt >> 8)

    # 生成解密后的文件路径
    decrypted_file_path = os.path.splitext(encrypted_file_path)[0] + "." + image_type

    # 使用 key 对整个文件进行异或运算并写入新的文件
    with open(encrypted_file_path, "rb") as encrypted_file:
        with open(decrypted_file_path, "wb") as decrypted_file:
            while byte := encrypted_file.read(1):
                decrypted_file.write(bytes([byte[0] ^ key]))

    logger.debug('Decrypted file saved as: %s', decrypted_file_path)
    return decrypted_file_path


def decrypt_file_return_io(encrypted_file_path):
    """
    解密返回字节流，供接口直接返回
    """
    logger.info('decrypt file: %s', encrypted_file_path)

    # 读取文件的前两个字节
    with open(encrypted_file_path, "rb") as f:
        first_byte = f.read(1)
        second_byte = f.read(1)

        if len(first_byte) < 1 or len(second_byte) < 1:
            logger.warn("File is too small to contain two bytes for matching.")
            return None

        a1 = first_byte[0]
        a2 = second_byte[0]

    # 使用前两个字节进行匹配
    result = match_bytes(a1, a2)

    if result is None:
        logger.warn("No matching key found for the given bytes.")
        return None

    key, image_type = result

    # 使用 key 对整个文件进行异或运算，并将解密数据写入字节流
    decrypted_stream = io.BytesIO()
    with open(encrypted_file_path, "rb") as encrypted_file:
        while byte := encrypted_file.read(1):
            decrypted_stream.write(bytes([byte[0] ^ key]))

    # 重置流的位置为文件开头，供 StreamingResponse 使用
    decrypted_stream.seek(0)

    logger.debug('Decrypted file data prepared.')
    return decrypted_stream  # 返回字节流数据
