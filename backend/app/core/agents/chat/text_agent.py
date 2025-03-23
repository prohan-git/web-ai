from typing import Dict, Any, List, Optional, Union
import logging
import json
from .base_chat_agent import BaseChatAgent

# 配置日志记录
logger = logging.getLogger(__name__)

class TextAgent(BaseChatAgent):
    """
    文本智能体
    
    处理高级文本任务，如内容创作、文本分析、数据提取等。
    """
    
    # 重写系统提示
    DEFAULT_SYSTEM_PROMPT_EXTENSION = """
    你是一个专业的文本处理助手，擅长内容创作、文本分析和数据提取。
    请根据用户的请求提供高质量的文本处理服务。
    在分析数据时保持客观准确，在创作内容时富有创意和逻辑性。
    如果用户的请求不明确，请主动询问以获取更多信息。
    """
    
    @classmethod
    async def create_content(
        cls,
        topic: str,
        content_type: str,
        tone: str = "专业",
        length: Optional[int] = None,
        keywords: Optional[List[str]] = None,
        audience: Optional[str] = None,
        temperature: float = 0.7,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建内容
        
        Args:
            topic: 内容主题
            content_type: 内容类型 (文章, 博客, 社交媒体帖子等)
            tone: 语气风格
            length: 内容长度
            keywords: 需要包含的关键词
            audience: 目标受众
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含创建的内容的字典
        """
        try:
            # 准备长度指令
            length_instruction = ""
            if length:
                length_instruction = f"内容长度应约为{length}字。"
                
            # 准备关键词指令
            keywords_instruction = ""
            if keywords and len(keywords) > 0:
                keywords_str = ", ".join(keywords)
                keywords_instruction = f"请在内容中自然地包含以下关键词: {keywords_str}。"
                
            # 准备受众指令
            audience_instruction = ""
            if audience:
                audience_instruction = f"目标受众是: {audience}。"
                
            # 构建完整提示
            prompt = f"""
            请创建一篇{tone}风格的{content_type}，主题是"{topic}"。
            
            {length_instruction}
            {keywords_instruction}
            {audience_instruction}
            
            内容应该信息丰富、结构清晰、逻辑连贯，能够吸引读者兴趣。
            请确保内容原创，没有事实错误，并避免使用陈词滥调。
            """
            
            # 系统提示
            system_prompt = f"""
            你是专业的{content_type}创作者，擅长{tone}风格的内容创作。
            你的任务是根据给定的主题和要求，创作出高质量的原创内容。
            内容应该结构清晰、逻辑连贯，同时符合特定受众的需求和期望。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加创作元数据
            if result["status"] == "success":
                result["content_type"] = content_type
                result["topic"] = topic
                result["tone"] = tone
                result["keywords"] = keywords
                result["audience"] = audience
                
            return result
        except Exception as e:
            logger.error(f"创建内容失败: {str(e)}")
            return cls.format_error_response(f"创建内容失败: {str(e)}")
    
    @classmethod
    async def analyze_text(
        cls,
        text: str,
        analysis_types: List[str],
        temperature: float = 0.3,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析文本
        
        Args:
            text: 要分析的文本
            analysis_types: 分析类型列表 (情感, 主题, 风格, 可读性, 关键词等)
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含分析结果的字典
        """
        try:
            # 支持的分析类型
            supported_types = ["情感", "主题", "风格", "可读性", "关键词", "结构", "语法", "语义"]
            
            # 验证分析类型
            invalid_types = [t for t in analysis_types if t not in supported_types]
            if invalid_types:
                return cls.format_error_response(
                    f"不支持的分析类型: {', '.join(invalid_types)}",
                    supported_types=supported_types
                )
                
            # 构建分析指令
            analysis_instructions = []
            for analysis_type in analysis_types:
                if analysis_type == "情感":
                    analysis_instructions.append("进行情感分析，判断文本的情感倾向(积极、消极、中性)，并给出情感强度评分(1-10)")
                elif analysis_type == "主题":
                    analysis_instructions.append("识别主要主题和子主题，分析主题之间的关系")
                elif analysis_type == "风格":
                    analysis_instructions.append("分析写作风格，包括正式程度、语气、修辞手法等")
                elif analysis_type == "可读性":
                    analysis_instructions.append("评估可读性，包括词汇复杂度、句子长度、整体易读性等")
                elif analysis_type == "关键词":
                    analysis_instructions.append("提取最重要的关键词和短语，并按相关性排序")
                elif analysis_type == "结构":
                    analysis_instructions.append("分析文本结构，包括段落组织、论点展开、逻辑连贯性等")
                elif analysis_type == "语法":
                    analysis_instructions.append("评估语法正确性、句法多样性等")
                elif analysis_type == "语义":
                    analysis_instructions.append("分析词语选择、语义连贯性、上下文关联等")
                    
            # 构建完整提示
            analysis_tasks = "\n".join([f"- {i}" for i in analysis_instructions])
            prompt = f"""
            请对以下文本进行分析:
            
            {text}
            
            请完成以下分析任务:
            {analysis_tasks}
            
            对于每个分析任务，请提供详细解释和具体例证。
            以结构化方式呈现结果，使用小标题分隔不同的分析部分。
            """
            
            # 系统提示
            system_prompt = """
            你是专业的文本分析师。你的任务是对给定文本进行深入、客观的分析，
            提供具有洞察力的观察和评估。分析应该基于文本的实际特征，
            避免主观臆断，并用文本中的具体例子支持你的分析结果。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加分析元数据
            if result["status"] == "success":
                result["analysis_types"] = analysis_types
                result["text_length"] = len(text)
                
            return result
        except Exception as e:
            logger.error(f"分析文本失败: {str(e)}")
            return cls.format_error_response(f"分析文本失败: {str(e)}")
    
    @classmethod
    async def extract_entities(
        cls,
        text: str,
        entity_types: List[str],
        temperature: float = 0.2,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        提取实体
        
        Args:
            text: 要处理的文本
            entity_types: 要提取的实体类型 (人名, 地点, 组织, 日期, 时间, 产品, 事件等)
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含提取的实体的字典
        """
        try:
            # 支持的实体类型
            supported_types = ["人名", "地点", "组织", "日期", "时间", "产品", "事件", "金额", "百分比", "职位", "联系方式"]
            
            # 验证实体类型
            invalid_types = [t for t in entity_types if t not in supported_types]
            if invalid_types:
                return cls.format_error_response(
                    f"不支持的实体类型: {', '.join(invalid_types)}",
                    supported_types=supported_types
                )
                
            # 构建提取指令
            entity_instructions = ", ".join(entity_types)
            
            # 构建提取模式
            schema = {
                "type": "object",
                "properties": {}
            }
            
            for entity_type in entity_types:
                schema["properties"][entity_type] = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "context": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                }
                
            # 构建完整提示
            extraction_prompt = f"""
            请从以下文本中提取所有的{entity_instructions}实体。
            
            对于每个提取的实体，请提供:
            1. 实体文本
            2. 实体所在的上下文 (包含实体的短句或短语)
            
            请确保提取的实体是准确的，不要遗漏任何符合条件的实体。
            """
            
            # 调用结构化提取
            result = await cls.structured_extraction(
                data=text,
                extraction_prompt=extraction_prompt,
                schema=schema,
                temperature=temperature,
                model_name=model_name
            )
            
            # 如果成功，解析JSON结果
            if result["status"] == "success":
                try:
                    # 尝试将结果解析为JSON
                    json_result = json.loads(result["result"])
                    
                    # 更新结果
                    result["entity_counts"] = {
                        entity_type: len(json_result.get(entity_type, []))
                        for entity_type in entity_types
                    }
                    result["result"] = json_result
                except json.JSONDecodeError:
                    # 如果解析失败，返回原始结果
                    logger.warning("JSON解析失败，返回原始结果")
                    result["parse_error"] = "无法解析为JSON格式"
                    
            return result
        except Exception as e:
            logger.error(f"提取实体失败: {str(e)}")
            return cls.format_error_response(f"提取实体失败: {str(e)}")
    
    @classmethod
    async def edit_text(
        cls,
        text: str,
        edit_instructions: str,
        preserve_original: bool = False,
        temperature: float = 0.4,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        编辑文本
        
        Args:
            text: 要编辑的文本
            edit_instructions: 编辑指令
            preserve_original: 是否在结果中保留原文
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含编辑结果的字典
        """
        try:
            # 构建完整提示
            prompt = f"""
            请根据以下指令编辑文本:
            
            指令: {edit_instructions}
            
            原文:
            {text}
            
            请提供编辑后的完整文本。编辑应准确反映指令的要求，
            同时保持文本的语义连贯性和风格一致性。
            """
            
            # 系统提示
            system_prompt = """
            你是专业的文本编辑助手。你的任务是根据给定的指令编辑文本，
            可能包括修改语法、调整风格、改变措辞、精简内容等各种编辑操作。
            编辑后的文本应该保持原文的主要意思，同时符合编辑指令的要求。
            除非特别说明，应保持原文的整体结构和组织方式。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加编辑元数据
            if result["status"] == "success":
                result["edit_instructions"] = edit_instructions
                
                # 如果需要保留原文
                if preserve_original:
                    result["original_text"] = text
                    
                # 添加统计信息
                result["original_length"] = len(text)
                result["edited_length"] = len(result["result"])
                result["length_change"] = result["edited_length"] - result["original_length"]
                
            return result
        except Exception as e:
            logger.error(f"编辑文本失败: {str(e)}")
            return cls.format_error_response(f"编辑文本失败: {str(e)}")
    
    @classmethod
    async def generate_variations(
        cls,
        text: str,
        variation_count: int = 3,
        variation_type: str = "措辞",
        constraints: Optional[str] = None,
        temperature: float = 0.7,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成文本变体
        
        Args:
            text: 原始文本
            variation_count: 要生成的变体数量
            variation_type: 变体类型 (措辞, 长度, 风格, 语气等)
            constraints: 额外约束条件
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含文本变体的字典
        """
        try:
            # 支持的变体类型
            supported_types = ["措辞", "长度", "风格", "语气", "复杂度", "专业度", "通俗度"]
            
            # 验证变体类型
            if variation_type not in supported_types:
                return cls.format_error_response(
                    f"不支持的变体类型: {variation_type}",
                    supported_types=supported_types
                )
                
            # 准备约束指令
            constraints_instruction = ""
            if constraints:
                constraints_instruction = f"请遵循以下约束条件: {constraints}。"
                
            # 构建变体指令
            variation_instruction = ""
            if variation_type == "措辞":
                variation_instruction = f"请生成{variation_count}个表达方式不同但含义相同的版本。使用不同的词汇和句式。"
            elif variation_type == "长度":
                variation_instruction = f"请生成{variation_count}个长度不同的版本，包括简短版、中等长度版和详细版。"
            elif variation_type == "风格":
                variation_instruction = f"请生成{variation_count}个不同风格的版本，如正式、随意、创意、故事性等。"
            elif variation_type == "语气":
                variation_instruction = f"请生成{variation_count}个不同语气的版本，如热情、严肃、幽默、质疑等。"
            elif variation_type == "复杂度":
                variation_instruction = f"请生成{variation_count}个复杂度不同的版本，从简单直接到复杂深入。"
            elif variation_type == "专业度":
                variation_instruction = f"请生成{variation_count}个专业程度不同的版本，从专家级到入门级。"
            elif variation_type == "通俗度":
                variation_instruction = f"请生成{variation_count}个通俗程度不同的版本，从学术性到通俗易懂。"
                
            # 构建完整提示
            prompt = f"""
            请为以下文本生成变体:
            
            原文:
            {text}
            
            {variation_instruction}
            {constraints_instruction}
            
            请为每个变体添加编号，并确保所有变体都保持原文的核心信息和意图。
            """
            
            # 系统提示
            system_prompt = f"""
            你是专业的文本变体生成助手。你的任务是根据指定的变体类型"{variation_type}"，
            为给定文本生成多个变体版本。每个变体应该保持原文的核心信息和意图，
            同时根据变体类型进行适当的调整。请确保每个变体都是完整的、连贯的文本。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加变体元数据
            if result["status"] == "success":
                result["original_text"] = text
                result["variation_type"] = variation_type
                result["variation_count"] = variation_count
                result["constraints"] = constraints
                
            return result
        except Exception as e:
            logger.error(f"生成文本变体失败: {str(e)}")
            return cls.format_error_response(f"生成文本变体失败: {str(e)}")
    
    @classmethod
    async def classify_text(
        cls,
        text: str,
        categories: List[str],
        multi_label: bool = False,
        explanation: bool = True,
        temperature: float = 0.3,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        文本分类
        
        Args:
            text: 要分类的文本
            categories: 分类类别列表
            multi_label: 是否允许多标签分类
            explanation: 是否提供分类解释
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含分类结果的字典
        """
        try:
            # 验证分类类别
            if not categories or len(categories) < 2:
                return cls.format_error_response(
                    "分类类别至少需要2个",
                    provided_categories=categories
                )
                
            # 准备多标签指令
            multi_label_instruction = ""
            if multi_label:
                multi_label_instruction = "文本可能属于多个类别，请列出所有适用的类别。"
            else:
                multi_label_instruction = "请选择最适合的一个类别。"
                
            # 准备解释指令
            explanation_instruction = ""
            if explanation:
                explanation_instruction = "请为你的分类提供详细解释，说明为什么文本属于该类别。"
                
            # 构建分类模式
            schema = {
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array" if multi_label else "string",
                        "items": {"type": "string"} if multi_label else None,
                        "description": "分类结果" + ("（可多选）" if multi_label else "")
                    }
                }
            }
            
            if explanation:
                schema["properties"]["explanation"] = {
                    "type": "string",
                    "description": "分类解释"
                }
                
                if multi_label:
                    schema["properties"]["category_explanations"] = {
                        "type": "object",
                        "description": "每个类别的解释"
                    }
                    
            # 构建完整提示
            categories_str = ", ".join(categories)
            extraction_prompt = f"""
            请将以下文本分类到这些类别中: {categories_str}
            
            {multi_label_instruction}
            {explanation_instruction}
            """
            
            # 调用结构化提取
            result = await cls.structured_extraction(
                data=text,
                extraction_prompt=extraction_prompt,
                schema=schema,
                temperature=temperature,
                model_name=model_name
            )
            
            # 如果成功，解析JSON结果
            if result["status"] == "success":
                try:
                    # 尝试将结果解析为JSON
                    json_result = json.loads(result["result"])
                    
                    # 更新结果
                    result["all_categories"] = categories
                    result["multi_label"] = multi_label
                    result["result"] = json_result
                except json.JSONDecodeError:
                    # 如果解析失败，返回原始结果
                    logger.warning("JSON解析失败，返回原始结果")
                    result["parse_error"] = "无法解析为JSON格式"
                    
            return result
        except Exception as e:
            logger.error(f"文本分类失败: {str(e)}")
            return cls.format_error_response(f"文本分类失败: {str(e)}")
    
    @classmethod
    async def question_answering(
        cls,
        context: str,
        question: str,
        answer_format: Optional[str] = None,
        temperature: float = 0.3,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        问答
        
        Args:
            context: 背景文本
            question: 问题
            answer_format: 回答格式要求
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含回答的字典
        """
        try:
            # 准备格式指令
            format_instruction = ""
            if answer_format:
                format_instruction = f"请按照以下格式回答: {answer_format}"
                
            # 构建完整提示
            prompt = f"""
            请基于以下背景信息回答问题:
            
            背景信息:
            {context}
            
            问题: {question}
            
            {format_instruction}
            
            请只回答问题中询问的内容，回答应该基于提供的背景信息。
            如果背景信息中没有足够的信息来回答问题，请说明无法回答。
            """
            
            # 系统提示
            system_prompt = """
            你是专业的问答助手。你的任务是基于提供的背景信息准确回答问题。
            回答应该直接基于背景信息，不要添加不在背景中的信息。
            如果背景信息不足以回答问题，请诚实地说明无法回答。
            保持回答简洁、准确，并直接针对所问问题。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加问答元数据
            if result["status"] == "success":
                result["question"] = question
                result["context_length"] = len(context)
                
            return result
        except Exception as e:
            logger.error(f"问答失败: {str(e)}")
            return cls.format_error_response(f"问答失败: {str(e)}")
    
    @classmethod
    async def extract_table(
        cls,
        text: str,
        headers: Optional[List[str]] = None,
        temperature: float = 0.2,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从文本中提取表格数据
        
        Args:
            text: 包含表格数据的文本
            headers: 表头列表，如果为None则自动识别
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含表格数据的字典
        """
        try:
            # 准备表头指令
            headers_instruction = ""
            if headers and len(headers) > 0:
                headers_str = ", ".join(headers)
                headers_instruction = f"请使用以下表头: {headers_str}"
                
            # 构建表格模式
            schema = {
                "type": "object",
                "properties": {
                    "table": {
                        "type": "array",
                        "items": {
                            "type": "object"
                        },
                        "description": "表格数据，每行为一个对象"
                    },
                    "headers": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "表格的表头"
                    }
                },
                "required": ["table", "headers"]
            }
                
            # 构建完整提示
            extraction_prompt = f"""
            请从以下文本中提取表格数据。
            
            {headers_instruction}
            
            请以JSON格式返回表格，包括表头和数据行。
            如果文本包含多个表格，请提取最主要的那个。
            如果文本不包含表格结构，请尝试将相关信息组织成表格形式。
            """
            
            # 调用结构化提取
            result = await cls.structured_extraction(
                data=text,
                extraction_prompt=extraction_prompt,
                schema=schema,
                temperature=temperature,
                model_name=model_name
            )
            
            # 如果成功，解析JSON结果
            if result["status"] == "success":
                try:
                    # 尝试将结果解析为JSON
                    json_result = json.loads(result["result"])
                    
                    # 添加统计信息
                    if "table" in json_result:
                        row_count = len(json_result["table"])
                        col_count = len(json_result.get("headers", []))
                        
                        # 更新结果
                        result["row_count"] = row_count
                        result["column_count"] = col_count
                        result["result"] = json_result
                except json.JSONDecodeError:
                    # 如果解析失败，返回原始结果
                    logger.warning("JSON解析失败，返回原始结果")
                    result["parse_error"] = "无法解析为JSON格式"
                    
            return result
        except Exception as e:
            logger.error(f"提取表格失败: {str(e)}")
            return cls.format_error_response(f"提取表格失败: {str(e)}")
    
    @classmethod
    async def rewrite_text(
        cls,
        text: str,
        purpose: str,
        target_audience: Optional[str] = None,
        style: Optional[str] = None,
        length_change: Optional[str] = None,
        temperature: float = 0.5,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        重写文本
        
        Args:
            text: 要重写的文本
            purpose: 重写目的
            target_audience: 目标受众
            style: 目标风格
            length_change: 长度变化 (如 "缩短10%", "扩展一倍")
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含重写结果的字典
        """
        try:
            # 准备受众指令
            audience_instruction = ""
            if target_audience:
                audience_instruction = f"目标受众: {target_audience}。"
                
            # 准备风格指令
            style_instruction = ""
            if style:
                style_instruction = f"目标风格: {style}。"
                
            # 准备长度指令
            length_instruction = ""
            if length_change:
                length_instruction = f"长度要求: {length_change}。"
                
            # 构建完整提示
            prompt = f"""
            请重写以下文本:
            
            原文:
            {text}
            
            重写目的: {purpose}
            {audience_instruction}
            {style_instruction}
            {length_instruction}
            
            请提供完整的重写版本，保持原文的核心信息和意图，
            同时根据指定的目的和要求进行适当调整。
            """
            
            # 系统提示
            system_prompt = """
            你是专业的文本重写助手。你的任务是根据指定的目的和要求重写文本，
            保持原文的核心信息和意图，同时根据需要调整风格、语气、长度和复杂度。
            重写应该是完整的、连贯的，并符合指定的目标受众和风格要求。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加重写元数据
            if result["status"] == "success":
                result["purpose"] = purpose
                result["target_audience"] = target_audience
                result["style"] = style
                result["length_change"] = length_change
                result["original_length"] = len(text)
                result["rewritten_length"] = len(result["result"])
                result["actual_length_change"] = f"{((result['rewritten_length'] - result['original_length']) / result['original_length'] * 100):.1f}%"
                
            return result
        except Exception as e:
            logger.error(f"重写文本失败: {str(e)}")
            return cls.format_error_response(f"重写文本失败: {str(e)}")
    
    @classmethod
    async def compare_texts(
        cls,
        text1: str,
        text2: str,
        aspects: Optional[List[str]] = None,
        temperature: float = 0.3,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        比较文本
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            aspects: 比较方面列表
            temperature: 温度参数
            model_name: 模型名称
            
        Returns:
            包含比较结果的字典
        """
        try:
            # 默认比较方面
            if not aspects:
                aspects = ["内容", "风格", "语气", "结构", "有效性"]
                
            # 构建比较指令
            aspects_str = ", ".join(aspects)
            
            # 构建完整提示
            prompt = f"""
            请比较以下两段文本:
            
            文本1:
            {text1}
            
            文本2:
            {text2}
            
            请从以下方面进行比较: {aspects_str}
            
            对于每个方面，请详细分析两段文本的异同点，并提供具体例子。
            最后，请总结两段文本的主要区别和相似之处。
            """
            
            # 系统提示
            system_prompt = """
            你是专业的文本比较分析师。你的任务是深入比较两段文本，
            分析它们在内容、风格、语气、结构等方面的异同点。
            比较应该客观、详细，并提供具体例子来支持你的分析。
            避免简单地列出表面差异，而应深入分析根本区别和共性。
            """
            
            # 获取LLM实例并调用
            result = await cls.ask(
                prompt=prompt,
                temperature=temperature,
                model_name=model_name,
                system_prompt=system_prompt
            )
            
            # 如果成功，添加比较元数据
            if result["status"] == "success":
                result["aspects"] = aspects
                result["text1_length"] = len(text1)
                result["text2_length"] = len(text2)
                
            return result
        except Exception as e:
            logger.error(f"比较文本失败: {str(e)}")
            return cls.format_error_response(f"比较文本失败: {str(e)}") 