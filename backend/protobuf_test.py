import subprocess

from wx.win.v3.models.micro_msg import Contact
from wx.win.v3.models.multi.msg import Msg
from db.wx_db import get_session_local


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


def msg_decode():
    db_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\Multi\\decoded_MSG5.db'
    sl = get_session_local(db_path)
    with sl() as db:
        msg = db.query(Msg).filter_by(localId=329).first()
        print(msg)
        if msg:
            print(decode_protobuf(msg.BytesExtra))


def contact_decode():
    db_path = 'D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\decoded_MicroMsg.db'
    sl = get_session_local(db_path)
    with sl() as db:
        c = db.query(Contact).filter_by(UserName='wxid_c04nvtu0zfek22').first()
        print(c)
        if c:
            print(decode_protobuf(c.ExtraBuf))


contact_decode()