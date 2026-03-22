import sys
sys.path.insert(0, '.')

from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.repositories import RecipeRepository
import asyncio

async def test():
    async with AsyncSessionLocal() as session:
        repo = RecipeRepository(session)
        count = await repo.get_total_recipes_count()
        print(f'菜谱总数: {count}')

asyncio.run(test())