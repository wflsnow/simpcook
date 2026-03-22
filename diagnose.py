#!/usr/bin/env python3
"""诊断工具 - 检查应用启动问题"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def diagnose():
    """诊断问题"""
    print("=" * 60)
    print("开始诊断...")
    print("=" * 60)
    
    # 1. 检查配置
    print("\n1. 检查配置...")
    try:
        from app.core.config import settings
        print(f"   - QWEN_API_KEY: {settings.QWEN_API_KEY[:8]}... (长度: {len(settings.QWEN_API_KEY)})")
        print(f"   - QWEN_BASE_URL: {settings.QWEN_BASE_URL}")
        print("   - 配置检查通过")
    except Exception as e:
        print(f"   - 配置检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 2. 检查数据库连接
    print("\n2. 检查数据库连接...")
    try:
        from app.infrastructure.database import engine
        from sqlalchemy import text
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"   - 数据库连接成功: {result.scalar()}")
        print("   - 数据库连接检查通过")
    except Exception as e:
        print(f"   - 数据库连接检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. 检查依赖注入
    print("\n3. 检查依赖注入...")
    try:
        from app.infrastructure.database import get_db
        from app.infrastructure.qwen_provider import QwenProvider
        from app.services.recipe_service import RecipeService
        
        async for db in get_db():
            print(f"   - 获取数据库会话成功: {type(db).__name__}")
            try:
                ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
                service = RecipeService(ai_provider, db)
                print(f"   - 创建 RecipeService 成功: {type(service).__name__}")
                break
            except Exception as e:
                print(f"   - 创建 RecipeService 失败: {e}")
                import traceback
                traceback.print_exc()
                return False
    except Exception as e:
        print(f"   - 依赖注入检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. 检查 FastAPI 应用
    print("\n4. 检查 FastAPI 应用...")
    try:
        from app.main import app
        
        # 检查路由
        routes = [r.path for r in app.routes]
        print(f"   - 注册的路由: {routes}")
        
        # 检查特定端点
        if "/api/v1/recipes/popular/list" in routes:
            print("   - /popular/list 路由已注册")
        else:
            print("   - /popular/list 路由未找到")
        
        print("   - FastAPI 应用检查通过")
    except Exception as e:
        print(f"   - FastAPI 应用检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. 检查 get_recipe_service 依赖
    print("\n5. 检查 get_recipe_service 依赖...")
    try:
        from app.api.deps import get_recipe_service
        print(f"   - get_recipe_service 函数: {get_recipe_service}")
        print(f"   - get_recipe_service 类型: {type(get_recipe_service).__name__}")
        print("   - get_recipe_service 检查通过")
    except Exception as e:
        print(f"   - get_recipe_service 检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 6. 检查路由模块
    print("\n6. 检查路由模块...")
    try:
        from app.api.v1.recipes import router
        print(f"   - router类型: {type(router).__name__}")
        print(f"   - router.prefix: {router.prefix}")
        print("   - 路由模块检查通过")
    except Exception as e:
        print(f"   - 路由模块检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("诊断完成 - 所有检查通过!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(diagnose())
    sys.exit(0 if success else 1)