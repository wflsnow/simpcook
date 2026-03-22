import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 使用SQLite数据库
# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # 设置为True可以查看SQL语句，生产环境设为False
    future=True
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    """
    获取数据库会话的依赖函数
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    初始化数据库，创建所有表
    """
    from app.domain.models import Base
    
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully")


async def close_db():
    """
    关闭数据库连接
    """
    await engine.dispose()
