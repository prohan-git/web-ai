from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.models.api_models import (ChatRequest, ChatResponse, CompetitionAnalysisRequest, ContentIdeasRequest, CreatorAnalysisRequest, DataAnalysisRequest)
from app.models.api_models import(InspirationRequest, ListingGenerationRequest, ProductPotentialRequest, ProductSearchRequest, SentimentMonitorRequest)
from app.models.api_models import(SimilarCreatorsRequest, SocialDataRequest, SupplierSearchRequest, TaskRequest, TaskResponse, TemplateTaskRequest, TrendingContentRequest)
from ...core.ai_agent.chat_agent import ChatAgent
from ...core.ai_agent.task_agent import TaskAgent
from ...core.ai_agent.social_agent import SocialAgent
from ...core.ai_agent.ecommerce_agent import EcommerceAgent
from typing import Optional, List, Dict, Any
import logging

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

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    基础对话接口
    """
    try:
        response = await ChatAgent.chat(
            message=request.message,
            session_id=request.session_id
        )
        logger.info(f"Chat API 成功处理消息，session_id: {request.session_id}")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Chat API错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/task", response_model=TaskResponse)
async def execute_task(request: TaskRequest, req: Request):
    """
    执行特定任务接口
    """
    try:
        result = await TaskAgent.execute_task(
            task=request.task,
            use_vision=request.use_vision
        )
        return TaskResponse(**result)
    except Exception as e:
        # 记录详细错误日志
        logger.error(f"Task API错误 - {req.url.path}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "任务执行失败",
                "error": str(e)
            }
        )

@router.post("/task/template", response_model=TaskResponse)
async def execute_template_task(request: TemplateTaskRequest):
    """
    使用预定义模板执行任务
    """
    try:
        result = await TaskAgent.execute_template_task(
            template_name=request.template_name,
            use_vision=request.use_vision,
            **request.template_params
        )
        return TaskResponse(**result)
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
@router.post("/social/collect", response_model=Dict[str, Any])
async def collect_social_data(request: SocialDataRequest):
    """
    从社交媒体平台收集数据
    """
    try:
        result = await SocialAgent.collect_from_platform(
            platform=request.platform,
            task_type=request.task_type,
            use_vision=request.use_vision,
            **request.params
        )
        return result
    except Exception as e:
        logger.error(f"社交数据收集错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "社交数据收集失败",
                "error": str(e)
            }
        )

@router.post("/social/monitor", response_model=Dict[str, Any])
async def monitor_sentiment(request: SentimentMonitorRequest):
    """
    监控社交媒体平台的舆情
    """
    try:
        result = await SocialAgent.monitor_sentiment(
            keywords=request.keywords,
            platforms=request.platforms
        )
        return result
    except Exception as e:
        logger.error(f"舆情监控错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "舆情监控失败",
                "error": str(e)
            }
        )

@router.post("/social/analyze", response_model=Dict[str, Any])
async def analyze_data(request: DataAnalysisRequest):
    """
    分析收集到的数据
    """
    try:
        result = await SocialAgent.analyze_data(
            data=request.data,
            analysis_type=request.analysis_type
        )
        return result
    except Exception as e:
        logger.error(f"数据分析错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "数据分析失败",
                "error": str(e)
            }
        )

@router.post("/social/trending", response_model=Dict[str, Any])
async def find_trending_content(request: TrendingContentRequest):
    """
    查找某领域的热门/趋势内容
    """
    try:
        result = await SocialAgent.find_trending_content(
            platform=request.platform,
            niche=request.niche,
            count=request.count,
            time_period=request.time_period,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"查找热门内容错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "查找热门内容失败",
                "error": str(e)
            }
        )

@router.post("/social/similar-creators", response_model=Dict[str, Any])
async def find_similar_creators(request: SimilarCreatorsRequest):
    """
    查找相似创作者
    """
    try:
        result = await SocialAgent.find_similar_creators(
            platform=request.platform,
            creator=request.creator,
            count=request.count,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"查找相似创作者错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "查找相似创作者失败",
                "error": str(e)
            }
        )

@router.post("/social/content-ideas", response_model=Dict[str, Any])
async def generate_content_ideas(request: ContentIdeasRequest):
    """
    生成内容创作灵感
    """
    try:
        result = await SocialAgent.generate_content_ideas(
            platform=request.platform,
            niche=request.niche,
            keywords=request.keywords,
            count=request.count
        )
        return result
    except Exception as e:
        logger.error(f"生成内容灵感错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成内容灵感失败",
                "error": str(e)
            }
        )

@router.post("/social/creator-analysis", response_model=Dict[str, Any])
async def analyze_creator(request: CreatorAnalysisRequest):
    """
    分析创作者增长数据
    """
    try:
        result = await SocialAgent.analyze_creator_growth(
            platform=request.platform,
            creator=request.creator,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"创作者分析错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "创作者分析失败",
                "error": str(e)
            }
        )

@router.post("/social/inspiration", response_model=Dict[str, Any])
async def collect_inspiration(request: InspirationRequest):
    """
    从多个平台收集创意灵感
    """
    try:
        result = await SocialAgent.collect_inspiration(
            keywords=request.keywords,
            sources=request.sources,
            count_per_source=request.count_per_source,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"收集灵感错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "收集灵感失败",
                "error": str(e)
            }
        )

# 电商API
@router.post("/ecommerce/products", response_model=Dict[str, Any])
async def search_products(request: ProductSearchRequest):
    """
    在电商平台搜索产品
    """
    try:
        result = await EcommerceAgent.search_products(
            platform=request.platform,
            task_type=request.task_type,
            use_vision=request.use_vision,
            **request.params
        )
        return result
    except Exception as e:
        logger.error(f"产品搜索错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "产品搜索失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/listing", response_model=Dict[str, Any])
async def generate_listing(request: ListingGenerationRequest):
    """
    生成电商上货素材
    """
    try:
        # 构建参数字典，排除None值
        params = {k: v for k, v in request.dict().items() if v is not None and k != "template_type"}
        
        result = await EcommerceAgent.generate_listing(
            template_type=request.template_type,
            **params
        )
        return result
    except Exception as e:
        logger.error(f"生成上货素材错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成上货素材失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/product-potential", response_model=Dict[str, Any])
async def analyze_product_potential(request: ProductPotentialRequest):
    """
    分析产品潜力
    """
    try:
        result = await EcommerceAgent.analyze_product_potential(
            product_info=request.product_info,
            niche=request.niche,
            platform=request.platform,
            dimensions=request.dimensions
        )
        return result
    except Exception as e:
        logger.error(f"产品潜力分析错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "产品潜力分析失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/competition", response_model=Dict[str, Any])
async def analyze_competition(request: CompetitionAnalysisRequest):
    """
    分析竞品情况
    """
    try:
        result = await EcommerceAgent.analyze_competition(
            product_keyword=request.product_keyword,
            platform=request.platform,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"竞品分析错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "竞品分析失败",
                "error": str(e)
            }
        )

@router.post("/ecommerce/suppliers", response_model=Dict[str, Any])
async def find_suppliers(request: SupplierSearchRequest):
    """
    查找产品供应商
    """
    try:
        result = await EcommerceAgent.find_suppliers(
            product=request.product,
            count=request.count,
            use_vision=request.use_vision
        )
        return result
    except Exception as e:
        logger.error(f"供应商查找错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "供应商查找失败",
                "error": str(e)
            }
        )