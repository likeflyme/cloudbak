import uuid


class Machine(object):

    @classmethod
    def get_machine_code(cls):
        """
        组合 MAC 地址 + CPU ID 生成唯一机器码
        """
        unique_id = uuid.uuid1()  # 基于 MAC 地址和时间生成
        return str(unique_id).upper()


if __name__ == "__main__":
    print("机器码:", Machine.get_machine_code())

