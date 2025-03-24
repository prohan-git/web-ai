from typing import Dict, Any, List, Optional, Union
import logging
import hashlib
import time
from .browser_task_agent import BrowserTaskAgent
from ..templates.template_manager import TemplateManager, TemplateCategory

# 配置日志记录
logger = logging.getLogger(__name__)

class EcommerceAgent(BrowserTaskAgent):
    """
    电子商务智能体
    
    负责从电子商务平台收集和分析数据，
    支持产品搜索、价格监控、竞品分析等功能
    """

    
    @classmethod
    async def search_products(
        cls,
        platform: str,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance",
        use_vision: bool = True,
        **filters
    ) -> Dict[str, Any]:
        """
        搜索产品
        
        Args:
            platform: 电商平台名称
            query: 搜索关键词
            max_results: 最大结果数量
            sort_by: 排序方式 (relevance, price_low, price_high, rating, sales)
            use_vision: 是否使用视觉能力
            **filters: 过滤条件 (如价格范围、品牌等)
            
        Returns:
            包含搜索结果的字典
        """
        # 获取支持的平台列表
        supported_platforms = TemplateManager.get_supported_ecommerce_platforms()
        
        # 验证平台
        error = cls.validate_platform(platform, supported_platforms)
        if error:
            return error
            
        try:
            # 准备过滤条件
            filter_text = ""
            if filters:
                filter_text = "过滤条件:\n"
                for key, value in filters.items():
                    filter_text += f"- {key}: {value}\n"
                    
            # 准备排序方式
            sort_methods = {
                "relevance": "按相关性排序",
                "price_low": "按价格从低到高排序",
                "price_high": "按价格从高到低排序",
                "rating": "按评分排序",
                "sales": "按销量排序"
            }
            
            sort_text = sort_methods.get(sort_by, "按相关性排序")
            
            # 构建任务
            task_params = {
                "platform": platform,
                "query": query,
                "max_results": max_results,
                "sort_text": sort_text,
                "filter_text": filter_text
            }
            
            # 执行任务
            result = await cls.execute_task(
                platform=platform,
                task_type="search",
                parameters=task_params,
                use_vision=use_vision
            )
            
            # 记录执行结果
            logger.info(f"在{platform}搜索产品: {query}, 状态: {result['status']}")
            
            # 添加搜索信息到结果
            if result["status"] == "success":
                result["platform"] = platform
                result["query"] = query
                result["filters"] = filters if filters else None
                result["sort_by"] = sort_by
                
            return result
        except Exception as e:
            logger.error(f"搜索产品失败: {str(e)}")
            return cls.format_error_response(
                f"搜索产品失败: {str(e)}",
                platform=platform,
                query=query
            )
    
    @classmethod
    async def monitor_price(
        cls,
        platform: str,
        product_urls: List[str],
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        监控产品价格
        
        Args:
            platform: 电商平台名称
            product_urls: 产品URL列表
            use_vision: 是否使用视觉能力
            
        Returns:
            包含价格监控结果的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        results = []
        errors = []
        
        for url in product_urls:
            try:
                # 构建任务
                task = f"""访问以下{platform}产品链接，获取价格信息:
                
                URL: {url}
                
                请提供:
                1. 产品名称
                2. 当前价格
                3. 原始价格 (如有折扣)
                4. 折扣率 (如有)
                5. 促销活动 (如有)
                6. 运费
                7. 库存状态
                
                重点是准确获取各类价格信息。
                """
                
                # 执行任务
                result = await cls.execute_ecommerce_task(
                    platform=platform,
                    task_type="monitor_price",
                    parameters={"product_urls": [url]},
                    use_vision=use_vision
                )
                
                if result["status"] == "success":
                    results.append({
                        "url": url,
                        "details": result["result"]
                    })
                else:
                    errors.append(f"{url}: {result['message']}")
                    
            except Exception as e:
                errors.append(f"{url}: {str(e)}")
                logger.error(f"监控价格失败 {url}: {str(e)}")
                
        if results:
            return cls.format_success_response(
                message="价格监控完成",
                platform=platform,
                results=results,
                errors=errors if errors else None
            )
        else:
            return cls.format_error_response(
                f"所有产品价格监控失败: {'; '.join(errors)}",
                platform=platform,
                product_urls=product_urls
            )
    
    @classmethod
    async def analyze_reviews(
        cls,
        platform: str,
        product_url: str,
        review_count: int = 20,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        分析产品评论
        
        Args:
            platform: 电商平台名称
            product_url: 产品URL
            review_count: 要分析的评论数量
            use_vision: 是否使用视觉能力
            
        Returns:
            包含评论分析的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""访问以下{platform}产品链接，分析最近{review_count}条评论:
            
            URL: {product_url}
            
            请提供:
            1. 产品基本信息 (名称、类别、品牌)
            2. 评分分布情况
            3. 正面评价要点 (按频率排序)
            4. 负面评价要点 (按频率排序)
            5. 常见问题和顾虑
            6. 顾客对产品的主要使用场景
            7. 最具代表性的正面与负面评论摘要
            
            对评论内容进行详细分析，提炼出关键洞察。
            """
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="analyze_reviews",
                parameters={"product_url": product_url, "review_count": review_count},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message="评论分析完成",
                    platform=platform,
                    product_url=product_url,
                    review_count=review_count,
                    analysis=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"分析评论失败: {str(e)}")
            return cls.format_error_response(
                f"分析评论失败: {str(e)}",
                platform=platform,
                product_url=product_url
            )
    
    @classmethod
    async def compare_products(
        cls,
        platform: str,
        product_urls: List[str],
        aspects: Optional[List[str]] = None,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        比较产品
        
        Args:
            platform: 电商平台名称
            product_urls: 产品URL列表
            aspects: 比较方面 (如价格、质量、功能等)
            use_vision: 是否使用视觉能力
            
        Returns:
            包含产品比较的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        # 默认比较方面
        if not aspects:
            aspects = ["价格", "质量", "功能", "评分", "性价比"]
            
        try:
            # 构建任务
            urls_text = "\n".join([f"- {url}" for url in product_urls])
            aspects_text = ", ".join(aspects)
            
            task = f"""比较以下{platform}产品的详细信息:
            
            产品链接:
            {urls_text}
            
            请重点比较以下方面:
            {aspects_text}
            
            请提供:
            1. 各产品基本信息概览 (名称、品牌、价格)
            2. 按比较方面做详细对比表格
            3. 各产品主要优势和劣势
            4. 适用人群和场景分析
            5. 总体评价和推荐
            
            确保比较公正客观，基于产品页面实际信息。
            """
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="compare_products",
                parameters={"product_urls": product_urls, "aspects": aspects},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message="产品比较完成",
                    platform=platform,
                    product_urls=product_urls,
                    aspects=aspects,
                    comparison=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"比较产品失败: {str(e)}")
            return cls.format_error_response(
                f"比较产品失败: {str(e)}",
                platform=platform,
                product_urls=product_urls
            )
    
    @classmethod
    async def analyze_sales(
        cls,
        platform: str,
        product_url: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        分析产品销售情况
        
        Args:
            platform: 电商平台名称
            product_url: 产品URL
            use_vision: 是否使用视觉能力
            
        Returns:
            包含销售分析的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""访问以下{platform}产品链接，分析销售情况:
            
            URL: {product_url}
            
            请提供:
            1. 产品基本信息 (名称、价格、品牌)
            2. 销量数据 (月销量或总销量)
            3. 销售趋势 (如有)
            4. 热门型号/规格/颜色 (如有)
            5. 库存状态
            6. 促销活动与折扣
            7. 买家地域分布 (如有)
            
            尽可能收集所有与销售相关的数据，如遇到数据不完整，请说明原因。
            """
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="analyze_sales",
                parameters={"product_url": product_url},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message="销售分析完成",
                    platform=platform,
                    product_url=product_url,
                    sales_analysis=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"分析销售情况失败: {str(e)}")
            return cls.format_error_response(
                f"分析销售情况失败: {str(e)}",
                platform=platform,
                product_url=product_url
            )
    
    @classmethod
    async def find_top_sellers(
        cls,
        platform: str,
        category: str,
        count: int = 10,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        查找类目热销产品
        
        Args:
            platform: 电商平台名称
            category: 产品类目
            count: 要返回的产品数量
            use_vision: 是否使用视觉能力
            
        Returns:
            包含热销产品的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""在{platform}平台查找{category}类目的热销产品，找出销量最高的{count}个:
            
            请提供:
            1. 产品名称
            2. 品牌
            3. 价格
            4. 销量/销售排名
            5. 评分
            6. 短链接
            7. 产品特点概述
            
            确保所选产品都是在{category}类目中销量领先的产品。
            """
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="find_top_sellers",
                parameters={"category": category, "count": count},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                return cls.format_success_response(
                    message=f"已找到{platform}平台{category}类目的热销产品",
                    platform=platform,
                    category=category,
                    count=count,
                    top_sellers=result["result"]
                )
            else:
                return result
        except Exception as e:
            logger.error(f"查找热销产品失败: {str(e)}")
            return cls.format_error_response(
                f"查找热销产品失败: {str(e)}",
                platform=platform,
                category=category
            )
    
    @classmethod
    async def extract_product_info(
        cls,
        platform: str,
        product_url: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        提取产品详细信息
        
        Args:
            platform: 电商平台名称
            product_url: 产品URL
            use_vision: 是否使用视觉能力
            
        Returns:
            包含产品信息的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        try:
            # 构建任务参数
            params = {
                "platform": platform,
                "product_url": product_url
            }
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="extract_product_info",
                parameters=params,
                use_vision=use_vision
            )
            
            # 记录执行结果
            logger.info(f"从{platform}提取产品信息: {result['status']}")
            
            # 添加平台和URL信息到结果
            if result["status"] == "success":
                result["platform"] = platform
                result["product_url"] = product_url
                
            return result
        except Exception as e:
            logger.error(f"提取产品信息失败: {str(e)}")
            return cls.format_error_response(
                f"提取产品信息失败: {str(e)}",
                platform=platform,
                product_url=product_url
            )
    
    @classmethod
    async def track_listing(
        cls,
        platform: str,
        product_url: str,
        check_interval: str = "daily",
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        跟踪产品刊登
        
        Args:
            platform: 电商平台名称
            product_url: 产品URL
            check_interval: 检查间隔 (hourly, daily, weekly)
            use_vision: 是否使用视觉能力
            
        Returns:
            包含跟踪设置的字典
        """
        # 验证平台
        error = cls.validate_platform(platform, TemplateManager.get_supported_ecommerce_platforms())
        if error:
            return error
            
        try:
            # 构建任务
            task = f"""访问并记录{platform}平台以下产品的当前状态:
            
            URL: {product_url}
            检查间隔: {check_interval}
            
            请提供:
            1. 产品基本信息 (标题, 品牌, SKU/ID)
            2. 当前价格和促销状态
            3. 库存状态
            4. 销量/评价数变化
            5. 产品描述和图片是否有更新
            6. 物流/配送信息
            
            这些信息将用于设置定期跟踪，请确保信息准确完整。
            """
            
            # 执行任务
            result = await cls.execute_ecommerce_task(
                platform=platform,
                task_type="track_listing",
                parameters={"product_url": product_url, "check_interval": check_interval},
                use_vision=use_vision
            )
            
            if result["status"] == "success":
                # 构造跟踪设置
                tracking_settings = {
                    "platform": platform,
                    "product_url": product_url,
                    "check_interval": check_interval,
                    "initial_data": result["result"],
                    "tracking_id": cls.generate_tracking_id(platform, product_url)
                }
                
                return cls.format_success_response(
                    message=f"产品跟踪已设置，间隔: {check_interval}",
                    tracking_settings=tracking_settings
                )
            else:
                return result
        except Exception as e:
            logger.error(f"设置产品跟踪失败: {str(e)}")
            return cls.format_error_response(
                f"设置产品跟踪失败: {str(e)}",
                platform=platform,
                product_url=product_url
            )
    
    @staticmethod
    def generate_tracking_id(platform: str, url: str) -> str:
        """生成跟踪ID"""
        # 使用平台、URL和时间戳生成唯一ID
        tracking_string = f"{platform}_{url}_{time.time()}"
        return hashlib.md5(tracking_string.encode()).hexdigest()[:10] 