from langchain_openai import ChatOpenAI
from browser_use import ActionResult, Agent, Browser, Controller
from ...config import settings
from typing import Optional, Dict, Any, List, Union
import logging

# 配置日志记录
logger = logging.getLogger(__name__)

# 初始化控制器
controller = Controller()

@controller.action('Ask user for information')
def ask_human(question: str) -> str:
    answer = input(f'\n{question}\nInput: ')
    return ActionResult(extracted_content=answer)


# @controller.action('Extract product data', param_model=ProductData)
# async def extract_product(params: ProductData, browser: Browser):
#     """提取并保存产品数据"""
#     logger.info(f"提取产品数据: {params.title} - ¥{params.price} 来自{params.platform}")
#     return ActionResult(extracted_content=f"成功提取产品: {params.title}")



# @controller.action('Extract social media post', param_model=SocialMediaPost)
# async def extract_social_post(params: SocialMediaPost, browser: Browser):
#     """提取并保存社交媒体帖子"""
#     logger.info(f"提取社交媒体内容 - 平台: {params.platform}, 创作者: {params.creator}")
#     return ActionResult(extracted_content=f"成功提取社交帖子: {params.content[:50]}...")


class TaskAgent:
    """
    浏览器任务 AI 代理类
    
    该类负责执行需要浏览器操作的任务，如网页爬取、数据收集等
    使用 browser_use 中的 Agent 类实现实际的浏览器操作
    """
    _instance: Optional[ChatOpenAI] = None
    
    # 默认系统提示扩展
    DEFAULT_SYSTEM_PROMPT_EXTENSION = """
    当执行任务时，请遵循以下指导原则：
    1. 始终验证所有提取的数据的准确性
    2. 记录重要事件或错误
    3. 尝试提供结构化数据作为结果
    4. 如果无法完成任务，提供详细的错误信息和原因
    """
    
    # 存储常见任务模板
    TASK_TEMPLATES = {
        "网页搜索": "搜索以下内容并返回前三个结果的摘要: {query}",
        "数据收集": "访问{url}并收集{data_type}信息",
        "舆情监控": "搜索并分析{keywords}的最新舆情信息，总结正面和负面评价",
        "社交媒体数据": "收集{platform}上关于{topic}的最新{count}条内容",
        "产品比较": "在{platform}上搜索{product}，比较前{count}个产品的价格、评分和特点",
        "商品详情": "访问{url}，提取产品名称、价格、卖家、评分和主要特点",
        "趋势分析": "在{platform}上分析{niche}类目的热门趋势，找出共同特征"
    }

    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        """获取 LLM 实例（单例模式）"""
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                base_url=settings.DEEPSEEK_API_BASE,
                model=settings.DEEPSEEK_MODEL,
                api_key=settings.DEEPSEEK_API_KEY
            )
        return cls._instance

    @classmethod
    async def execute_task(
        cls, 
        task: str, 
        use_vision: bool = False, 
        system_prompt_extension: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行浏览器任务
        
        Args:
            task: 要执行的任务描述
            use_vision: 是否使用视觉功能
            browser_options: 浏览器选项，如果为None则使用默认配置
            system_prompt_extension: 扩展系统提示以自定义Agent行为
            
        Returns:
            包含任务执行结果的字典
        """
        logger.info(f"执行任务: {task[:50]}... (使用视觉: {use_vision})")
        
        # 使用默认系统提示扩展，除非提供了自定义的
        extend_system_message = system_prompt_extension if system_prompt_extension else cls.DEFAULT_SYSTEM_PROMPT_EXTENSION
        
        try: 
            llm = cls.get_llm()
            agent = Agent(
                task=task,
                llm=llm,
                controller=controller,
                use_vision=use_vision,
                #extend_system_message=extend_system_message
            )
            
            # 执行任务并获取结果
            result = await agent.run()
           
            # 结果处理与格式化
            return {
                "status": "success",
                "message": "任务执行成功",
                "result": str(result) if result else "",
                "task": task,
                "use_vision": use_vision
            }
        except Exception as e:
            logger.error(f"任务执行失败: {str(e)}")
            return {
                "status": "error",
                "message": f"任务执行失败: {str(e)}",
                "task": task,
                "result": None,
                "use_vision": use_vision
            }
    
    @classmethod
    def get_task_template(cls, template_name: str, **kwargs) -> str:
        """
        获取预定义任务模板并填充参数
        
        Args:
            template_name: 模板名称
            **kwargs: 模板参数
            
        Returns:
            填充后的任务描述
        """
        if template_name not in cls.TASK_TEMPLATES:
            raise ValueError(f"未找到模板: {template_name}")
        
        return cls.TASK_TEMPLATES[template_name].format(**kwargs)
    
    @classmethod
    async def execute_template_task(
        cls, 
        template_name: str, 
        use_vision: bool = False, 
        system_prompt_extension: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        使用预定义模板执行任务
        
        Args:
            template_name: 模板名称
            use_vision: 是否使用视觉功能
            system_prompt_extension: 扩展系统提示以自定义Agent行为
            **kwargs: 模板参数
            
        Returns:
            包含任务执行结果的字典
        """
        task = cls.get_task_template(template_name, **kwargs)
        return await cls.execute_task(task, use_vision, system_prompt_extension=system_prompt_extension)
