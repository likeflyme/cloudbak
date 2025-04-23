import os.path
import re
import subprocess

import lz4.block as lb
import xmltodict

from app.helper.directory_helper import get_wx_dir
from wx.win.v3.models.micro_msg import Contact
from app.models.proto import test_pb2, msg_bytes_extra_pb2
from db.sys_db import SessionLocal
from db.wx_db import get_session_local
from app.models.sys import SysUser, SysSession
from app.dependencies.auth_dep import pwd_context
from config.app_config import settings as app_settings
from config.wx_config import settings as wx_settings
from wx.win.v3.models.multi.msg import Msg

msg0_db_path = os.path.join(app_settings.sys_dir, 'sessions\\1\\wxid_b125nd5rc59r12\Msg\\Multi\\decoded_MSG0.db')
msg7_db_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\Multi\\decoded_MSG7.db'


def create_user():
    """
    创建新用户
    :return:
    """
    session = SessionLocal()

    try:
        password = pwd_context.hash('secret')
        user = SysUser(username='admin', password=password, nickname='nickname', state=1)
        session.add(user)
        session.commit()
    finally:
        session.close()


def decrypt_yinyong():
    db_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\Multi\\decoded_MSG7.db'
    session_local = get_session_local(db_path)
    db = session_local()
    try:
        msg = db.query(Msg).filter_by(localId=64109).first()
        print(msg)
        if msg:
            unzipStr = lb.decompress(msg.BytesExtra, uncompressed_size=0x10004)
            text = unzipStr.decode('utf-8')
            print(text)
    finally:
        db.close()


def decode_protobuf(data):
    """
    聊天记录图片 BytesExtra protobuf 结构
    :param data:
    :return:
    """
    process = subprocess.Popen([r'protoc', '--decode_raw'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = error = None
    try:
        output, error = process.communicate(data)
        if error:
            print(error)
    except OSError as e:
        print(e)
        pass
    finally:
        if process.poll() != 0:
            process.wait()
    return output



def generate_proto():
    animal = test_pb2.Animal()
    animal.title = 'dog'
    animal.age = 12
    animal.isDead = False

    child1 = test_pb2.Animal()
    child1.title = 'child1'
    child1.age = 1
    child1.isDead = False
    child1.foot.extend(['foot1', 'foot2', 'foot3'])

    child2 = test_pb2.Animal()
    child2.title = 'child2'
    child2.age = 2
    child2.isDead = True
    child2.foot.extend(['foot1', 'foot2', 'foot3'])

    animal.children.append(child1)
    animal.children.append(child2)

    animal.foot.extend(['pfoot1', 'pfoot2', 'pfoot3'])

    serialized_data = animal.SerializeToString()
    print(f"Serialized data: {serialized_data}")

    out = decode_protobuf(serialized_data)

    print(out)


def deserialize_img():
    session_local = get_session_local(msg7_db_path)
    db = session_local()
    try:
        msg = db.query(Msg).filter_by(localId=64109).first()
        print(msg)
        if msg:
            # print('-----decode protobuf-------')
            print(decode_protobuf(msg.BytesExtra))
            # print(decode_protobuf(msg.CompressContent))

            print('-----lz4 decompress compress content-----')
            unzipStr = lb.decompress(msg.CompressContent, uncompressed_size=0x10004)
            text = unzipStr.decode('utf-8')
            print(text)
            # print(xml_data)
            compress_content_dict = xmltodict.parse(clean_xml_data(text))
            print(compress_content_dict)

            be = msg_bytes_extra_pb2.BytesExtra()
            be.ParseFromString(msg.BytesExtra)

            print('print f1')
            for f1 in be.f1:
                print(f'{f1.s1}: {f1.s2}')
            print('print f3')
            for f3 in be.f3:
                print(f'{f3.s1}: {f3.s2}')
    finally:
        db.close()


deserialize_img()


# 清理XML数据函数
def clean_xml_data(xml_str):
    # 删除非XML字符
    xml_str = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\u4e00-\u9fff]', '', xml_str)
    # 删除空的CDATA节点
    xml_str = re.sub(r'<!\[CDATA\[\]\]>', '', xml_str)
    return xml_str


def decrypt_contact_ExtraBuf():
    db_path = os.path.join(app_settings.sys_dir, 'wx\\jianghu\\wxid_b125nd5rc59r12\\Msg\\decoded_MicroMsg.db')
    session_local = get_session_local(db_path)
    db = session_local()
    try:
        contact = db.query(Contact).filter_by(UserName='guxuefei0719').first()
        print(contact.NickName)
        if contact:
            unzipStr = lb.decompress(contact.ExtraBuf, uncompressed_size=0x10004)
            text = unzipStr.decode('utf-8')
            print(text)
    finally:
        db.close()


def msg_db_count():
    path = os.path.join("D:\\workspace\\sessions\\1\\wxid_b125nd5rc59r12", wx_settings.db_multi)

    pattern = re.compile(r'^decoded_FTSMSG\d\.db$')
    # 计数器
    count = 0

    # 遍历目录中的文件
    for filename in os.listdir(path):
        if pattern.match(filename):
            print(filename)
            count += 1
    return count


