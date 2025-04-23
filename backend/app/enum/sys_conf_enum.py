from enum import StrEnum


class SysConfEnum(StrEnum):
    SESSION_CONF = 'session_conf'
    USER_CONF = 'user_conf'
    SYS_CONF = 'sys_conf'
    SYS_INFO = 'sys_info'
    # 用户两步验证密钥配置
    AUTH_SECRET_CONF = 'auth_secret'
