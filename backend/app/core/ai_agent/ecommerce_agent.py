import logging
from langchain_openai import ChatOpenAI
from .task_agent import TaskAgent
from typing import Dict, Any, List, Optional, Union
from ...config import settings

# 配置日志记录
logger = logging.getLogger(__name__)

class EcommerceAgent:
    """
    电商运营代理
    
    该类负责执行电商相关任务，如产品搜索、上货素材生成、竞品分析、
    供应商查找和产品潜力评估等
    """
    _instance: Optional[ChatOpenAI] = None
    
    # 支持的平台列表
    SUPPORTED_PLATFORMS = ["亚马逊", "淘宝", "京东", "拼多多", "天猫", "速卖通", "Shopee", "Shopify", "跨境通", "1688", "阿里巴巴"]
    
    # 平台特定任务
    PLATFORM_TASKS = {
        "亚马逊": {
            "热销产品": "访问亚马逊，查找{category}类目下销量前{count}的产品，收集产品名称、价格、评分和评价数量",
            "评价分析": "查找亚马逊产品{product_id}的评价，分析前{count}条评价的情感倾向和主要反馈点",
            "竞品比较": "在亚马逊搜索{keywords}，比较前{count}个产品的价格、评分、功能特点和卖点",
            "产品趋势": "分析亚马逊{category}类目近期热销产品的共同特点和趋势",
            "BSR变化": "追踪亚马逊产品{product_id}在过去{period}的BSR变化趋势"
        },
        "淘宝": {
            "热销分析": "在淘宝搜索{keywords}，收集销量前{count}名产品的信息，包括价格、销量、店铺等级",
            "店铺考察": "分析淘宝店铺{shop_id}，收集主营产品、销量、评分和客户评价情况",
            "直播数据": "收集淘宝{category}类目热门直播带货数据，包括主播、销量和转化率",
            "价格区间": "分析淘宝{keywords}产品的主要价格区间分布和各区间的销量占比"
        },
        "拼多多": {
            "爆款产品": "在拼多多搜索{keywords}，收集销量前{count}名产品的信息和关键卖点",
            "低价策略": "分析拼多多{category}类目下的低价策略和销量关系",
            "团购效果": "收集拼多多{keywords}产品的团购数据和转化效果"
        },
        "1688": {
            "供应商考察": "在1688搜索{product}的供应商，收集前{count}名供应商的基本信息、产品价格、起订量和评分",
            "工厂直供": "查找1688上{product}的工厂直供货源，比较价格和质量",
            "原料搜索": "在1688上搜索{material}原料供应商，收集价格、起订量和供货能力"
        },
        "速卖通": {
            "跨境热销": "分析速卖通{category}类目在{country}市场的热销产品",
            "价格对比": "对比速卖通和亚马逊上{product}产品的价格差异和市场表现",
            "买家分析": "收集速卖通{product}产品的主要购买国家和买家特征"
        },
        "Shopee": {
            "东南亚市场": "分析Shopee平台{country}市场{category}类目的热销产品和价格区间",
            "卖家排名": "查找Shopee{category}类目销量前{count}的卖家及其主打产品"
        }
    }
    
    # 电商分析模板
    ECOMMERCE_TEMPLATES = {
        "产品上架": "为{product}创建{platform}平台的上架素材，包括标题、描述、卖点和关键词",
        "竞品分析": "分析{platform}平台上与{product_keyword}相关的竞争产品，提取价格区间、主要功能和用户评价",
        "定价策略": "基于{platform}平台{product}的成本{cost}和竞品价格{competitor_prices}，制定最优定价策略",
        "营销文案": "为{platform}平台的{product}创建营销文案，突出以下卖点: {features}",
        "市场潜力": "评估{product_info}在{platform}平台{niche}领域的市场潜力，考虑竞争度、需求和增长趋势",
        "供应链分析": "为{product}查找并分析潜在供应商，比较价格、质量和供货能力"
    }
    
    # 上货模板类型
    LISTING_TEMPLATES = {
        "标准上货": "标准格式的产品上架素材，包括标题、5点卖点和描述",
        "亚马逊专用": "亚马逊平台专用上架格式，包括标题、要点、描述和搜索关键词",
        "简约风格": "简洁明了的产品上架素材，突出核心卖点",
        "详细描述": "包含丰富细节的产品描述，适合复杂或高端产品",
        "创意文案": "具有吸引力和创意的产品文案，适合时尚或生活方式产品"
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
    async def search_products(
        cls, 
        platform: str, 
        task_type: str, 
        use_vision: bool = True, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        在电商平台搜索产品
        
        Args:
            platform: 电商平台名称
            task_type: 任务类型
            use_vision: 是否使用视觉功能
            **kwargs: 任务特定参数
            
        Returns:
            包含搜索结果的字典
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
            
            # 执行任务
            result = await TaskAgent.execute_task(task, use_vision=use_vision)
            
            return {
                "status": result["status"],
                "message": result["message"],
                "platform": platform,
                "task_type": task_type,
                "parameters": kwargs,
                "result": result["result"] if result["status"] == "success" else None
            }
        except KeyError as e:
            error_msg = f"缺少参数: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "platform": platform,
                "task_type": task_type
            }
        except Exception as e:
            error_msg = f"产品搜索错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "platform": platform,
                "task_type": task_type
            }
    
    @classmethod
    async def generate_listing(
        cls,
        template_type: str,
        product: str,
        features: Optional[str] = None,
        platform: Optional[str] = None,
        description: Optional[str] = None,
        cost: Optional[float] = None,
        competitor_prices: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成电商上货素材
        
        Args:
            template_type: 模板类型
            product: 产品名称
            features: 产品特点
            platform: 目标平台
            description: 产品描述
            cost: 产品成本
            competitor_prices: 竞品价格
            
        Returns:
            包含生成结果的字典
        """
        if template_type not in cls.LISTING_TEMPLATES:
            return {
                "status": "error",
                "message": f"未知的模板类型: {template_type}，可用模板: {', '.join(cls.LISTING_TEMPLATES.keys())}"
            }
            
        try:
            # 构建提示词
            template_description = cls.LISTING_TEMPLATES[template_type]
            
            prompt = f"""请为以下产品生成{template_type}格式的电商上货素材:

产品: {product}
"""
            if features:
                prompt += f"产品特点: {features}\n"
                
            if description:
                prompt += f"产品描述: {description}\n"
                
            if platform:
                prompt += f"目标平台: {platform}\n"
                
            if cost:
                prompt += f"产品成本: {cost}\n"
                
            if competitor_prices:
                prompt += f"竞品价格: {competitor_prices}\n"
                
            prompt += f"""
模板说明: {template_description}

请按以下格式输出:
1. 产品标题 (吸引人且包含关键词)
2. 产品要点 (5点主要卖点)
3. 产品描述 (详细介绍产品特点和使用场景)
4. 搜索关键词 (10-15个相关关键词)
5. 建议售价 (如提供了成本或竞品价格)
"""
            
            # 使用TaskAgent执行，因为可能需要搜索竞品信息
            use_vision = False
            if platform:
                use_vision = True
                prompt += f"\n在生成上货素材前，请先在{platform}平台搜索同类产品，了解标题格式和关键卖点。"
                
            result = await TaskAgent.execute_task(prompt, use_vision=use_vision)
            
            return {
                "status": result["status"],
                "message": "上货素材生成成功" if result["status"] == "success" else result["message"],
                "template_type": template_type,
                "product": product,
                "platform": platform,
                "listing_content": result["result"] if result["status"] == "success" else None
            }
        except Exception as e:
            error_msg = f"生成上货素材错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "template_type": template_type,
                "product": product
            }
    
    @classmethod
    async def analyze_product_potential(
        cls,
        product_info: str,
        niche: str,
        platform: str = "全平台",
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        分析产品在市场中的潜力
        
        Args:
            product_info: 产品信息
            niche: 产品所在领域
            platform: 目标平台
            dimensions: 评估维度
            
        Returns:
            包含分析结果的字典
        """
        try:
            # 默认评估维度
            if not dimensions:
                dimensions = ["市场规模", "竞争程度", "利润空间", "趋势发展", "进入壁垒"]
                
            dimensions_str = "、".join(dimensions)
            
            prompt = f"""请分析以下产品在{platform}平台{niche}领域的市场潜力:

产品信息: {product_info}

请从以下维度进行全面评估:
{dimensions_str}

评分标准:
1-10分评分(1分最低，10分最高)，并提供详细分析。

输出格式:
1. 总体评分: [1-10分]
2. 各维度详细分析:
   - [维度1]: [评分] - [分析]
   - [维度2]: [评分] - [分析]
   ...
3. 市场机会:
   [列出3-5个市场机会点]
4. 潜在风险:
   [列出3-5个潜在风险]
5. 建议策略:
   [提供3-5条进入该市场的建议策略]
"""
            
            # 执行任务
            use_vision = platform != "全平台"  # 如果指定了具体平台，使用视觉搜索该平台
            if use_vision:
                prompt += f"\n请先在{platform}搜索\"{niche} {product_info.split()[0]}\"，了解市场现状后再进行分析。"
                
            result = await TaskAgent.execute_task(prompt, use_vision=use_vision)
            
            return {
                "status": result["status"],
                "message": "产品潜力分析完成" if result["status"] == "success" else result["message"],
                "product_info": product_info,
                "niche": niche,
                "platform": platform,
                "dimensions": dimensions,
                "analysis_result": result["result"] if result["status"] == "success" else None
            }
        except Exception as e:
            error_msg = f"产品潜力分析错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "product_info": product_info,
                "niche": niche
            }
    
    @classmethod
    async def analyze_competition(
        cls,
        product_keyword: str,
        platform: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        分析产品在特定平台的竞争情况
        
        Args:
            product_keyword: 产品关键词
            platform: 电商平台
            use_vision: 是否使用视觉功能
            
        Returns:
            包含竞争分析结果的字典
        """
        if platform not in cls.SUPPORTED_PLATFORMS:
            return {
                "status": "error",
                "message": f"不支持的平台: {platform}，支持的平台有: {', '.join(cls.SUPPORTED_PLATFORMS)}"
            }
            
        try:
            prompt = f"""请访问{platform}平台，搜索"{product_keyword}"，分析前10个搜索结果的竞争情况:

请收集和分析以下信息:
1. 价格区间分析 (最低价、最高价、平均价、主流价格区间)
2. 销量/评价数量对比
3. 主要竞争品牌/卖家 (前3-5名)
4. 产品特点和卖点对比
5. 用户评价分析 (主要正面评价和负面评价)
6. 广告/推广情况 (搜索结果中的广告比例)
7. 市场定位分析 (高端、中端、低端市场分布)

输出格式:
请以结构化JSON格式输出分析结果，包含上述各项分析。
"""
            
            # 执行任务
            result = await TaskAgent.execute_task(prompt, use_vision=use_vision)
            
            return {
                "status": result["status"],
                "message": "竞品分析完成" if result["status"] == "success" else result["message"],
                "product_keyword": product_keyword,
                "platform": platform,
                "analysis_result": result["result"] if result["status"] == "success" else None
            }
        except Exception as e:
            error_msg = f"竞品分析错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "product_keyword": product_keyword,
                "platform": platform
            }
    
    @classmethod
    async def find_suppliers(
        cls,
        product: str,
        count: int = 5,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        查找产品供应商
        
        Args:
            product: 产品名称
            count: 需要查找的供应商数量
            use_vision: 是否使用视觉功能
            
        Returns:
            包含供应商信息的字典
        """
        try:
            platforms = ["1688", "阿里巴巴", "淘宝批发"]
            platforms_str = "、".join(platforms)
            
            prompt = f"""请在{platforms_str}上搜索"{product}"的供应商，找出最优质的{count}家供应商。

请收集以下信息:
1. 供应商名称
2. 供应商评分/等级
3. 主营产品
4. 产品价格范围
5. 最小起订量
6. 工厂/贸易商类型
7. 发货地
8. 联系方式(如有)

对于每个供应商，请尽量收集上述所有信息，并按性价比排序。
"""
            
            # 执行任务
            result = await TaskAgent.execute_task(prompt, use_vision=use_vision)
            
            return {
                "status": result["status"],
                "message": "供应商查找完成" if result["status"] == "success" else result["message"],
                "product": product,
                "count": count,
                "supplier_info": result["result"] if result["status"] == "success" else None
            }
        except Exception as e:
            error_msg = f"查找供应商错误: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "product": product
            } 