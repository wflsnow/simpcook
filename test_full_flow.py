#!/usr/bin/env python3
"""
测试完整流程
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.qwen_provider import QwenProvider
from app.services.recipe_service import RecipeService
from app.core.config import settings

async def test_recipe_service():
    """测试RecipeService"""
    try:
        # 创建数据库会话
        async with AsyncSessionLocal() as db:
            # 创建AI提供者
            ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
            
            # 创建RecipeService
            service = RecipeService(ai_provider, db)
            
            # 测试获取菜谱总数
            count = await service.get_total_recipes_count()
            print(f"✅ 获取菜谱总数成功: {count}")
            
            # 测试获取热门菜谱
            popular = await service.get_popular_recipes(3)
            print(f"✅ 获取热门菜谱成功: {len(popular)} 个")
            
            for recipe in popular:
                print(f"  - {recipe['title']}")
            
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔧 测试完整流程...")
    success = await test_recipe_service()
    
    if success:
        print("\n🎉 完整流程测试通过！")
        return 0
    else:
        print("\n❌ 完整流程测试失败")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)