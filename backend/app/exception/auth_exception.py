from fastapi import HTTPException

from app.enum.event_enum import EventType


class LoginException(HTTPException):
    status_code = 401
    detail = ''
    key = ''
    event_type = EventType.LOGIN_FAIL

    def __init__(self, detail, status_code=401, key=''):
        self.detail = detail
        self.status_code = status_code
        self.key = key
        super(LoginException, self).__init__(status_code=self.status_code, detail=detail)

