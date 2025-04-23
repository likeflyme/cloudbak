from fastapi import Request

from config.log_config import set_log_id, logger


async def add_request_id(request: Request, call_next):
    """
    为每个请求生成一个唯一的 request_id
    :param request:
    :param call_next:
    :return:
    """
    set_log_id()

    logger.info('%s %s', request.method, request.url.path)

    response = await call_next(request)

    logger.info('Response code: %s', response.status_code)
    return response
