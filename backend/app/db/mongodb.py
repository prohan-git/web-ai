from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from ..config import settings

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    
    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        try:
            await cls.client.admin.command('ping')
            print(f"✅ MongoDB连接成功！数据库：{settings.MONGODB_DB_NAME}")
        except Exception as e:
            print("❌ 连接失败:", e)
            raise e

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None

# 测试代码
if __name__ == "__main__":
    async def test():
        await MongoDB.connect_db()
        await MongoDB.close_db()
    
    import asyncio
    asyncio.run(test())
