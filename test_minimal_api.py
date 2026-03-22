#!/usr/bin/env python3
"""
最小化API测试
"""

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.infrastructure.repositories import RecipeRepository

app = FastAPI(title="Minimal Test API")

@app.get("/test")
async def test_endpoint(db: AsyncSession = Depends(get_db)):
    """测试端点"""
    try:
        repo = RecipeRepository(db)
        count = await repo.get_total_recipes_count()
        return {"status": "success", "recipe_count": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("test_minimal_api:app", host="127.0.0.1", port=8002, reload=False)