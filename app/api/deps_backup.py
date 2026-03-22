from app.infrastructure.qwen_provider import QwenProvider
from app.services.recipe_service import RecipeService
from app.core.config import settings

def get_recipe_service() -> RecipeService:
    ai_provider = QwenProvider(settings.QWEN_API_KEY, settings.QWEN_BASE_URL)
    return RecipeService(ai_provider)