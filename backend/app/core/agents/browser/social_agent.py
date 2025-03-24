from typing import Dict, Any, List, Optional, Union
import logging
from .browser_task_agent import BrowserTaskAgent
from ..templates.template_manager import TemplateManager, TemplateCategory

# 配置日志记录
logger = logging.getLogger(__name__)

class SocialAgent(BrowserTaskAgent):
    """
    社交媒体智能体
    
    负责从各大社交媒体平台收集和分析数据，
    支持内容监控、趋势分析、创作者分析等功能
    """
    
    @classmethod
    async def execute_social_task(
        cls,
        platform: str,
        task_type: str,
        parameters: Dict[str, Any] = None,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        执行社交媒体相关任务的便捷方法
        
        自动设置TemplateCategory为SOCIAL，简化调用
        
        Args:
            platform: 平台名称
            task_type: 任务类型
            parameters: 任务参数
            use_vision: 是否使用视觉能力
            
        Returns:
            任务执行结果
        """
        return await cls.execute_category_task(
            category=TemplateCategory.SOCIAL,
            platform=platform,
            task_type=task_type,
            parameters=parameters or {},
            use_vision=use_vision
        )
    
    @classmethod
    async def collect_from_platform(
        cls, 
        platform: str, 
        task_type: str, 
        use_vision: bool = True, 
        **params
    ) -> Dict[str, Any]:
        """
        从社交媒体平台收集数据
        
        Args:
            platform: 社交媒体平台名称
            task_type: 任务类型
            use_vision: 是否使用视觉功能
            **params: 任务特定参数
            
        Returns:
            包含收集到的数据的字典
        """
        # 获取支持的平台列表
        supported_platforms = TemplateManager.get_supported_social_platforms()
        
        # 验证平台
        error = cls.validate_platform(platform, supported_platforms)
        if error:
            return error
        
        # 获取平台支持的任务类型
        supported_task_types = TemplateManager.get_platform_task_types(TemplateCategory.SOCIAL, platform)
        
        # 验证任务类型
        if task_type not in supported_task_types:
            return cls.format_error_response(f"平台{platform}不支持任务类型: {task_type}")
            
        try:
            # 执行任务
            result = await cls.execute_social_task(
                platform=platform,
                task_type=task_type,
                parameters=params,
                use_vision=use_vision
            )
            
            # 记录执行结果
            logger.info(f"从{platform}收集{task_type}数据: {result['status']}")
            
            # 添加平台和任务类型信息到结果
            result["platform"] = platform
            result["task_type"] = task_type
            
            return result
        except Exception as e:
            logger.error(f"从{platform}收集数据失败: {str(e)}")
            return cls.format_error_response(
                f"从{platform}收集数据失败: {str(e)}",
                platform=platform,
                task_type=task_type
            )
    
    @classmethod
    async def monitor_sentiment(
        cls,
        keywords: List[str],
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        监控社交媒体平台的舆情
        
        Args:
            keywords: 要监控的关键词列表
            platforms: 要监控的平台列表，如果为None则监控所有支持的平台
            
        Returns:
            包含舆情监控结果的字典
        """
        if not platforms:
            platforms = TemplateManager.get_supported_social_platforms()
            
        results = {}
        errors = []
        
        for platform in platforms:
            try:
                # 构建任务
                task = f"""在{platform}平台搜索以下关键词的最新舆情信息:
                
                关键词: {', '.join(keywords)}
                
                请分析以下内容:
                1. 关键词近期热度
                2. 正面评价要点
                3. 负面评价要点
                4. 中性讨论主题
                5. 舆情发展趋势
                
                对每个关键词提供单独分析，最后给出综合评估。
                """
                
                # 执行任务
                result = await cls.execute_social_task(
                    platform=platform,
                    task_type="sentiment",
                    parameters={"keywords": keywords},
                    use_vision=True
                )
                
                if result["status"] == "success":
                    results[platform] = result["result"]
                else:
                    errors.append(f"{platform}: {result['message']}")
                    
            except Exception as e:
                errors.append(f"{platform}: {str(e)}")
                logger.error(f"监控{platform}舆情失败: {str(e)}")
                
        if results:
            return cls.format_success_response(
                message="舆情监控完成",
                keywords=keywords,
                platforms=platforms,
                results=results,
                errors=errors if errors else None
            )
        else:
            return cls.format_error_response(
                f"所有平台舆情监控失败: {'; '.join(errors)}",
                keywords=keywords,
                platforms=platforms
            )
    
    @classmethod
    async def analyze_data(
        cls,
        data: str,
        analysis_type: str = "sentiment"
    ) -> Dict[str, Any]:
        """
        分析收集到的数据
        
        Args:
            data: 要分析的数据文本
            analysis_type: 分析类型，如sentiment (情感分析)、trend (趋势分析) 等
            
        Returns:
            包含分析结果的字典
        """
        analysis_types = {
            "sentiment": "对以下内容进行情感分析，区分正面、负面和中性评价，计算各类别占比",
            "trend": "分析以下内容中的主要趋势和模式，识别关键主题和变化",
            "demographic": "分析以下内容的人口统计学特征，如年龄、性别、地域等分布",
            "topic": "对以下内容进行主题分析，识别主要讨论主题和子主题"
        }
        
        if analysis_type not in analysis_types:
            return cls.format_error_response(
                f"不支持的分析类型: {analysis_type}，支持的类型有: {', '.join(analysis_types.keys())}"
            )
            
        try:
            # 构建任务
            task = f"""{analysis_types[analysis_type]}:
            
            {data}
            
            请提供详细分析并用数据支持你的发现。
            """
            
            # 执行任务
            result = await cls.execute_social_task(
                platform="",
                task_type=analysis_type,
                parameters={"data": data},
                use_vision=False
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"{analysis_type}分析完成",
                    analysis_type=analysis_type,
                    analysis_result=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"数据分析错误: {str(e)}")
            return cls.format_error_response(
                f"数据分析错误: {str(e)}",
                analysis_type=analysis_type
            )
            
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
        查找热门内容
        
        Args:
            platform: 社交媒体平台
            niche: 内容领域/类目
            count: 需要返回的内容数量
            time_period: 时间范围 (今日, 本周, 本月等)
            use_vision: 是否使用视觉功能
            
        Returns:
            包含热门内容的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_social_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""在{platform}平台搜索{time_period}{niche}领域的热门内容，找出排名前{count}的内容:
            
            请收集以下信息:
            1. 内容标题/描述
            2. 创作者名称
            3. 发布时间
            4. 互动数据 (点赞, 评论, 转发等)
            5. 内容主题和关键点
            
            对热门内容进行分析，找出共同特点和成功要素。
            """
            
            # 执行任务
            result = await cls.execute_social_task(
                platform=platform,
                task_type="trending_content",
                parameters={"niche": niche, "count": count, "time_period": time_period},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"已找到{platform}平台的热门{niche}内容",
                    platform=platform,
                    niche=niche,
                    time_period=time_period,
                    count=count,
                    trending_content=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"查找热门内容错误: {str(e)}")
            return cls.format_error_response(
                f"查找热门内容错误: {str(e)}",
                platform=platform,
                niche=niche
            )
    
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
            creator: 参考创作者
            count: 需要返回的创作者数量
            use_vision: 是否使用视觉功能
            
        Returns:
            包含相似创作者的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_social_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""在{platform}平台查找与{creator}类似的创作者，找出最相似的{count}个:
            
            请先研究{creator}的:
            1. 内容风格和主题
            2. 目标受众
            3. 互动特点
            
            然后查找相似创作者，收集:
            1. 创作者名称/ID
            2. 粉丝数量
            3. 内容类型和特点
            4. 与参考创作者的相似点
            5. 独特之处
            
            提供详细比较分析。
            """
            
            # 执行任务
            result = await cls.execute_social_task(
                platform=platform,
                task_type="similar_creators",
                parameters={"creator": creator, "count": count},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"已找到与{creator}相似的创作者",
                    platform=platform,
                    reference_creator=creator,
                    count=count,
                    similar_creators=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"查找相似创作者错误: {str(e)}")
            return cls.format_error_response(
                f"查找相似创作者错误: {str(e)}",
                platform=platform,
                creator=creator
            )
    
    @classmethod
    async def generate_content_ideas(
        cls,
        platform: str,
        niche: str,
        keywords: List[str],
        count: int = 5
    ) -> Dict[str, Any]:
        """
        生成内容创意
        
        Args:
            platform: 社交媒体平台
            niche: 内容领域/类目
            keywords: 相关关键词
            count: 需要生成的创意数量
            
        Returns:
            包含内容创意的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_social_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""为{platform}平台的{niche}领域生成{count}个内容创意，围绕以下关键词:
            
            关键词: {', '.join(keywords)}
            
            对每个创意，提供:
            1. 引人注目的标题
            2. 内容简介 (200-300字)
            3. 关键卖点和吸引点
            4. 目标受众
            5. 预期效果和互动方式
            
            确保创意符合{platform}平台的内容特点和受众习惯。
            """
            
            # 执行任务
            result = await cls.execute_social_task(
                platform=platform,
                task_type="content_ideas",
                parameters={"niche": niche, "keywords": keywords, "count": count},
                use_vision=False
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"已为{platform}平台生成{niche}领域的内容创意",
                    platform=platform,
                    niche=niche,
                    keywords=keywords,
                    count=count,
                    content_ideas=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"生成内容创意错误: {str(e)}")
            return cls.format_error_response(
                f"生成内容创意错误: {str(e)}",
                platform=platform,
                niche=niche
            )
    
    @classmethod
    async def analyze_creator(
        cls,
        platform: str,
        creator: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        分析创作者
        
        Args:
            platform: 社交媒体平台
            creator: 创作者名称/ID
            use_vision: 是否使用视觉功能
            
        Returns:
            包含创作者分析的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_social_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""在{platform}平台分析创作者{creator}，收集以下信息:
            
            1. 基本信息 (粉丝数, 发布频率, 账号创建时间等)
            2. 内容类型和主题分布
            3. 互动数据分析 (平均点赞, 评论, 转发等)
            4. 受众特征和粉丝画像
            5. 内容风格和特点
            6. 成功内容案例分析
            7. 商业合作和变现方式
            
            提供全面分析并给出该创作者的优势和特点。
            """
            
            # 执行任务
            result = await cls.execute_social_task(
                platform=platform,
                task_type="creator_analysis",
                parameters={"creator": creator},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"已完成对{platform}平台创作者{creator}的分析",
                    platform=platform,
                    creator=creator,
                    creator_analysis=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"分析创作者错误: {str(e)}")
            return cls.format_error_response(
                f"分析创作者错误: {str(e)}",
                platform=platform,
                creator=creator
            )
    
    @classmethod
    async def collect_inspiration(
        cls,
        keywords: List[str],
        sources: List[str],
        count_per_source: int = 3,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        收集灵感素材
        
        Args:
            keywords: 关键词列表
            sources: 来源列表 (平台或网站)
            count_per_source: 每个来源收集的素材数量
            use_vision: 是否使用视觉功能
            
        Returns:
            包含灵感素材的字典
        """
        results = {}
        errors = []
        
        for source in sources:
            try:
                # 构建任务
                task = f"""在{source}搜索关于{', '.join(keywords)}的灵感素材，收集{count_per_source}个最有创意的例子:
                
                对每个例子收集:
                1. 标题/描述
                2. 创作者/来源
                3. 创意亮点和独特之处
                4. 视觉元素描述
                5. 受众反应和互动情况
                
                选择最具启发性和创新性的例子，并说明它们的优点。
                """
                
                # 执行任务
                result = await cls.execute_social_task(
                    platform=source,
                    task_type="inspiration",
                    parameters={"keywords": keywords, "count_per_source": count_per_source},
                    use_vision=use_vision
                )
                
                if result["status"] == "success":
                    results[source] = result["result"]
                else:
                    errors.append(f"{source}: {result['message']}")
                    
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
                logger.error(f"从{source}收集灵感素材失败: {str(e)}")
                
        if results:
            return cls.format_success_response(
                message="灵感素材收集完成",
                keywords=keywords,
                sources=sources,
                count_per_source=count_per_source,
                results=results,
                errors=errors if errors else None
            )
        else:
            return cls.format_error_response(
                f"所有来源灵感素材收集失败: {'; '.join(errors)}",
                keywords=keywords,
                sources=sources
            ) 