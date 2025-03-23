from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
from app.models.api_models import BaseResponse, DataResponse, StatusEnum
from ..dependencies.ai_dependencies import get_ai_service, AIService
from ...core.agents.composite.chain_agent import ChainAgent

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chain",
    tags=["代理链"],
    responses={404: {"description": "Not found"}},
)

class TextToSocialRequest(BaseModel):
    """文本到社交分析请求模型"""
    text: str = Field(..., description="分析主题或关键词")
    content_type: str = Field("社交媒体帖子", description="内容类型")
    platform: str = Field("小红书", description="目标平台")
    analysis_type: str = Field("sentiment", description="分析类型")
    
class SocialToEcommerceRequest(BaseModel):
    """社交到电商请求模型"""
    keyword: str = Field(..., description="搜索关键词")
    platform: str = Field("小红书", description="社交媒体平台")
    search_count: int = Field(5, description="社交搜索结果数量")
    ecommerce_platform: str = Field("淘宝", description="电商平台")
    
class MarketResearchRequest(BaseModel):
    """市场研究请求模型"""
    product: str = Field(..., description="产品名称或类别")
    target_audience: str = Field("年轻女性", description="目标受众")
    social_platform: str = Field("小红书", description="社交媒体平台")
    ecommerce_platform: str = Field("淘宝", description="电商平台")
    
class ChainConfigRequest(BaseModel):
    """链配置请求模型"""
    type: str = Field(..., description="链类型")
    params: Dict[str, Any] = Field({}, description="链参数")


@router.post("/text-to-social", response_model=DataResponse)
async def text_to_social_analysis(request: TextToSocialRequest = Body(...)):
    """
    执行文本到社交分析链
    
    首先使用TextAgent创建内容，然后将输出传给SocialAgent进行分析
    """
    try:
        result = await ChainAgent.text_to_social_analysis(
            text=request.text,
            content_type=request.content_type,
            platform=request.platform,
            analysis_type=request.analysis_type
        )
        
        if result.get("status") == "success":
            return DataResponse(
                status=StatusEnum.SUCCESS,
                message=result.get("message", "文本到社交分析链执行成功"),
                data=result
            )
        else:
            return DataResponse(
                status=StatusEnum.ERROR,
                message=result.get("message", "文本到社交分析链执行失败"),
                data=result
            )
    except Exception as e:
        logger.error(f"文本到社交分析链错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "文本到社交分析链执行失败",
                "error": str(e)
            }
        )
        
@router.post("/social-to-ecommerce", response_model=DataResponse)
async def social_to_ecommerce(request: SocialToEcommerceRequest = Body(...)):
    """
    执行社交到电商链
    
    首先使用SocialAgent搜索社交媒体平台，然后将结果传给EcommerceAgent进行产品搜索
    """
    try:
        result = await ChainAgent.social_to_ecommerce(
            keyword=request.keyword,
            platform=request.platform,
            search_count=request.search_count,
            ecommerce_platform=request.ecommerce_platform
        )
        
        if result.get("status") == "success":
            return DataResponse(
                status=StatusEnum.SUCCESS,
                message=result.get("message", "社交到电商链执行成功"),
                data=result
            )
        else:
            return DataResponse(
                status=StatusEnum.ERROR,
                message=result.get("message", "社交到电商链执行失败"),
                data=result
            )
    except Exception as e:
        logger.error(f"社交到电商链错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "社交到电商链执行失败",
                "error": str(e)
            }
        )
        
@router.post("/market-research", response_model=DataResponse)
async def advanced_market_research(request: MarketResearchRequest = Body(...)):
    """
    执行高级市场研究链
    
    执行多步骤的市场研究：社交媒体趋势 -> 电商产品分析 -> 文本总结
    """
    try:
        result = await ChainAgent.advanced_market_research(
            product=request.product,
            target_audience=request.target_audience,
            social_platform=request.social_platform,
            ecommerce_platform=request.ecommerce_platform
        )
        
        if result.get("status") == "success":
            return DataResponse(
                status=StatusEnum.SUCCESS,
                message=result.get("message", "高级市场研究执行成功"),
                data=result
            )
        else:
            return DataResponse(
                status=StatusEnum.ERROR,
                message=result.get("message", "高级市场研究执行失败"),
                data=result
            )
    except Exception as e:
        logger.error(f"高级市场研究错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "高级市场研究执行失败",
                "error": str(e)
            }
        )
        
@router.post("/custom", response_model=DataResponse)
async def custom_chain(request: ChainConfigRequest = Body(...)):
    """
    执行自定义Agent链
    
    基于配置动态创建和执行Agent处理链
    """
    try:
        # 获取链函数
        chain_func = await ChainAgent.create_agent_chain({"type": request.type})
        
        # 执行链
        result = await chain_func(**request.params)
        
        if result.get("status") == "success":
            return DataResponse(
                status=StatusEnum.SUCCESS,
                message=result.get("message", "自定义链执行成功"),
                data=result
            )
        else:
            return DataResponse(
                status=StatusEnum.ERROR,
                message=result.get("message", "自定义链执行失败"),
                data=result
            )
    except Exception as e:
        logger.error(f"自定义链错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "自定义链执行失败",
                "error": str(e)
            }
        ) 