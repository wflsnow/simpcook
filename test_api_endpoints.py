#!/usr/bin/env python3
"""
测试API端点是否正确定义
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.api.v1.recipes import router as recipe_router

# 创建测试应用
app = FastAPI(title="Test App")
app.include_router(recipe_router, prefix="/api/v1/recipes", tags=["Recipes"])

# 打印所有路由
print("已注册的路由:")
for route in app.routes:
    if hasattr(route, "path"):
        print(f"  {route.path} - {route.methods}")

print(f"\n总路由数: {len([r for r in app.routes if hasattr(r, 'path')])}")

# 检查特定端点
required_endpoints = [
    "/api/v1/recipes/simplify",
    "/api/v1/recipes/search",
    "/api/v1/recipes/popular/list",
    "/api/v1/recipes/categories/list",
    "/api/v1/recipes/home/data",
]

print("\n检查必需端点:")
all_paths = [route.path for route in app.routes if hasattr(route, "path")]
for endpoint in required_endpoints:
    if endpoint in all_paths:
        print(f"  ✅ {endpoint}")
    else:
        print(f"  ❌ {endpoint} (缺失)")