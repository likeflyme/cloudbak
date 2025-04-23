from app.services.decode_wx_pictures import decrypt_file


# 图片的特征码
tp = {
    "jpg": 0xFFD8,
    "gif": 0x4749,
    "png": 0x8950,
}


def print_file_header(file_path, num_bytes=100):
    with open(file_path, "rb") as f:
        header = f.read(num_bytes)
    print(" ".join(f"{b:02X}" for b in header))


def xor_decrypt(file_path, output_path, key):
    with open(file_path, "rb") as f:
        data = f.read()

    key_bytes = key.to_bytes(4, 'little')  # 变换密钥为字节数组（尝试 'big' 也可以）
    decrypted_data = bytearray()

    # 尝试从第 0 个字节或 10 个字节后开始
    for i in range(len(data)):
        decrypted_byte = data[i] ^ key_bytes[i % 4]  # 轮流 XOR 4 字节
        decrypted_data.append(decrypted_byte)

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print(f"解密完成，输出文件: {output_path}")


def decrypt_image(input_path: str, output_path: str):
    """
    读取加密的图片文件，执行两次异或解密，并保存解密后的图片。

    :param input_path: 加密图片文件的路径
    :param output_path: 解密后保存的图片文件路径
    """
    try:
        with open(input_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        # 进行两次异或操作解密
        decrypted_data = bytes((byte ^ 0x3C) ^ 0x01 for byte in encrypted_data)

        with open(output_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        print(f"解密完成，已保存到 {output_path}")
    except Exception as e:
        print(f"解密失败: {e}")


def decrypt_image_v4(key: bytearray, input_path: str, output_path: str):
    """
    读取加密的图片文件，执行两次异或解密，并保存解密后的图片。

    :param input_path: 加密图片文件的路径
    :param output_path: 解密后保存的图片文件路径
    """
    try:
        with open(input_path, 'rb') as enc_file:
            encrypted_data = enc_file.read()

        # 进行两次异或操作解密
        decrypted_data = bytes((byte ^ 0x3C) ^ 0x01 for byte in encrypted_data)

        with open(output_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        print(f"解密完成，已保存到 {output_path}")
    except Exception as e:
        print(f"解密失败: {e}")


def xor_decrypt_new(data, key):
    key_bytes = key.to_bytes((key.bit_length() + 7) // 8, 'big')  # 转换为字节数组
    key_len = len(key_bytes)
    return bytes(data[i] ^ key_bytes[i % key_len] for i in range(len(data)))


if __name__ == '__main__':

    # 0x104AA022
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\d31638f7b62b99ff7245e692b150655d\\2025-02\\Img\\d29c797435a3cccba70f3f6c413888ab.dat'
    # print_file_header(dat_path)
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\d31638f7b62b99ff7245e692b150655d\\2025-02\\Img\\d29c797435a3cccba70f3f6c413888ab_t.dat'
    # print_file_header(dat_path)
    # # 0x10B52E
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\\d03607872ee740aa9d4eee630fb6c617\\2025-02\\Img\\1b3d18c6ff37cfc8ef4b265294e730cc.dat'
    # print_file_header(dat_path)
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\\d03607872ee740aa9d4eee630fb6c617\\2025-02\\Img\\1b3d18c6ff37cfc8ef4b265294e730cc_t.dat'
    # print_file_header(dat_path)
    # # 0x10B33B
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\\d03607872ee740aa9d4eee630fb6c617\\2025-02\\Img\\af69f7609d32ed39e653ac091034c4ae.dat'
    # print_file_header(dat_path)
    # dat_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\\d03607872ee740aa9d4eee630fb6c617\\2025-02\\Img\\af69f7609d32ed39e653ac091034c4ae_t.dat'
    # print_file_header(dat_path)
    #
    # key = 0x104AA022
    # input_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\d31638f7b62b99ff7245e692b150655d\\2025-02\\Img\\d29c797435a3cccba70f3f6c413888ab.dat'
    # out_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\d31638f7b62b99ff7245e692b150655d\\2025-02\\Img\\d29c797435a3cccba70f3f6c413888ab.jpg'
    # xor_decrypt(input_path, out_path, key)

    # # 0x10A4A022
    # print('0x10A4A022')
    # input_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\\d31638f7b62b99ff7245e692b150655d\\2025-02\\Img\\d29c797435a3cccba70f3f6c413888ab.dat'
    # print_file_header(input_path)
    #
    # key = 0x10A4A022
    # with open(input_path, 'rb') as enc_file:
    #     encrypted_data = enc_file.read()
    #     data = xor_decrypt_new(encrypted_data, key)
    #     print(data[:100])


    # key = 0x10A4A022
    # data = decrypt_image(input_path, input_path)
    # # 0x10B52E
    # print('0x10B52E')
    # input_path = 'D:\\微信文件\\xwechat_files\\wxid_x1j6ne5cnl8r19_4e0d\\msg\\attach\d03607872ee740aa9d4eee630fb6c617\\2025-02\\Img\\1b3d18c6ff37cfc8ef4b265294e730cc.dat'
    # print_file_header(input_path)
    # output_path = 'D:/test/6cc1fa07322d7a0420a457df00d00da6_t.jpg'
    # decrypt_image(input_path, output_path)
    # print_file_header(output_path)

    md5 = 'f1bc881c4c678f066f6ecfcd27270505'
    
