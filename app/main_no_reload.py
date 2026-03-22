import uvicorn
from fastapi import FastAPI
from app.api.v1.recipes import router as recipe_router

app = FastAPI(title="SimpCook 简烹")

app.include_router(recipe_router, prefix="/api/v1/recipes", tags=["Recipes"])

if __name__ == "__main__":
    uvicorn.run("app.main_no_reload:app", host="127.0.0.1", port=8000, reload=False)