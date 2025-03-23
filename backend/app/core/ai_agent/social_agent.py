import logging
from langchain_openai import ChatOpenAI
from .task_agent import TaskAgent
from typing import Dict, Any, List, Optional, Union
from ...config import settings
import json

# 配置日志记录
logger = logging.getLogger(__name__)

class SocialAgent:
    """
    社交媒体监控与数据收集代理
    
    该类负责从各种社交媒体平台（如小红书、Instagram、Pinterest等）
    收集和分析数据，实现自动化舆情监控和数据分析
    """
    _instance: Optional[ChatOpenAI] = None
    
    # 支持的平台列表
    SUPPORTED_PLATFORMS = ["小红书", "Instagram", "Pinterest", "Twitter", "微博", "抖音", "TikTok", "YouTube"]
    
    # 平台特定任务
    PLATFORM_TASKS = {
        "小红书": {
            "热门话题": "访问小红书并收集当前热门话题前{count}个，包括标题和点赞数",
            "用户笔记": "访问小红书用户{username}的主页，收集最新{count}条笔记的内容、发布时间和点赞数",
            "关键词搜索": "在小红书搜索{keywords}，收集前{count}条结果的标题、发布者和点赞数",
            "高赞内容": "在小红书搜索{keywords}，按点赞数排序，收集前{count}条高赞内容的标题、点赞数、评论数及核心卖点",
            "行业达人": "在小红书搜索{niche}行业的热门达人，收集前{count}名达人的用户名、粉丝数、内容风格和主要话题",
            "内容趋势": "分析小红书{niche}类目下最近一个月的内容趋势，包括热门话题、常用标签和爆款内容特点"
        },
        "Instagram": {
            "用户帖子": "访问Instagram用户{username}的主页，收集最新{count}条帖子的图片链接、发布时间和点赞数",
            "热门标签": "访问Instagram标签#{hashtag}页面，收集前{count}条热门帖子",
            "同类账号": "分析Instagram用户{username}的相似账号，找出{count}个内容风格相似的创作者",
            "增长账号": "查找Instagram中{niche}领域近期粉丝增长最快的{count}个账号及其内容特点",
            "互动分析": "分析Instagram账号{username}的互动数据，包括平均点赞数、评论数和参与率"
        },
        "Pinterest": {
            "收集灵感板": "访问Pinterest用户{username}的{board_name}灵感板，收集所有图片链接和描述",
            "趋势搜索": "在Pinterest上搜索{keywords}相关的趋势内容，收集前{count}个结果的图片和描述",
            "相关灵感板": "查找与{keyword}相关的热门灵感板，收集前{count}个灵感板的名称、创建者和内容概述"
        },
        "抖音": {
            "热门挑战": "查找抖音当前热门挑战/话题，收集前{count}个挑战的名称、参与人数和代表性视频",
            "创作者分析": "分析抖音创作者{username}的内容特点、粉丝构成和高赞视频类型",
            "热门音乐": "收集抖音当前热门音乐/BGM前{count}首，包括使用该音乐的热门视频类型"
        },
        "TikTok": {
            "趋势分析": "分析TikTok当前{count}个热门趋势及其内容特点",
            "创作者搜索": "查找TikTok上{niche}领域的热门创作者前{count}名"
        }
    }
    
    # 内容分析模板
    CONTENT_ANALYSIS_TEMPLATES = {
        "创作灵感": "基于以下关键词，生成{count}个{platform}平台的内容创作灵感:\n关键词: {keywords}\n目标领域: {niche}",
        "受众分析": "分析{platform}平台上{niche}领域的主要受众特征，包括年龄段、兴趣爱好、消费能力和内容偏好",
        "内容规划": "为{platform}平台的{niche}账号制定{period}内容规划，包括内容主题、发布频率和预期效果",
        "爆款解析": "深入分析{platform}平台{niche}领域的爆款内容模式，提取关键成功因素和可复制的元素"
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
    async def collect_from_platform(
        cls, 
        platform: str, 
        task_type: str, 
        use_vision: bool = True, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        从特定平台收集数据
        
        Args:
            platform: 社交媒体平台名称
            task_type: 任务类型
            use_vision: 是否使用视觉功能
            **kwargs: 任务特定参数
            
        Returns:
            包含收集结果的字典
        """
        if platform not in cls.SUPPORTED_PLATFORMS:
            return {
                "status": "error",
                "message": f"不支持的平台: {platform}，支持的平台有: {', '.join(cls.SUPPORTED_PLATFORMS)}"
            }
            
        if platform not in cls.PLATFORM_TASKS or task_type not in cls.PLATFORM_TASKS[platform]:
            return {
                "status": "error",
                "message": f"平台{platform}不支持任务类型: {task_type}"
            }
            
        try:
            # 获取任务模板并填充参数
            task_template = cls.PLATFORM_TASKS[platform][task_type]
            task = task_template.format(**kwargs)
            
            # 调用TaskAgent执行实际任务
            result = await TaskAgent.execute_task(task, use_vision)
            
            # 记录执行结果
            logger.info(f"从{platform}收集{task_type}数据: {result['status']}")
            
            # 添加平台和任务类型信息到结果
            result["platform"] = platform
            result["task_type"] = task_type
            
            return result
        except Exception as e:
            logger.error(f"从{platform}收集数据失败: {str(e)}")
            return {
                "status": "error",
                "message": f"从{platform}收集数据失败: {str(e)}",
                "platform": platform,
                "task_type": task_type
            }
    
    @classmethod
    async def monitor_sentiment(cls, keywords: List[str], platforms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        舆情监控功能
        
        Args:
            keywords: 需要监控的关键词列表
            platforms: 需要监控的平台列表，默认为所有支持的平台
            
        Returns:
            包含舆情分析结果的字典
        """
        if platforms is None:
            platforms = cls.SUPPORTED_PLATFORMS
            
        results = {}
        errors = []
        
        for platform in platforms:
            if platform not in cls.SUPPORTED_PLATFORMS:
                errors.append(f"不支持的平台: {platform}")
                continue
                
            try:
                # 构建舆情监控任务
                keywords_str = ', '.join(keywords)
                task = f"在{platform}上搜索关键词\"{keywords_str}\"，分析最新100条内容的情感倾向，统计正面评价和负面评价的比例，提取热门评论观点，返回JSON格式的分析结果"
                
                # 执行任务
                result = await TaskAgent.execute_task(task, use_vision=True)
                
                if result["status"] == "success":
                    results[platform] = result["result"]
                else:
                    errors.append(f"{platform}: {result['message']}")
            except Exception as e:
                logger.error(f"监控{platform}舆情失败: {str(e)}")
                errors.append(f"{platform}: {str(e)}")
                
        return {
            "status": "success" if results else "error",
            "message": "舆情监控完成" if not errors else f"部分平台监控失败: {', '.join(errors)}",
            "keywords": keywords,
            "platforms": platforms,
            "results": results,
            "errors": errors
        }
        
    @classmethod
    async def analyze_data(cls, data: str, analysis_type: str = "sentiment") -> Dict[str, Any]:
        """
        分析收集到的数据
        
        Args:
            data: 待分析的数据
            analysis_type: 分析类型，如情感分析、主题提取等
            
        Returns:
            包含分析结果的字典
        """
        try:
            llm = cls.get_llm()
            
            analysis_prompts = {
                "sentiment": f"对以下数据进行情感分析，识别正面、负面和中性观点的比例，提取关键观点。数据内容:\n{data}",
                "topics": f"从以下数据中提取主要话题和关键词，按重要性排序。数据内容:\n{data}",
                "trends": f"分析以下数据中的趋势和模式，找出重复出现的主题和随时间变化的趋势。数据内容:\n{data}",
                "audience": f"分析以下数据，提取目标受众的人口统计特征、兴趣爱好和内容偏好。数据内容:\n{data}",
                "engagement": f"分析以下数据中的互动模式，识别哪类内容获得最高互动率及其共同特点。数据内容:\n{data}"
            }
            
            if analysis_type not in analysis_prompts:
                return {
                    "status": "error",
                    "message": f"不支持的分析类型: {analysis_type}，支持的类型有: {', '.join(analysis_prompts.keys())}"
                }
            
            # 构建分析任务
            task = analysis_prompts[analysis_type]
            
            # 直接使用LLM进行分析，而不是通过浏览器
            response = await llm.ainvoke(task)
            
            return {
                "status": "success",
                "message": "数据分析完成",
                "analysis_type": analysis_type,
                "result": response
            }
        except Exception as e:
            logger.error(f"数据分析失败: {str(e)}")
            return {
                "status": "error",
                "message": f"数据分析失败: {str(e)}",
                "analysis_type": analysis_type
            }
    
    @classmethod
    async def find_trending_content(
        cls,
        platform: str,
        niche: str,
        count: int = 10,
        time_period: str = "本周",
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        查找某领域的热门/趋势内容
        
        Args:
            platform: 社交媒体平台
            niche: 内容领域/类目
            count: 返回结果数量
            time_period: 时间范围
            use_vision: 是否使用视觉功能
            
        Returns:
            包含热门内容的字典
        """
        try:
            task = f"""在{platform}上搜索{time_period}内{niche}领域的热门内容，收集前{count}个热门内容的以下信息:
1. 内容标题/简述
2. 创作者信息
3. 互动数据（点赞、评论、分享）
4. 发布时间
5. 核心卖点或吸引因素
6. 使用的标签/话题

请以结构化JSON格式返回分析结果，确保包含所有可获取的信息。
"""
            
            result = await TaskAgent.execute_task(task, use_vision)
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "热门内容查找完成",
                    "platform": platform,
                    "niche": niche,
                    "time_period": time_period,
                    "count": count,
                    "result": result["result"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"热门内容查找失败: {result['message']}",
                    "platform": platform,
                    "niche": niche
                }
        except Exception as e:
            logger.error(f"热门内容查找失败: {str(e)}")
            return {
                "status": "error",
                "message": f"热门内容查找失败: {str(e)}",
                "platform": platform,
                "niche": niche
            }
    
    @classmethod
    async def find_similar_creators(
        cls,
        platform: str,
        creator: str,
        count: int = 5,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        查找相似创作者
        
        Args:
            platform: 社交媒体平台
            creator: 参考创作者用户名
            count: 返回结果数量
            use_vision: 是否使用视觉功能
            
        Returns:
            包含相似创作者的字典
        """
        try:
            task = f"""在{platform}上查找与{creator}相似的创作者，收集{count}个相似创作者的以下信息:
1. 用户名/账号
2. 粉丝数量
3. 内容风格和主题
4. 特色或差异化卖点
5. 高互动内容示例

请以结构化JSON格式返回分析结果。
"""
            
            result = await TaskAgent.execute_task(task, use_vision)
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "相似创作者查找完成",
                    "platform": platform,
                    "reference_creator": creator,
                    "count": count,
                    "result": result["result"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"相似创作者查找失败: {result['message']}",
                    "platform": platform,
                    "reference_creator": creator
                }
        except Exception as e:
            logger.error(f"相似创作者查找失败: {str(e)}")
            return {
                "status": "error",
                "message": f"相似创作者查找失败: {str(e)}",
                "platform": platform,
                "reference_creator": creator
            }
    
    @classmethod
    async def generate_content_ideas(
        cls,
        platform: str,
        niche: str,
        keywords: List[str],
        count: int = 10
    ) -> Dict[str, Any]:
        """
        生成内容创作灵感
        
        Args:
            platform: 目标平台
            niche: 内容领域
            keywords: 关键词列表
            count: 灵感数量
            
        Returns:
            包含内容灵感的字典
        """
        try:
            llm = cls.get_llm()
            
            keywords_str = ", ".join(keywords)
            
            prompt = f"""作为{platform}平台的内容创作专家，请为{niche}领域生成{count}个独特的内容创作灵感。

关键词: {keywords_str}

对于每个内容灵感，请提供:
1. 引人注目的标题/主题
2. 内容简述（包括核心卖点）
3. 适合的内容类型（图片、视频、长文等）
4. 建议的话题标签
5. 受众吸引点

请确保这些灵感具有以下特点:
- 符合平台特性和算法偏好
- 有病毒式传播的潜力
- 独特且能引起受众共鸣
- 可以展示专业知识或个人特色

请以结构化JSON格式返回结果。
"""
            
            response = await llm.ainvoke(prompt)
            
            return {
                "status": "success",
                "message": "内容灵感生成完成",
                "platform": platform,
                "niche": niche,
                "keywords": keywords,
                "count": count,
                "result": response
            }
        except Exception as e:
            logger.error(f"内容灵感生成失败: {str(e)}")
            return {
                "status": "error",
                "message": f"内容灵感生成失败: {str(e)}",
                "platform": platform,
                "niche": niche
            }
    
    @classmethod
    async def analyze_creator_growth(
        cls,
        platform: str,
        creator: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        分析创作者增长数据
        
        Args:
            platform: 社交媒体平台
            creator: 创作者用户名
            use_vision: 是否使用视觉功能
            
        Returns:
            包含创作者分析的字典
        """
        try:
            task = f"""访问{platform}上{creator}的账号，分析该创作者的以下方面:
1. 粉丝增长趋势（如可获取）
2. 内容发布频率和规律
3. 高互动内容特点（收集3-5个代表性案例）
4. 内容风格和传播策略
5. 盈利模式（广告合作、自有产品等）
6. 受众特征和互动模式

请详细分析其成功因素，并以结构化JSON格式返回结果。
"""
            
            result = await TaskAgent.execute_task(task, use_vision)
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "创作者分析完成",
                    "platform": platform,
                    "creator": creator,
                    "result": result["result"]
                }
            else:
                return {
                    "status": "error",
                    "message": f"创作者分析失败: {result['message']}",
                    "platform": platform,
                    "creator": creator
                }
        except Exception as e:
            logger.error(f"创作者分析失败: {str(e)}")
            return {
                "status": "error",
                "message": f"创作者分析失败: {str(e)}",
                "platform": platform,
                "creator": creator
            }
    
    @classmethod
    async def collect_inspiration(
        cls,
        keywords: List[str],
        sources: List[str] = ["Pinterest", "Instagram", "Dribbble"],
        count_per_source: int = 5,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        从多个平台收集创意灵感
        
        Args:
            keywords: 关键词列表
            sources: 灵感来源平台
            count_per_source: 每个来源的收集数量
            use_vision: 是否使用视觉功能
            
        Returns:
            包含灵感收集结果的字典
        """
        keywords_str = ", ".join(keywords)
        results = {}
        errors = []
        
        for source in sources:
            if source not in cls.SUPPORTED_PLATFORMS:
                errors.append(f"不支持的平台: {source}")
                continue
                
            try:
                task = f"""在{source}上搜索"{keywords_str}"，收集{count_per_source}个创意灵感:
1. 图片/内容链接（如可获取）
2. 作者/创作者信息
3. 简短描述
4. 主要设计/创意元素
5. 标签或分类

请确保收集多样化的灵感，并以结构化JSON格式返回结果。
"""
                
                result = await TaskAgent.execute_task(task, use_vision)
                
                if result["status"] == "success":
                    results[source] = result["result"]
                else:
                    errors.append(f"{source}: {result['message']}")
            except Exception as e:
                logger.error(f"从{source}收集灵感失败: {str(e)}")
                errors.append(f"{source}: {str(e)}")
                
        return {
            "status": "success" if results else "error",
            "message": "灵感收集完成" if not errors else f"部分平台收集失败: {', '.join(errors)}",
            "keywords": keywords,
            "sources": sources,
            "results": results,
            "errors": errors
        } 