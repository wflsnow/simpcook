from fastapi import APIRouter, Depends, Body, Query, Path, HTTPException
from typing import Optional, List
from app.domain.schemas import RecipeResponse
from app.services.recipe_service import RecipeService
from app.infrastructure.repositories import UserRepository, FavoriteRepository, SearchHistoryRepository
from app.api.deps import get_recipe_service, get_user_repository, get_favorite_repository, get_search_history_repository

router = APIRouter()


@router.post("/simplify", response_model=RecipeResponse)
async def simplify(
    content: str = Body(..., embed=True, description="原始菜谱内容"),
    service: RecipeService = Depends(get_recipe_service)
):
    """简化菜谱内容"""
    return await service.get_simplified_recipe(content)


@router.post("/crawl")
async def crawl_recipe(
    url: str = Body(..., embed=True, description="菜谱网页URL"),
    service: RecipeService = Depends(get_recipe_service)
):
    """爬取并简化网页菜谱"""
    result = await service.crawl_and_simplify(url)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result.get("error", "爬取失败"))
    
    return result


@router.get("/search")
async def search_recipes(
    keyword: str = Query("", description="搜索关键词"),
    category: Optional[str] = Query(None, description="分类筛选"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    service: RecipeService = Depends(get_recipe_service)
):
    """搜索菜谱"""
    recipes = await service.search_recipes(keyword, category, limit, offset)
    return {
        "total": len(recipes),
        "recipes": recipes
    }


@router.get("/{recipe_id}")
async def get_recipe(
        recipe_id: int = Path(..., description="菜谱ID"),
        service: RecipeService = Depends(get_recipe_service)
):
    """根据ID获取菜谱详情"""
    recipe = await service.get_recipe_by_id(recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="菜谱不存在")

    return recipe


@router.get("/popular/list")
async def get_popular_recipes(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    service: RecipeService = Depends(get_recipe_service)
):
    """获取热门菜谱列表"""
    recipes = await service.get_popular_recipes(limit)
    return {
        "total": len(recipes),
        "recipes": recipes
    }


@router.get("/category/{category}")
async def get_recipes_by_category(
    category: str = Path(..., description="分类名称"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    service: RecipeService = Depends(get_recipe_service)
):
    """根据分类获取菜谱列表"""
    recipes = await service.get_recipes_by_category(category, limit, offset)
    return {
        "category": category,
        "total": len(recipes),
        "recipes": recipes
    }


@router.get("/categories/list")
async def get_categories():
    """获取所有分类"""
    from app.domain.schemas import CategoryEnum
    
    categories = [
        {"value": category.value, "label": category.value}
        for category in CategoryEnum
    ]
    
    return {
        "total": len(categories),
        "categories": categories
    }


@router.get("/random/list")
async def get_random_recipes(
    limit: int = Query(5, ge=1, le=20, description="返回数量"),
    service: RecipeService = Depends(get_recipe_service)
):
    """获取随机菜谱（用于推荐）"""
    recipes = await service.get_random_recipes(limit)
    return {
        "total": len(recipes),
        "recipes": recipes
    }


# 用户相关端点
@router.post("/users/login")
async def user_login(
    code: str = Body(..., embed=True, description="微信登录code"),
    user_repo: UserRepository = Depends(get_user_repository)
):
    """微信用户登录"""
    # 这里需要实现微信登录逻辑
    # 暂时返回模拟数据
    return {
        "user_id": 1,
        "openid": "mock_openid_123",
        "token": "mock_jwt_token",
        "nickname": "测试用户",
        "avatar_url": "https://example.com/avatar.jpg"
    }


@router.get("/users/{user_id}")
async def get_user_info(
    user_id: int = Path(..., description="用户ID"),
    user_repo: UserRepository = Depends(get_user_repository)
):
    """获取用户信息"""
    # 这里需要实现获取用户信息逻辑
    return {
        "user_id": user_id,
        "nickname": "测试用户",
        "avatar_url": "https://example.com/avatar.jpg",
        "created_at": "2024-01-01T00:00:00"
    }


# 收藏相关端点
@router.post("/favorites/{recipe_id}")
async def add_favorite(
    recipe_id: int = Path(..., description="菜谱ID"),
    user_id: int = Body(..., embed=True, description="用户ID"),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository)
):
    """添加收藏"""
    favorite = await favorite_repo.add_favorite(user_id, recipe_id)
    
    if not favorite:
        raise HTTPException(status_code=400, detail="已收藏该菜谱")
    
    return {
        "success": True,
        "favorite_id": favorite.id
    }


@router.delete("/favorites/{recipe_id}")
async def remove_favorite(
    recipe_id: int = Path(..., description="菜谱ID"),
    user_id: int = Body(..., embed=True, description="用户ID"),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository)
):
    """取消收藏"""
    success = await favorite_repo.remove_favorite(user_id, recipe_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="未收藏该菜谱")
    
    return {"success": True}


