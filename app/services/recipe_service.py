import json
from typing import Optional, List, Dict
from app.domain.schemas import RecipeResponse
from app.infrastructure.ai_base import AIBase
from app.infrastructure.web_crawler import WebCrawler
from app.infrastructure.repositories import RecipeRepository, CrawlTaskRepository
from sqlalchemy.ext.asyncio import AsyncSession


class RecipeService:
    def __init__(self, ai_provider: AIBase, db: AsyncSession):
        self.ai_provider = ai_provider
        self.db = db
        self.crawler = WebCrawler()
        self.recipe_repo = RecipeRepository(db)
        self.crawl_task_repo = CrawlTaskRepository(db)
    
    async def get_simplified_recipe(self, raw_content: str) -> RecipeResponse:
        """简化菜谱内容"""
        system_prompt = self._get_simplify_prompt()
        
        raw_json = await self.ai_provider.chat_completion(system_prompt, raw_content)
        print(f"AI返回的原始JSON: {raw_json}")
        
        # 兼容性处理：Qwen 有时会返回带 Markdown 代码块的字符串
        clean_json = raw_json.strip().replace("```json", "").replace("```", "")
        
        try:
            recipe_data = RecipeResponse.model_validate_json(clean_json)
            return recipe_data
        except Exception as e:
            print(f"解析AI返回的JSON失败: {e}")
            print(f"原始内容: {clean_json}")
            raise
    
    async def crawl_and_simplify(self, url: str) -> Dict:
        """爬取URL并简化菜谱"""
        # 创建爬虫任务
        task = await self.crawl_task_repo.create_crawl_task(url)
        
        try:
            # 更新任务状态为处理中
            await self.crawl_task_repo.update_crawl_task(task.id, status="processing")
            
            # 爬取菜谱内容
            raw_content = await self.crawler.fetch_recipe_from_url(url)
            
            if not raw_content:
                await self.crawl_task_repo.update_crawl_task(
                    task.id, 
                    status="failed", 
                    error_message="爬取失败"
                )
                return {
                    "task_id": task.id,
                    "status": "failed",
                    "error": "爬取失败"
                }
            
            # 简化菜谱
            simplified_recipe = await self.get_simplified_recipe(raw_content)
            
            # 保存到数据库
            recipe = await self.recipe_repo.create_recipe(
                simplified_recipe, 
                source_url=url, 
                source_content=raw_content
            )
            
            # 更新任务状态为完成
            await self.crawl_task_repo.update_crawl_task(
                task.id,
                status="completed",
                result={
                    "recipe_id": recipe.id,
                    "title": recipe.title,
                    "category": recipe.category
                }
            )
            
            return {
                "task_id": task.id,
                "status": "completed",
                "recipe_id": recipe.id,
                "recipe": simplified_recipe.model_dump()
            }
            
        except Exception as e:
            await self.crawl_task_repo.update_crawl_task(
                task.id,
                status="failed",
                error_message=str(e)
            )
            return {
                "task_id": task.id,
                "status": "failed",
                "error": str(e)
            }
    
    async def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict]:
        """根据ID获取菜谱详情"""
        recipe = await self.recipe_repo.get_recipe_by_id(recipe_id)
        
        if recipe:
            # 增加查看次数
            await self.recipe_repo.increment_view_count(recipe_id)
            
            # 转换为响应格式
            return {
                "id": recipe.id,
                "title": recipe.title,
                "category": recipe.category,
                "summary": recipe.summary,
                "ingredients": recipe.ingredients,
                "steps": recipe.steps,
                "tips": recipe.tips,
                "view_count": recipe.view_count,
                "favorite_count": recipe.favorite_count,
                "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
                "source_url": recipe.source_url
            }
        return None
    
    async def search_recipes(self, keyword: str, category: str = None, limit: int = 20, offset: int = 0) -> List[Dict]:
        """搜索菜谱"""
        recipes = await self.recipe_repo.search_recipes(keyword, category, limit, offset)
        
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "category": recipe.category,
                "summary": recipe.summary[:100] + "..." if len(recipe.summary) > 100 else recipe.summary,
                "view_count": recipe.view_count,
                "favorite_count": recipe.favorite_count,
                "created_at": recipe.created_at.isoformat() if recipe.created_at else None
            }
            for recipe in recipes
        ]
    
    async def get_popular_recipes(self, limit: int = 10) -> List[Dict]:
        """获取热门菜谱"""
        recipes = await self.recipe_repo.get_popular_recipes(limit)
        
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "category": recipe.category,
                "summary": recipe.summary[:80] + "..." if len(recipe.summary) > 80 else recipe.summary,
                "view_count": recipe.view_count,
                "favorite_count": recipe.favorite_count
            }
            for recipe in recipes
        ]
    
    async def get_recipes_by_category(self, category: str, limit: int = 20, offset: int = 0) -> List[Dict]:
        """根据分类获取菜谱"""
        recipes = await self.recipe_repo.get_recipes_by_category(category, limit, offset)
        
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "category": recipe.category,
                "summary": recipe.summary[:100] + "..." if len(recipe.summary) > 100 else recipe.summary,
                "view_count": recipe.view_count,
                "favorite_count": recipe.favorite_count,
                "created_at": recipe.created_at.isoformat() if recipe.created_at else None
            }
            for recipe in recipes
        ]
    
    async def get_random_recipes(self, limit: int = 5) -> List[Dict]:
        """获取随机菜谱"""
        # 这里可以实现随机获取逻辑
        # 暂时返回空列表
        return []
    
    async def get_total_recipes_count(self) -> int:
        """获取菜谱总数"""
        return await self.recipe_repo.get_total_recipes_count()
    
    def _get_simplify_prompt(self) -> str:
        """获取简化菜谱的提示词"""
        return """
        你是一位专业的数字化大厨，专门制作极简风格的菜谱。请将菜谱转换为 JSON，严格遵守以下字段逻辑：

        核心原则：极简、清晰、实用
        1. 标题：简洁明了，不超过10个字
        2. 分类：热菜、凉菜、烘焙、调酒、空气炸锅、其他
        3. 摘要：一句话概括这道菜的特点，不超过30字
        4. 食材：
           - 名称要常见易懂
           - 用量要精确（如：2根、200g、1汤匙）
           - 按使用顺序排列
        5. 步骤（最关键的部分）：
           - **action**: 核心动词+对象（如：拍碎黄瓜、调制酱汁）。**字数必须在 20 字以内**。
           - **detail**: 具体的细节描述。包含调料配比、动作要领或颜色状态（如：用刀背拍散后斜切成块，保持清脆）。
           - **heat**: 大火|中火|小火|180°C|无。
           - **timer**: 倒计时秒数，无则为 0。
           - 每个步骤都要独立、清晰，最多8个步骤
        6. 小贴士：实用的烹饪技巧或注意事项，不超过50字

        ### 必须输出的格式：
        {
          "category": "凉菜",
          "title": "拍黄瓜",
          "summary": "清爽开胃的夏日凉菜",
          "ingredients": [
            {
              "name": "黄瓜",
              "amount": "2根"
            },
            {
              "name": "蒜",
              "amount": "3瓣"
            }
          ],
          "steps": [
            {
              "step_num": 1,
              "action": "拍碎切块",
              "detail": "黄瓜洗净，用刀背拍松散，切成2厘米的小块。",
              "heat": "无",
              "timer": 0
            },
            {
              "step_num": 2,
              "action": "调制酱汁",
              "detail": "蒜末、2勺生抽、1勺醋、半勺糖、少许香油混合均匀。",
              "heat": "无",
              "timer": 0
            }
          ],
          "tips": "拍黄瓜时用刀背，不要用刀刃，这样更容易入味。"
        }

        注意：
        1. 保持极简风格，去掉所有废话
        2. 步骤要具体可操作
        3. 用量要精确
        4. 时间要明确
        """