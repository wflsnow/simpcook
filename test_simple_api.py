#!/usr/bin/env python3
"""
测试简单的API
"""

import uvicorn
from fastapi import FastAPI
from app.api.v1.recipes import router as recipe_router

app = FastAPI(title="Test API")
app.include_router(recipe_router, prefix="/api/v1/recipes", tags=["Recipes"])

if __name__ == "__main__":
    uvicorn.run("test_simple_api:app", host="127.0.0.1", port=8001, reload=False)