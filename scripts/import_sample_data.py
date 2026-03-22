#!/usr/bin/env python3
"""
导入示例菜谱数据到数据库
"""

import asyncio
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories import RecipeRepository
from app.domain.schemas import RecipeResponse


async def import_sample_data():
    """导入示例数据"""
    # 读取示例数据
    sample_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_recipes.json")
    
    if not os.path.exists(sample_file):
        print(f"❌ 示例数据文件不存在: {sample_file}")
        return False
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_recipes = json.load(f)
    except Exception as e:
        print(f"❌ 读取示例数据失败: {e}")
        return False
    
    print(f"📋 找到 {len(sample_recipes)} 个示例菜谱")
    
    async with AsyncSessionLocal() as session:
        recipe_repo = RecipeRepository(session)
        imported_count = 0
        
        for i, recipe_data in enumerate(sample_recipes, 1):
            try:
                # 验证数据格式
                recipe_response = RecipeResponse(**recipe_data)
                
                # 导入到数据库
                recipe = await recipe_repo.create_recipe(recipe_response)
                
                print(f"✅ [{i}/{len(sample_recipes)}] 导入成功: {recipe.title}")
                imported_count += 1
                
            except Exception as e:
                print(f"❌ [{i}/{len(sample_recipes)}] 导入失败: {recipe_data.get('title', '未知')} - {e}")
        
        await session.commit()
        
    print(f"\n🎉 导入完成: 成功 {imported_count}/{len(sample_recipes)}")
    return imported_count > 0


async def check_existing_data():
    """检查数据库中是否已有数据"""
    async with AsyncSessionLocal() as session:
        recipe_repo = RecipeRepository(session)
        count = await recipe_repo.get_total_recipes_count()
        
        if count > 0:
            print(f"📊 数据库中已有 {count} 个菜谱")
            return True
        else:
            print("📊 数据库中没有菜谱数据")
            return False


async def main():
    """主函数"""
    print("=" * 60)
    print("简烹示例数据导入工具")
    print("=" * 60)
    
    # 检查现有数据
    has_data = await check_existing_data()
    
    if has_data:
        print("\n⚠️  数据库中已有数据，是否继续导入？")
        print("输入 'yes' 继续，其他任意键取消: ", end="")
        choice = input().strip().lower()
        
        if choice != 'yes':
            print("❌ 用户取消导入")
            return 1
    
    print("\n🚀 开始导入示例数据...")
    
    success = await import_sample_data()
    
    if success:
        print("\n✅ 示例数据导入成功！")
        print("现在可以启动服务并访问以下功能：")
        print("1. 热门菜谱: GET /api/v1/recipes/popular/list")
        print("2. 搜索菜谱: GET /api/v1/recipes/search?keyword=西红柿")
        print("3. 查看API文档: http://127.0.0.1:8000/docs")
        return 0
    else:
        print("\n❌ 示例数据导入失败")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)