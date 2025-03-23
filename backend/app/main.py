from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
# 导入原有的路由模块
from .api.routes import ai
# 配置详细日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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

app = FastAPI(
    title="Web AI API",
    description="Web AI 工具箱 API 提供电商和社交媒体分析工具",
    version="0.1.0",
    lifespan=lifespan
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(ai.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)