from fastapi import Depends
from app.infrastructure.qwen_provider import QwenProvider
from app.services.recipe_service import RecipeService
from app.infrastructure.database import get_db
from app.infrastructure.repositories import UserRepository, FavoriteRepository, SearchHistoryRepository
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession


def get_recipe_service(db: AsyncSession = Depends(get_db)) -> RecipeService:
    ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
    return RecipeService(ai_provider, db)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_favorite_repository(db: AsyncSession = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepository(db)


def get_search_history_repository(db: AsyncSession = Depends(get_db)) -> SearchHistoryRepository:
    return SearchHistoryRepository(db)