from typing import Dict, Any, List, Optional, Union, Type, Callable
import logging
from langchain.schema import BaseOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from ..chat.text_agent import TextAgent
from ..chat.base_chat_agent import BaseChatAgent
from ..browser.social_agent import SocialAgent
from ..browser.ecommerce_agent import EcommerceAgent

# 配置日志记录
logger = logging.getLogger(__name__)

class ChainAgent:
    """
    组合智能体
    
    将多个智能体组合在一起，形成处理链，一个智能体的输出作为下一个智能体的输入
    """
    
    @classmethod
    async def text_to_social_analysis(
        cls,
        text: str,
        content_type: str = "社交媒体帖子",
        platform: str = "小红书",
        analysis_type: str = "sentiment"
    ) -> Dict[str, Any]:
        """
        文本创作后进行社交媒体分析链
        
        首先使用TextAgent创建内容，然后将输出传给SocialAgent进行分析
        
        Args:
            text: 分析主题或关键词
            content_type: 内容类型，如"社交媒体帖子"、"产品描述"等
            platform: 目标平台
            analysis_type: 分析类型，如"sentiment"、"trend"等
            
        Returns:
            分析结果
        """
        try:
            logger.info(f"开始文本到社交分析链，主题: {text}")
            
            # 第一步：使用TextAgent创建内容
            text_agent = TextAgent()
            content_result = await text_agent.create_content(
                topic=text,
                content_type=content_type,
                tone="informative",
                length="medium",
                keywords=[text],
                audience="一般网民"
            )
            
            # 检查是否成功
            if not content_result.get("status") == "success":
                return BaseChatAgent.format_error_response(
                    f"内容创建失败: {content_result.get('message')}"
                )
            
            generated_content = content_result.get("result", "")
            logger.info(f"内容创建成功，长度: {len(generated_content)}")
            
            # 第二步：使用SocialAgent分析内容
            social_agent = SocialAgent()
            analysis_result = await social_agent.analyze_data(
                data=generated_content,
                analysis_type=analysis_type
            )
            
            # 组合结果
            return {
                "status": "success",
                "message": "文本到社交分析链执行成功",
                "generated_content": generated_content,
                "analysis_result": analysis_result,
                "platform": platform,
                "analysis_type": analysis_type
            }
        except Exception as e:
            logger.error(f"文本到社交分析链失败: {str(e)}")
            return BaseChatAgent.format_error_response(f"文本到社交分析链失败: {str(e)}")
    
    @classmethod
    async def social_to_ecommerce(
        cls,
        keyword: str,
        platform: str = "小红书",
        search_count: int = 5,
        ecommerce_platform: str = "淘宝"
    ) -> Dict[str, Any]:
        """
        社交媒体分析到电商搜索链
        
        首先使用SocialAgent搜索社交媒体平台，然后将结果传给EcommerceAgent进行产品搜索
        
        Args:
            keyword: 搜索关键词
            platform: 社交媒体平台
            search_count: 社交搜索结果数量
            ecommerce_platform: 电商平台
            
        Returns:
            搜索结果
        """
        try:
            logger.info(f"开始社交到电商链，关键词: {keyword}")
            
            # 第一步：使用SocialAgent搜索社交媒体
            social_agent = SocialAgent()
            social_result = await social_agent.collect_from_platform(
                platform=platform,
                task_type="搜索",
                keyword=keyword,
                top_n=search_count
            )
            
            # 检查是否成功
            if not social_result.get("status") == "success":
                return BaseChatAgent.format_error_response(
                    f"社交媒体搜索失败: {social_result.get('message')}"
                )
            
            # 从社交媒体结果中提取关键信息
            social_data = social_result.get("result", "")
            
            # 使用TextAgent提取热门产品和特征
            text_agent = TextAgent()
            
            # 定义提取schema
            class ProductExtraction(BaseModel):
                popular_products: List[str] = Field(description="从社交媒体搜索结果中提取的热门产品名称列表")
                product_features: List[str] = Field(description="从社交媒体搜索结果中提取的产品重要特征列表")
                
            extraction_prompt = f"""
            请分析以下来自{platform}的搜索结果，提取其中提到的热门产品和产品特征:
            
            {social_data}
            
            仅返回JSON格式的提取结果，不要包含其他解释。
            """
            
            # 执行结构化提取
            extraction_result = await text_agent.structured_extraction(
                data=social_data,
                extraction_prompt=extraction_prompt,
                schema=ProductExtraction.schema()
            )
            
            # 检查是否成功
            if not extraction_result.get("status") == "success":
                logger.warning(f"结构化提取失败，使用关键词继续: {extraction_result.get('message')}")
                product_query = keyword
            else:
                # 解析提取结果
                try:
                    import json
                    extraction_data = json.loads(extraction_result.get("result", "{}"))
                    products = extraction_data.get("popular_products", [])
                    features = extraction_data.get("product_features", [])
                    
                    # 组合查询
                    if products:
                        product_query = products[0]  # 使用第一个热门产品
                    else:
                        product_query = keyword
                        
                    logger.info(f"从社交媒体提取的产品: {products}")
                    logger.info(f"从社交媒体提取的特征: {features}")
                except Exception as e:
                    logger.warning(f"解析提取结果失败: {str(e)}")
                    product_query = keyword
            
            # 第二步：使用EcommerceAgent搜索产品
            ecommerce_agent = EcommerceAgent()
            search_result = await ecommerce_agent.search_products(
                platform=ecommerce_platform,
                query=product_query,
                max_results=5,
                sort_by="default",
                filters=None
            )
            
            # 组合结果
            return {
                "status": "success",
                "message": "社交到电商链执行成功",
                "social_platform": platform,
                "social_keyword": keyword,
                "ecommerce_platform": ecommerce_platform,
                "product_query": product_query,
                "social_result_summary": social_data[:500] + "..." if len(social_data) > 500 else social_data,
                "ecommerce_result": search_result
            }
        except Exception as e:
            logger.error(f"社交到电商链失败: {str(e)}")
            return BaseChatAgent.format_error_response(f"社交到电商链失败: {str(e)}")
    
    @classmethod
    async def advanced_market_research(
        cls,
        product: str,
        target_audience: str = "年轻女性",
        social_platform: str = "小红书",
        ecommerce_platform: str = "淘宝"
    ) -> Dict[str, Any]:
        """
        高级市场研究链
        
        执行多步骤的市场研究：社交媒体趋势 -> 电商产品分析 -> 文本总结
        
        Args:
            product: 产品名称或类别
            target_audience: 目标受众
            social_platform: 社交媒体平台
            ecommerce_platform: 电商平台
            
        Returns:
            市场研究结果
        """
        try:
            logger.info(f"开始高级市场研究，产品: {product}, 目标受众: {target_audience}")
            results = {}
            
            # 第一步：使用SocialAgent查找趋势内容
            social_agent = SocialAgent()
            trend_result = await social_agent.find_trending_content(
                platform=social_platform,
                niche=product,
                count=5,
                time_period="最近一个月"
            )
            
            results["social_trends"] = trend_result
            
            # 第二步：使用EcommerceAgent查找产品信息
            ecommerce_agent = EcommerceAgent()
            product_result = await ecommerce_agent.search_products(
                platform=ecommerce_platform,
                query=product,
                max_results=5,
                sort_by="default"
            )
            
            results["product_info"] = product_result
            
            # 第三步：同时获取竞争分析
            competition_result = await ecommerce_agent.analyze_competition(
                product_keyword=product,
                platform=ecommerce_platform
            )
            
            results["competition_analysis"] = competition_result
            
            # 第四步：使用TextAgent总结所有信息
            text_agent = TextAgent()
            
            # 准备要总结的内容
            summary_content = f"""
            ## 社交媒体趋势分析 ({social_platform})
            {trend_result.get('result', '无数据')}
            
            ## 电商产品信息 ({ecommerce_platform})
            {product_result.get('result', '无数据')}
            
            ## 竞争分析
            {competition_result.get('result', '无数据')}
            """
            
            summary_result = await text_agent.summarize(
                text=summary_content,
                max_length=1000,
                focus=f"针对{target_audience}的{product}市场机会和挑战"
            )
            
            # 最终结果
            return {
                "status": "success",
                "message": "高级市场研究完成",
                "product": product,
                "target_audience": target_audience,
                "summary": summary_result.get("result", ""),
                "detailed_results": results
            }
        except Exception as e:
            logger.error(f"高级市场研究失败: {str(e)}")
            return BaseChatAgent.format_error_response(f"高级市场研究失败: {str(e)}")
    
    @classmethod
    async def create_agent_chain(cls, chain_config: Dict[str, Any]) -> Callable:
        """
        创建自定义Agent链
        
        基于配置动态创建Agent处理链
        
        Args:
            chain_config: 链配置，包含步骤和参数
            
        Returns:
            可调用的函数，执行Agent链
        """
        # 这里只是一个概念演示，实际实现需要更复杂的逻辑
        # 根据配置创建不同的链
        chain_type = chain_config.get("type", "")
        
        if chain_type == "text_to_social":
            return cls.text_to_social_analysis
        elif chain_type == "social_to_ecommerce":
            return cls.social_to_ecommerce
        elif chain_type == "market_research":
            return cls.advanced_market_research
        else:
            async def custom_chain(**kwargs):
                return BaseChatAgent.format_error_response(f"未知的链类型: {chain_type}")
            
            return custom_chain 