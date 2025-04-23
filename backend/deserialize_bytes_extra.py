import subprocess

from app.models.proto import msg_pb2, cr_extra_buf_pb2
from config.log_config import logger
from db.wx_db import get_session_local
from wx.win.v3.models.micro_msg import ChatRoom


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


def decode_chat_room_data():
    wx_dir = "D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\decoded_MicroMsg.db"

    chatroom_maker = get_session_local(wx_dir)
    chat_room_db = chatroom_maker()

    try:
        chatroom = chat_room_db.query(ChatRoom).filter_by(ChatRoomName='4320150454@chatroom').first()
        result = decode(chatroom.RoomData)
        print(result)
        room_data = cr_extra_buf_pb2.RoomData()
        room_data.ParseFromString(chatroom.RoomData)
        for u in room_data.users:
            if u.name and u.name.strip():
                print(f"id: {u.id}, name: {u.name}")
    except Exception as e:
        print(e)


decode_chat_room_data()

try:
    wx_dir = "D:\\workspace\\sessions\\8\\wxid_b125nd5rc59r12\\Msg\\decoded_MicroMsg.db"

    # chatroom_maker = get_session_local(wx_dir)
    # chat_room_db = chatroom_maker()
    # chatroom = db.query(ChatRoom).filter_by(ChatRoomName='4320150454@chatroom').first()
    #
    # # print(decode(msg.BytesExtra))
    # proto_msg = deserialize_proto_message(chatroom.RoomData)
    # # 输出反序列化后的数据
    # for tv_type in proto_msg.TVMsg:
    #     print(f"Type: {tv_type.Type}")
    #     print(f"TypeValue: {tv_type.TypeValue}")
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
    print("end")
