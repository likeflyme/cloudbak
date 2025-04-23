import subprocess


class ProtobufUtils(object):
    @staticmethod
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
