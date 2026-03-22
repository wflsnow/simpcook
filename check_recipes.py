#!/usr/bin/env python3
"""
检查recipes表中的数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories import RecipeRepository


async def check_recipes():
    """检查recipes表数据"""
    async with AsyncSessionLocal() as session:
        recipe_repo = RecipeRepository(session)
        
        # 获取总记录数
        count = await recipe_repo.get_total_recipes_count()
        print(f"📊 recipes表中共有 {count} 条记录")
        
        # 获取前5条记录
        if count > 0:
            recipes = await recipe_repo.get_popular_recipes(limit=5)
            print("\n📋 前5条记录:")
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}. {recipe.title} - {recipe.category}")
                print(f"   食材数量: {len(recipe.ingredients)}")
                print(f"   步骤数量: {len(recipe.steps)}")
                print()


async def main():
    """主函数"""
    print("=" * 60)
    print("检查recipes表数据")
    print("=" * 60)
    
    try:
        await check_recipes()
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)