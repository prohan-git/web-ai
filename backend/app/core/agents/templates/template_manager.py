from typing import Dict, Any, List, Optional
import logging

# 配置日志记录
logger = logging.getLogger(__name__)

class TemplateCategory:
    """模板类别常量"""
    SOCIAL = "SOCIAL"
    ECOMMERCE = "ECOMMERCE"
    CONTENT_ANALYSIS = "CONTENT_ANALYSIS"
    ECOMMERCE_ANALYSIS = "ECOMMERCE_ANALYSIS"
    LISTING = "LISTING"

class TemplateManager:
    """
    模板管理器
    
    集中管理所有任务模板，包括通用模板、平台特定模板等。
    提供模板检索、渲染功能。
    """
    
    # 通用任务模板
    _general_templates: Dict[str, str] = {
        "网页搜索": """
        请在网络上搜索关于"{query}"的信息。
        
        要求：
        1. 使用搜索引擎进行搜索
        2. 访问至少{min_sources}个相关网页收集信息
        3. 提供关于"{query}"的全面信息总结
        4. 按以下方面组织信息：{aspects}
        5. 提供信息来源/引用
        
        请确保信息准确、全面且最新。
        """,
        
        "数据收集": """
        从网站"{website}"收集关于"{topic}"的数据。
        
        收集要点:
        1. {point1}
        2. {point2}
        3. {point3}
        
        请按结构化格式呈现结果，并注明数据来源页面。
        """,
        
        "网页摘要": """
        请访问网页"{url}"，并提供内容摘要。
        
        要求：
        1. 概述网页的主要内容和目的
        2. 提取关键信息点
        3. 总结主要观点和结论
        4. 评估信息的可靠性和时效性
        
        如遇登录墙或访问限制，请说明情况。
        """,
        
        "比较分析": """
        请比较以下网页/产品/实体：
        
        1. {item1} - {url1}
        2. {item2} - {url2}
        
        比较维度：
        {dimensions}
        
        请提供详细比较分析，指出相同点和不同点，并给出最终推荐。
        """,
        
        "趋势监控": """
        请监控"{topic}"领域的最新趋势和发展。
        
        要求：
        1. 寻找最近{time_period}内的最新消息和发展
        2. 关注关键变化和新兴趋势
        3. 分析趋势背后的驱动因素
        4. 预测可能的未来发展方向
        
        请从多个来源收集信息，确保全面性。
        """
    }
    
    # 社交媒体平台模板
    _social_platform_templates: Dict[str, Dict[str, str]] = {
        "小红书": {
            "搜索": """
            在小红书平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型
            2. 分析前{top_n}条笔记的共同特点
            3. 提取热门标签和关键词
            4. 分析用户互动情况（点赞、收藏、评论等）
            5. 总结内容创作趋势和用户关注点
            
            请提供详细分析和具体例子。
            """,
            
            "博主分析": """
            分析小红书博主"{blogger_name}"的账号。
            
            分析内容：
            1. 博主定位和风格特点
            2. 内容类型和主题分布
            3. 粉丝数量和特征
            4. 互动数据分析（平均点赞、收藏、评论数）
            5. 高性能内容特点分析
            6. 合作品牌和商业模式
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "内容监控": """
            监控小红书平台上关于"{topic}"的最新内容动态。
            
            监控重点：
            1. 最近{time_period}发布的相关内容
            2. 热门讨论和话题标签
            3. 用户情感倾向和评价
            4. 相关品牌/产品提及
            5. 内容传播和互动趋势
            
            请提供监控摘要和关键发现。
            """,
            
            "热门分析": """
            分析小红书平台"{category}"类目下的热门内容。
            
            分析要点：
            1. 热门排行榜内容特点
            2. 高互动内容的共同特征
            3. 流行的内容形式和表现手法
            4. 热门话题和讨论点
            5. 用户偏好和需求洞察
            
            请提供详细分析并突出关键趋势。
            """
        },
        
        "抖音": {
            "搜索": """
            在抖音平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型（视频、用户、挑战等）
            2. 分析前{top_n}个视频的共同特点
            3. 提取热门标签和话题
            4. 分析用户互动情况（点赞、评论、分享等）
            5. 总结内容创作趋势和算法推荐倾向
            
            请提供详细分析和具体例子。
            """,
            
            "达人分析": """
            分析抖音达人"{creator_name}"的账号。
            
            分析内容：
            1. 达人定位和风格特点
            2. 内容类型和主题分布
            3. 粉丝数量和特征
            4. 互动数据分析（平均点赞、评论、分享数）
            5. 高性能视频特点分析
            6. 商业合作和变现方式
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "内容监控": """
            监控抖音平台上关于"{topic}"的最新内容动态。
            
            监控重点：
            1. 最近{time_period}发布的相关视频
            2. 热门挑战和话题标签
            3. 用户情感倾向和评价
            4. 相关品牌/产品提及
            5. 内容传播和互动趋势
            
            请提供监控摘要和关键发现。
            """,
            
            "热门分析": """
            分析抖音平台"{category}"类目下的热门内容。
            
            分析要点：
            1. 热门榜单视频特点
            2. 高互动视频的共同特征
            3. 流行的视频形式和表现手法
            4. 热门音乐和特效使用
            5. 用户偏好和需求洞察
            
            请提供详细分析并突出关键趋势。
            """
        },
        
        "Instagram": {
            "搜索": """
            在Instagram平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型（帖子、用户、标签）
            2. 分析前{top_n}条帖子的共同特点
            3. 提取热门标签和相关话题
            4. 分析用户互动情况（点赞、评论等）
            5. 总结内容创作趋势和视觉风格
            
            请提供详细分析和具体例子。
            """,
            
            "博主分析": """
            分析Instagram博主"{account_name}"的账号。
            
            分析内容：
            1. 博主定位和风格特点
            2. 内容类型和主题分布
            3. 粉丝数量和增长趋势
            4. 互动数据分析（平均点赞、评论数）
            5. 高性能内容特点分析
            6. 合作品牌和商业模式
            7. 内容日历和发布频率
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "内容监控": """
            监控Instagram平台上关于"{topic}"的最新内容动态。
            
            监控重点：
            1. 最近{time_period}发布的相关内容
            2. 热门标签和话题趋势
            3. 用户情感倾向和评价
            4. 相关品牌/产品提及
            5. 内容传播和互动趋势
            6. 有影响力的创作者动态
            
            请提供监控摘要和关键发现。
            """,
            
            "热门分析": """
            分析Instagram平台"{category}"类目下的热门内容。
            
            分析要点：
            1. 探索页和热门内容特点
            2. 高互动内容的共同特征
            3. 流行的视觉风格和表现手法
            4. 热门滤镜和编辑技巧
            5. 叙事方式和内容结构
            6. 用户偏好和需求洞察
            
            请提供详细分析并突出关键趋势。
            """
        },
        
        "Facebook": {
            "搜索": """
            在Facebook平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型（帖子、页面、群组、活动等）
            2. 分析前{top_n}条结果的共同特点
            3. 提取相关话题和讨论组
            4. 分析用户互动情况（反应、评论、分享等）
            5. 总结内容传播情况和社区特点
            
            请提供详细分析和具体例子。
            """,
            
            "页面分析": """
            分析Facebook页面"{page_name}"的详细情况。
            
            分析内容：
            1. 页面定位和内容策略
            2. 粉丝数量和增长趋势
            3. 内容类型和发布频率
            4. 互动数据分析（不同类型内容的平均互动率）
            5. 高性能内容特点分析
            6. 社区管理和用户互动方式
            7. 广告活动和商业模式
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "内容监控": """
            监控Facebook平台上关于"{topic}"的最新内容动态。
            
            监控重点：
            1. 最近{time_period}发布的相关内容
            2. 热门讨论和话题标签
            3. 用户情感倾向和评价
            4. 相关品牌/产品提及
            5. 内容传播和互动趋势
            6. 相关群组和社区活动
            
            请提供监控摘要和关键发现。
            """,
            
            "群组分析": """
            分析Facebook群组"{group_name}"的情况。
            
            分析要点：
            1. 群组规模和活跃度
            2. 成员构成和特征
            3. 内容类型和讨论主题
            4. 互动模式和参与度
            5. 管理方式和规则执行
            6. 社区文化和氛围
            
            请提供详细分析并评估群组的健康度和价值。
            """
        },
        
        "Twitter": {
            "搜索": """
            在Twitter平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型（推文、账户、话题等）
            2. 分析前{top_n}条推文的共同特点
            3. 提取相关标签和讨论话题
            4. 分析用户互动情况（喜欢、回复、转发等）
            5. 总结舆论倾向和观点分布
            
            请提供详细分析和具体例子。
            """,
            
            "账号分析": """
            分析Twitter账号"{account_name}"的详细情况。
            
            分析内容：
            1. 账号定位和内容风格
            2. 粉丝数量和类型
            3. 内容主题和发布频率
            4. 互动数据分析（平均喜欢、回复、转发数）
            5. 高性能推文特点分析
            6. 网络影响力和互动对象
            7. 内容策略和传播特征
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "话题监控": """
            监控Twitter平台上关于"{topic}"的最新讨论动态。
            
            监控重点：
            1. 最近{time_period}发布的相关推文
            2. 热门标签和关联话题
            3. 用户情感倾向和评价
            4. 有影响力的发言者和观点领袖
            5. 内容传播和演变趋势
            6. 争议点和讨论焦点
            
            请提供监控摘要和关键发现。
            """,
            
            "趋势分析": """
            分析Twitter平台当前或特定地区"{location}"的热门趋势。
            
            分析要点：
            1. 热门话题和标签列表
            2. 各趋势的起因和背景
            3. 讨论内容和主要观点
            4. 参与用户特征分析
            5. 传播路径和影响力
            6. 趋势持续时间和演变
            
            请提供详细分析并评估趋势的社会影响和商业价值。
            """
        },
        
        "YouTube": {
            "搜索": """
            在YouTube平台搜索"{keyword}"，并分析搜索结果。
            
            要求：
            1. 记录搜索结果数量和类型（视频、频道、播放列表）
            2. 分析前{top_n}个视频的共同特点
            3. 提取相关关键词和标签
            4. 分析用户互动情况（观看量、点赞、评论等）
            5. 总结内容创作趋势和算法推荐倾向
            
            请提供详细分析和具体例子。
            """,
            
            "频道分析": """
            分析YouTube频道"{channel_name}"的详细情况。
            
            分析内容：
            1. 频道定位和内容策略
            2. 订阅者数量和增长趋势
            3. 内容类型和更新频率
            4. 互动数据分析（平均观看量、点赞率、评论数）
            5. 高性能视频特点分析
            6. 商业模式和变现方式
            7. 频道发展历程和里程碑
            
            请提供详细分析报告，包含数据支持和案例说明。
            """,
            
            "视频分析": """
            分析YouTube视频"{video_url}"的详细情况。
            
            分析内容：
            1. 视频基本信息（标题、时长、发布时间等）
            2. 观看数据和互动情况
            3. 内容结构和叙事方式
            4. 受众参与度和评论主题
            5. SEO策略和元数据优化
            6. 相关推荐和算法表现
            7. 商业元素（如赞助、广告等）
            
            请提供详细分析报告，评估视频效果和优化空间。
            """,
            
            "趋势监控": """
            监控YouTube平台上关于"{topic}"的最新内容趋势。
            
            监控重点：
            1. 最近{time_period}发布的相关视频
            2. 热门视频和突发内容
            3. 用户情感倾向和评价
            4. 内容创新点和表现形式
            5. 相关创作者动态和合作
            6. 观众反应和互动模式
            
            请提供监控摘要和关键发现。
            """
        }
    }
    
    # 电商平台模板
    _ecommerce_platform_templates: Dict[str, Dict[str, str]] = {
        "淘宝": {
            "搜索": """
            在淘宝平台搜索"{query}"，分析搜索结果。
            
            搜索参数：
            - 排序方式: {sort_text}
            {filter_text}
            - 最大结果数: {max_results}
            
            分析要点：
            1. 产品价格区间和分布
            2. 主流品牌和店铺
            3. 产品特点和卖点
            4. 销量和评价情况
            5. 促销活动和营销策略
            
            请提供详细分析并列出符合条件的{max_results}个产品信息。
            """,
            
            "产品分析": """
            分析淘宝产品"{product_url}"的详细信息。
            
            分析内容：
            1. 产品基本信息（名称、价格、品牌、店铺）
            2. 产品描述和卖点
            3. 规格和型号
            4. 销量和评价分析
            5. 促销信息和优惠活动
            6. 物流和服务承诺
            7. 相似产品和竞品推荐
            
            请提供全面分析并评估产品的市场定位和竞争力。
            """,
            
            "店铺分析": """
            分析淘宝店铺"{shop_url}"的详细信息。
            
            分析内容：
            1. 店铺基本信息（名称、类型、评分）
            2. 主营产品和类目
            3. 产品价格区间和定位
            4. 销量和人气商品
            5. 评价和服务水平
            6. 营销活动和促销策略
            7. 店铺特色和竞争优势
            
            请提供全面分析并评估店铺的市场地位和经营状况。
            """
        },
        
        "京东": {
            "搜索": """
            在京东平台搜索"{query}"，分析搜索结果。
            
            搜索参数：
            - 排序方式: {sort_text}
            {filter_text}
            - 最大结果数: {max_results}
            
            分析要点：
            1. 产品价格区间和分布
            2. 主流品牌和自营/POP店铺比例
            3. 产品特点和卖点
            4. 销量和评价情况
            5. 促销活动和营销策略
            
            请提供详细分析并列出符合条件的{max_results}个产品信息。
            """,
            
            "产品分析": """
            分析京东产品"{product_url}"的详细信息。
            
            分析内容：
            1. 产品基本信息（名称、价格、品牌、店铺）
            2. 产品描述和卖点
            3. 规格和型号
            4. 销量和评价分析
            5. 促销信息和优惠活动
            6. 物流和售后服务
            7. 相似产品和竞品推荐
            
            请提供全面分析并评估产品的市场定位和竞争力。
            """,
            
            "店铺分析": """
            分析京东店铺"{shop_url}"的详细信息。
            
            分析内容：
            1. 店铺基本信息（名称、类型、是否自营）
            2. 主营产品和类目
            3. 产品价格区间和定位
            4. 销量和人气商品
            5. 评价和服务水平
            6. 营销活动和促销策略
            7. 店铺特色和竞争优势
            
            请提供全面分析并评估店铺的市场地位和经营状况。
            """
        },
        
        "亚马逊": {
            "搜索": """
            在亚马逊平台搜索"{query}"，分析搜索结果。
            
            搜索参数：
            - 排序方式: {sort_text}
            {filter_text}
            - 最大结果数: {max_results}
            
            分析要点：
            1. 产品价格区间和分布
            2. 主流品牌和卖家类型
            3. Amazon's Choice和畅销产品特点
            4. 评分和评价情况
            5. 促销活动和Prime标记
            6. 配送选项和时间
            
            请提供详细分析并列出符合条件的{max_results}个产品信息。
            """,
            
            "产品分析": """
            分析亚马逊产品"{product_url}"的详细信息。
            
            分析内容：
            1. 产品基本信息（名称、ASIN、价格、品牌）
            2. 产品描述和亮点功能
            3. 规格和型号选择
            4. 销售排名和类目表现
            5. 评价数量、评分分布和主要反馈
            6. A+内容和品牌店铺情况
            7. 购买选项和卖家比较
            8. 相关产品和"经常一起购买"推荐
            
            请提供全面分析并评估产品的市场定位和竞争力。
            """,
            
            "卖家分析": """
            分析亚马逊卖家"{seller_name}"的详细信息。
            
            分析内容：
            1. 卖家基本信息（名称、评分、卖家类型）
            2. 主营产品和类目
            3. 产品价格区间和定位
            4. 评价和服务水平
            5. 物流和配送表现
            6. 库存和上新情况
            7. 卖家特色和竞争优势
            
            请提供全面分析并评估卖家的市场地位和经营状况。
            """,
            
            "评价分析": """
            分析亚马逊产品"{product_url}"的买家评价。
            
            分析内容：
            1. 评价总量和评分分布
            2. 评价时间分布和趋势
            3. 正面评价的主要内容和关键词
            4. 负面评价的主要问题和痛点
            5. 评价中提到的产品优势和缺点
            6. 买家关注点和购买决策因素
            7. 卖家回复情况和客户服务
            
            请提供全面分析并总结产品表现和改进机会。
            """
        },
        
        "天猫": {
            "搜索": """
            在天猫平台搜索"{query}"，分析搜索结果。
            
            搜索参数：
            - 排序方式: {sort_text}
            {filter_text}
            - 最大结果数: {max_results}
            
            分析要点：
            1. 产品价格区间和分布
            2. 主流品牌和旗舰店比例
            3. 产品特点和卖点
            4. 销量和评价情况
            5. 促销活动和营销策略
            6. 直播和短视频带货情况
            
            请提供详细分析并列出符合条件的{max_results}个产品信息。
            """,
            
            "产品分析": """
            分析天猫产品"{product_url}"的详细信息。
            
            分析内容：
            1. 产品基本信息（名称、价格、品牌、店铺）
            2. 产品描述和卖点
            3. 规格和型号
            4. 销量和评价分析
            5. 促销信息和优惠活动
            6. 详情页设计和内容质量
            7. 服务承诺和物流选项
            8. 相似产品和竞品推荐
            
            请提供全面分析并评估产品的市场定位和竞争力。
            """,
            
            "店铺分析": """
            分析天猫店铺"{shop_url}"的详细信息。
            
            分析内容：
            1. 店铺基本信息（名称、类型、品牌、评分）
            2. 主营产品和类目
            3. 产品价格区间和定位
            4. 销量和人气商品
            5. 评价和服务水平
            6. 营销活动和促销策略
            7. 店铺装修和视觉设计
            8. 会员体系和粉丝运营
            
            请提供全面分析并评估店铺的市场地位和经营状况。
            """,
            
            "直播分析": """
            分析天猫店铺"{shop_url}"的直播销售情况。
            
            分析内容：
            1. 直播频率和时间安排
            2. 主播风格和表现特点
            3. 直播间装修和布局
            4. 产品展示和讲解方式
            5. 互动策略和用户参与度
            6. 转化技巧和成交模式
            7. 优惠力度和专属福利
            8. 与竞品直播的对比
            
            请提供全面分析并评估直播带货效果和优化空间。
            """
        }
    }
    
    # 内容分析模板
    _content_analysis_templates: Dict[str, str] = {
        "情感分析": """
        对以下内容进行情感分析：
        
        内容：
        {content}
        
        分析要点：
        1. 整体情感倾向（积极/消极/中性）
        2. 情感强度评分（1-10分）
        3. 关键情感词和表达
        4. 积极和消极观点摘录
        5. 情感变化和转折点
        6. 潜在的用户需求和关注点
        
        请提供详细的情感分析报告，支持判断的依据和具体例证。
        """,
        
        "主题提取": """
        从以下内容中提取主要主题和话题：
        
        内容：
        {content}
        
        分析要点：
        1. 核心主题和子主题
        2. 关键词和术语
        3. 主题间的关联性
        4. 主题重要性排序
        5. 隐含主题和潜在关注点
        6. 上下文和背景信息
        
        请提供详细的主题分析报告，包括主题结构图和关键点摘要。
        """,
        
        "趋势分析": """
        分析以下内容中的趋势和变化：
        
        内容：
        {content}
        
        分析要点：
        1. 主要趋势和发展方向
        2. 上升和下降趋势
        3. 变化点和转折因素
        4. 季节性和周期性模式
        5. 未来趋势预测
        6. 影响因素分析
        
        请提供详细的趋势分析报告，包括数据支持和图表描述。
        """,
        
        "竞品分析": """
        分析以下内容中的竞品信息：
        
        内容：
        {content}
        
        分析要点：
        1. 主要竞争对手识别
        2. 各竞品的优势和特点
        3. 市场定位和差异化策略
        4. 用户评价和口碑分析
        5. 产品功能和性能对比
        6. 价格策略和促销活动
        
        请提供详细的竞品分析报告，包括比较表格和竞争格局分析。
        """
    }
    
    # 电商分析模板
    _ecommerce_analysis_templates: Dict[str, str] = {
        "市场规模": """
        分析{category}类目的市场规模和发展趋势。
        
        分析要点：
        1. 市场总体规模和增长率
        2. 细分市场结构和占比
        3. 市场发展阶段评估
        4. 近期市场变化和波动
        5. 未来增长预测和潜力
        6. 影响市场的关键因素
        
        请提供详细的市场规模分析，包括数据来源和分析方法。
        """,
        
        "价格分析": """
        分析{category}类目的价格分布和策略。
        
        分析要点：
        1. 价格区间和分布
        2. 不同价格段的产品特点
        3. 价格与销量的关系
        4. 价格变动趋势和季节性
        5. 促销折扣和价格策略
        6. 价格敏感度和心理价位
        
        请提供详细的价格分析报告，包括价格分布图和关键发现。
        """,
        
        "销量分析": """
        分析{category}类目的销量情况和影响因素。
        
        分析要点：
        1. 总体销量和转化率
        2. 销量分布和排名情况
        3. 销量与价格/评价的关系
        4. 销售高峰期和淡季
        5. 促销活动对销量的影响
        6. 畅销产品的共同特点
        
        请提供详细的销量分析报告，包括数据图表和关键洞察。
        """,
        
        "消费者分析": """
        分析{category}类目的消费者特征和行为。
        
        分析要点：
        1. 消费者人口统计特征
        2. 购买动机和决策因素
        3. 消费者偏好和需求变化
        4. 复购率和忠诚度
        5. 购买路径和触点分析
        6. 消费者评价和反馈分析
        
        请提供详细的消费者分析报告，包括用户画像和行为模式。
        """
    }
    
    # 刊登模板
    _listing_templates: Dict[str, str] = {
        "标题优化": """
        为{platform}平台的{category}类目产品优化标题。
        
        原标题：{original_title}
        
        优化要点：
        1. 关键词布局和排序
        2. 符合平台标题规则和限制
        3. 提升点击率和转化率
        4. 包含核心卖点和差异点
        5. 改善搜索排名和展现
        
        请提供5个优化后的标题方案，并解释优化思路和预期效果。
        """,
        
        "详情页分析": """
        分析{platform}平台"{product_url}"的产品详情页。
        
        分析要点：
        1. 整体结构和布局评估
        2. 图片质量和展示效果
        3. 文案描述和卖点呈现
        4. 规格选项和购买引导
        5. 营销元素和促销信息
        6. 信任建立和疑虑消除
        
        请提供详细的分析报告和改进建议。
        """,
        
        "竞品监控": """
        监控{platform}平台上"{keyword}"的竞争产品。
        
        监控要点：
        1. 主要竞争对手和产品
        2. 价格变动和促销活动
        3. 排名变化和展现位置
        4. 销量和评价趋势
        5. 产品更新和优化情况
        6. 新进入者和市场变化
        
        请提供详细的竞品监控报告和竞争态势分析。
        """,
        
        "评价分析": """
        分析{platform}平台"{product_url}"的买家评价。
        
        分析要点：
        1. 总体评分和评价分布
        2. 正面评价和卖点确认
        3. 负面评价和问题识别
        4. 用户反馈中的改进机会
        5. 评价中的购买决策因素
        6. 与竞品评价的对比
        
        请提供详细的评价分析报告和产品优化建议。
        """
    }
    
    @classmethod
    def get_general_template(cls, template_name: str) -> Optional[str]:
        """获取通用模板"""
        return cls._general_templates.get(template_name)
    
    @classmethod
    def get_general_template_names(cls) -> List[str]:
        """获取所有通用模板名称"""
        return list(cls._general_templates.keys())
    
    @classmethod
    def get_social_platform_template(cls, platform: str, task_type: str) -> Optional[str]:
        """获取社交平台特定模板"""
        platform_templates = cls._social_platform_templates.get(platform)
        if platform_templates:
            return platform_templates.get(task_type)
        return None
    
    @classmethod
    def get_ecommerce_platform_template(cls, platform: str, task_type: str) -> Optional[str]:
        """获取电商平台特定模板"""
        platform_templates = cls._ecommerce_platform_templates.get(platform)
        if platform_templates:
            return platform_templates.get(task_type)
        return None
    
    @classmethod
    def get_content_analysis_template(cls, task_type: str) -> Optional[str]:
        """获取内容分析模板"""
        return cls._content_analysis_templates.get(task_type)
    
    @classmethod
    def get_ecommerce_analysis_template(cls, task_type: str) -> Optional[str]:
        """获取电商分析模板"""
        return cls._ecommerce_analysis_templates.get(task_type)
    
    @classmethod
    def get_listing_template(cls, task_type: str) -> Optional[str]:
        """获取刊登模板"""
        return cls._listing_templates.get(task_type)
    
    @classmethod
    def render_template(cls, template: str, parameters: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template: 模板字符串
            parameters: 模板参数
            
        Returns:
            渲染后的文本
        """
        try:
            return template.format(**parameters)
        except KeyError as e:
            logger.error(f"模板参数错误: 缺少参数 {e}")
            raise KeyError(f"模板参数错误: 缺少参数 {e}")
        except Exception as e:
            logger.error(f"模板渲染错误: {str(e)}")
            raise ValueError(f"模板渲染错误: {str(e)}")
    
    @classmethod
    def get_supported_social_platforms(cls) -> List[str]:
        """获取支持的社交平台列表"""
        return list(cls._social_platform_templates.keys())
    
    @classmethod
    def get_supported_ecommerce_platforms(cls) -> List[str]:
        """获取支持的电商平台列表"""
        return list(cls._ecommerce_platform_templates.keys())
    
    @classmethod
    def get_platform_task_types(cls, category: str, platform: str) -> List[str]:
        """
        获取平台支持的任务类型
        
        Args:
            category: 任务类别
            platform: 平台名称
            
        Returns:
            任务类型列表
        """
        if category == TemplateCategory.SOCIAL:
            platform_templates = cls._social_platform_templates.get(platform, {})
            return list(platform_templates.keys())
        elif category == TemplateCategory.ECOMMERCE:
            platform_templates = cls._ecommerce_platform_templates.get(platform, {})
            return list(platform_templates.keys())
        return [] 