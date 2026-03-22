from fastapi import APIRouter, Depends, Body
from app.domain.schemas import RecipeResponse
from app.services.recipe_service import RecipeService
from app.api.deps import get_recipe_service

router = APIRouter()


@router.post("/simplify", response_model=RecipeResponse)
async def simplify(
        content: str = Body(..., embed=True),
        service: RecipeService = Depends(get_recipe_service)
):
    return await service.get_simplified_recipe(content)
