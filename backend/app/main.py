from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from contextlib import asynccontextmanager
from typing import Callable

# 导入路由模块
from .api.routes import ai, chain
from .models.api_models import StatusEnum
from .config.config_manager import ConfigManager

# 获取配置
config = ConfigManager.get_settings()

# 配置详细日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
)

# 创建一个专用的API请求日志记录器
api_logger = logging.getLogger("api")
api_logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    logging.info("应用程序启动中...")
    yield
    # 关闭事件
    logging.info("应用程序关闭中...")


def create_app() -> FastAPI:
    """创建并配置FastAPI应用实例"""
    # 获取API配置
    api_config = ConfigManager.get_api_config()
    
    # 创建FastAPI实例
    app = FastAPI(
        title=api_config["project_name"],
        description=api_config["project_description"],
        version=api_config["version"],
        lifespan=lifespan
    )
    
    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config["cors_origins"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 添加全局异常处理中间件
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        处理请求验证错误，返回标准格式的错误响应
        """
        errors = exc.errors()
        error_messages = []
        
        for error in errors:
            error_messages.append({
                "field": ".".join([str(loc) for loc in error["loc"]]),
                "message": error["msg"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": StatusEnum.ERROR,
                "message": "请求验证失败",
                "errors": error_messages
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        处理所有未捕获的异常，返回标准格式的错误响应
        """
        # 记录异常详情
        logging.error(f"未捕获的异常: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": StatusEnum.ERROR,
                "message": "服务器内部错误",
                "detail": str(exc)
            }
        )
    
    # 注册路由
    app.include_router(ai.router, prefix=api_config["api_v1_str"])
    app.include_router(chain.router, prefix=api_config["api_v1_str"])
    
    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)