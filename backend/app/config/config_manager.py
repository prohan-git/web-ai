from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict, Any, Optional, List

class Settings(BaseSettings):
    """应用配置类，使用环境变量和.env文件加载配置"""
    # API配置
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Web AI API"
    PROJECT_DESCRIPTION: str = "Web AI 工具箱 API 提供电商和社交媒体分析工具"
    VERSION: str = "0.1.0"
    
    # AI模型配置
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com"
    DEEPSEEK_API_KEY: str = "your-api-key"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./ai_service.db"
    
    # 任务执行配置
    DEFAULT_TIMEOUT: int = 60
    DEFAULT_RETRIES: int = 3
    MAX_CONCURRENT_TASKS: int = 10
    
    # 浏览器配置
    BROWSER_HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30
    
    # 安全配置
    CORS_ORIGINS: List[str] = ["*"]
    API_KEY_HEADER: str = "X-API-Key"
    SECRET_KEY: str = "your-secret-key"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置，使用LRU缓存避免重复加载"""
    return Settings()


class ConfigManager:
    """配置管理类，提供统一的配置访问接口"""
    
    @staticmethod
    def get_settings() -> Settings:
        """获取应用配置"""
        return get_settings()
    
    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """获取LLM相关配置"""
        settings = get_settings()
        return {
            "base_url": settings.DEEPSEEK_API_BASE,
            "model": settings.DEEPSEEK_MODEL,
            "api_key": settings.DEEPSEEK_API_KEY
        }
    
    @staticmethod
    def get_db_config() -> Dict[str, Any]:
        """获取数据库相关配置"""
        settings = get_settings()
        return {
            "database_url": settings.DATABASE_URL
        }
    
    @staticmethod
    def get_browser_config() -> Dict[str, Any]:
        """获取浏览器相关配置"""
        settings = get_settings()
        return {
            "headless": settings.BROWSER_HEADLESS,
            "timeout": settings.BROWSER_TIMEOUT
        }
    
    @staticmethod
    def get_api_config() -> Dict[str, Any]:
        """获取API相关配置"""
        settings = get_settings()
        return {
            "api_v1_str": settings.API_V1_STR,
            "project_name": settings.PROJECT_NAME,
            "project_description": settings.PROJECT_DESCRIPTION,
            "version": settings.VERSION,
            "cors_origins": settings.CORS_ORIGINS
        }
    
    @staticmethod
    def get_security_config() -> Dict[str, Any]:
        """获取安全相关配置"""
        settings = get_settings()
        return {
            "api_key_header": settings.API_KEY_HEADER,
            "secret_key": settings.SECRET_KEY
        }
    
    @staticmethod
    def get_task_config() -> Dict[str, Any]:
        """获取任务执行相关配置"""
        settings = get_settings()
        return {
            "default_timeout": settings.DEFAULT_TIMEOUT,
            "default_retries": settings.DEFAULT_RETRIES,
            "max_concurrent_tasks": settings.MAX_CONCURRENT_TASKS
        } 