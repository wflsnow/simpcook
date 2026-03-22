#!/usr/bin/env python3
"""Debug 主应用程序"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.api.deps import get_recipe_service
from app.services.recipe_service import RecipeService

app = FastAPI(title="Debug SimpCook")


@app.get("/debug-test")
async def debug_test(service: RecipeService = Depends(get_recipe_service)):
    """Debug test endpoint"""
    try:
        print(f"Service type: {type(service)}")
        print(f"Service: {service}")
        
        # Test a simple method
        result = await service.get_popular_recipes(3)
        print(f"Result: {result}")
        
        return {
            "status": "ok",
            "service_type": type(service).__name__,
            "recipe_count": len(result),
            "recipes": result
        }
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("Starting debug server...")
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=False)