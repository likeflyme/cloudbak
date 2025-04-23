from pydantic import BaseModel


class AuthConfig(BaseModel):
    # 默认每日登陆错误次数5次
    login_error_count_day: int = 100


class PictureConfig(BaseModel):
    use_proxy: bool = False


class SystemConfig(BaseModel):
    auth: AuthConfig = AuthConfig()
    picture: PictureConfig = PictureConfig()

