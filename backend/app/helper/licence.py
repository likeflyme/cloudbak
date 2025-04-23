import base64
import hashlib
from typing import Optional

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pydantic import BaseModel

from app.enum.license_enum import LicenseType


class License(BaseModel):
    license_type: Optional[LicenseType] = None
    client_id: Optional[str] = None
    expiry_date: Optional[str] = None
    order_id: Optional[str] = None


class LicenseManager:
    def __init__(self, version: str, key: str):
        """
        初始化 License 类，使用 256 位 AES 密钥
        :param version: 授权算法版本，v01为 AES
        :param key: 用于 AES 加密的密钥（建议为固定密钥或通过其他方式存储）
        """
        self.version = version
        self.key = hashlib.sha256(key.encode()).digest()  # 生成固定 32 字节密钥

    def encrypt(self, data: License) -> str:
        """
        AES 加密
        :param data: 需要加密的文本（JSON 格式）
        :return: 加密后的 Base64 编码字符串
        """
        cipher = AES.new(self.key, AES.MODE_CBC)  # 使用 CBC 模式
        iv = cipher.iv  # 生成 16 字节 IV
        data_json_str = data.model_dump_json()
        encrypted_data = cipher.encrypt(pad(data_json_str.encode(), AES.block_size))  # 加密并填充
        return self.version + base64.b64encode(iv + encrypted_data).decode()  # Base64 编码

    def decrypt(self, encrypted_data: str) -> str:
        """
        AES 解密
        :param encrypted_data: Base64 编码的加密数据
        :return: 解密后的 JSON 文本
        """
        encrypted_data = base64.b64decode(encrypted_data)  # Base64 解码
        iv = encrypted_data[:AES.block_size]  # 取出前 16 字节 IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)  # 重新初始化 AES
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)  # 解密并去填充
        return decrypted_data.decode()

    def generate_license(self, license_info: License) -> str:
        """
        生成授权码
        :param license_info: 授权信息
        :return: 加密后的授权码
        """
        return self.encrypt(license_info)

    def parse_license(self, license_code: str) -> License:
        """
        解析授权码
        :param license_code: 加密的授权码，前三位为加密版本号

        :return: 解析后的字典（包含机器码、授权类型、过期时间）
        """
        try:
            enc_version = license_code[:3]
            if enc_version != 'v01':
                raise ValueError("Invalid license code")
            real_license_code = license_code[3:]
            decrypted_data = self.decrypt(real_license_code)
            return License.model_validate_json(decrypted_data)
        except ValueError as e:
            raise e
        except Exception:
            raise ValueError("Invalid license code")


# 示例
if __name__ == "__main__":
    version = "v01"  # 加密版本
    secret_key = "license.cloudbak.org"  # 密钥
    license_manager = LicenseManager(version, secret_key)

    # client_id = "A7E6DA66-19C5-11F0-B628-462664C98C0C"  # 授权码
    license_type = LicenseType.PRO  # 授权类型，1为PRO授权
    # expiry_date = "0"  # 过期时间，0为无期限
    # order_id = "lost"  # 订单号
    #
    # license_info = License(license_type=license_type, client_id=client_id, expiry_date=expiry_date, order_id=order_id)
    #
    # print(f"机器码：{client_id}")
    # print(f"授权类型：{license_type}")
    # print(f"有效期：{expiry_date}")
    # print(f"订单号：{order_id}")

    # license_code = license_manager.generate_license(license_info)
    license_code = 'v01o4FmNconninXxhU4wusStTODdt0e3g9WCCaxaJa8hEKjAh5e/9VXtoan4RCAc7+6irW5Sul1QJXhmk20xGj5SQiIHwpuNV6RvfVzxS2ycWhcf74tmYtUeNboshyzVPraKxWPPUa1tzLJzYwT+I/+Vt7QWp6ecitQxLoIkJG2hBud/1zHNvEXbe2cplq+H5yvJ3GbWzPF8GZFm9FifSZupw=='
    print("生成的授权码:", license_code)

    # 解析授权码
    parsed_data = license_manager.parse_license(license_code)
    print("解析后的数据:", parsed_data)

    # license_code = "v01HcRfRffeu18KzwxPf2cBs6RU1dDhhOd+UZ+BqnzfdwNwnTUB+IJuHC8OuzxXRHi0YlxdYAgPEVQMaS7YaPIIq8wQ6kO7vVRBiAu+QxYN1/nI22SFHAmLFEG9HjRg4/r4/SMruYIK+s0uqu8+QC9P9ldt9lrYhQNc0JyXd4oiglgTOaTtvCxDfH3kGWZDv7rx"
    # parsed_data = license_manager.parse_license(license_code)
    # print("解析后的数据:", parsed_data)
