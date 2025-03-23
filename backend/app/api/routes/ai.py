from fastapi import APIRouter, HTTPException, Request, Depends, Body, Query
from pydantic import BaseModel
from app.models.api_models import (ChatRequest, ChatResponse, CompetitionAnalysisRequest, ContentIdeasRequest, CreatorAnalysisRequest, DataAnalysisRequest)
from app.models.api_models import(InspirationRequest, ListingGenerationRequest, ProductPotentialRequest, ProductSearchRequest, SentimentMonitorRequest)
from app.models.api_models import(SimilarCreatorsRequest, SocialDataRequest, SupplierSearchRequest, TaskRequest, TaskResponse, TemplateTaskRequest, TrendingContentRequest)
from app.models.api_models import StatusEnum, BaseResponse, DataResponse
from ..dependencies.ai_dependencies import AIService, get_ai_service
from typing import Optional, List, Dict, Any
import logging
from ...core.agents.chat.chat_agent import ChatAgent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


# 创建路由器
router = APIRouter(
    prefix="/ai",
    tags=["AI服务"],
    responses={404: {"description": "Not found"}},
)

@router.post("/chat", response_model=BaseResponse)
async def chat(
    request: ChatRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    与AI聊天
    """
    try:
        # 使用AIService中的chat方法
        result = await ai_service.chat(request.message, request.session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天处理错误: {str(e)}")

@router.post("/task", response_model=BaseResponse)
async def execute_task(
    request: TaskRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    执行通用任务
    """
    try:
        result = await ai_service.execute_task(request.task, request.use_vision)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务执行错误: {str(e)}")

@router.post("/task/template", response_model=TaskResponse)
async def execute_template_task(
    request: TemplateTaskRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    使用预定义模板执行任务
    """
    try:
        # 使用AIService执行模板任务
        result = await ai_service.execute_template_task(
            template_name=request.template_name,
            parameters=request.parameters,
            use_vision=request.use_vision,
            system_prompt_extension=request.system_prompt_extension
        )
        
        if isinstance(result, dict) and "status" in result and "message" in result:
            # 确保响应字段一致性
            result["status"] = StatusEnum.SUCCESS if result["status"] == "success" else StatusEnum.ERROR
            return TaskResponse(**result)
        else:
            # 处理不符合预期的返回值
            return TaskResponse(
                status=StatusEnum.SUCCESS,
                message="模板任务执行成功",
                task=request.template_name,
                use_vision=request.use_vision,
                result=str(result) if result else None
            )
    except ValueError as e:
        logger.error(f"模板任务错误: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "模板任务执行失败",
                "error": str(e)
            }
        )
    except Exception as e:
        logger.error(f"模板任务未知错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "模板任务执行失败",
                "error": str(e)
            }
        )

# 社交媒体API
@router.post("/social/collect", response_model=BaseResponse)
async def collect_social_data(
    request: SocialDataRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    从社交媒体平台收集数据
    """
    try:
        # 调用AIService收集社交数据
        result = await ai_service.collect_social_data(
            platform=request.platform,
            task_type=request.task_type,
            use_vision=request.use_vision,
            **request.params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"社交数据收集错误: {str(e)}")

@router.post("/social/monitor", response_model=BaseResponse)
async def monitor_sentiment(
    request: SentimentMonitorRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    监控社交媒体舆情
    """
    try:
        result = await ai_service.monitor_sentiment(
            keywords=request.keywords,
            platforms=request.platforms
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"舆情监控错误: {str(e)}")

@router.post("/social/analyze", response_model=BaseResponse)
async def analyze_social_data(
    request: DataAnalysisRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    分析社交媒体数据
    """
    try:
        result = await ai_service.analyze_social_data(
            data=request.data,
            analysis_type=request.analysis_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"社交数据分析错误: {str(e)}")

@router.post("/social/trending", response_model=BaseResponse)
async def find_trending_content(
    request: TrendingContentRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    查找热门内容
    """
    try:
        result = await ai_service.find_trending_content(
            platform=request.platform,
            niche=request.niche,
            count=request.count,
            time_period=request.time_period,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查找热门内容错误: {str(e)}")

@router.post("/social/similar-creators", response_model=BaseResponse)
async def find_similar_creators(
    request: SimilarCreatorsRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    查找相似创作者
    """
    try:
        result = await ai_service.find_similar_creators(
            platform=request.platform,
            creator=request.creator,
            count=request.count,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查找相似创作者错误: {str(e)}")

@router.post("/social/content-ideas", response_model=DataResponse)
async def generate_content_ideas(
    request: ContentIdeasRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    生成内容创意
    """
    try:
        result = await ai_service.generate_content_ideas(
            platform=request.platform,
            niche=request.niche,
            keywords=request.keywords,
            count=request.count
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已为{request.platform}平台生成{request.niche}领域的内容创意",
            data=result
        )
    except Exception as e:
        logger.error(f"生成内容创意错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成内容创意失败",
                "error": str(e)
            }
        )

@router.post("/social/creator-analysis", response_model=DataResponse)
async def analyze_creator(
    request: CreatorAnalysisRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    分析创作者
    """
    try:
        result = await ai_service.analyze_creator(
            platform=request.platform,
            creator=request.creator,
            use_vision=request.use_vision
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已完成对{request.platform}平台创作者{request.creator}的分析",
            data=result
        )
    except Exception as e:
        logger.error(f"分析创作者错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "分析创作者失败",
                "error": str(e)
            }
        )

@router.post("/social/inspiration", response_model=DataResponse)
async def collect_inspiration(
    request: InspirationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    收集灵感素材
    """
    try:
        result = await ai_service.collect_inspiration(
            keywords=request.keywords,
            sources=request.sources,
            count_per_source=request.count_per_source,
            use_vision=request.use_vision
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message="灵感素材收集完成",
            data=result
        )
    except Exception as e:
        logger.error(f"收集灵感素材错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "收集灵感素材失败",
                "error": str(e)
            }
        )

# 电商API
@router.post("/ecommerce/products", response_model=BaseResponse)
async def search_products(
    request: ProductSearchRequest = Body(...),
    ai_service: AIService = Depends(get_ai_service)
) -> Dict[str, Any]:
    """
    搜索电商产品
    """
    try:
        result = await ai_service.search_products(
            platform=request.platform,
            task_type=request.task_type,
            use_vision=request.use_vision,
            **request.params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"产品搜索错误: {str(e)}")

@router.post("/ecommerce/listing", response_model=DataResponse)
async def generate_listing(
    request: ListingGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    生成产品listing
    """
    try:
        result = await ai_service.generate_listing(
            template_type=request.template_type,
            product=request.product,
            features=request.features,
            platform=request.platform,
            description=request.description,
            cost=request.cost,
            competitor_prices=request.competitor_prices
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已为产品{request.product}生成listing",
            data=result
        )
    except Exception as e:
        logger.error(f"生成listing错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成listing失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/product-potential", response_model=DataResponse)
async def analyze_product_potential(
    request: ProductPotentialRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    分析产品潜力
    """
    try:
        result = await ai_service.analyze_product_potential(
            product_info=request.product_info,
            niche=request.niche,
            platform=request.platform,
            dimensions=request.dimensions
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已完成对{request.niche}领域产品的潜力分析",
            data=result
        )
    except Exception as e:
        logger.error(f"分析产品潜力错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "分析产品潜力失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/competition", response_model=DataResponse)
async def analyze_competition(
    request: CompetitionAnalysisRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    分析竞争情况
    """
    try:
        result = await ai_service.analyze_competition(
            product_keyword=request.product_keyword,
            platform=request.platform,
            use_vision=request.use_vision
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已完成{request.platform}平台关于{request.product_keyword}的竞争分析",
            data=result
        )
    except Exception as e:
        logger.error(f"分析竞争情况错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "分析竞争情况失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/suppliers", response_model=DataResponse)
async def find_suppliers(
    request: SupplierSearchRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    查找供应商
    """
    try:
        result = await ai_service.find_suppliers(
            product=request.product,
            count=request.count,
            use_vision=request.use_vision
        )
        return DataResponse(
            status=StatusEnum.SUCCESS,
            message=f"已找到{request.product}的供应商信息",
            data=result
        )
    except Exception as e:
        logger.error(f"查找供应商错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "查找供应商失败",
                "error": str(e)
            }
        )