#!/usr/bin/env python3
"""
测试真实API
"""

import uvicorn
from fastapi import FastAPI
from app.api.v1.recipes import router as recipe_router

app = FastAPI(title="Real API Test")
app.include_router(recipe_router, prefix="/api/v1/recipes", tags=["Recipes"])

if __name__ == "__main__":
    uvicorn.run("test_real_api:app", host="127.0.0.1", port=8003, reload=False)