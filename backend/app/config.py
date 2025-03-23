from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """
    应用配置类，使用 pydantic_settings 管理配置
    支持:
    1. 从环境变量自动加载配置
    2. 从 .env 文件自动加载配置
    3. 类型检查和验证
    4. 不同环境（开发、测试、生产）的配置切换
    """
    # 基础配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Web AI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI Web Application with FastAPI"
    
    # MongoDB配置
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "web_ai_db"
    
    # AI服务配置
    DEEPSEEK_API_KEY: Optional[str] = 'sk-hmeewkkyvnvbkztqnenmtknhaksppqjpbpylrtwtqwogwssp'
    DEEPSEEK_API_BASE: str = "https://api.siliconflow.cn/v1"
    DEEPSEEK_MODEL: str = "deepseek-ai/DeepSeek-V3"
    
    # 爬虫配置
    CRAWLER_TIMEOUT: int = 30
    CRAWLER_RETRY: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    """
    获取配置单例
    使用 lru_cache 确保只创建一次配置实例
    """
    return Settings()

# 配置实例
settings = get_settings()