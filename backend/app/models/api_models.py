from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union

# 基础响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    status: str
    message: str

# 定义请求和响应模型
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str

# Task相关模型 - 保留与agent_models.py中相同的定义，以便后续合并
class TaskRequest(BaseModel):
    """任务执行请求"""
    task: str
    use_vision: bool = False
    system_prompt_extension: Optional[str] = None

class TemplateTaskRequest(BaseModel):
    """模板任务执行请求"""
    template_name: str
    parameters: Dict[str, Any]
    use_vision: bool = False
    system_prompt_extension: Optional[str] = None

class TaskResponse(BaseModel):
    """任务执行响应"""
    status: str
    message: str
    result: Optional[str] = None
    task: str
    use_vision: bool

# 社交媒体相关模型
class SocialDataRequest(BaseModel):
    """社交数据请求"""
    platform: str
    task_type: str
    params: Dict[str, Any]
    use_vision: bool = True
    
    # 数据提取模型
class ProductData(BaseModel):
    """电商产品数据模型"""
    title: str
    price: str
    platform: str
    url: Optional[str] = None
    rating: Optional[str] = None
    reviews_count: Optional[str] = None
    seller: Optional[str] = None

class SocialMediaPost(BaseModel):
    """社交媒体帖子数据模型"""
    platform: str
    creator: str
    content: str
    likes: Optional[str] = None
    comments: Optional[str] = None
    post_url: Optional[str] = None
    post_date: Optional[str] = None 
    

class SentimentMonitorRequest(BaseModel):
    """舆情监控请求"""
    keywords: List[str]
    platforms: Optional[List[str]] = None

class DataAnalysisRequest(BaseModel):
    """数据分析请求"""
    data: str
    analysis_type: str = "sentiment"

class TrendingContentRequest(BaseModel):
    """热门内容请求"""
    platform: str
    niche: str
    count: int = 10
    time_period: str = "本周"
    use_vision: bool = True

class SimilarCreatorsRequest(BaseModel):
    """相似创作者请求"""
    platform: str
    creator: str
    count: int = 5
    use_vision: bool = True

class ContentIdeasRequest(BaseModel):
    """内容灵感请求"""
    platform: str
    niche: str
    keywords: List[str]
    count: int = 10

class CreatorAnalysisRequest(BaseModel):
    """创作者分析请求"""
    platform: str
    creator: str
    use_vision: bool = True

class InspirationRequest(BaseModel):
    """灵感请求"""
    keywords: List[str]
    sources: List[str] = ["Pinterest", "Instagram"]
    count_per_source: int = 5
    use_vision: bool = True

# 电商相关模型
class ProductSearchRequest(BaseModel):
    """产品搜索请求"""
    platform: str
    task_type: str
    params: Dict[str, Any]
    use_vision: bool = True

class ListingGenerationRequest(BaseModel):
    """列表生成请求"""
    template_type: str
    product: str
    features: Optional[str] = None
    platform: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    competitor_prices: Optional[str] = None

class ProductPotentialRequest(BaseModel):
    """产品潜力分析请求"""
    product_info: str
    niche: str
    platform: str = "全平台"
    dimensions: Optional[List[str]] = None

class CompetitionAnalysisRequest(BaseModel):
    """竞争分析请求"""
    product_keyword: str
    platform: str
    use_vision: bool = True

class SupplierSearchRequest(BaseModel):
    """供应商搜索请求"""
    product: str
    count: int = 5
    use_vision: bool = True 