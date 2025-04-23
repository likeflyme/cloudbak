from typing import List

from fastapi import APIRouter, Depends

from app.dependencies.auth_dep import get_wx_client
from app.exception.biz_exception import BizException
from wx.common.filters.fts_filter import FtsFilterObj
from wx.common.output.fts import FtsMsgCountTop, FtsMsgCount, FtsMsgCross
from wx.interface.wx_interface import ClientInterface

router = APIRouter(
    prefix="/fts"
)


@router.get("/msgs-match-top5", response_model=FtsMsgCountTop)
def msgs_match_top5(match: str, client: ClientInterface = Depends(get_wx_client)):
    """
    搜索前匹配数量与前5条数据
    """
    fts_manager = client.get_fts_manager()
    if fts_manager is None:
        raise BizException("该微信版本暂不支持全文搜索")
    contact_msgs = fts_manager.fts_search(match)

    totalCount = len(contact_msgs)
    if totalCount <= 5:
        return FtsMsgCountTop(total_count=totalCount, contact_list=contact_msgs)
    return FtsMsgCountTop(total_count=totalCount, contact_list=contact_msgs[:5])


@router.get("/msgs-match", response_model=List[FtsMsgCount])
def msgs_match(match: str, client: ClientInterface = Depends(get_wx_client)):
    """
    搜索
    """
    fts_manager = client.get_fts_manager()
    return fts_manager.fts_search(match)


@router.post("/msgs-split", response_model=FtsMsgCross)
def msgs_split(filter_obj: FtsFilterObj, client: ClientInterface = Depends(get_wx_client)):
    """
    聊天分页搜索
    """
    fts_manager = client.get_fts_manager()
    return fts_manager.fts_messages(filter_obj)

