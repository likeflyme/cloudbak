# exception_handlers.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exception.auth_exception import LoginException
from app.services.event_service import record_event
from config.log_config import logger


async def login_exception_handler(request: Request, exc: LoginException):
    logger.error(f"Login error occurred: {exc.detail}")
    # 记录登录错误事件
    try:
        record_event(exc.event_type, exc.key, exc.detail)
    except Exception as e:
        logger.error(f"Unexpected error occurred when record LoginException event: {str(e)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    if exc.status_code == 404:
        raise exc
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error occurred: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error, {str(exc)}"},
    )
