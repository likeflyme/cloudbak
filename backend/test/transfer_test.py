# 微信 cdnthumburl 数据
hex_data = "3057020100044b304902010002048de1b35602032f54050204916a42b70204677f33af042438616638613265332d356165332d343031322d616334302d3164343135303031343062620204019820010201000405004c543d00"

# 将 Hex 转换为二进制数据
byte_data = bytes.fromhex(hex_data)

# 解析函数
def parse_cdnthumburl(data):
    try:
        # 检查头部
        header = data[:2]  # 假设头部是 2 字节
        if header == b'0W':  # 示例：假设 0W 为特征头部
            # 跳过头部，解析后续字段
            content_length = int.from_bytes(data[2:4], 'big')  # 假设长度字段为 2 字节
            content = data[4:4+content_length]  # 根据长度提取内容
            return {
                "header": header.decode('utf-8', errors='replace'),
                "content_length": content_length,
                "content": content.decode('utf-8', errors='replace')  # 假设内容为 ASCII
            }
        else:
            return {"error": "Unknown header"}
    except Exception as e:
        return {"error": str(e)}

# 调用解析函数
parsed_data = parse_cdnthumburl(byte_data)
print(parsed_data)
