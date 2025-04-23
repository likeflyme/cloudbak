import pyotp
from pydantic import BaseModel


class TwoStepModel(BaseModel):
    two_step_auth_open: bool = False
    secret: str = pyotp.random_base32()


class UserConfig(BaseModel):
    # 是否开启两步验证
    two_step_auth: TwoStepModel = TwoStepModel()



