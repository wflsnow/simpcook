#!/usr/bin/env python3
"""测试服务器启动"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.database import get_db, engine
from sqlalchemy import text


async def test_db_connection():
    """测试数据库连接"""
    print("Testing database connection...")
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Database connection successful: {result.scalar()}")
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
    
    return True


async def test_get_db_dependency():
    """测试 get_db 依赖"""
    print("\nTesting get_db dependency...")
    try:
        async for session in get_db():
            print(f"Got database session: {session}")
            # Test a simple query
            from sqlalchemy import text
            result = await session.execute(text("SELECT 1"))
            print(f"Query result: {result.scalar()}")
            break
        print("get_db dependency works!")
        return True
    except Exception as e:
        print(f"get_db dependency failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("=" * 50)
    print("Testing server startup...")
    print("=" * 50)
    
    result1 = await test_db_connection()
    result2 = await test_get_db_dependency()
    
    print("\n" + "=" * 50)
    if result1 and result2:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())