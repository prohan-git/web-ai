from typing import Dict, Any, List, Optional, Callable, Type, TypeVar
from langchain_openai import ChatOpenAI
from ...config.config_manager import ConfigManager
from ...core.agents.browser.browser_task_agent import BrowserTaskAgent
from ...core.agents.browser.social_agent import SocialAgent
from ...core.agents.browser.ecommerce_agent import EcommerceAgent
from ...core.agents.chat.chat_agent import ChatAgent
from fastapi import Depends

# 定义泛型类型变量
T = TypeVar('T')

class AgentFactory:
    """AI代理工厂类，用于创建和管理AI代理实例"""
    
    _instances: Dict[Type, Any] = {}
    
    @classmethod
    def get_agent(cls, agent_class: Type[T]) -> T:
        """
        获取指定类型的代理实例，使用单例模式
        
        Args:
            agent_class: 代理类类型
            
        Returns:
            代理类实例
        """
        if agent_class not in cls._instances:
            cls._instances[agent_class] = agent_class()
        return cls._instances[agent_class]
    
    @classmethod
    def get_social_agent(cls) -> SocialAgent:
        """获取SocialAgent实例"""
        return cls.get_agent(SocialAgent)
    
    @classmethod
    def get_ecommerce_agent(cls) -> EcommerceAgent:
        """获取EcommerceAgent实例"""
        return cls.get_agent(EcommerceAgent)
    
    @classmethod
    def get_chat_agent(cls) -> ChatAgent:
        """获取ChatAgent实例"""
        return cls.get_agent(ChatAgent)


def get_llm() -> ChatOpenAI:
    """获取LLM实例的依赖函数"""
    llm_config = ConfigManager.get_llm_config()
    return ChatOpenAI(
        base_url=llm_config["base_url"],
        model=llm_config["model"],
        api_key=llm_config["api_key"]
    )


def get_social_agent() -> SocialAgent:
    """获取SocialAgent实例的依赖函数"""
    return AgentFactory.get_social_agent()


def get_ecommerce_agent() -> EcommerceAgent:
    """获取EcommerceAgent实例的依赖函数"""
    return AgentFactory.get_ecommerce_agent()


def get_chat_agent() -> ChatAgent:
    """获取ChatAgent实例的依赖函数"""
    return AgentFactory.get_chat_agent()


class AIService:
    """
    AI服务类，提供统一的AI服务接口
    
    使用依赖注入方式获取所需的代理实例
    """
    
    def __init__(
        self,
        social_agent: SocialAgent = Depends(get_social_agent),
        ecommerce_agent: EcommerceAgent = Depends(get_ecommerce_agent),
        chat_agent: ChatAgent = Depends(get_chat_agent),
        llm: ChatOpenAI = Depends(get_llm)
    ):
        self.social_agent = social_agent
        self.ecommerce_agent = ecommerce_agent
        self.chat_agent = chat_agent
        self.llm = llm
    
    # 聊天相关方法
    async def chat(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """处理聊天消息"""
        return await self.chat_agent.process_message(message, session_id)
    
    # 通用任务方法
    async def execute_task(self, task: str, use_vision: bool = False) -> Dict[str, Any]:
        """执行通用任务"""
        return await self.social_agent.execute_task(task, use_vision)
    
    async def execute_template_task(
        self, 
        template_name: str, 
        parameters: Dict[str, Any],
        use_vision: bool = False, 
        system_prompt_extension: Optional[str] = None
    ) -> Dict[str, Any]:
        """使用预定义模板执行任务"""
        return await self.social_agent.execute_template_task(
            template_name=template_name,
            parameters=parameters,
            use_vision=use_vision,
            system_prompt_extension=system_prompt_extension
        )
    
    # 社交媒体相关方法
    async def collect_social_data(
        self, platform: str, task_type: str, use_vision: bool = True, **params
    ) -> Dict[str, Any]:
        """从社交媒体平台收集数据"""
        return await self.social_agent.collect_from_platform(platform, task_type, use_vision, **params)
    
    async def monitor_sentiment(
        self, keywords: List[str], platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """监控社交媒体平台的舆情"""
        return await self.social_agent.monitor_sentiment(keywords, platforms)
    
    async def analyze_social_data(
        self, data: str, analysis_type: str = "sentiment"
    ) -> Dict[str, Any]:
        """分析社交媒体数据"""
        return await self.social_agent.analyze_data(data, analysis_type)
    
    async def find_trending_content(
        self, platform: str, niche: str, count: int = 10, 
        time_period: str = "本周", use_vision: bool = True
    ) -> Dict[str, Any]:
        """查找热门内容"""
        return await self.social_agent.find_trending_content(
            platform, niche, count, time_period, use_vision
        )
    
    async def find_similar_creators(
        self, platform: str, creator: str, count: int = 5, use_vision: bool = True
    ) -> Dict[str, Any]:
        """查找相似创作者"""
        return await self.social_agent.find_similar_creators(
            platform, creator, count, use_vision
        )
    
    async def generate_content_ideas(
        self, platform: str, niche: str, keywords: List[str], count: int = 5
    ) -> Dict[str, Any]:
        """生成内容创意"""
        return await self.social_agent.generate_content_ideas(
            platform, niche, keywords, count
        )
    
    async def analyze_creator(
        self, platform: str, creator: str, use_vision: bool = True
    ) -> Dict[str, Any]:
        """分析创作者"""
        return await self.social_agent.analyze_creator(
            platform, creator, use_vision
        )
    
    async def collect_inspiration(
        self, keywords: List[str], sources: List[str], 
        count_per_source: int = 3, use_vision: bool = True
    ) -> Dict[str, Any]:
        """收集灵感素材"""
        return await self.social_agent.collect_inspiration(
            keywords, sources, count_per_source, use_vision
        )
    
    # 电商相关方法
    async def search_products(
        self, platform: str, task_type: str, use_vision: bool = True, **params
    ) -> Dict[str, Any]:
        """在电商平台搜索产品"""
        return await self.ecommerce_agent.search_products(platform, task_type, use_vision, **params)
    
    async def generate_listing(
        self, template_type: str, product: str, features: List[str],
        platform: str = None, description: str = None,
        cost: float = None, competitor_prices: List[float] = None
    ) -> Dict[str, Any]:
        """生成产品listing"""
        return await self.ecommerce_agent.generate_listing(
            template_type, product, features, platform, 
            description, cost, competitor_prices
        )
    
    async def analyze_product_potential(
        self, product_info: str, niche: str, platform: str, 
        dimensions: List[str] = None
    ) -> Dict[str, Any]:
        """分析产品潜力"""
        return await self.ecommerce_agent.analyze_product_potential(
            product_info, niche, platform, dimensions
        )
    
    async def analyze_competition(
        self, product_keyword: str, platform: str, use_vision: bool = True
    ) -> Dict[str, Any]:
        """分析竞争情况"""
        return await self.ecommerce_agent.analyze_competition(
            product_keyword, platform, use_vision
        )
    
    async def find_suppliers(
        self, product: str, count: int = 5, use_vision: bool = True
    ) -> Dict[str, Any]:
        """查找供应商"""
        return await self.ecommerce_agent.find_suppliers(
            product, count, use_vision
        )


def get_ai_service(
    social_agent: SocialAgent = Depends(get_social_agent),
    ecommerce_agent: EcommerceAgent = Depends(get_ecommerce_agent),
    chat_agent: ChatAgent = Depends(get_chat_agent),
    llm: ChatOpenAI = Depends(get_llm)
) -> AIService:
    """获取AIService实例的依赖函数"""
    return AIService(social_agent, ecommerce_agent, chat_agent, llm) 