from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    # 项目信息
    PROJECT_NAME: str = "Web AI API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Web AI 工具箱 API 提供电商和社交媒体分析工具"
    
    # API密钥
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_BASE: str = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # 浏览器设置
    BROWSER_HEADLESS: bool = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    
    # 数据库设置（未来可能会使用）
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

# 创建全局配置对象
settings = Settings() 