@router.get("/favorites/list")
async def get_user_favorites(
    user_id: int = Query(..., description="用户ID"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository)
):
    """获取用户的收藏列表"""
    favorites = await favorite_repo.get_user_favorites(user_id, limit, offset)
    
    recipes = []
    for fav in favorites:
        if fav.recipe:
            recipes.append({
                "id": fav.recipe.id,
                "title": fav.recipe.title,
                "category": fav.recipe.category,
                "summary": fav.recipe.summary[:100] + "..." if len(fav.recipe.summary) > 100 else fav.recipe.summary,
                "view_count": fav.recipe.view_count,
                "favorite_count": fav.recipe.favorite_count,
                "favorited_at": fav.created_at.isoformat() if fav.created_at else None
            })
    
    return {
        "total": len(recipes),
        "recipes": recipes
    }


@router.get("/favorites/check")
async def check_favorite(
    user_id: int = Query(..., description="用户ID"),
    recipe_id: int = Query(..., description="菜谱ID"),
    favorite_repo: FavoriteRepository = Depends(get_favorite_repository)
):
    """检查用户是否已收藏该菜谱"""
    is_favorited = await favorite_repo.is_favorited(user_id, recipe_id)
    return {"is_favorited": is_favorited}


# 搜索历史相关端点
@router.post("/search/history")
async def add_search_history(
    user_id: int = Body(..., embed=True, description="用户ID"),
    keyword: str = Body(..., embed=True, description="搜索关键词"),
    history_repo: SearchHistoryRepository = Depends(get_search_history_repository)
):
    """添加搜索历史"""
    history = await history_repo.add_search_history(user_id, keyword)
    return {
        "success": True,
        "history_id": history.id
    }


@router.get("/search/history")
async def get_search_history(
    user_id: int = Query(..., description="用户ID"),
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    history_repo: SearchHistoryRepository = Depends(get_search_history_repository)
):
    """获取搜索历史"""
    history = await history_repo.get_user_search_history(user_id, limit)
    
    return [
        {
            "id": h.id,
            "keyword": h.keyword,
            "created_at": h.created_at.isoformat() if h.created_at else None
        }
        for h in history
    ]


@router.delete("/search/history/clear")
async def clear_search_history(
    user_id: int = Body(..., embed=True, description="用户ID"),
    history_repo: SearchHistoryRepository = Depends(get_search_history_repository)
):
    """清空搜索历史"""
    count = await history_repo.clear_user_search_history(user_id)
    return {
        "success": True,
        "cleared_count": count
    }


# 首页数据端点
@router.get("/home/data")
async def get_home_data(
    service: RecipeService = Depends(get_recipe_service)
):
    """获取首页数据"""
    # 获取热门菜谱
    popular_recipes = await service.get_popular_recipes(6)
    
    # 获取分类列表
    from app.domain.schemas import CategoryEnum
    categories = [
        {"value": category.value, "label": category.value}
        for category in CategoryEnum
    ]
    
    # 获取随机推荐
    recommended_recipes = await service.get_random_recipes(4)
    
    return {
        "popular_recipes": popular_recipes,
        "categories": categories,
        "recommended_recipes": recommended_recipes,
        "banners": [
            {
                "id": 1,
                "image_url": "https://example.com/banner1.jpg",
                "title": "极简烹饪",
                "link": "/category/热菜"
            },
            {
                "id": 2,
                "image_url": "https://example.com/banner2.jpg",
                "title": "新手必学",
                "link": "/category/凉菜"
            }
        ]
    }