from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm


class OAuth2PasswordCodeRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
        grant_type: str = Form(default="password", regex="password"),
        scope: str = Form(default=""),
        client_id: str = Form(None),
        client_secret: str = Form(None),
        captcha: str = Form(None)  # 新增验证码字段
    ):
        super().__init__(
            username=username,
            password=password,
            grant_type=grant_type,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret
        )
        self.captcha = captcha