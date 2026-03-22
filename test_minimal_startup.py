#!/usr/bin/env python3
"""最小化启动测试"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.qwen_provider import QwenProvider
from app.services.recipe_service import RecipeService
from app.core.config import settings

app = FastAPI(title="Minimal Test")


# 定义依赖
def get_recipe_service(db: AsyncSession = Depends(get_db)) -> RecipeService:
    print(f"Creating RecipeService with QwenAPI key: {settings.QWEN_API_KEY[:8]}...")
    ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
    return RecipeService(ai_provider, db)


@app.get("/test")
async def test_endpoint(service: RecipeService = Depends(get_recipe_service)):
    # 测试服务是否正常工作
    try:
        result = await service.get_popular_recipes(3)
        return {"status": "ok", "recipes": result}
    except Exception as e:
        return {"status": "error", "error": str(e), "error_type": type(e).__name__}


if __name__ == "__main__":
    import uvicorn
    print("Starting minimal test server...")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)