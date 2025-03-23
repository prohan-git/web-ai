from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from ....config.config_manager import ConfigManager
from typing import Optional, Dict, Any, List
import logging

# 配置日志记录
logger = logging.getLogger(__name__)

class ChatAgent:
    """
    聊天智能体
    
    提供纯文本对话功能，不执行浏览器任务
    """
    _instance: Optional[ChatOpenAI] = None
    _message_history_store: Dict[str, InMemoryChatMessageHistory] = {}
    
    SYSTEM_PROMPT = """你是一个友好的AI助手，可以回答用户的各种问题。
    尽量给出简洁、准确的回答，并在适当的时候提供有用的建议。
    """

    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        """获取 LLM 实例（单例模式）"""
        if cls._instance is None:
            llm_config = ConfigManager.get_llm_config()
            cls._instance = ChatOpenAI(
                base_url=llm_config["base_url"],
                model=llm_config["model"],
                api_key=llm_config["api_key"]
            )
        return cls._instance

    @classmethod
    def get_session_history(cls, session_id: str) -> InMemoryChatMessageHistory:
        """获取会话历史（按会话ID分开存储）"""
        if session_id not in cls._message_history_store:
            cls._message_history_store[session_id] = InMemoryChatMessageHistory()
            # 添加系统提示
            system_message = SystemMessage(content=cls.SYSTEM_PROMPT)
            cls._message_history_store[session_id].add_message(system_message)
        return cls._message_history_store[session_id]

    @classmethod
    async def chat(cls, message: str, session_id: str = "default") -> str:
        """
        与 AI 进行对话
        
        Args:
            message: 用户消息
            session_id: 会话ID，用于区分不同会话
            
        Returns:
            AI 的回复文本
        """
        try:
            logger.info(f"收到聊天消息: {message[:50]}...")
            
            llm = cls.get_llm()
            
            # 获取会话历史
            history = cls.get_session_history(session_id)
            
            # 添加当前消息到历史
            human_message = HumanMessage(content=message)
            history.add_message(human_message)
            
            # 获取所有历史消息
            all_messages = history.messages
            logger.info(f"对话历史消息数: {len(all_messages)}")
            
            # 使用完整的历史消息调用LLM
            response = await llm.ainvoke(all_messages)
            
            # 添加AI回复到历史
            history.add_message(response)
            
            logger.info(f"AI回复: {response.content[:50]}...")
            
            # 返回AI回复的内容
            return response.content
        except Exception as e:
            logger.error(f"AI 对话错误: {str(e)}")
            raise Exception(f"AI 对话错误: {str(e)}") 
    
    @classmethod
    def format_response(cls, ai_response: str) -> Dict[str, Any]:
        """
        格式化AI回复为统一的响应格式
        
        Args:
            ai_response: AI回复的文本
            
        Returns:
            格式化的响应字典
        """
        return {
            "status": "success",
            "message": "对话成功",
            "response": ai_response
        }
    
    @classmethod
    def format_error(cls, error_message: str) -> Dict[str, Any]:
        """
        格式化错误消息为统一的响应格式
        
        Args:
            error_message: 错误消息
            
        Returns:
            格式化的错误响应字典
        """
        return {
            "status": "error",
            "message": error_message,
            "response": None
        }
    
    @classmethod
    async def process_message(cls, message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        处理用户消息并返回格式化响应
        
        Args:
            message: 用户消息
            session_id: 会话ID
            
        Returns:
            格式化的响应字典
        """
        try:
            ai_response = await cls.chat(message, session_id)
            return cls.format_response(ai_response)
        except Exception as e:
            logger.error(f"处理消息错误: {str(e)}")
            return cls.format_error(f"处理消息错误: {str(e)}") 