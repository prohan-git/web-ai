from typing import Dict, Any, List, Optional, TypeVar, Type, Union
import logging
import json
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, create_model
from ....config.config_manager import ConfigManager

# 配置日志记录
logger = logging.getLogger(__name__)

class BaseChatAgent:
    """
    聊天智能体基类
    
    处理纯文本对话任务，无需浏览器操作。
    所有聊天智能体都应继承此类。
    """
    
    # 默认系统提示扩展
    DEFAULT_SYSTEM_PROMPT: str = """
    你是一个专业的AI助手，我们将进行文本对话。
    请根据用户的问题或请求，提供准确、有用的信息。
    """
    
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
        final_system_prompt = system_prompt or cls.DEFAULT_SYSTEM_PROMPT
        
        try:
            # 创建LLM实例
            llm = ChatOpenAI(
                api_key=config.get("api_key"),
                model_name=model,
                temperature=temperature,
                openai_api_base=config.get("api_base", None),
                system_prompt=final_system_prompt
            )
            
            logger.debug(f"已创建LLM实例，模型: {model}, 温度: {temperature}")
            return llm
        except Exception as e:
            logger.error(f"创建LLM实例失败: {str(e)}")
            raise ValueError(f"创建LLM实例失败: {str(e)}")
    
    @classmethod
    async def ask(
        cls,
        prompt: str,
        temperature: float = 0.7,
        model_name: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        向LLM提问
        
        Args:
            prompt: 提示文本
            temperature: 温度参数
            model_name: 模型名称
            system_prompt: 系统提示
            
        Returns:
            包含回答的字典
        """
        try:
            # 获取LLM实例
            llm = cls.get_llm(temperature, model_name, system_prompt)
            
            # 记录提示长度
            logger.info(f"提示长度: {len(prompt)}, 温度: {temperature}")
            
            # 调用LLM
            response = await llm.ainvoke(prompt)
            
            # 提取回答
            answer = response.content
            
            return cls.format_success_response(
                "回答成功",
                result=answer
            )
        except Exception as e:
            logger.error(f"提问失败: {str(e)}")
            return cls.format_error_response(f"提问失败: {str(e)}")
    
    @classmethod
    async def structured_extraction(
        cls,
        data: str,
        extraction_prompt: str,
        schema: Dict[str, Any],
        temperature: float = 0.2,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        结构化信息提取
        
        从提供的数据中提取结构化信息
        
        Args:
            data: 要提取信息的数据
            extraction_prompt: 提取指令
            schema: 提取模式
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含提取结果的字典
        """
        try:
            # 构建提取提示
            prompt = f"""
            {extraction_prompt}
            
            提取数据:
            ```
            {data}
            ```
            
            输出格式应为有效的JSON，符合以下schema:
            {json.dumps(schema, ensure_ascii=False, indent=2)}
            
            仅返回JSON结果，不包含其他文本。
            """
            
            # 调用LLM
            llm = cls.get_llm(temperature, model_name, "你是一个结构化数据提取专家，擅长从文本中提取信息为JSON格式。")
            
            # 记录提示长度
            logger.info(f"结构化提取，数据长度: {len(data)}, 提示长度: {len(extraction_prompt)}")
            
            # 调用LLM
            response = await llm.ainvoke(prompt)
            
            # 提取回答并解析JSON
            try:
                answer = response.content.strip()
                # 如果回答被```json和```包围，则提取中间部分
                if answer.startswith("```json"):
                    answer = answer.split("```json")[1].split("```")[0].strip()
                elif answer.startswith("```"):
                    answer = answer.split("```")[1].split("```")[0].strip()
                
                # 解析JSON
                result = json.loads(answer)
                
                return cls.format_success_response(
                    "提取成功",
                    result=json.dumps(result, ensure_ascii=False)
                )
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {str(e)}, 原始回答: {answer}")
                return cls.format_error_response(f"JSON解析失败: {str(e)}", original_response=answer)
        except Exception as e:
            logger.error(f"结构化提取失败: {str(e)}")
            return cls.format_error_response(f"结构化提取失败: {str(e)}")
    
    @classmethod
    async def summarize(
        cls,
        text: str,
        max_length: Optional[int] = None,
        focus: Optional[str] = None,
        temperature: float = 0.5,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        文本摘要
        
        生成文本摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            focus: 摘要重点关注的方面
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含摘要的字典
        """
        try:
            # 构建摘要提示
            prompt = f"""请对以下文本进行摘要:
            
            ```
            {text}
            ```
            """
            
            if max_length:
                prompt += f"\n摘要最大长度: {max_length}个字符。"
                
            if focus:
                prompt += f"\n摘要重点关注: {focus}。"
                
            prompt += "\n请保留关键信息，确保摘要准确代表原文内容。"
            
            # 记录提示长度
            logger.info(f"摘要任务，文本长度: {len(text)}, 最大长度: {max_length}")
            
            # 调用LLM
            response = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt="你是一个专业的文本摘要专家，擅长从长文中提取关键信息并生成简洁摘要。"
            )
            
            return response
        except Exception as e:
            logger.error(f"摘要失败: {str(e)}")
            return cls.format_error_response(f"摘要失败: {str(e)}")
    
    @classmethod
    async def translate(
        cls,
        text: str,
        target_language: str,
        preserve_format: bool = True,
        temperature: float = 0.3,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        文本翻译
        
        将文本翻译成目标语言
        
        Args:
            text: 要翻译的文本
            target_language: 目标语言
            preserve_format: 是否保留原文格式
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含翻译结果的字典
        """
        try:
            # 构建翻译提示
            prompt = f"""请将以下文本翻译成{target_language}:
            
            ```
            {text}
            ```
            """
            
            if preserve_format:
                prompt += "\n请保持原文的格式、段落划分和标点符号风格。"
            
            # 记录提示长度
            logger.info(f"翻译任务，文本长度: {len(text)}, 目标语言: {target_language}")
            
            # 调用LLM
            response = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=f"你是一个专业的翻译专家，擅长将文本精准翻译成{target_language}，同时保持原文的风格和语气。"
            )
            
            return response
        except Exception as e:
            logger.error(f"翻译失败: {str(e)}")
            return cls.format_error_response(f"翻译失败: {str(e)}")
    
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