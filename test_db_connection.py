#!/usr/bin/env python3
"""
测试数据库连接
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories import RecipeRepository

async def test_db():
    """测试数据库连接和查询"""
    try:
        async with AsyncSessionLocal() as session:
            recipe_repo = RecipeRepository(session)
            
            # 测试查询
            count = await recipe_repo.get_total_recipes_count()
            print(f"✅ 数据库连接成功，菜谱总数: {count}")
            
            # 测试获取热门菜谱
            popular = await recipe_repo.get_popular_recipes(3)
            print(f"✅ 获取热门菜谱成功，数量: {len(popular)}")
            
            for recipe in popular:
                print(f"  - {recipe.title} (ID: {recipe.id})")
            
            return True
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🔧 测试数据库连接...")
    success = await test_db()
    
    if success:
        print("\n🎉 数据库测试通过！")
        return 0
    else:
        print("\n❌ 数据库测试失败")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)