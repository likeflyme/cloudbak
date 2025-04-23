from app.models.proto import msg_pb2
from db.wx_db import get_session_local
from wx.win.v3.models.multi.msg import Msg
import subprocess
from config.log_config import logger


def deserialize_proto_message(byte_array):
    proto_msg = msg_pb2.ProtoMsg()
    proto_msg.ParseFromString(byte_array)
    return proto_msg


def decode(data):
    process = subprocess.Popen([r'protoc', '--decode_raw'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = error = None
    try:
        output, error = process.communicate(data)
        if error:
            print(error)
    except OSError as e:
        logger.error('decrypt error', e)
        pass
    finally:
        if process.poll() != 0:
            process.wait()
    return output


# f = open("writebuff.txt", "rb")
# data = f.read()
# print(decode(data))
# f.close()

wx_dir = "D:\\wxdec\\wx\\jianghu\\wxid_b125nd5rc59r12\\Msg\\Multi\\decoded_MSG5.db"

session_local = get_session_local(wx_dir)
db = session_local()

# try:
#     msgs = db.query(Msg).filter_by(TalkerId=130).order_by(Msg.localId.desc()).limit(20)
#     for msg in msgs:
#         print(msg.BytesExtra.decode('latin-1'))
#         print('----------------')
# finally:
#     db.close()

try:
    msg = db.query(Msg).filter_by(localId=302).first()
    # print(decode(msg.BytesExtra))
    proto_msg = deserialize_proto_message(msg.BytesExtra)
    # 输出反序列化后的数据
    for tv_type in proto_msg.TVMsg:
        print(f"Type: {tv_type.Type}")
        print(f"TypeValue: {tv_type.TypeValue}")
    # msg = db.query(Msg).filter_by(localId=63360).first()
    # result = []
    # print(msg.BytesExtra.decode('latin-1'))
    # for byte in msg.BytesExtra:
    #     try:
    #         # 尝试将单个字节解码为 Latin-1 字符
    #         char = bytes([byte]).decode('latin-1')
    #         result.append(char)
    #         if byte > 150:
    #             print(char)
    #             print(byte)
    #             print(hex(byte))
    #             print('--------')
    #     except UnicodeDecodeError:
    #         # 如果解码失败，则打印该字节的十六进制字符串
    #         hex_str = f"\\x{byte:02x}"
    #         print('x:' + hex_str)
    # print(''.join(result))

    # msg = db.query(Msg).filter_by(localId=63359).first()
    # print(decode(msg.CompressContent))
    # proto_msg = deserialize_proto_message(msg.CompressContent)
    # # 输出反序列化后的数据
    # for tv_type in proto_msg.TVMsg:
    #     print(f"Type: {tv_type.Type}")
    #     print(f"TypeValue: {tv_type.TypeValue}")
finally:
    db.close()
