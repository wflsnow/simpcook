#!/usr/bin/env python3
"""测试 RecipeService 初始化"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.infrastructure.qwen_provider import QwenProvider
from app.services.recipe_service import RecipeService
from app.core.config import settings


async def test_service_creation():
    """测试服务创建"""
    print("Testing RecipeService creation...")
    
    try:
        # 创建 AI provider
        print(f"Creating QwenProvider with API key: {settings.QWEN_API_KEY[:8]}...")
        ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
        print("QwenProvider created successfully")
        
        # 创建服务
        async for db in get_db():
            print(f"Got database session: {db}")
            try:
                service = RecipeService(ai_provider, db)
                print("RecipeService created successfully")
                
                # 测试一个简单的方法
                result = await service.get_popular_recipes(3)
                print(f"get_popular_recipes returned: {len(result)} recipes")
                break
            except Exception as e:
                print(f"Error in service creation or method call: {e}")
                import traceback
                traceback.print_exc()
                break
    except Exception as e:
        print(f"Error creating service: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_service_creation())