#!/usr/bin/env python3
"""
从项目根目录运行应用
"""

import uvicorn
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.api.v1.recipes import router as recipe_router

app = FastAPI(title="SimpCook 简烹")
app.include_router(recipe_router, prefix="/api/v1/recipes", tags=["Recipes"])

if __name__ == "__main__":
    uvicorn.run("run_app:app", host="127.0.0.1", port=8000, reload=False)