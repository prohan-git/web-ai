from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from enum import Enum

# 状态枚举类型，用于统一响应状态
class StatusEnum(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"

# 基础响应模型
class BaseResponse(BaseModel):
    """基础响应模型，所有API响应都应继承此模型"""
    status: StatusEnum = Field(..., description="响应状态: success/error/pending")
    message: str = Field(..., description="响应信息")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "操作成功"
            }
        }

# 通用数据响应模型
class DataResponse(BaseResponse):
    """带数据的响应模型"""
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")

# 定义请求和响应模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息")
    session_id: Optional[str] = Field("default", description="会话ID，用于区分不同对话")

class ChatResponse(BaseResponse):
    """聊天响应模型"""
    response: str = Field(..., description="AI回复内容")

# Task相关模型
class TaskRequest(BaseModel):
    """任务执行请求"""
    task: str = Field(..., description="需要执行的任务描述")
    use_vision: bool = Field(False, description="是否启用视觉能力")
    system_prompt_extension: Optional[str] = Field(None, description="系统提示词扩展")

class TemplateTaskRequest(BaseModel):
    """模板任务执行请求"""
    template_name: str = Field(..., description="模板名称")
    parameters: Dict[str, Any] = Field(..., description="模板参数")
    use_vision: bool = Field(False, description="是否启用视觉能力")
    system_prompt_extension: Optional[str] = Field(None, description="系统提示词扩展")

class TaskResponse(BaseResponse):
    """任务执行响应"""
    result: Optional[str] = Field(None, description="任务执行结果")
    task: str = Field(..., description="任务描述")
    use_vision: bool = Field(..., description="是否启用了视觉能力")

# 社交媒体相关模型
class SocialDataRequest(BaseModel):
    """社交数据请求模型"""
    platform: str = Field(..., description="社交媒体平台名称")
    task_type: str = Field(..., description="任务类型")
    params: Dict[str, Any] = Field(..., description="任务参数")
    use_vision: bool = Field(True, description="是否启用视觉能力")
    
# 数据提取模型
class ProductData(BaseModel):
    """电商产品数据模型"""
    title: str = Field(..., description="产品标题")
    price: str = Field(..., description="产品价格")
    platform: str = Field(..., description="平台名称")
    url: Optional[str] = Field(None, description="产品链接")
    rating: Optional[str] = Field(None, description="产品评分")
    reviews_count: Optional[str] = Field(None, description="评论数量")
    seller: Optional[str] = Field(None, description="卖家信息")

class SocialMediaPost(BaseModel):
    """社交媒体帖子数据模型"""
    platform: str = Field(..., description="平台名称")
    creator: str = Field(..., description="创作者")
    content: str = Field(..., description="内容")
    likes: Optional[str] = Field(None, description="点赞数")
    comments: Optional[str] = Field(None, description="评论数")
    post_url: Optional[str] = Field(None, description="帖子链接")
    post_date: Optional[str] = Field(None, description="发布日期")

class SentimentMonitorRequest(BaseModel):
    """舆情监控请求"""
    keywords: List[str] = Field(..., description="监控关键词列表")
    platforms: Optional[List[str]] = Field(None, description="监控平台列表")

class DataAnalysisRequest(BaseModel):
    """数据分析请求"""
    data: str = Field(..., description="要分析的数据")
    analysis_type: str = Field("sentiment", description="分析类型, 默认为情感分析")

class TrendingContentRequest(BaseModel):
    """热门内容请求"""
    platform: str = Field(..., description="社交媒体平台")
    niche: str = Field(..., description="内容领域")
    count: int = Field(10, description="返回内容数量", ge=1, le=50)
    time_period: str = Field("本周", description="时间周期")
    use_vision: bool = Field(True, description="是否启用视觉能力")

class SimilarCreatorsRequest(BaseModel):
    """相似创作者请求"""
    platform: str = Field(..., description="社交媒体平台")
    creator: str = Field(..., description="参照创作者")
    count: int = Field(5, description="返回创作者数量", ge=1, le=20)
    use_vision: bool = Field(True, description="是否启用视觉能力")

class ContentIdeasRequest(BaseModel):
    """内容灵感请求"""
    platform: str = Field(..., description="目标平台")
    niche: str = Field(..., description="内容领域")
    keywords: List[str] = Field(..., description="相关关键词")
    count: int = Field(10, description="生成创意数量", ge=1, le=30)

class CreatorAnalysisRequest(BaseModel):
    """创作者分析请求"""
    platform: str = Field(..., description="社交媒体平台")
    creator: str = Field(..., description="创作者ID或用户名")
    use_vision: bool = Field(True, description="是否启用视觉能力")

class InspirationRequest(BaseModel):
    """灵感请求"""
    keywords: List[str] = Field(..., description="相关关键词")
    sources: List[str] = Field(["Pinterest", "Instagram"], description="灵感来源平台")
    count_per_source: int = Field(5, description="每个来源返回的灵感数量", ge=1, le=20)
    use_vision: bool = Field(True, description="是否启用视觉能力")

# 电商相关模型
class ProductSearchRequest(BaseModel):
    """产品搜索请求"""
    platform: str = Field(..., description="电商平台")
    query: str = Field(..., description="搜索关键词")
    max_results: int = Field(10, description="最大结果数量")
    sort_by: str = Field("relevance", description="排序方式 (relevance, price_low, price_high, rating, sales)")
    use_vision: bool = Field(True, description="是否启用视觉能力")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件 (如价格范围、品牌等)")

class ListingGenerationRequest(BaseModel):
    """列表生成请求"""
    template_type: str = Field(..., description="模板类型")
    product: str = Field(..., description="产品名称")
    features: Optional[str] = Field(None, description="产品特性")
    platform: Optional[str] = Field(None, description="目标平台")
    description: Optional[str] = Field(None, description="产品描述")
    cost: Optional[float] = Field(None, description="产品成本", ge=0)
    competitor_prices: Optional[str] = Field(None, description="竞品价格信息")

class ProductPotentialRequest(BaseModel):
    """产品潜力分析请求"""
    product_info: str = Field(..., description="产品信息")
    niche: str = Field(..., description="产品领域")
    platform: str = Field("全平台", description="目标平台")
    dimensions: Optional[List[str]] = Field(None, description="分析维度")

class CompetitionAnalysisRequest(BaseModel):
    """竞争分析请求"""
    product_keyword: str = Field(..., description="产品关键词")
    platform: str = Field(..., description="电商平台")
    use_vision: bool = Field(True, description="是否启用视觉能力")

class SupplierSearchRequest(BaseModel):
    """供应商搜索请求"""
    product: str = Field(..., description="产品名称") 
    count: int = Field(5, description="返回供应商数量", ge=1, le=20)
    use_vision: bool = Field(True, description="是否启用视觉能力") 