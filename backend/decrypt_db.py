import ctypes
import hashlib
import hmac
from pathlib import Path

from Crypto.Cipher import AES


SQLITE_FILE_HEADER = bytes('SQLite format 3', encoding='ASCII') + bytes(1)
IV_SIZE = 16
HMAC_SHA1_SIZE = 20
KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000


def decode():
    path = input("请输入文件路径: ")
    print(f"您输入的文件路径: {path}")
    key = input("请输入key: ")
    print(f"您输入的key: {key}")
    try:
        # 生成password
        password = bytes.fromhex(key.replace(' ', ''))
        decode_one(path, password)
    except Exception as e:
        print(e)
    input("输入任意字符结束：")


def decode_one(input_file, password):
    """
    解码数据库文件
    :param input_file:
    :param password:
    :return:
    """
    input_file = Path(input_file)

    with open(input_file, 'rb') as (f):
        blist = f.read()
    salt = blist[:16]
    key = hashlib.pbkdf2_hmac('sha1', password, salt, DEFAULT_ITER, KEY_SIZE)
    first = blist[16:DEFAULT_PAGESIZE]
    mac_salt = bytes([x ^ 58 for x in salt])
    mac_key = hashlib.pbkdf2_hmac('sha1', key, mac_salt, 2, KEY_SIZE)
    hash_mac = hmac.new(mac_key, digestmod='sha1')
    hash_mac.update(first[:-32])
    hash_mac.update(bytes(ctypes.c_int(1)))

    if hash_mac.digest() == first[-32:-12]:
        print('decryption success')
    else:
        print('password error')
    blist = [
        blist[i:i + DEFAULT_PAGESIZE]
        for i in range(DEFAULT_PAGESIZE, len(blist), DEFAULT_PAGESIZE)
    ]

    with open(input_file.parent / f'decoded_{input_file.name}', 'wb') as (f):
        f.write(SQLITE_FILE_HEADER)
        t = AES.new(key, AES.MODE_CBC, first[-48:-32])
        f.write(t.decrypt(first[:-48]))
        f.write(first[-48:])
        for i in blist:
            t = AES.new(key, AES.MODE_CBC, i[-48:-32])
            f.write(t.decrypt(i[:-48]))
            f.write(i[-48:])


decode()
