from typing import Dict, Any, List, Optional, ClassVar, Union
import logging
from langchain_openai import ChatOpenAI
from ....config.config_manager import ConfigManager
from ..templates.template_manager import TemplateManager

# 配置日志记录
logger = logging.getLogger(__name__)

class BrowserTaskAgent:
    """
    浏览器任务智能体基类
    
    处理需要浏览器操作的任务，如网页内容提取、社交媒体监控、电商数据分析等。
    所有需要浏览器操作的智能体都应继承此类。
    """
    
    # 控制器实例，用于管理用户交互
    controller: Optional[Any] = None
    
    # 默认系统提示扩展
    DEFAULT_SYSTEM_PROMPT_EXTENSION: ClassVar[str] = """
    你是一个专业的AI助手，负责执行需要浏览器的任务。
    请按照以下准则工作:
    
    1. 仔细理解用户的请求，确保理解任务目标和需求
    2. 使用浏览器有效地访问和处理网页内容
    3. 提供清晰、结构化的信息摘要，而非原始数据
    4. 关注用户真正需要的信息，过滤噪音和无关内容
    5. 如果遇到障碍（如验证码、登录墙），尝试合理绕过或清晰说明问题
    6. 保持客观，不添加未在网页上找到的信息
    
    任务过程中遇到问题要积极寻找解决方案，如果确实无法完成，请诚实说明原因。
    """
    
    @classmethod
    def ask_user(cls, message: str) -> str:
        """
        向用户询问信息
        
        Args:
            message: 询问消息
            
        Returns:
            用户回答
        """
        if cls.controller is None:
            logger.warning("未设置控制器，无法与用户交互")
            return "无法与用户交互"
            
        return cls.controller.ask_user(message)
    
    @classmethod
    def get_llm(
        cls,
        temperature: float = 0.7,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> ChatOpenAI:
        """
        获取LLM实例
        
        Args:
            temperature: 温度参数，控制回答的随机性
            model_name: 模型名称，如果未指定则使用配置中的默认模型
            system_prompt: 系统提示，如果未指定则使用默认提示
            
        Returns:
            配置好的ChatOpenAI实例
        """
        # 获取配置
        config = ConfigManager.get_llm_config()
        
        # 确定模型名称
        model = model_name or config.get("default_model")
        
        # 确定系统提示
        final_system_prompt = system_prompt or cls.DEFAULT_SYSTEM_PROMPT_EXTENSION
        
        try:
            # 创建LLM实例
            llm = ChatOpenAI(
                openai_api_key=config.get("api_key"),
                model=model,
                temperature=temperature,
                openai_api_base=config.get("api_base", None),
                system=final_system_prompt
            )
            
            logger.debug(f"已创建LLM实例，模型: {model}, 温度: {temperature}")
            return llm
        except Exception as e:
            logger.error(f"创建LLM实例失败: {str(e)}")
            raise ValueError(f"创建LLM实例失败: {str(e)}")
    
    @classmethod
    def format_success_response(cls, message: str, **kwargs) -> Dict[str, Any]:
        """
        格式化成功响应
        
        Args:
            message: 成功消息
            **kwargs: 其他数据
            
        Returns:
            格式化的响应字典
        """
        response = {
            "status": "success",
            "message": message
        }
        
        # 添加其他数据
        response.update(kwargs)
        
        return response
    
    @classmethod
    def format_error_response(cls, message: str, **kwargs) -> Dict[str, Any]:
        """
        格式化错误响应
        
        Args:
            message: 错误消息
            **kwargs: 其他数据
            
        Returns:
            格式化的响应字典
        """
        response = {
            "status": "error",
            "message": message
        }
        
        # 添加其他数据
        response.update(kwargs)
        
        return response
    
    @classmethod
    def validate_platform(cls, platform: str, supported_platforms: List[str]) -> Optional[Dict[str, Any]]:
        """
        验证平台是否支持
        
        Args:
            platform: 平台名称
            supported_platforms: 支持的平台列表
            
        Returns:
            如果不支持，返回错误响应；否则返回None
        """
        if platform not in supported_platforms:
            return cls.format_error_response(
                f"不支持的平台: {platform}",
                supported_platforms=supported_platforms
            )
        return None
    
    @classmethod
    async def execute_task(
        cls,
        task: str,
        use_vision: bool = True,
        temperature: float = 0.7,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行浏览器任务
        
        Args:
            task: 任务描述
            use_vision: 是否使用视觉能力
            temperature: 温度参数
            model_name: 模型名称
            system_prompt: 系统提示
            
        Returns:
            包含任务执行结果的字典
        """
        try:
            # 获取LLM实例
            llm = cls.get_llm(
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 任务执行逻辑 - 简化实现，仅返回任务描述
            # 实际项目中，这里应该调用浏览器自动化逻辑执行任务
            logger.info(f"执行浏览器任务: {task[:100]}...")
            
            # 模拟任务执行结果
            result = {
                "task_description": task,
                "use_vision": use_vision,
                "model": model_name or "默认模型",
                "content": "任务执行结果将在实际实现中提供"
            }
            
            return cls.format_success_response(
                "任务执行成功（模拟结果）",
                result=result
            )
        except Exception as e:
            logger.error(f"执行任务失败: {str(e)}")
            return cls.format_error_response(f"执行任务失败: {str(e)}")
    
    @classmethod
    async def execute_template_task(
        cls,
        template_name: str,
        parameters: Dict[str, Any],
        use_vision: bool = True,
        temperature: float = 0.7,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行基于通用模板的任务
        
        Args:
            template_name: 模板名称
            parameters: 模板参数
            use_vision: 是否使用视觉能力
            temperature: 温度参数
            model_name: 模型名称
            system_prompt: 系统提示
            
        Returns:
            包含任务执行结果的字典
        """
        try:
            # 获取模板
            template = TemplateManager.get_general_template(template_name)
            
            # 检查模板是否存在
            if not template:
                return cls.format_error_response(
                    f"未找到模板: {template_name}",
                    supported_templates=TemplateManager.get_general_template_names()
                )
                
            # 渲染模板
            try:
                task = TemplateManager.render_template(template, parameters)
            except KeyError as e:
                return cls.format_error_response(
                    f"模板参数错误: 缺少参数 {str(e)}",
                    required_parameters=list(parameters.keys())
                )
                
            # 执行任务
            return await cls.execute_task(
                task=task,
                use_vision=use_vision,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
        except Exception as e:
            logger.error(f"执行模板任务失败: {str(e)}")
            return cls.format_error_response(f"执行模板任务失败: {str(e)}")
    
     