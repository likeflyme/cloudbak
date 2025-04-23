from wx.client_factory import ClientFactory


def analyze(sys_session_id: int, deep: bool = False):
    """
    用户上传的zip文件分析处理
    :param sys_session_id: 用户建立的 session_id
    :param deep，全量解析
    :return:
    """
    client = ClientFactory.get_client_by_id(sys_session_id)
    if client:
        client.clear()
        client.get_decryptor().decrypt(deep)

