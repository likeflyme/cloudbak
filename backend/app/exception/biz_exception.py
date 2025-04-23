from fastapi import HTTPException


class IllegalArgumentsException(HTTPException):
    status_code = 462
    detail = ''

    def __init__(self, detail, status_code=462):
        self.detail = detail
        self.status_code = status_code
        super(IllegalArgumentsException, self).__init__(status_code=self.status_code, detail=detail)


class BizException(HTTPException):
    status_code = 470
    detail = ''

    def __init__(self, detail, status_code=470):
        self.detail = detail
        self.status_code = status_code
        super(BizException, self).__init__(status_code=self.status_code, detail=detail)


