from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, desc
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.domain.models import User, Recipe, Favorite, SearchHistory, CrawlTask
from app.domain.schemas import RecipeResponse, Ingredient, RecipeStep


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_openid(self, openid: str) -> Optional[User]:
        """根据微信openid获取用户"""
        result = await self.db.execute(
            select(User).where(User.openid == openid)
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, openid: str, nickname: str = None, avatar_url: str = None) -> User:
        """创建新用户"""
        user = User(
            openid=openid,
            nickname=nickname,
            avatar_url=avatar_url
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """更新用户信息"""
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**kwargs, updated_at=datetime.utcnow())
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()


class RecipeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_recipe(self, recipe_data: RecipeResponse, source_url: str = None, source_content: str = None) -> Recipe:
        """创建新菜谱"""
        recipe = Recipe(
            title=recipe_data.title,
            category=recipe_data.category,
            summary=recipe_data.summary,
            ingredients=[ingredient.dict() for ingredient in recipe_data.ingredients],
            steps=[step.dict() for step in recipe_data.steps],
            tips=recipe_data.tips,
            source_url=source_url,
            source_content=source_content,
            simplified_content=recipe_data.model_dump_json()
        )
        self.db.add(recipe)
        await self.db.commit()
        await self.db.refresh(recipe)
        return recipe
    
    async def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """根据ID获取菜谱"""
        result = await self.db.execute(
            select(Recipe).where(Recipe.id == recipe_id)
        )
        return result.scalar_one_or_none()
    
    async def increment_view_count(self, recipe_id: int) -> None:
        """增加菜谱查看次数"""
        stmt = (
            update(Recipe)
            .where(Recipe.id == recipe_id)
            .values(view_count=Recipe.view_count + 1)
        )
        await self.db.execute(stmt)
        await self.db.commit()
    
    async def search_recipes(self, keyword: str, category: str = None, limit: int = 20, offset: int = 0) -> List[Recipe]:
        """搜索菜谱"""
        query = select(Recipe)
        
        if keyword:
            query = query.where(
                Recipe.title.contains(keyword) | 
                Recipe.summary.contains(keyword) |
                Recipe.tips.contains(keyword)
            )
        
        if category:
            query = query.where(Recipe.category == category)
        
        query = query.order_by(desc(Recipe.view_count)).limit(limit).offset(offset)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_popular_recipes(self, limit: int = 10) -> List[Recipe]:
        """获取热门菜谱"""
        result = await self.db.execute(
            select(Recipe)
            .order_by(desc(Recipe.view_count))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recipes_by_category(self, category: str, limit: int = 20, offset: int = 0) -> List[Recipe]:
        """根据分类获取菜谱"""
        result = await self.db.execute(
            select(Recipe)
            .where(Recipe.category == category)
            .order_by(desc(Recipe.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
    
    async def get_total_recipes_count(self) -> int:
        """获取菜谱总数"""
        result = await self.db.execute(
            select(func.count()).select_from(Recipe)
        )
        return result.scalar_one()


class FavoriteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_favorite(self, user_id: int, recipe_id: int) -> Favorite:
        """添加收藏"""
        # 检查是否已经收藏
        existing = await self.db.execute(
            select(Favorite)
            .where(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id)
        )
        if existing.scalar_one_or_none():
            return None
        
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        self.db.add(favorite)
        
        # 更新菜谱的收藏计数
        stmt = (
            update(Recipe)
            .where(Recipe.id == recipe_id)
            .values(favorite_count=Recipe.favorite_count + 1)
        )
        await self.db.execute(stmt)
        
        await self.db.commit()
        await self.db.refresh(favorite)
        return favorite
    
    async def remove_favorite(self, user_id: int, recipe_id: int) -> bool:
        """取消收藏"""
        result = await self.db.execute(
            delete(Favorite)
            .where(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id)
            .returning(Favorite.id)
        )
        
        if result.scalar_one_or_none():
            # 更新菜谱的收藏计数
            stmt = (
                update(Recipe)
                .where(Recipe.id == recipe_id)
                .values(favorite_count=Recipe.favorite_count - 1)
            )
            await self.db.execute(stmt)
            await self.db.commit()
            return True
        return False
    
    async def get_user_favorites(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Favorite]:
        """获取用户的收藏列表"""
        result = await self.db.execute(
            select(Favorite)
            .options(selectinload(Favorite.recipe))
            .where(Favorite.user_id == user_id)
            .order_by(desc(Favorite.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
    
    async def is_favorited(self, user_id: int, recipe_id: int) -> bool:
        """检查用户是否已收藏该菜谱"""
        result = await self.db.execute(
            select(Favorite.id)
            .where(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id)
        )
        return result.scalar_one_or_none() is not None


class SearchHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_search_history(self, user_id: int, keyword: str) -> SearchHistory:
        """添加搜索历史"""
        history = SearchHistory(user_id=user_id, keyword=keyword)
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history
    
    async def get_user_search_history(self, user_id: int, limit: int = 10) -> List[SearchHistory]:
        """获取用户的搜索历史"""
        result = await self.db.execute(
            select(SearchHistory)
            .where(SearchHistory.user_id == user_id)
            .order_by(desc(SearchHistory.created_at))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def clear_user_search_history(self, user_id: int) -> int:
        """清空用户的搜索历史"""
        result = await self.db.execute(
            delete(SearchHistory)
            .where(SearchHistory.user_id == user_id)
            .returning(SearchHistory.id)
        )
        await self.db.commit()
        return len(result.scalars().all())


class CrawlTaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_crawl_task(self, url: str) -> CrawlTask:
        """创建爬虫任务"""
        task = CrawlTask(url=url)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def get_crawl_task(self, task_id: int) -> Optional[CrawlTask]:
        """获取爬虫任务"""
        result = await self.db.execute(
            select(CrawlTask).where(CrawlTask.id == task_id)
        )
        return result.scalar_one_or_none()
    
    async def update_crawl_task(self, task_id: int, **kwargs) -> Optional[CrawlTask]:
        """更新爬虫任务状态"""
        stmt = (
            update(CrawlTask)
            .where(CrawlTask.id == task_id)
            .values(**kwargs, updated_at=datetime.utcnow())
            .returning(CrawlTask)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()
    
    async def get_pending_tasks(self, limit: int = 10) -> List[CrawlTask]:
        """获取待处理的爬虫任务"""
        result = await self.db.execute(
            select(CrawlTask)
            .where(CrawlTask.status == "pending")
            .order_by(CrawlTask.created_at)
            .limit(limit)
        )
        return result.scalars().all()