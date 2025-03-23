from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from ...config import settings
from typing import Optional, Dict, Any, List
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatAgent:
    """
    基础 AI 代理类
    用于处理一般对话和任务
    """
    _instance: Optional[ChatOpenAI] = None
    _message_history_store: Dict[str, InMemoryChatMessageHistory] = {}

    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        """获取 LLM 实例（单例模式）"""
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                base_url=settings.DEEPSEEK_API_BASE,
                model=settings.DEEPSEEK_MODEL,
                api_key=settings.DEEPSEEK_API_KEY,
                temperature=0.7
            )
        return cls._instance

    @classmethod
    def get_session_history(cls, session_id: str) -> InMemoryChatMessageHistory:
        """获取会话历史（按会话ID分开存储）"""
        if session_id not in cls._message_history_store:
            cls._message_history_store[session_id] = InMemoryChatMessageHistory()
        return cls._message_history_store[session_id]

    @classmethod
    async def chat(cls, message: str, session_id: str = "default") -> str:
        """与 AI 进行对话"""
        try:
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
            
            # 返回AI回复的内容
            return response.content
        except Exception as e:
            logger.error(f"AI 对话错误: {str(e)}")
            raise Exception(f"AI 对话错误: {str(e)}")